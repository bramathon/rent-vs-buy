import numpy as np

from numbers import Real

from .utils import continuous_rate, opportunity_cost


def rent(
    years: Real,
    monthly_rent: Real,
    rent_increase: float,
    renter_insurance_rate: float,
    return_on_investment: float,
    inflation: float,
    report: bool = False,
) -> float:
    """
    Calculate the total cost of renting.

    :param years:
    :param monthly_rent: Monthly rent.
    :param rent_increase: Annual rent increase.
    :param renter_insurance_rate:
    :param return_on_investment:
    :param report:
    """
    i = continuous_rate(annual_rate=inflation, n_compounds=1)
    r = continuous_rate(annual_rate=rent_increase, n_compounds=1)

    initial_costs = monthly_rent / 2
    insurance_total = (
        renter_insurance_rate * 12 * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    )
    rent_total = monthly_rent * 12 * (1 / i) * (np.exp(r * years) - np.exp(r * 0))
    recurring_costs = rent_total + insurance_total
    opportunity_cost_total = opportunity_cost(
        initial_costs, recurring_costs, years, return_on_investment
    )
    proceeds = initial_costs
    net_cost = initial_costs + recurring_costs + opportunity_cost_total - proceeds

    if report:
        print("Initial Costs: ${0:,.0f}".format(initial_costs))
        print("Recurring Costs: ${0:,.0f}".format(recurring_costs))
        print("Opportunity Costs: ${0:,.0f}".format(opportunity_cost_total))
        print("Proceeds: ${0:,.0f}".format(-proceeds))
        print("Net Cost: ${0:,.0f}".format(net_cost))

    return np.round(net_cost)