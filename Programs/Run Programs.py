import Math.Loan as loan

params = loan.LoanCalculatorParams(100000, 0.025, None, 120)
results = loan.LoanCalculator.equal_payments(params)

print(params.balance,"debt @",params.decimal_interest_rate(),"% interest paying ???/month")
print(results.term,"monthly payments of £",results.consecutive_equal_payment,"with a first payment of £",results.first_payment)
print("Total to pay: £", results.total_to_pay)

params = loan.LoanCalculatorParams(100000, 0.025, 4000, None)
results = loan.LoanCalculator.term_to_run(params)

print(params.balance,"debt @",params.decimal_interest_rate(),"% interest paying",params.payment_amount,"/month")
print(results.term,"monthly payments of £",results.consecutive_equal_payment,"with a first payment of £",results.first_payment)
print("Total to pay: £", results.total_to_pay)

params = loan.LoanCalculatorParams(params.balance, params.interest_rate, None, results.term)
results = loan.LoanCalculator.equal_payments(params)

print(params.balance,"debt @",params.decimal_interest_rate(),"% interest paying",params.payment_amount,"/month")
print(results.term,"monthly payments of £",results.consecutive_equal_payment,"with a first payment of £",results.first_payment)
print("Total to pay: £", results.total_to_pay)



