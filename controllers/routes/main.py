import json
from typing import Callable, KeysView, Tuple, List

from data.types import Test, TestRegistry
from mutils.utils import get_comments, sort_by_date, status_src
from .atri import Atri
from fastapi import Request, Response
from atri_utils import *

def iterate_alias(at: Atri, alias_prefix: str, limits: Tuple[int, int], arr: List[str], reg: TestRegistry, cb: Callable[[Atri, int, str, List[str], TestRegistry], None]):
    start_index = limits[0]
    end_index = limits[1] + 1

    for curr in range(start_index, end_index):
        cb(at, curr, alias_prefix + str(curr), arr, reg)

def hide_testitems(at: Atri, index: int, alias: str, arr: List[str], reg: TestRegistry):
    testitem: at.testitem_1.__class__ = getattr(at, alias)
    testitem.styles.display = "none"

def show_testitems(at: Atri, index: int, alias: str, arr: List[str], reg: TestRegistry):
    testitem: at.testitem_1.__class__ = getattr(at, alias)
    testitem.styles.display = "flex"

def set_initial_item_count(at: Atri):
    at.current_range.custom.text = "0-0"
    at.total_tests.custom.text = "-"

def set_item_count(at: Atri, start_index: int, end_index: int):
    at.current_range.custom.text = str(start_index) + "-" + str(end_index)

def set_total_count(at: Atri, total: int):
    at.total_tests.custom.text = str(total)

def get_item_range(at: Atri):
    [start, end] = at.current_range.custom.text.split("-")
    try:
        parsed_start = int(start)
        parsed_end = int(end)
        return [parsed_start, parsed_end]
    except:
        return [0, 0]

def set_testitems(at: Atri, index: int, alias: str, arr: List[str], reg: TestRegistry):
    [start, end] = get_item_range(at)

    sorted_test_index = start + index - 1 - 1
    print(sorted_test_index)
    # get the test instance
    if sorted_test_index < len(arr):
        testname = arr[sorted_test_index]
        test = reg[testname]
        # status picture
        status: at.status_1.__class__ = getattr(at, "status_" + str(index))
        status.custom.src = status_src[test.get("status")] if test.get("status") in status_src else "/app-assets/gray_circle.svg"
        # testname/filename
        testname_comp: at.testname_1.__class__ = getattr(at, "testname_" + str(index))
        testname_comp.custom.text = testname
        # #comments
        comments = get_comments(testname)
        num_comments: at.commentnum_1.__class__ = getattr(at, "commentnum_" + str(index))
        num_comments.custom.text = str(len(comments))

        # show test item
        show_testitems(at, index, alias, arr, reg)
    else:
        hide_testitems(at, index, alias, arr, reg)

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    iterate_alias(at, "testitem_", [1, 10], [], {}, hide_testitems)
    set_initial_item_count(at)

def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    with open("data/tests.json") as f:
        reg: TestRegistry = json.load(f)
        keys = list(reg.keys())
        [start, end] = get_item_range(at)

        new_start = min(end + 1, len(keys))
        new_end = min(end + 10, len(keys))
        total_count = len(keys)
        set_item_count(at, new_start, new_end)
        set_total_count(at, total_count)

        # sort in reverse time
        keys.sort(reverse=True, key=sort_by_date(reg))
        iterate_alias(at, "testitem_", [1, 10], keys, reg, set_testitems)

def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    if at.next.onClick:
        with open("data/tests.json") as f:
            reg: TestRegistry = json.load(f)
            keys = list(reg.keys())
            [start, end] = get_item_range(at)

            if end >= len(keys):
                return

            new_start = min(start + 10, len(keys))
            new_end = min(new_start + 10, len(keys))
            total_count = len(keys)
            set_item_count(at, new_start, new_end)
            set_total_count(at, total_count)

            # sort in reverse time
            keys.sort(reverse=True, key=sort_by_date(reg))
            iterate_alias(at, "testitem_", [1, 10], keys, reg, set_testitems)

    if at.prev.onClick:
        with open("data/tests.json") as f:
            reg: TestRegistry = json.load(f)
            keys = list(reg.keys())
            [start, end] = get_item_range(at)

            new_start = max(start - 10, 1 if len(keys) > 0 else 0)
            new_end = min(new_start + 9, len(keys))
            total_count = len(keys)
            set_item_count(at, new_start, new_end)
            set_total_count(at, total_count)

            # sort in reverse time
            keys.sort(reverse=True, key=sort_by_date(reg))
            iterate_alias(at, "testitem_", [1, 10], keys, reg, set_testitems)

    for i in range(1, 11):
        navtest = getattr(at, "navtest_" + str(i))
        if navtest.onClick:
            testnamebox = getattr(at, "testname_" + str(i))
            testname = testnamebox.custom.text
            res.headers.append("location", "/viewtest?testname=" + testname)
            break