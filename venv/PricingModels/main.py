from math import exp
from datetime import datetime

def future_discrete_value(x, r, n):
    return x * (1 + r) ** n

def present_discrete_value(x, r, n):
    return x * (1 + r) ** -n

def future_continuous_value(x, r, t):
    return x * exp(r * t)

def present_continuous_value(x, r, t):
    return x * exp(-r * t)

def write_to_output_file(content):
    """Write content to the financial analysis output file"""
    with open('../../financial_analysis_output.txt', 'a') as f:
        f.write(content + '\n')

if __name__ == '__main__':
    # Clear and initialize the output file
    with open('../../financial_analysis_output.txt', 'w') as f:
        f.write(f"FINANCIAL ANALYSIS OUTPUT\n")
        f.write(f"========================\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"This file contains the complete output from all financial models in the project.\n\n")

    # value of investment in dollars
    x = 100
    # define the interest rate (r)
    r = 0.05
    # duration in years
    n = 5

    # Write to both console and file
    output_content = f"""
TIME VALUE OF MONEY CALCULATIONS
================================
Input Parameters:
- Initial Investment (x): ${x}
- Interest Rate (r): {r*100}%
- Time Period (n): {n} years

Results:
- Future value (discrete model): ${future_discrete_value(x, r, n):.2f}
- Present value (discrete model): ${present_discrete_value(x, r, n):.2f}
- Future value (continuous model): ${future_continuous_value(x, r, n):.2f}
- Present value (continuous model): ${present_continuous_value(x, r, n):.2f}
"""

    print(output_content)
    write_to_output_file(output_content)
