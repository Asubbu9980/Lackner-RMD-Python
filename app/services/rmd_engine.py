from datetime import datetime
from app.services.life_tables import (
    TABLE_I_SINGLE,
    TABLE_III_UNIFORM
)
from app.services.helpers import get_rbd_age


def calculate_schedule(inputs: dict):

    max_years = 50
    rows = []

    balance = float(inputs["balance_Start"])

    growth_rate = float(inputs["growth_Rate"]) / 100
    tax_rate = float(inputs["tax_Rate"]) / 100

    birth_owner = int(inputs["year_Birth_Owner"])
    birth_beny = int(inputs["year_Birth_Beny"])

    death_date = inputs.get("date_Death_Owner")

    scenario = inputs["scenario"]

    cum_rmd = 0
    cum_tax = 0
    cum_growth = 0

    years_to_distribute = None

    if scenario in ["LIVING_UNIFORM", "LIVING_JOINT"]:

        rbd_age = get_rbd_age(birth_owner)

        start_age = int(rbd_age)

        start_year = birth_owner + start_age

        if scenario == "LIVING_JOINT":

            def factor_fn(age, year):

                uniform = TABLE_III_UNIFORM.get(age, 2.0)

                diff = max(0, (birth_beny - birth_owner) - 10)

                return uniform + (diff * 0.3)

        else:

            def factor_fn(age, year):
                return TABLE_III_UNIFORM.get(age, 2.0)

    elif scenario == "DECEASED_SPOUSE_INHERIT":

        death_year = datetime.fromisoformat(death_date).year

        start_year = death_year + 1
        start_age = start_year - birth_beny

        def factor_fn(age, year):
            return TABLE_I_SINGLE.get(age, 2.0)

    elif scenario == "DECEASED_EDB_SINGLELIFE":

        death_year = datetime.fromisoformat(death_date).year

        start_year = death_year + 1
        start_age = start_year - birth_beny

        initial_factor = TABLE_I_SINGLE.get(start_age, 2.0)

        def factor_fn(age, year):
            return max(initial_factor - (year - start_year), 1.0)

    elif scenario == "DECEASED_10YEAR":

        death_year = datetime.fromisoformat(death_date).year

        start_year = death_year + 1
        start_age = start_year - birth_beny

        years_to_distribute = 10

        def factor_fn(age, year):

            yr_in_plan = year - start_year + 1

            if yr_in_plan < 10:
                return float("inf")

            return 1.0

    elif scenario == "DECEASED_10YEAR_ANNUAL":

        death_year = datetime.fromisoformat(death_date).year

        start_year = death_year + 1
        start_age = start_year - birth_beny

        initial_factor = TABLE_I_SINGLE.get(start_age, 2.0)

        def factor_fn(age, year):

            yr_in_plan = year - start_year + 1

            if yr_in_plan >= 10:
                return 1.0

            return max(initial_factor - (year - start_year), 1.0)

    for i in range(max_years):

        year = start_year + i
        age = start_age + i

        if balance <= 0.01:
            break

        factor = factor_fn(age, year)

        rmd = 0 if factor == float("inf") else balance / factor

        rmd = min(rmd, balance)

        tax = rmd * tax_rate

        net = rmd - tax

        after_rmd = balance - rmd

        growth = after_rmd * growth_rate

        end_balance = after_rmd + growth

        cum_rmd += rmd
        cum_tax += tax
        cum_growth += growth

        rows.append({
            "yr": i + 1,
            "year": year,
            "age": age,
            "factor": None if factor == float("inf") else round(factor, 1),
            "beginBalance": round(balance, 2),
            "rmd": round(rmd, 2),
            "tax": round(tax, 2),
            "net": round(net, 2),
            "growth": round(growth, 2),
            "endBalance": round(end_balance, 2),
            "cumRmd": round(cum_rmd, 2),
            "cumTax": round(cum_tax, 2),
            "cumGrowth": round(cum_growth, 2)
        })

        balance = end_balance

        if years_to_distribute and (i + 1 >= years_to_distribute):
            break

    return {
        "balanceStart": inputs["balance_Start"],
        "totalRmd": round(cum_rmd, 2),
        "totalTax": round(cum_tax, 2),
        "totalGrowth": round(cum_growth, 2),
        "endingBalance": round(balance, 2),
        "rows": rows
    }