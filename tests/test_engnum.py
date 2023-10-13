import pytest
from engineering_notation import EngNumber, EngUnit, __version__


def test_import_version():
    assert __version__
    assert len(__version__.split('.')) == 3


''' tests for EngNum '''


def test_enum_to_str_large():
    # positive_numbers
    assert str(EngNumber('220k')) == '220k'
    assert str(EngNumber('220000')) == '220k'
    assert str(EngNumber(220000)) == '220k'
    assert str(EngNumber(220000.00)) == '220k'
    assert str(EngNumber(220001.25)) == '220k'

    # negative_numbers
    assert str(EngNumber('-220k')) == '-220k'
    assert str(EngNumber('-220000')) == '-220k'
    assert str(EngNumber(-220000)) == '-220k'
    assert str(EngNumber(-220000.00)) == '-220k'
    assert str(EngNumber(-220001.25)) == '-220k'


def test_engum_to_str_small():
    # positive_numbers
    assert str(EngNumber('220m')) == '220m'
    assert str(EngNumber('0.220')) == '220m'
    assert str(EngNumber(0.220)) == '220m'
    assert str(EngNumber(0.220000125)) == '220m'

    # negative_numbers
    assert str(EngNumber('-220m')) == '-220m'
    assert str(EngNumber('-0.220')) == '-220m'
    assert str(EngNumber(-0.220)) == '-220m'
    assert str(EngNumber(-0.220000125)) == '-220m'


def test_1000f():
    assert str(EngNumber('1000f')) == '1p'
    assert str(EngNumber('1p')) == '1p'
    assert str(EngNumber(0.000000000001)) == '1p'


def test_engnum_significant():
    assert str(EngNumber('220m', significant=0)) == '220m'
    assert str(EngNumber('220m', significant=1)) == '200m'
    assert str(EngNumber('220m', significant=2)) == '220m'
    assert str(EngNumber('220m', significant=3)) == '220m'
    assert str(EngNumber('220m', significant=4)) == '220.0m'
    assert str(EngNumber('220m', significant=5)) == '220.00m'

    assert str(EngNumber('22m', significant=0)) == '22m'
    assert str(EngNumber('22m', significant=1)) == '20m'
    assert str(EngNumber('22m', significant=2)) == '22m'
    assert str(EngNumber('22m', significant=3)) == '22.0m'
    assert str(EngNumber('22.2m', significant=3)) == '22.2m'
    assert str(EngNumber('22m', significant=4)) == '22.00m'
    assert str(EngNumber('22.22m', significant=4)) == '22.22m'

    assert str(EngNumber('2m', significant=0)) == '2m'
    assert str(EngNumber('2m', significant=1)) == '2m'
    assert str(EngNumber('2m', significant=2)) == '2.0m'
    assert str(EngNumber('2.2m', significant=2)) == '2.2m'
    assert str(EngNumber('2.2m', significant=3)) == '2.20m'
    assert str(EngNumber('2.22m', significant=3)) == '2.22m'


def test_engnum_separator():
    assert str(EngNumber("1.23k", separator=" ")) == "1.23 k"
    assert str(EngNumber("1.23k", separator=" ").to_pn()) == "1k23"


def test_new_units():
    """
    any new units - such as femto, atto, zepto, etc. should have
    some basic testing added here
    """

    # testing femto
    assert str(EngNumber('220f')) == '220f'
    assert str(EngNumber(0.000000000000220)) == '220f'

    # testing atto
    assert str(EngNumber('220a')) == '220a'
    assert str(EngNumber(0.000000000000000220)) == '220a'

    # testing zepto
    assert str(EngNumber('220z')) == '220z'
    assert str(EngNumber(0.000000000000000000220)) == '220z'

    # testing yocto
    assert str(EngNumber('220y')) == '220y'
    assert str(EngNumber(0.000000000000000000000220)) == '220y'

    # testing peta
    assert str(EngNumber('220P')) == '220P'
    assert str(EngNumber(1e15)) == '1P'

    # testing exxa
    assert str(EngNumber('220E')) == '220E'
    assert str(EngNumber(1e18)) == '1E'

    # testing zetta
    assert str(EngNumber('220Z')) == '220Z'
    assert str(EngNumber(1e21)) == '1Z'

    # wrap it all up
    assert str(EngNumber('1f') + EngNumber('330a')) == '1.33f'
    assert str(EngNumber('3z') + EngNumber('440y')) == '3.44z'


