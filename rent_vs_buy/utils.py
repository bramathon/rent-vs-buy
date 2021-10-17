import numpy as np

from numbers import Real
from typing import Tuple


def seller_commission(home_price: Real) -> float:
    """Calculate the seller commission on a home using the standard formula."""
    first_rate = 0.07
    second_rate = 0.025
    threshold = 100000
    return first_rate * min(threshold, home_price) + second_rate * max(0, home_price - threshold)


def buyer_commission(home_price: Real) -> float:
    """Calculate the buyer commission on a home using the standard formula."""
    first_rate = 0.03125
    second_rate = 0.011625
    threshold = 100000
    return first_rate * min(threshold, home_price) + second_rate * max(0, home_price - threshold)


def property_transfer_tax(home_price: Real) -> float:
    """Calculate the property transfer tax."""
    # for what jurisidiction?
    first_rate = 0.01
    second_rate = 0.02
    threshold = 200000
    return first_rate * min(threshold, home_price) + second_rate * max(0, home_price - threshold)


def continuous_rate(annual_rate: float, n_compounds: int = 1) -> float:
    """
    Convert an annual rate to a continuously compounding annual rate.

    ## Continuous Compounding

    All rates will be converted to continuously compounding.

    To convert from an annual interest rate, $r$, to a continuous rate, $r^*$:

    $r* = ln(r + 1)$

    This is easy because the period of the stated interest rate matches the compounding period. But sometimes annual rates are compounded at different intervals, eg monthly. In this case:

    $r* = ln$

    ### Calculating the future value

    Calculating the future value of an investment would normally be done as such:

    $V = V_{0}(1 + r/n)^{nt}$

    Where $n$ is the number of compounding periods and $r$ is the stated interest rate and $t$ is the time in interest rate periods.

    With continuous rates, this simply reads:

    $V=V_0e^{rt}$

    ### Calculating the Rate of Return

    To caluclation the continuous rate of return, we use

    $r_{log} = \frac{1}{t}\ln \big(\frac{V_f}{V_0}\big)$
    """
    annual_return = (1 + annual_rate / n_compounds) ** (n_compounds)
    r_log = np.log(annual_return)
    return r_log


def mortgage_payment(mortgage: Real, mortgage_rate: float, term: int = 25) -> float:
    """
    Calculate the monthly mortgage payment.

    :param mortgage: The amount of the mortgage.
    :param mortgage_rate: The annual mortgage interest rate.
    :param term: The length of the mortgage in years.
    :return: The mortgage payment in $/year.
    """
    # in Canada, mortgage interest is compounded semi-annually!
    # https://wowa.ca/calculators/mortgage-interest-calculator
    # mortgage interest and payments are calculated to the day, however
    cr = continuous_rate(mortgage_rate, 2)
    discount_factor = cr * np.exp(cr * term) / (np.exp(cr * term) - 1)
    annual_mortgage = mortgage * discount_factor
    return annual_mortgage


def mortgage_balance(years: Real, mortgage: Real, mortgage_rate: float, term: int = 25) -> Tuple[float, float, float]:
    """
    Calculate the mortgage balance.

    :param years: The number of years to calculate the balance at.
    :param mortgage: The amount of the mortgage.
    :param mortgage_rate: The annual mortgage interest rate.
    :param term: The length of the mortgage in years.
    :return: The interest_cost, the principal_cost and the principal balance
    """
    years = min(years, term)
    cr = continuous_rate(mortgage_rate, 2)
    annual_payment = mortgage_payment(mortgage, mortgage_rate, term)
    total_cost = annual_payment * years
    interest_cost = (mortgage * cr - annual_payment) * (np.exp(cr * years) - 1) / cr + annual_payment * years
    principal_cost = total_cost - interest_cost
    principal_balance = mortgage - principal_cost
    return interest_cost, principal_cost, principal_balance


def opportunity_cost(
    initial_cost: float,
    recurring_costs: float,
    years: Real,
    return_on_investment: float,
) -> float:
    """Calculate the opportunity cost of owning the house."""
    # note, I can't get this to match the NYT calculator. Not sure why.
    roi = continuous_rate(annual_rate=return_on_investment, n_compounds=1)
    initial_opportunity = initial_cost * (np.exp(roi * years) - 1)
    recurring_opportunity = (
        recurring_costs / (years * 12) * ((np.exp(roi / 12 * (years * 12)) - 1) / (np.exp(roi / 12) - 1) - years * 12)
    )
    return initial_opportunity + recurring_opportunity
