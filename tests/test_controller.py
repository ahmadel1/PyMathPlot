import pytest 
from src.controller import MainController

@pytest.fixture
def controller():
    return MainController()

