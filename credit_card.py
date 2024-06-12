
"""
Driver: Jordan Lin
Navigator: None
Assignment: Homework 1 - Credit Card
"""
from argparse import ArgumentParser
import sys

def get_min_payment(balance, fees):
    """Determine the minimum credit card payment

    Args:
        balance (int) : The total amount of the balance in an account that is left to pay 
        fees (int) : The fees associated with the credit card account

    Returns:
        int: the minimum credit card payment
    """
    min_payment = ((balance * 0.02) + fees) #min_payment = ((b * m) + f)
    #if min payment is less than 25 return 25
    if min_payment < 25:
        return 25
    return min_payment
    
def interest_charged(balance, apr):
    """Compute and return i, the amount of interest accrued in the next payment according to the
    formula i = (a/y)*b*d 

    Args:
        balance (int) : The balance of the credit card
        apr (int ) : int between 0 and 100; the annual APR

    """
    return apr/100/365*balance*30

def remaining_payments(balance, apr, targetamount, credit_line=5000, fees=0):
    """Compute and return the number of payments required to pay off the credit card balance.

    Args:
        balance (int ) : the balance of the credit card
        apr (int) : int between 0 and 100; the annual APR
        targetamount (int) : the target 
        credit_line (int) : the credit line. The maximum amount of balance that an account holder 
        can keep in their account.
        fees (int) : the amount of fees that will be charged in addition to the minimum payment.

    Returns:
        tuple : all counters together as a tuple which represent the number of months that
        the balance remains over 25%, 50% and 75%
    """
    payments = 0
    months25 = 0
    months50 = 0
    months75 = 0
    while balance > 0:
        if (targetamount == None):
            targetamount = get_min_payment()
        balanceAmount = targetamount - interest_charged(balance, apr)
        if balanceAmount < 0:
            print("The card balance cannot be paid off")
            exit()
        balance = balance - balanceAmount
        if balance > 0.75 * credit_line:
            months25 += 1
        if balance > 0.5 * credit_line:
            months50 += 1
        if balance > 0.25 * credit_line:
            months25 += 1
        payments += 1
    return payments, months25, months50, months75

def main(balance, apr, targetamount, credit_line=5000, fees=0):
    """Tell the user how many payments they will have above 25, 50 and 75 percent thresholds
    
    Args:
        balance (int ) : the balance of the credit card
        apr (int) : int between 0 and 100; the annual APR
        targetamount (int) : the target 
        credit_line (int) : the credit line. The maximum amount of balance that an account holder 
        can keep in their account.
        fees (int) : the amount of fees that will be charged in addition to the minimum payment.

    Returns:
        str : message that will tell the user how many payments they will be
        above 25, 50 and 75 percent thresholds.
    """
    print("Your recommended starting minimum pay is $" + get_min_payment(balance, fees) + ".")
    pays_minimun = False
    if targetamount == None:
        pays_minimum = True
    if targetamount < get_min_payment():
        print("Your target payment is less than the minimum payment for this credit card")
        exit()
    remaining = remaining_payments(balance, apr, targetamount, credit_line, fees)
    if targetamount >= get_min_payment(balance, fees):
        str = "If you pay the minimum payments each month, you will pay off the balance in " + remaining + " payments."
    else:
        str = "If you make payments of $" + get_min_payment(balance, fees) + ", you will pay off the balance in " + remaining + " payments."
    print(str)
    payments, months25, months50, months75 = remaining_payments(balance, apr, targetamount, credit_line, fees)
    return str

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))