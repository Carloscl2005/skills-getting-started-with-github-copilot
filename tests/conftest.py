import copy

import pytest

from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity data after each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
