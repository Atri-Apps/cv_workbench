from datetime import datetime
from mutils.utils import TESTS_IMAGES_DIR, TESTS_OUTPUT_DIR
from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
from urllib.parse import parse_qs
from pathlib import Path
from mutils.utils import status_src, date_to_str
import json

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    at.comment_input_wrapper.styles.display = "none"

def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    testname = parse_qs(query[1:])["testname"][0]
    
    # TODO: send output image instead of input image
    at.output_img.custom.src = create_media_response(Path.cwd() / TESTS_OUTPUT_DIR / testname)
    at.testname.custom.text = testname

    address = parse_qs(query[1:])["address"][0]
    dob = parse_qs(query[1:])["dob"][0]
    exp = parse_qs(query[1:])["exp"][0]
    name = parse_qs(query[1:])["name"][0]
    lno = parse_qs(query[1:])["lno"][0]
    at.address.custom.text = address
    at.dob.custom.text = dob
    at.expiry.custom.text = exp
    at.driver_name.custom.text = name
    at.license.custom.text = lno


def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    if at.correct.onClick:
        at.correct.custom.src = status_src["correct"]
    if at.incorrect.onClick:
        at.incorrect.custom.src = status_src["incorrect"]
    if at.exclaim.onClick:
        at.exclaim.custom.src = status_src["exclaim"]
    if at.comment_btn.onClick:
        at.comment_input_wrapper.styles.display = "flex"
        at.comment_btn_wrapper.styles.display = "none"
    
    if at.save_test.onClick:
        # TODO: save test result in comments.json
        testname = at.testname.custom.text
        address = at.address.custom.text
        dob = at.dob.custom.text
        exp = at.expiry.custom.text
        name = at.driver_name.custom.text
        lno = at.license.custom.text
        comment = at.comment_input.custom.value
        status = ""
        if at.correct.custom.src == status_src["correct"]:
            status = "correct"
        if at.incorrect.custom.src == status_src["incorrect"]:
            status = "incorrect"
        if at.exclaim.custom.src == status_src["exclaim"]:
            status = "exclaim"

        now = datetime.now()

        with open("data/comments.json") as f:
            comments = json.load(f)
            username = req.cookies.get("username")
            comments[testname] = [{
                "time": date_to_str(now),
                "text": comment,
                "username": username
                }] if len(comment) > 0 else []
        
        with open("data/comments.json", "w") as f:
            json.dump(comments, f, indent=4)

        with open("data/tests.json") as f:
            tests = json.load(f)
            output = {"name": name, "lno": lno, "dob": dob, "address": address, "exp": exp}
            tests[testname] = {
                "name": testname,
                "time": date_to_str(now),
                "input_file": testname,
                "output": output,
                "status": status
                }
        
        with open("data/tests.json", "w") as f:
            json.dump(tests, f, indent=4)