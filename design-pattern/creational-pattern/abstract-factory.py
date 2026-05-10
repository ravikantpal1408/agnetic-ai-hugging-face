from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        """all sub class must implement this"""
        pass


# fail = PaymentMethod()


# class Crypto(PaymentMethod)
#         pass


# fail_again = Crypto()


class CreditCard(PaymentMethod):
    def process_payment(self, amount):
        print(f"Changing ${amount} to credit card")


success = CreditCard()
success.process_payment(100)
