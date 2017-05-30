from engineering_notation import EngNumber, __version__


def test_import_version():
    assert __version__
    assert len(__version__.split('.')) == 3


def test_to_str_large():
    assert str(EngNumber('220k')) == '220k'
    assert str(EngNumber('220000')) == '220k'
    assert str(EngNumber(220000)) == '220k'
    assert str(EngNumber(220000.00)) == '220k'
    assert str(EngNumber(220001.25)) == '220k'


def test_to_str_small():
    assert str(EngNumber('220m')) == '220m'
    assert str(EngNumber('0.220')) == '220m'
    assert str(EngNumber(0.220)) == '220m'
    assert str(EngNumber(0.220000125)) == '220m'


def test_add():
    assert str(EngNumber('220m') + EngNumber('10m')) == '230m'
    assert str(EngNumber('220m') + 0.01) == '230m'
    assert str(0.01 + EngNumber('220m')) == '230m'

    assert str(EngNumber('220m') + EngNumber('220u')) == '220.22m'
    assert str(EngNumber('220m') + EngNumber('220n')) == '220m'


def test_sub():
    assert str(EngNumber('220m') - EngNumber('10m')) == '210m'
    assert str(EngNumber('220m') - 0.01) == '210m'

    assert str(EngNumber('220m') - EngNumber('220u')) == '219.78m'
    assert str(EngNumber('220m') - EngNumber('220n')) == '220m'

    assert str(0.220 - EngNumber('0.01')) == '210m'


def test_mul():
    assert str(EngNumber('220m') * EngNumber('2')) == '440m'
    assert str(EngNumber('220m') * 2) == '440m'
    assert str(EngNumber('220m') * 2.0) == '440m'

    assert str(2 * EngNumber('220m')) == '440m'
    assert str(2.0 * EngNumber('220m')) == '440m'


def test_div():
    assert str(EngNumber('220m') / EngNumber('2')) == '110m'
    assert str(EngNumber('220m') / 2) == '110m'
    assert str(EngNumber('220m') / 2.0) == '110m'

    assert str(2 / EngNumber('220m')) == '9.09'
    assert str(2.0 / EngNumber('220m')) == '9.09'


def test_eq():
    assert EngNumber('220k') == EngNumber(220000)
    assert EngNumber('220k') == 220000
    assert EngNumber('220k') == 220000.0

    assert 220000 == EngNumber('220k')
    assert 220000.0 == EngNumber('220k')


def test_gt():
    assert EngNumber('220k') > 219000


def test_lt():
    assert EngNumber('220k') < 221000


def test_ge():
    assert EngNumber('220k') >= 219000
    assert EngNumber('220k') >= 220000


def test_le():
    assert EngNumber('220k') <= 221000
    assert EngNumber('220k') <= 220000

