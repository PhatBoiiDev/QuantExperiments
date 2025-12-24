import math


class CouponBond:
    def __init__(self, principal, rate, maturity, interest_rate):

        self.principal = principal
        self.rate = rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def present_value(self, x, n):
        return x / (1 + self.interest_rate) ** n

    def calculate_price(self):
        price = 0
        # discount the coupon payments
        for t in (1, self.maturity + 1):
            price += self.present_value(self.principal * self.rate, t)

        # discount principle amount
        price += self.present_value(self.principal, self.maturity)

        return price

    def present_continuous_value(self, x, n):
        return x * math.e ** (-1 * self.interest_rate * n)

    def calculate_continuous_price(self):
        price = 0;
        for t in (1, self.maturity + 1):
            price += self.present_continuous_value(self.principal * self.rate, t)

        price += self.present_continuous_value(self.principal, self.maturity)

        return price

def write_to_output_file(content):
    """Write content to the financial analysis output file"""
    with open('../../financial_analysis_output.txt', 'a') as f:
        f.write(content + '\n')

if __name__ == "__main__":
    bond = CouponBond(1000, 10, 3, 4)
    
    # Calculate results
    discrete_price = bond.calculate_price()
    continuous_price = bond.calculate_continuous_price()
    
    # Create formatted output
    output_content = f"""
COUPON BOND ANALYSIS
===================
Bond Parameters:
- Principal Amount: ${bond.principal}
- Coupon Rate: {bond.rate*100}%
- Maturity: {bond.maturity} years
- Market Interest Rate: {bond.interest_rate*100}%

Results:
- Bond price (discrete model): ${discrete_price:.2f}
- Bond price (continuous model): ${continuous_price:.2f}
- Price difference: ${abs(discrete_price - continuous_price):.2f}
"""

    print(output_content)
    write_to_output_file(output_content)