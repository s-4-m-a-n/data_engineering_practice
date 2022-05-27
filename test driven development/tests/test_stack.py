import pytest 

# @pytest.fixture
# def val():
#     return 4
val = 4


def show(n):
    return n

def return_5(val):
    return val

def return_sysexc():
    raise SystemExit(1)

    
def test_show(val):
    assert show(val) == 4, "should return 4"

def test_sysexc():
    with pytest.raises(SystemExit):
        return_sysexc()

