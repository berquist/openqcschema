from decimal import Decimal

import pytest
import os

import qcelemental


@pytest.mark.parametrize("inp", ["He100", '-1', -1, -1.0, 'cat', 200, 'Cr_highspin', 'Bk'])
def test_id_resolution_error(inp):
    with pytest.raises(qcelemental.exceptions.NotAnElementError):
        ans = qcelemental.covalentradii.get(inp)


a2b = 1. / qcelemental.constants.bohr2angstroms


@pytest.mark.parametrize(
    "inp,expected",
    [
        # Kr 84
        ("KRYPTON", 1.16),
        ("kr", 1.16),
        ("kr84", 1.16),
        (36, 1.16),

        # aliases
        ("C", 0.76),
        ("C_sp", 0.69),
        ("MN", 1.61),
        ("Mn_lowspin", 1.39),

        # Deuterium
        ("D", 0.31),
        ("h2", 0.31),
    ])
def test_get(inp, expected):
    assert qcelemental.covalentradii.get(inp) == pytest.approx(expected, 1.e-9)
    assert qcelemental.covalentradii.get(inp, units='bohr') == pytest.approx(a2b * expected, 1.e-9)


def test_c_header():
    qcelemental.covalentradii.write_c_header("header.h")
    os.remove("header.h")


#@pytest.mark.xfail(True, reason='comparison data not available for installed repository', run=True, strict=False)
#def test_constants_comparison():
#    qcelemental.constants.run_comparison()


def test_representation():
    qcelemental.covalentradii.string_representation()


#def test_str():
#    assert "PhysicalConstantsContext(" in str(qcelemental.constants)


def test_covradmaker2018():
    with pytest.raises(KeyError) as e:
        qcelemental.CovalentRadii("COVRADMAKER2018")

    assert "only contexts {'ALVAREZ2008', } are currently supported" in str(e)
