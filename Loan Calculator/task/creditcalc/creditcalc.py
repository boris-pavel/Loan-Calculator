import math
import argparse
import sys


def calculate_nominal_interest(interest):
    return (interest / 100) / 12


def calculate_payment(principal, periods, interest):
    i = calculate_nominal_interest(interest)
    return principal * i * (math.pow((i + 1), periods)) / (math.pow((i + 1), periods) - 1)


def calculate_principal(payment, periods, interest):
    i = calculate_nominal_interest(interest)
    return payment / ((i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1))


def calculate_periods(payment, principal, interest):
    i = calculate_nominal_interest(interest)
    return math.ceil(math.log(payment / (payment - i * principal), 1 + i))


def calculate_differentiated_payments(m, principal, interest, periods):
    i = calculate_nominal_interest(interest)
    return math.ceil(principal / periods + i * (principal - (principal * (m - 1) / periods)))


def calculate_total_differentiated_payments(periods, principal, interest):
    total = 0
    current_month = 1
    while current_month <= periods:
        total += calculate_differentiated_payments(current_month, principal, interest, periods)
        current_month += 1
    return total


def print_differentiated_payments(periods, principal, interest):
    current_month = 1
    while current_month <= periods:
        diff_payments = calculate_differentiated_payments(current_month, principal, interest, periods)
        print(f"Month {current_month}: payment is {diff_payments}")
        current_month += 1


def calculate_overpayment(principal, added_payments):
    return added_payments - principal


def convert_to_years(periods):
    months = periods % 12
    years = periods // 12

    if months == 0 and years == 1:
        return f"{years} year"
    elif months == 0 and years > 1:
        return f"{years} years"
    elif years == 0 and months > 1:
        return f"{months} months"
    elif years == 0 and months == 1:
        return f"{months} month"
    elif years > 1 and months == 1:
        return f"{years} years and {months} month"
    elif years == 1 and months > 1:
        return f"{years} year and {months} months"
    else:
        return f"{years} years and {months} months"


parser = argparse.ArgumentParser()
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--type")

args = parser.parse_args()

if args.payment is not None:
    float_payment = float(args.payment)
if args.principal is not None:
    float_principal = float(args.principal)
if args.periods is not None:
    float_periods = float(args.periods)
if args.interest is not None:
    float_interest = float(args.interest)


def run():
    # parameter checking
    for arg in vars(args):
        if getattr(args, arg) is not None and arg != "type" and float(getattr(args, arg)) < 0:
            print("Incorrect parameters")
            return
    if args.interest is None:
        print("Incorrect parameters")
        return

    # calculating payments
    match args.type:
        case "annuity":
            if args.payment is None:
                payment = math.ceil(calculate_payment(float_principal, float_periods, float_interest))
                print(f"Your monthly payment = {payment}!")
            elif args.principal is None:
                principal = int(calculate_principal(float_payment, float_periods, float_interest))
                print(f"Your loan principal = {principal}!")
                overpayment = calculate_overpayment(principal, float_periods*float_payment)
                print(f"Overpayment = {overpayment}")
            else:
                period = calculate_periods(float_payment, float_principal, float_interest)
                periods = convert_to_years(period)
                print(f"It will take {periods} to repay this loan!")
                overpayment = calculate_overpayment(float_principal, float_payment * period)
                print(f"Overpayment = {overpayment}")
        case "diff":
            # parameter checking
            if args.payment is not None:
                print("Incorrect parameters")
                return
            if len(sys.argv) < 4:
                print("Incorrect parameters")
                return

            print_differentiated_payments(float_periods, float_principal, float_interest)
            overpayment = calculate_overpayment(float_principal,
                                                calculate_total_differentiated_payments(float_periods, float_principal,
                                                                                        float_interest))
            print(f"Overpayment = {overpayment}")
        case _:
            print("Incorrect parameters")


run()
