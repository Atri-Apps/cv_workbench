from PIL import Image
import io
import boto3
import pandas as pd
import os
from dotenv import load_dotenv
from .paths import env_variable_path




def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }


def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']


def main(filepath):
    load_dotenv(env_variable_path('example.env'))
    im = Image.open(filepath)
    buffered = io.BytesIO()
    im.save(buffered, format='PNG')

    client = boto3.client('textract', region_name='ap-south-1', aws_access_key_id=os.environ['AWS_KEY_ID'],
                          aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    response = client.analyze_document(
        Document={'Bytes': buffered.getvalue()},
        FeatureTypes=['TABLES']
    )

    blocks = response['Blocks']
    tables = map_blocks(blocks, 'TABLE')
    cells = map_blocks(blocks, 'CELL')
    words = map_blocks(blocks, 'WORD')
    selections = map_blocks(blocks, 'SELECTION_ELEMENT')

    dataframes = []

    for table in tables.values():

        # Determine all the cells that belong to this table
        table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

        # Determine the table's number of rows and columns
        n_rows = max(cell['RowIndex'] for cell in table_cells)
        n_cols = max(cell['ColumnIndex'] for cell in table_cells)
        content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

        # Fill in each cell
        for cell in table_cells:
            cell_contents = [
                words[child_id]['Text']
                if child_id in words
                else selections[child_id]['SelectionStatus']
                for child_id in get_children_ids(cell)
            ]
            i = cell['RowIndex'] - 1
            j = cell['ColumnIndex'] - 1
            content[i][j] = ' '.join(cell_contents)

        # We assume that the first row corresponds to the column names
        dataframe = pd.DataFrame(content[1:], columns=content[0])
        dataframes.append(dataframe)
    return dataframes


