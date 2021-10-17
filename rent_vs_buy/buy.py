import numpy as np

from typing import Optional
from numbers import Real
from dataclasses import dataclass


from .utils import (
    continuous_rate,
    opportunity_cost,
    buyer_commission,
    mortgage_balance,
    seller_commission,
    property_transfer_tax,
)

# in %. last updated 2020
# source: https://www.wealthsimple.com/en-ca/learn/canadian-property-taxes
tax_rates = {
    "vancouver": 0.247,
    "toronto": 0.636,
    "montreal": 0.767,
    "kelowna": 0.526,
    "victoria": 0.520,
    "abbotsford": 0.513,
    "calgary": 0.636,
    "edmonton": 0.869,
    "lethbridge": 1.11,
    "burlington": 0.816,
    "ottawa": 1.068,
    "mississauga": 0.823,
    "waterloo": 1.11,
    "kitchener": 1.13,
    "hamilton": 1.26,
    "guelph": 1.17,
    "london": 1.35,
    "saint john": 1.79,
    "fredericton": 1.42,
    "saskatoon": 0.866,
    "regina": 1.07,
    "quebec": 0.878,
    "st. jonh's": 0.730,
    "halifax": 1.11,
    "winnipeg": 1.25,
}


@dataclass
class BuyConfiguration:
    """
    Class for describing a buy scenario. The default assumption here is that this is for an apartment, which will have strata fees, but relatively low maintainence. For fee-simple properties, remember to set the state-fee to 0 and account for maintainence.

    Units are % and $. Monthly fees  are specified in monthly terms.

    But all values will be returned as decimals for calculations. Ie. 7% -> 0.07 on annual basis.

    :param years: The number of years spent in the house.
    :param price: The price of the home.
    :param downpayment: The fraction of the home price in down payment. Default 20%.
    :param mortgage_rate: The mortgage rate. Default 3%.
    :param mortgage_term: The term of the mortgage. Default 25 years.
    :param appreciation: The estimated annual appreciation of the house. Default 2%.
    :param return_on_investment: The estimated annual market return on investment. Default 4%.
    :param inflation: The expected annual rate of inflation. Default 2%.
    :param city: The city the property is in. Used to determine the property tax rate.
    :param property_tax_rate: The property tax rate in %. If city is supported, current property tax rate with be filled in.
    :param maintenance: The cost of monthly maintenance, expressed as a fraction of the home value.
    :param strata_fee: The monthly condo/strata fee. Default 0.7% of home's value annually.
    :param insurance: The amonthly cost of insurance. Default 0.1% of home's value annually.
    :param utilities: The monthly cost of utilties. Default $100.
    """

    years: Real
    price: Real
    downpayment: Real = 20.0
    mortgage_rate: Real = 3.0
    mortgage_term: int = 25
    appreciation: Real = 2.0
    return_on_investment: Real = 4.0
    inflation: Real = 2.0
    city: str = "vancouver"
    property_tax_rate: Optional[Real] = None
    maintenance: Optional[Real] = None
    strata_fee: Optional[Real] = None
    insurance: Optional[Real] = None
    utilities: Real = 100

    def __post_init__(self):
        if self.strata_fee is None:
            # 0.7% strata fee
            self.strata_fee = 0.007 * self.home_price

        if self.insurance is None:
            # 0.1% insurance
            self.insurance = 0.001 * self.home_price

        if self.property_tax_rate is None:
            city = self.city.lower()
            assert city in tax_rates, f"Sorry, property tax rate for {self.city} is not known."
            self.property_tax_rate = tax_rates[city]

        # convert the percentages
        self.downpayment *= 0.01
        self.mortgage_rate *= 0.01
        self.appreciation *= 0.01
        self.return_on_investment *= 0.01
        self.inflation *= 0.01
        self.property_tax_rate *= 0.01

        # convert the monthly payments to annual
        self.maintenance *= 12
        self.strata_fee *= 12
        self.insurance *= 12
        self.utilities *= 12


def buy(
    parameters: BuyConfiguration,
    report: bool = False,
) -> float:
    """
    Calculate the net financial cost of buying a home.

    :param parameters: A configuration for buying a home.
    :param report: Print the breakdown.
    """
    years = parameters.years
    r = continuous_rate(annual_rate=parameters.appreciation, n_compounds=1)
    i = continuous_rate(annual_rate=parameters.inflation, n_compounds=1)

    # initial cost
    down_payment_cost = parameters.price * parameters.downpayment
    buyer_commission_cost = buyer_commission(parameters.price)
    property_tax_transfer_cost = property_transfer_tax(parameters.price)
    initial_costs = down_payment_cost + buyer_commission_cost + property_tax_transfer_cost

    # mortgage
    mortgage_amount = parameters.price * (1 - parameters.downpayment)
    interest_cost, principal_cost, balance = mortgage_balance(
        years, mortgage_amount, parameters.mortgage_rate, parameters.mortgage_term
    )
    mortgage_payment_total = interest_cost + principal_cost
    # recurring costs
    property_tax_total = parameters.property_tax_rate * parameters.price * (1 / r) * (np.exp(r * years) - np.exp(r * 0))
    maintenance_total = parameters.maintenance * (1 / r) * (np.exp(r * years) - np.exp(r * 0))
    insurance_total = parameters.insurance * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    utilities_total = parameters.utilities * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    strata_fee_total = parameters.strata_fee * (1 / i) * (np.exp(i * years) - np.exp(i * 0))

    recurring_costs = (
        property_tax_total
        + maintenance_total
        + insurance_total
        + utilities_total
        + strata_fee_total
        + mortgage_payment_total
    )

    # opportunity costs
    opportunity_cost_total = opportunity_cost(initial_costs, recurring_costs, years, parameters.return_on_investment)

    final_home_price = parameters.price * np.exp(r * years)
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
