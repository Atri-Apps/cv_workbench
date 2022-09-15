from .atri import Atri
from fastapi import Request, Response
from atri_utils import *

import json

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    # TODO: display property should be available in all components
    at.errorwrapper.styles.display = "none"

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
    username = at.username.custom.value
    password = at.password.custom.value

    # validate username & password
    with open("data/users.json") as f:
        users = json.load(f)
        if username in users:
            if users[username]["passwd"] == password:
                res.set_cookie("username", username)
                res.headers.append("location", "http://localhost:4005")
            else:
                at.errorwrapper.styles.display = "flex"
            
        else:
            at.errorwrapper.styles.display = "flex"          
