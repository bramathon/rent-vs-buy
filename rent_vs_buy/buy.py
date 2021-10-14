import numpy as np

from numbers import Real

from .utils import (
    continuous_rate,
    opportunity_cost,
    buyer_commission,
    mortgage_payment,
    mortgage_balance,
    seller_commission,
    property_transfer_tax
)


def buy(
    years: Real,
    home_price: Real,
    appreciation: float,
    return_on_investment: float,
    mortgage_rate: float,
    maintenance: float,
    property_tax_rate: float,
    strata_fee: Real = 0,
    utilities: Real = 100,
    homeowner_insurance: float = 0.046,
    down_payment: float = 0.2,
    inflation: float = 0.02,
    mortgage_term: int = 25,
    report: bool = False,
) -> float:
    """
    Calculate the net financial cost of buying a house.

    :param years: The number of years spent in the house.
    :param home_price: The price of the home.
    :param appreciation: The estimated annual appreciation of the house.
    :param return_on_investment: The estimated annual return on investment from the market.
    :param mortgage_rate: The mortgage rate.
    :param maintenance: The cost of monthly maintenance, expressed as a fraction of the home value.
    :param property_tax_rate: The property tax rate.
    :param strata_fee: The monthly condo/strata fee. Default 0.
    :param utilities: The monthly cost of utilties.
    :param homeowner_insurance: The annual cost of insurance as a fraction of the home's value.
    :param down_payment: The fraction of the home price in down payment. Default 20%.
    :param inflation: The expected annual rate of inflation. Default is 2%.
    :param mortgage_term: The term of the mortgage. Default 25 years.
    :param report: Print the breakdown.
    """

    r = continuous_rate(annual_rate=appreciation, n_compounds=1)
    i = continuous_rate(annual_rate=inflation, n_compounds=1)

    # initial cost
    down_payment_cost = down_payment * home_price
    buyer_commission_cost = buyer_commission(home_price)
    property_tax_transfer_cost = property_transfer_tax(home_price)
    initial_costs = (
        down_payment_cost + buyer_commission_cost + property_tax_transfer_cost
    )

    # mortgage
    mortgage_amount = home_price * (1 - down_payment)
    interest_cost, principal_cost, balance = mortgage_balance(years, mortgage_amount, mortgage_rate, mortgage_term)
    mortgage_payment_total = interest_cost + principal_cost
    # recurring costs
    property_tax_total = (
        property_tax_rate * home_price * (1 / r) * (np.exp(r * years) - np.exp(r * 0))
    )
    maintenance_total = (
        maintenance * home_price * (1 / r) * (np.exp(r * years) - np.exp(r * 0))
    )
    insurance_total = (
        homeowner_insurance * 12 * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    )
    utilities_total = utilities * 12 * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    strata_fee_total = strata_fee * 12 * (1 / i) * (np.exp(i * years) - np.exp(i * 0))

    recurring_costs = (
        property_tax_total
        + maintenance_total
        + insurance_total
        + utilities_total
        + strata_fee_total
        + mortgage_payment_total
    )

    # opportunity costs
    opportunity_cost_total = opportunity_cost(
        initial_costs, recurring_costs, years, return_on_investment
    )

    final_home_price = home_price * np.exp(r * years)
    seller_commission_cost = seller_commission(final_home_price)
    proceeds = final_home_price - seller_commission_cost - balance

    net_cost = initial_costs + recurring_costs + opportunity_cost_total - proceeds

    if report:
        print("Initial Costs: ${0:,.0f}".format(initial_costs))
        print("  Down Payment: ${0:,.0f}".format(down_payment_cost))
        print("  Buyer Commission Cost: ${0:,.0f}".format(buyer_commission_cost))
        print("  Property Transfer Tax: ${0:,.0f}".format(property_tax_transfer_cost))
        print("Recurring Costs: ${0:,.0f}".format(recurring_costs))
        print("  Property Taxes: ${0:,.0f}".format(property_tax_total))
        print("  Maintenance: ${0:,.0f}".format(maintenance_total))
        print("  Insurance: ${0:,.0f}".format(insurance_total))
        print("  Utilities: ${0:,.0f}".format(utilities_total))
        print("  Strata Fees: ${0:,.0f}".format(strata_fee_total))
        print("  Mortgage Payments: ${0:,.0f}".format(mortgage_payment_total))
        print("Opportunity Costs: ${0:,.0f}".format(opportunity_cost_total))
        print("Proceeds: ${0:,.0f}".format(-proceeds))
        print("  Selling Price: ${0:,.0f}".format(-final_home_price))
        print("  Seller Commission: ${0:,.0f}".format(seller_commission_cost))
        print("  Mortgage Balance: ${0:,.0f}".format(balance))
        print("Net Cost: ${0:,.0f}".format(net_cost))

    return np.round(net_cost)