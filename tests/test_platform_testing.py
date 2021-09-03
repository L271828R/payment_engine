import pytest
from payment_engine.core.python_version_validation import validate


def test_unsupported_python_version():
    with pytest.raises(AssertionError) as e:
        validate(3,4, (3,1,0))
    assert(str(e.value) == "Error: Python 3.4 or above is supported")