from ..yolov5.detect import run
import easyocr
from pathlib import Path
import os
from PIL import Image
import shutil


def get_us_driving_license_data(filepath: str):
    return run(
        data='cv_transformations/yolov5/US_DL.yaml',
        weights='cv_transformations/yolov5/best.pt',
        project=Path.cwd() / "data" / "temp",
        name="",
        source=filepath,
        save_crop=True
        )

def run_driving_detection(filepath: str):
    image, dic = get_us_driving_license_data(filepath)
    reader = easyocr.Reader(['en', 'hi'], gpu=True)
    fin = {}
    for i, j in dic.items():
        im = Image.fromarray(j)
        im.save(f'{i}.jpg')
        fin[i] = ' '.join(reader.readtext(f'{i}.jpg',detail=False))
        os.remove(f'{i}.jpg')
    
    filename = Path(filepath).stem + Path(filepath).suffix
    temp_dir = Path.cwd() / "data" / "temp"
    output_dir = Path.cwd() / "data" / "test_outputs"
    shutil.copy(str(temp_dir / filename), str(output_dir))

    shutil.rmtree(str(temp_dir), ignore_errors=True)

    return fin
