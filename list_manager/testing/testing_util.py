import pytest
from list_manager.util import to_float, to_mixed_num

def test_to_float():
    assert to_float("1") == 1.0
    assert to_float("0") == 0.0
    assert to_float("½") == to_float("0.5") == 0.5
    assert to_float("1½") == to_float("1 ½") == 1.5
    assert to_float("12½") == 12.5
    assert to_float("1/2") == 0.5
    assert to_float("1 1/2") == 1.5
    assert to_float("11/2") == 5.5
    with pytest.raises(ValueError):
        assert to_float("")
        assert to_float("½½")
        assert to_float("1/2½")
        assert to_float("1/2 ½")

def test_to_mixed_num():
    assert to_mixed_num(1.5) == "1 1/2"
    assert to_mixed_num(0.5) == "1/2"
    assert to_mixed_num(0.125) == "1/8"
    assert to_mixed_num(1) == "1"