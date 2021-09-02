import pytest
from payment_engine.core.python_version_validation import validate


def test_unsupported_file_type():
    # validate(2,5)
    with pytest.raises(AssertionError) as e:
        validate(2,3)
    assert(str(e.value) == "Error: Python 3.4 or above is supported")