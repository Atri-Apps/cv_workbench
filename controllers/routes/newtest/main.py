from mutils.utils import TESTS_IMAGES_DIR, TESTS_OUTPUT_DIR
from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
from pathlib import Path
from cv_transformations.data_field_detection.data_field_detection import run_driving_detection
import re
import urllib.parse

Path(TESTS_IMAGES_DIR).mkdir(parents=True, exist_ok=True)
Path(TESTS_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def test_image_exists(filename: str):
    full_path = Path(TESTS_IMAGES_DIR) / filename
    if Path.exists(full_path):
        return True
    return False

def create_filename(filename: str, count: int):
    stem = Path(filename).stem  + str(count)
    suffix = Path(filename).suffix
    return stem + suffix

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    at.preview_wrapper.styles.display = "none"

def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    pass

def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    # check if file upload event has been triggered
    if at.Upload1.onChange:
        # sanity check if user has successfully uploaded a file
        if at.Upload1.io.files != None:
            files = at.Upload1.io.files
            # check if user has uploaded one or more files
            if len(files) > 0:
                uploadFile = files[0]
                binaryFile = uploadFile.file
                filename = uploadFile.filename
                data = binaryFile.read()
                count = 0
                while True:
                    final_filename = filename if count == 0 else create_filename(filename, count)
                    if not test_image_exists(final_filename):
                        break
                    count = count + 1
                
                final_full_path = Path(TESTS_IMAGES_DIR) / final_filename
                print(str(final_full_path))
                with open(str(final_full_path), "wb") as f:
                    f.write(data)
                    at.preview_wrapper.styles.display = "flex"
                    at.preview.custom.src = create_media_response(data, filename)
                    at.image_placeholder.styles.display = "none"
                    at.filename.custom.text = final_filename
    
    if at.runtest.onClick:
        # TODO: run test
        final_filename = at.filename.custom.text
        final_input_path = Path.joinpath(Path.cwd(), Path(TESTS_IMAGES_DIR) / final_filename)
        final_output_path = Path.joinpath(Path.cwd(), Path(TESTS_OUTPUT_DIR) / final_filename)
        if Path.exists(final_input_path):
            # TODO: get data from test result
            fin = run_driving_detection(str(final_input_path))
            # write output fields
            if "name" in fin:
                name = re.sub(r'[^\x00-\x7F]+',' ', fin["name"])
            else:
                name = "N/A"

            if "license_number" in fin:
                lno = re.sub(r'[^\x00-\x7F]+',' ', fin["license_number"])
            else:
                lno = "N/A"

            if "date_of_birth" in fin:
                dob = re.sub(r'[^\x00-\x7F]+',' ', fin["date_of_birth"])
            else:
                dob = "N/A"

            if "expiry_date" in fin:
                exp = re.sub(r'[^\x00-\x7F]+',' ', fin["expiry_date"])
            else:
                exp = "N/A"

            if "address" in fin:   
                address = re.sub(r'[^\x00-\x7F]+',' ', fin["address"])
            else:
                address = "N/A"
            query = {
                "testname": final_filename,
                "name": name,
                "lno": lno,
                "dob": dob,
                "exp": exp,
                "address": address
                }
            url = "/newtestresult?" + urllib.parse.urlencode(query)
            res.headers.append("location", url)


