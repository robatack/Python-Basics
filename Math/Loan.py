import Math

class LoanCalculatorParams(object):
    def __init__(self, outstanding_balance, interest_rate, payment_amount, term):
        self.balance = outstanding_balance
        self.interest_rate = interest_rate
        self.payment_amount = payment_amount
        self.term = term

    def rate_over_term(self, term=None):
        return self.rate_over_term_less(term, 0)

    def rate_over_term_less(self, term=None, less=0):
        if self.interest_rate > 0:
            if term is None:
                if self.term is not None:
                    term = self.term
                else:
                    term = self.payment_frequency

            return (1 + self.checked_interest_rate()) ** term - less

        else:
            return None

    def decimal_interest_rate(self):
        #this should be a %age as float so anything onver 1 is > 100%
        return self.checked_interest_rate() * 100

    def checked_interest_rate(self):
        #this should be a %age as float so anything onver 1 is > 100%
        assumed = self.interest_rate

        if self.interest_rate >= 1:
            assumed = self.interest_rate / 100

        return assumed

    def growth_rate(self):
        return 1 + self.checked_interest_rate()

    def validate_balance(self):
        if self.balance <= 0:
            raise ValueError('Minimum balance to calculate payments for must be > 0')

    def validate_interest_rate(self):
        if self.interest_rate < 0:
            raise ValueError('Interest rate to calculate payments for must be >= 0')

    def validate_term(self):
        if self.term <= 0:
            raise ValueError('The payment term must be > 0')

    def validate_payment_amount(self):
        if self.payment_amount <= 0:
            raise ValueError('Payment amount made must be > 0')

class LoanPayments(object):
    def __init__(self, first_payment, term, consecutive_equal_payment = None):
        self.first_payment = first_payment
        if consecutive_equal_payment is None:
            self.consecutive_equal_payment = first_payment
        else:
            self.consecutive_equal_payment = consecutive_equal_payment
        self.term = term

    @property
    def total_to_pay(self):
        return self.consecutive_equal_payment * (self.term - 1) + self.first_payment

class LoanCalculator(LoanCalculatorParams):
    def equal_payments(self):
        self.validate_balance()
        self.validate_interest_rate()
        self.validate_term()

        equal_payment = self.balance * ((self.interest_rate * self.rate_over_term().__float__()) /
                                         self.rate_over_term_less(less=1).__float__())

        rounded_equal_payment = float.__round__(equal_payment, 2)
        diff = float.__round__(abs(float.__round__(equal_payment * self.term, 2) - (rounded_equal_payment * self.term)), 2)
        first_payment = float.__round__(diff + equal_payment, 2)

        return LoanPayments(first_payment, self.term, rounded_equal_payment)

    def term_to_run(self):
        self.validate_balance()
        self.validate_interest_rate()
        self.validate_payment_amount()

        tries = 0

        #set a starting point guess for the term
        term = int((self.balance / self.payment_amount) * self.decimal_interest_rate())

        #keep the last guess so we can adjust through iterations
        last_term = 0

        while tries < 25:
            tries += 1

            fv = (self.balance * self.rate_over_term(term).__float__()) - \
                    (self.payment_amount * (self.rate_over_term_less(term, 1).__float__() / self.interest_rate))

            if fv > 0:
                last_term = term

                if fv < self.payment_amount:
                    #stop here
                    self.term = term
                    results = LoanCalculator.equal_payments(self)

                    loan_details = LoanPayments(results.first_payment, term, results.consecutive_equal_payment)
                    return loan_details
                else:
                    term = int(term * 1.2)

            elif fv < 0:
                term -= int(abs(term - last_term) / 2)

        return None