import numpy as np
from typing import Optional
from numbers import Real
from dataclasses import dataclass

from .utils import continuous_rate, opportunity_cost

@dataclass
class RentConfiguration:
    """
    Class for describing a rent scenario.
    
    Units are % and $. Monthly fees are specified in monthly terms.
    
    However, all values will be returned as decimals for calculations. Ie. 7% -> 0.07 on annual basis.
    
    :param years: The number of years spent in the house.
    :param rent: The monthly rent of the home.
    :param rent_increase: The annual rent increase. Default 2%.
    :param deposit: The deposit. Default 0.5 months rents.
    :param insurance: The monthly cost of insurance. Default $15.
    :param return_on_investment: The estimated annual market return on investment. Default 4%.
    :param inflation: The expected annual rate of inflation. Default 2%.
    :param utilities: The monthly cost of utilties. Default $100.
    """
    years: Real
    rent: Real
    deposit: Optional[Real] = None
    rent_increase: Real = 2.0
    insurance: Real = 15
    return_on_investment: Real = 4.0
    inflation: Real = 2.0
    utilities: Real = 100
    
    def __post_init__(self):
        
        if self.deposit is None:
            # 0.1% insurance
            self.deposit = 0.5*self.rent
            
        # convert the percentages
        self.rent_increase *= 0.01
        self.return_on_investment *= 0.01
        self.inflation *= 0.01
        
        # convert the monthly payments to annual
        self.rent *= 12
        self.utilities *= 12
        
        
def rent(
    parameters: RentConfiguration,
    report: bool = False,
) -> float:
    """
    Calculate the total cost of renting.

    :param parameters: A rent configuration.
    :param report: Print the breakdown.
    """
    years = parameters.years
    
    i = continuous_rate(annual_rate=parameters.inflation, n_compounds=1)
    r = continuous_rate(annual_rate=parameters.rent_increase, n_compounds=1)

    initial_costs = parameters.deposit
    insurance_total = (
        parameters.insurance * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
    )
    rent_total = parameters.rent * (1 / r) * (np.exp(r * years) - np.exp(r * 0))
    recurring_costs = rent_total + insurance_total
    opportunity_cost_total = opportunity_cost(
        initial_costs, recurring_costs, years, parameters.return_on_investment
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

# def rent(
#     years: Real,
#     monthly_rent: Real,
#     rent_increase: float,
#     renter_insurance_rate: float,
#     return_on_investment: float,
#     inflation: float,
#     report: bool = False,
# ) -> float:
#     """
#     Calculate the total cost of renting.

#     :param years:
#     :param monthly_rent: Monthly rent.
#     :param rent_increase: Annual rent increase.
#     :param renter_insurance_rate:
#     :param return_on_investment:
#     :param report:
#     """
#     i = continuous_rate(annual_rate=inflation, n_compounds=1)
#     r = continuous_rate(annual_rate=rent_increase, n_compounds=1)

#     initial_costs = monthly_rent / 2
#     insurance_total = (
#         renter_insurance_rate * 12 * (1 / i) * (np.exp(i * years) - np.exp(i * 0))
#     )
#     rent_total = monthly_rent * 12 * (1 / i) * (np.exp(r * years) - np.exp(r * 0))
#     recurring_costs = rent_total + insurance_total
#     opportunity_cost_total = opportunity_cost(
#         initial_costs, recurring_costs, years, return_on_investment
#     )
#     proceeds = initial_costs
#     net_cost = initial_costs + recurring_costs + opportunity_cost_total - proceeds

#     if report:
#         print("Initial Costs: ${0:,.0f}".format(initial_costs))
#         print("Recurring Costs: ${0:,.0f}".format(recurring_costs))
#         print("Opportunity Costs: ${0:,.0f}".format(opportunity_cost_total))
#         print("Proceeds: ${0:,.0f}".format(-proceeds))
#         print("Net Cost: ${0:,.0f}".format(net_cost))

#     return np.round(net_cost)