def test_enum_add():
    # positive_numbers
    assert str(EngNumber('220m') + EngNumber('10m')) == '230m'
    assert str(EngNumber('220m') + 0.01) == '230m'
    assert str(0.01 + EngNumber('220m')) == '230m'

    assert str(EngNumber('220m') + EngNumber('220u')) == '220.22m'
    assert str(EngNumber('220m') + EngNumber('220n')) == '220m'

    # negative_numbers
    assert str(EngNumber('-220m') + EngNumber('-10m')) == '-230m'
    assert str(EngNumber('-220m') + -0.01) == '-230m'
    assert str(-0.01 + EngNumber('-220m')) == '-230m'

    assert str(EngNumber('-220m') + EngNumber('-220u')) == '-220.22m'
    assert str(EngNumber('-220m') + EngNumber('-220n')) == '-220m'


def test_enum_sub():
    # positive_numbers
    assert str(EngNumber('220m') - EngNumber('10m')) == '210m'
    assert str(EngNumber('220m') - 0.01) == '210m'

    assert str(EngNumber('220m') - EngNumber('220u')) == '219.78m'
    assert str(EngNumber('220m') - EngNumber('220n')) == '220m'

    assert str(0.220 - EngNumber('0.01')) == '210m'

    # negative_numbers
    assert str(EngNumber('-220m') - EngNumber('-10m')) == '-210m'
    assert str(EngNumber('-220m') - -0.01) == '-210m'

    assert str(EngNumber('-220m') - EngNumber('-220u')) == '-219.78m'
    assert str(EngNumber('-220m') - EngNumber('-220n')) == '-220m'

    assert str(-0.220 - EngNumber('-0.01')) == '-210m'


def test_enum_mul():
    # positive_numbers
    assert str(EngNumber('220m') * EngNumber('2')) == '440m'
    assert str(EngNumber('220m') * 2) == '440m'
    assert str(EngNumber('220m') * 2.0) == '440m'

    assert str(2 * EngNumber('220m')) == '440m'
    assert str(2.0 * EngNumber('220m')) == '440m'

    # negative_numbers
    assert str(EngNumber('-220m') * EngNumber('-2')) == '440m'
    assert str(EngNumber('-220m') * -2) == '440m'
    assert str(EngNumber('-220m') * -2.0) == '440m'

    assert str(-2 * EngNumber('-220m')) == '440m'
    assert str(-2.0 * EngNumber('-220m')) == '440m'


def test_enum_div():
    # positive_numbers
    assert str(EngNumber('220m') / EngNumber('2')) == '110m'
    assert str(EngNumber('220m') / 2) == '110m'
    assert str(EngNumber('220m') / 2.0) == '110m'

    assert str(2 / EngNumber('220m')) == '9.09'
    assert str(2.0 / EngNumber('220m')) == '9.09'

    # negative_numbers
    assert str(EngNumber('-220m') / EngNumber('-2')) == '110m'
    assert str(EngNumber('-220m') / -2) == '110m'
    assert str(EngNumber('-220m') / -2.0) == '110m'

    assert str(-2 / EngNumber('-220m')) == '9.09'
    assert str(-2.0 / EngNumber('-220m')) == '9.09'


def test_enum_eq():
    # positive_numbers
    assert EngNumber('220k') == EngNumber(220000)
    assert EngNumber('220k') == 220000
    assert EngNumber('220k') == 220000.0

    assert 220000 == EngNumber('220k')
    assert 220000.0 == EngNumber('220k')

    # positive_numbers
    assert EngNumber('-220k') == EngNumber(-220000)
    assert EngNumber('-220k') == -220000
    assert EngNumber('-220k') == -220000.0

    assert -220000 == EngNumber('-220k')
    assert -220000.0 == EngNumber('-220k')

    assert not (EngNumber('220k') == object)


def test_enum_gt():
    # positive_numbers
    assert EngNumber('220k') > 219000

    # negative_numbers
    assert EngNumber('-220k') < -219000


def test_enum_lt():
    # positive_numbers
    assert EngNumber('220k') < 221000

    # negative_numbers
    assert EngNumber('-220k') > -221000


def test_enum_ge():
    # positive_numbers
    assert EngNumber('220k') >= 219000
    assert EngNumber('220k') >= 220000

    # negative_numbers
    assert EngNumber('-220k') <= -219000
    assert EngNumber('-220k') <= -220000


def test_enum_le():
    # positive_numbers
    assert EngNumber('220k') <= 221000
    assert EngNumber('220k') <= 220000

    # negative_numbers
    assert EngNumber('-220k') >= -221000
    assert EngNumber('-220k') >= -220000


