from typing import Dict, List, TypedDict
from enum import Enum

class TestOutput(TypedDict):
    name: str
    lno: str
    dob: str
    address: str
    exp: str

class TestStatus(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    EXCLAIM = "exclaim"

class Test(TypedDict):
    name: str
    time: str
    input_file: str
    output: TestOutput
    status: TestStatus

TestRegistry = Dict[str, Test]

class Comment(TypedDict):
    time: str
    text: str
    username: str

# map of test name & comments
CommentRegistry = Dict[str, List[Comment]]