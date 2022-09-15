from datetime import datetime
from data.types import Comment, TestOutput
from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
from urllib.parse import parse_qs
from pathlib import Path
from mutils.utils import TESTS_OUTPUT_DIR, date_to_str, sort_comments_by_date, status_src
import json

def set_status(testname, status):
    with open("data/tests.json") as f:
        tests = json.load(f)
        
    with open("data/tests.json", "w") as f:
        if testname in tests:
            tests[testname]["status"] = status
            json.dump(tests, f, indent=4)

def reload_page(res: Response, testname: str):
    res.headers.append("location", "/viewtest?testname=" + testname)

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    at.comment_wrapper_1.styles.display = "none"
    at.comment_wrapper_2.styles.display = "none"
    at.comment_wrapper_3.styles.display = "none"

    at.comment_input_wrapper.styles.display = "none"

def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    testname = parse_qs(query[1:])["testname"][0]
    at.output_img.custom.src = create_media_response(Path.cwd() / TESTS_OUTPUT_DIR / testname)
    at.testname.custom.text = testname

    with open("data/tests.json") as f:
        tests = json.load(f)
        if testname in tests:
            test: TestOutput = tests[testname]["output"]
            address = test.get("address")
            dob = test.get("dob")
            exp = test.get("exp")
            name = test.get("name")
            lno = test.get("lno")
            status = tests[testname]["status"]
            at.address.custom.text = address
            at.dob.custom.text = dob
            at.expiry.custom.text = exp
            at.driver_name.custom.text = name
            at.license.custom.text = lno
            
        if status == "correct":
            at.correct.custom.src = status_src["correct"]
        if status == "incorrect":
            at.incorrect.custom.src = status_src["incorrect"]
        if status == "exclaim":
            at.exclaim.custom.src = status_src["exclaim"]
    
    with open("data/comments.json") as f:
        comments_reg = json.load(f)
        if testname in comments_reg:
            comments = comments_reg[testname]
            sort_comments_by_date(comments)
            for i in range(1, 4):
                if i <= len(comments):
                    comment: Comment = comments[i - 1]
                    username_box = getattr(at, "username_" + str(i))
                    comment_box = getattr(at, "comment_" + str(i))
                    time_box = getattr(at, "time_" + str(i))
                    comment_wrapper = getattr(at, "comment_wrapper_" + str(i))

                    username_box.custom.text = comment.get("username")
                    comment_box.custom.text = comment.get("text")
                    time_box.custom.text = comment.get("time")
                    comment_wrapper.styles.display = "flex"


def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    testname = at.testname.custom.text

    if at.comment_btn.onClick:
        at.comment_input_wrapper.styles.display = "flex"
        at.comment_btn_wrapper.styles.display = "none"
    
    if at.submit.onClick:
        username = req.cookies.get("username")
        text = at.comment_input.custom.value
        time = date_to_str(datetime.now())
        new_comment = {"username": username, "text": text, "time": time}
        with open("data/comments.json") as f:
            comments_reg = json.load(f)
        
        with open("data/comments.json", "w") as f:
            if testname in comments_reg:
                comments_reg[testname].append(new_comment)
            else:
                comments_reg[testname] = [new_comment]
            
            json.dump(comments_reg, f, indent=4)

            reload_page(res, testname)
    

    if at.correct.onClick:
        set_status(testname, "correct")
        reload_page(res, testname)

    if at.incorrect.onClick:
        set_status(testname, "incorrect")
        reload_page(res, testname)

    if at.exclaim.onClick:
        set_status(testname, "exclaim")
        reload_page(res, testname)
