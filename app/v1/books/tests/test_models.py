import pytest
from pydantic import ValidationError

from ..models import BookCreate, Language

test_inputs = [
    ({
        "title":"books to do",
        "num_pages":-30,
        "language":Language.SPANISH,
        "prize":20
    }, 1),
    ({
        "title":"books to do",
        "num_pages":999999999999,
        "language":Language.SPANISH,
        "prize":20
    }, 1),
    ({
        "title":"books to do",
        "num_pages":30,
        "language":-90,
        "prize":20
    }, 1),
    ({
        "title":"books to do",
        "num_pages":30,
        "language":Language.JAPANESE,
        "prize":-20
    }, 1),
    ({
        "title":"books to do",
        "num_pages":30,
        "language":Language.JAPANESE,
        "prize":999999999999
    }, 1)
]

@pytest.mark.parametrize("test_input,expected", test_inputs)
def test_failure(test_input, expected):
    try:
        BookCreate(**test_input)
    except ValidationError as e:
        assert len(e.errors()) == expected
        return
    raise

def test_success():
    try:
        BookCreate(
            title="books to do",
            num_pages=30,
            language=Language.JAPANESE,
            prize=12
        )
    except ValidationError:
        raise