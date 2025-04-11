"""
I calculated the trade-off between salary and equity by comparing the total value of the shares over the
4-year vesting period with the total additional salary I’m requesting over the same timeframe. Since shares
are granted with a 4-year vesting schedule, it makes sense to compare them to the full salary I would earn
in that period. For example, increasing the salary by 1,000 kr/month results in an additional 48,000 kr
over 4 years. At todays share price, this corresponds to about 218 shares. So to keep total
compensation balanced, a higher salary would fairly come with a proportional reduction in equity based
on current share value.
"""

import numpy as np
import pandas as pd


def compute_salary_equity_tradeoff(
    base_salary: float = 42000,  # Starting monthly salary in SEK
    base_shares: int = 3142,  # Number of shares offered at base salary
    base_percentage: float = 0.8,  # Corresponding percentage of company equity
    share_price: float = 220,  # Current market value of a single share in SEK
    salary_increment: float = 1000,  # How much you want to increase salary per step (in SEK/month)
    steps: int = 7,  # Number of salary levels (rows in the output table)
    vesting_years: int = 4,  # Equity vests over this many years
) -> pd.DataFrame:
    """
    Generate a table that shows, for each salary increase step, the fair reduction in equity,
    assuming you're trading long-term salary increases for fewer shares.

    The tradeoff is computed by comparing the total additional salary (over 4 years)
    with the value of the shares given up (at today's share price).
    """

    # Calculate total value of the full share package today
    base_equity_value = base_shares * share_price

    # Derive the total number of company shares from the offer
    # For example, if 3,142 shares = 0.8%, then total = 3,142 / 0.008 = ~392,750
    total_shares = base_shares / base_percentage

    # Store results in a list of dictionaries, each one representing a row
    results = []

    for i in range(steps):
        # Compute the new salary for this step
        salary = base_salary + i * salary_increment

        # Compute the total additional salary earned over the full vesting period
        # For example, a 1,000 kr/month increase over 4 years = 48,000 kr extra
        extra_salary_total = i * salary_increment * 12 * vesting_years

        # Subtract that value from the original equity value to keep compensation constant
        equity_value = base_equity_value - extra_salary_total

        # Convert remaining equity value into number of shares at today's price
        n_qeso = round(equity_value / share_price)

        # Calculate what percent of the company those shares represent
        perc_qeso = n_qeso / total_shares

        # Store this step in the results table
        results.append(
            {
                "Salary": salary,  # Updated salary level
                "N_qeso": n_qeso,  # Fair number of shares at this salary
                "perc_qeso": perc_qeso,  # What % of the company that represents
            }
        )

    # Return the table as a DataFrame
    return pd.DataFrame(results)


for share_price in np.arange(180, 260, 10):
    print(f"Share price: {share_price} SEK")
    df = compute_salary_equity_tradeoff(share_price=share_price)
    print(df.to_string(index=False))
    print("\n")