def test_enum_to_int():
    # positive_numbers
    assert int(EngNumber('220k')) == 220000
    assert int(EngNumber('220m')) == 0

    # negative_numbers
    assert int(EngNumber('-220k')) == -220000
    assert int(EngNumber('-220m')) == 0


def test_enum_to_float():
    # positive_numbers
    assert float(EngNumber('220k')) == 220000.0
    assert float(EngNumber('220m')) == 0.220

    # negative_numbers
    assert float(EngNumber('-220k')) == -220000.0
    assert float(EngNumber('-220m')) == -0.220


def test_to_pn():
    # positive_numbers
    assert EngNumber('1.2M').to_pn() == '1M20'
    assert EngNumber('220M').to_pn() == '220M'

    assert EngNumber('220k').to_pn() == '220k'
    assert EngNumber('1.2k').to_pn() == '1k20'

    assert EngNumber('220').to_pn() == '220'
    assert EngNumber('1.2').to_pn() == '1.20'

    assert EngNumber('220m').to_pn() == '220m'
    assert EngNumber('1.2m').to_pn() == '1m20'

    # negative_numbers
    assert EngNumber('-1.2M').to_pn() == '-1M20'
    assert EngNumber('-220M').to_pn() == '-220M'

    assert EngNumber('-220k').to_pn() == '-220k'
    assert EngNumber('-1.2k').to_pn() == '-1k20'

    assert EngNumber('-220').to_pn() == '-220'
    assert EngNumber('-1.2').to_pn() == '-1.20'

    assert EngNumber('-220m').to_pn() == '-220m'
    assert EngNumber('-1.2m').to_pn() == '-1m20'


def test_to_pn_with_letter():
    # positive_numbers
    assert EngNumber('1.2').to_pn('R') == '1R20'
    assert EngNumber(22.0).to_pn('C') == '22'
    assert EngNumber(22.1).to_pn('C') == '22C10'

    # negative_numbers
    assert EngNumber('-1.2').to_pn('R') == '-1R20'
    assert EngNumber(-22.0).to_pn('C') == '-22'
    assert EngNumber(-22.1).to_pn('C') == '-22C10'


def test_enum_to_enum():
    # positive_numbers
    enum = EngNumber('1.2')
    assert str(EngNumber(enum)) == '1.20'

    # negative_numbers
    enum = EngNumber('-1.2')
    assert str(EngNumber(enum)) == '-1.20'


''' tests for EngUnit()'''


def test_to_str():
    # positive_numbers
    assert str(EngUnit('220')) == '220'
    assert str(EngUnit('220ohm')) == '220ohm'
    assert str(EngUnit('220ohm', separator=" ")) == '220 ohm'

    # negative_numbers
    assert str(EngUnit('-220')) == '-220'
    assert str(EngUnit('-220ohm')) == '-220ohm'
    assert str(EngUnit('-220ohm', separator=" ")) == '-220 ohm'

    assert EngUnit('220ohm').unit == 'ohm'
    assert EngUnit('220', unit='ohm').unit == 'ohm'

    assert EngUnit('2m', unit='meter').unit == 'meter'
    assert EngUnit('2m', unit='meter').eng_num == EngNumber('2m')


def test_to_str_large():
    # positive_numbers
    assert str(EngUnit('220kHz')) == '220kHz'
    assert str(EngUnit('220000')) == '220k'
    assert str(EngUnit(220000)) == '220k'
    assert str(EngUnit(220000.00)) == '220k'
    assert str(EngUnit(220001.25)) == '220k'

    # negative_numbers
    assert str(EngUnit('-220kHz')) == '-220kHz'
    assert str(EngUnit('-220000')) == '-220k'
    assert str(EngUnit(-220000)) == '-220k'
    assert str(EngUnit(-220000.00)) == '-220k'
    assert str(EngUnit(-220001.25)) == '-220k'


def test_to_str_small():
    # positive_numbers
    assert str(EngUnit('220mohm')) == '220mohm'
    assert str(EngUnit('0.220')) == '220m'
    assert str(EngUnit(0.220)) == '220m'
    assert str(EngUnit(0.220000125)) == '220m'

    # negative_numbers
    assert str(EngUnit('-220mohm')) == '-220mohm'
    assert str(EngUnit('-0.220')) == '-220m'
    assert str(EngUnit(-0.220)) == '-220m'
    assert str(EngUnit(-0.220000125)) == '-220m'


