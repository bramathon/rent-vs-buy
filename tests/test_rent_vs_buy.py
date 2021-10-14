import numpy as np

from rent_vs_buy import __version__
from rent_vs_buy.utils import mortgage_payment, mortgage_balance


def test_version():
    assert __version__ == "0.1.0"


def test_mortgage_payment():
    """Test whether the monthly mortgage payment is calculated correctly."""
    
    # note there is still a very slight discrepancy between my calculation and the online calculators
    # https://www.cmhc-schl.gc.ca/en/consumers/home-buying/calculators/mortgage-calculator
    # https://tools.td.com/mortgage-payment-calculator/

    mortgage = 150000
    mortgage_rate = 0.0229
    mortgage_term = 25
    annual_payment = mortgage_payment(mortgage, mortgage_rate, mortgage_term)
    monthly_payment = annual_payment/12
    assert np.isclose(monthly_payment, 656.36, rtol=0.01), f"${monthly_payment:.2f} does not equal $656.36"
    
    mortgage = 150000
    mortgage_rate = 0.0459
    mortgage_term = 25
    annual_payment = mortgage_payment(mortgage, mortgage_rate, mortgage_term)
    monthly_payment = annual_payment/12
    assert np.isclose(monthly_payment, 837.73, rtol=0.01), f"${monthly_payment:.2f} does not equal $837.73"
    
    mortgage = 250000
    mortgage_rate = 0.0459
    mortgage_term = 25
    annual_payment = mortgage_payment(mortgage, mortgage_rate, mortgage_term)
    monthly_payment = annual_payment/12
    assert np.isclose(monthly_payment, 1396.22, rtol=0.01), f"${monthly_payment:.2f} does not equal $1,396.22"


def test_mortgage_balance():
    """Test the mortgage balance calculation."""
    
    years = 5
    mortgage = 150000
    mortgage_rate = 0.0229
    mortgage_term = 25
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage, mortgage_rate, mortgage_term)

    total_payments = interest_cost + principal_cost
    assert np.isclose(total_payments, 39381.60, rtol=0.01), f"${total_payments:.2f} does not equal $39,381.60"
    assert np.isclose(interest_cost, 15796.17, rtol=0.01), f"${interest_cost:.2f} does not equal $15,796.17"
    assert np.isclose(principal_cost, 23585.43, rtol=0.01), f"${principal_cost:.2f} does not equal $23,585.43"
    assert np.isclose(balance, 126414.57, rtol=0.01), "${balance:.2f} does not equal $126,414.57"
    
    years = 5
    mortgage = 150000
    mortgage_rate = 0.0459
    mortgage_term = 25
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage, mortgage_rate, mortgage_term)

    total_payments = interest_cost + principal_cost
    assert np.isclose(total_payments, 50263.80, rtol=0.01), f"${total_payments:.2f} does not equal $50,263.80"
    assert np.isclose(interest_cost, 32149.76, rtol=0.01), f"${interest_cost:.2f} does not equal $32,149.76"
    assert np.isclose(principal_cost, 18114.04, rtol=0.01), f"${principal_cost:.2f} does not equal $18,114.04"
    assert np.isclose(balance, 131885.96, rtol=0.01), f"${balance:.2f} does not equal $131,885.96"
    
    years = 5
    mortgage = 250000
    mortgage_rate = 0.0459
    mortgage_term = 25
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage, mortgage_rate, mortgage_term)

    total_payments = interest_cost + principal_cost
    assert np.isclose(total_payments, 83773.20, rtol=0.01), f"${total_payments:.2f} does not equal $83,773.20"
    assert np.isclose(interest_cost, 53582.82, rtol=0.01), f"${interest_cost:.2f} does not equal $53,582.82"
    assert np.isclose(principal_cost, 30190.38, rtol=0.01), f"${principal_cost:.2f} does not equal $30,190.38"
    assert np.isclose(balance, 219809.62, rtol=0.01), f"${balance:.2f} does not equal $219,809.62"
    
    years = 25
    mortgage = 150000
    mortgage_rate = 0.0229
    mortgage_term = 25
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage, mortgage_rate, mortgage_term)

    total_payments = interest_cost + principal_cost
    assert np.isclose(total_payments, 196909.12, rtol=0.01), f"${total_payments:.2f} does not equal $196,909.12"
    assert np.isclose(interest_cost, 46909.12, rtol=0.01), f"${interest_cost:.2f} does not equal $46,909.12"
    assert np.isclose(principal_cost, 150000, rtol=0.01), f"${principal_cost:.2f} does not equal $150,000.00"
    assert np.isclose(balance, 0.00, rtol=0.01), f"${balance:.2f} does not equal $0.00"
    
    years = 50
    mortgage = 150000
    mortgage_rate = 0.0229
    mortgage_term = 25
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage, mortgage_rate, mortgage_term)

    total_payments = interest_cost + principal_cost
    assert np.isclose(total_payments, 196909.12, rtol=0.01), f"${total_payments:.2f} does not equal $196,909.12"
    assert np.isclose(interest_cost, 46909.12, rtol=0.01), f"${interest_cost:.2f} does not equal $46,909.12"
    assert np.isclose(principal_cost, 150000, rtol=0.01), f"${principal_cost:.2f} does not equal $150,000.00"
    assert np.isclose(balance, 0.00, rtol=0.01), f"${balance:.2f} does not equal $0.00"