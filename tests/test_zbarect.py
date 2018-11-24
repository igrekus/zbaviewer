from zbarect import ZbaRect
from pyexpect import expect


def test_constructor():
    expect(str(ZbaRect(1.0, 1.0, 0.5, 0.5, 3))).to_equal('ZbaRect(x=1.0, y=1.0, w=0.5, h=0.5, d=3)')


def test_from_string_list():
    expect(str(ZbaRect.from_string_list(['.0', '.2', '5.7', '.2', '1']))).to_equal('ZbaRect(x=0.0, y=0.2, w=5.7, h=0.2, d=1)')


def test_should_raise_on_incorrect_dose_id():
    expect(lambda: ZbaRect(d=9)).to_raise(ValueError)
    expect(lambda: ZbaRect(d=0)).to_raise(ValueError)