def test_add():
    # positive_numbers
    assert str(EngUnit('220mHz') + EngUnit('10mHz')) == '230mHz'
    assert str(EngUnit('220mohm') + EngUnit('220uohm')) == '220.22mohm'
    assert str(EngUnit('220m') + EngUnit('220n')) == '220m'

    assert str(EngUnit('220m') + 0.01) == '230m'
    assert str(0.01 + EngUnit('220m')) == '230m'

    with pytest.raises(AttributeError):
        EngUnit('220mHz') + EngUnit('10m')
    with pytest.raises(AttributeError):
        EngUnit('10m') + EngUnit('220mHz')

    # negative_numbers
    assert str(EngUnit('-220mHz') + EngUnit('-10mHz'))    == '-230mHz'
    assert str(EngUnit('-220mohm') + EngUnit('-220uohm')) == '-220.22mohm'
    assert str(EngUnit('-220m') + EngUnit('-220n'))       == '-220m'

    assert str(EngUnit('-220m') + -0.01) == '-230m'
    assert str(-0.01 + EngUnit('-220m')) == '-230m'

    with pytest.raises(AttributeError):
        EngUnit('-220mHz') + EngUnit('-10m')
    with pytest.raises(AttributeError):
        EngUnit('-10m') + EngUnit('-220mHz')


def test_sub():
    # positive_numbers
    assert str(EngUnit('220mHz') - EngUnit('10mHz')) == '210mHz'
    assert str(EngUnit('220mohm') - EngUnit('220uohm')) == '219.78mohm'
    assert str(EngUnit('220m') - EngUnit('220n')) == '220m'

    assert str(EngUnit('220m') - 0.01) == '210m'
    assert str(0.220 - EngUnit('0.01')) == '210m'

    with pytest.raises(AttributeError):
        EngUnit('220mHz') - EngUnit('10m')
    with pytest.raises(AttributeError):
        EngUnit('10m') - EngUnit('220mHz')
    with pytest.raises(AttributeError):
        10.0 - EngUnit('220mHz')

    # negative_numbers
    assert str(EngUnit('-220mHz') - EngUnit('-10mHz')) == '-210mHz'
    assert str(EngUnit('-220mohm') - EngUnit('-220uohm')) == '-219.78mohm'
    assert str(EngUnit('-220m') - EngUnit('-220n'))       == '-220m'

    assert str(EngUnit('-220m') - -0.01)  == '-210m'
    assert str(-0.220 - EngUnit('-0.01')) == '-210m'

    with pytest.raises(AttributeError):
        EngUnit('-220mHz') - EngUnit('-10m')
    with pytest.raises(AttributeError):
        EngUnit('-10m') - EngUnit('-220mHz')
    with pytest.raises(AttributeError):
        -10.0 - EngUnit('-220mHz')


def test_mul():
    # positive_numbers
    assert str(EngUnit('220ms') * EngUnit('2Hz')) == '440msHz'
    assert str(EngUnit('220ms') * EngUnit('2')) == '440ms'
    assert str(EngUnit('220m') * EngUnit('2s')) == '440ms'

    assert str(EngUnit('220ms') * 2) == '440ms'
    assert str(EngUnit('220ms') * 2.0) == '440ms'

    assert str(2 * EngUnit('220ms')) == '440ms'
    assert str(2.0 * EngUnit('220ms')) == '440ms'

    # negative_numbers
    assert str(EngUnit('-220ms') * EngUnit('-2Hz')) == '440msHz'
    assert str(EngUnit('-220ms') * EngUnit('-2'))   == '440ms'
    assert str(EngUnit('-220m') * EngUnit('-2s'))   == '440ms'

    assert str(EngUnit('-220ms') * -2)   == '440ms'
    assert str(EngUnit('-220ms') * -2.0) == '440ms'

    assert str(-2 * EngUnit('-220ms'))   == '440ms'
    assert str(-2.0 * EngUnit('-220ms')) == '440ms'


def test_div():
    # positive_numbers
    assert str(EngUnit('220ms') / EngUnit('2s')) == '110ms/s'
    assert str(EngUnit('220ms') / EngUnit('2')) == '110ms'
    assert str(EngUnit('220m') / EngUnit('2s')) == '110m/s'

    assert str(EngUnit('220ms') / 2) == '110ms'
    assert str(EngUnit('220ms') / 2.0) == '110ms'

    assert str(2 / EngUnit('220ms')) == '9.09/s'
    assert str(2.0 / EngUnit('220ms')) == '9.09/s'

    # negative_numbers
    assert str(EngUnit('-220ms') / EngUnit('-2s')) == '110ms/s'
    assert str(EngUnit('-220ms') / EngUnit('-2'))  == '110ms'
    assert str(EngUnit('-220m') / EngUnit('-2s'))  == '110m/s'

    assert str(EngUnit('-220ms') / -2)   == '110ms'
    assert str(EngUnit('-220ms') / -2.0) == '110ms'

    assert str(-2 / EngUnit('-220ms'))   == '9.09/s'
    assert str(-2.0 / EngUnit('-220ms')) == '9.09/s'


def test_eq():
    # positive_numbers
    assert EngUnit('220k') == EngUnit(220000)
    assert EngUnit('220k') == 220000
    assert EngUnit('220k') == 220000.0

    assert 220000 == EngUnit('220k')
    assert 220000.0 == EngUnit('220k')

    with pytest.raises(AttributeError):
        EngUnit('220mHz') == EngUnit('0.220ohm')
    with pytest.raises(AttributeError):
        EngUnit('220mHz') == 10
    with pytest.raises(AttributeError):
        EngUnit('220mHz') == 10.0
    assert not (EngUnit('220k') == object)

    # negative_numbers
    assert EngUnit('-220k') == EngUnit(-220000)
    assert EngUnit('-220k') == -220000
    assert EngUnit('-220k') == -220000.0

    assert -220000   == EngUnit('-220k')
    assert -220000.0 == EngUnit('-220k')

    with pytest.raises(AttributeError):
        EngUnit('-220mHz') == EngUnit('-0.220ohm')
    with pytest.raises(AttributeError):
        EngUnit('-220mHz') == -10
    with pytest.raises(AttributeError):
        EngUnit('-220mHz') == -10.0


def test_gt():
    # positive_numbers
    assert EngUnit('220kohm') > EngUnit('219000ohm')

    with pytest.raises(AttributeError):
        EngUnit('220kohm') > 219000

    # negative_numbers
    assert EngUnit('-220kohm') < EngUnit('-219000ohm')

    with pytest.raises(AttributeError):
        EngUnit('-220kohm') < -219000


def test_lt():
    # positive_numbers
    assert EngUnit('220kohm') < EngUnit('221000ohm')

    with pytest.raises(AttributeError):
        EngUnit('220kohm') < 221000

        # negative_numbers
        # ##ERROR:assert EngUnit('-220kohm') > EngUnit('-221000ohm')

        # ##ERROR:with pytest.raises(AttributeError):
        # ##ERROR:    EngUnit('-220kohm') > -221000


def test_ge():
    # positive_numbers
    assert EngUnit('220kohm') >= EngUnit('219000ohm')
    assert EngUnit('220kohm') >= EngUnit('220000ohm')

    with pytest.raises(AttributeError):
        EngUnit('220kohm') >= 219000

    # negative_numbers
    assert EngUnit('-220kohm') <= EngUnit('-219000ohm')
    assert EngUnit('-220kohm') <= EngUnit('-220000ohm')

    with pytest.raises(AttributeError):
        EngUnit('-220kohm') <= -219000


def test_le():
    # positive_numbers
    assert EngUnit('220kohm') <= EngUnit('221000ohm')
    assert EngUnit('220kohm') <= EngUnit('220000ohm')

    with pytest.raises(AttributeError):
        EngUnit('220kohm') >= 219000
    with pytest.raises(AttributeError):
        219000 >= EngUnit('220kohm')

    # negative_numbers
    assert EngUnit('-220kohm') >= EngUnit('-221000ohm')
    assert EngUnit('-220kohm') >= EngUnit('-220000ohm')

    with pytest.raises(AttributeError):
        EngUnit('-220kohm') <= -219000
    with pytest.raises(AttributeError):
        -219000 <= EngUnit('-220kohm')


def test_to_int():
    # positive_numbers
    assert int(EngUnit('220k')) == 220000
    assert int(EngUnit('220m')) == 0

    # negative_numbers
    assert int(EngUnit('-220k')) == -220000
    assert int(EngUnit('-220m')) == -0


def test_to_float():
    # positive_numbers
    assert float(EngUnit('220k')) == 220000.0
    assert float(EngUnit('220m')) == 0.220

    # negative_numbers
    assert float(EngUnit('-220k')) == -220000.0
    assert float(EngUnit('-220m')) == -0.220
