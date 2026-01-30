"""
Payment Processing Module
Demonstrates: Polymorphism, Abstraction, Strategy Pattern
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Payment(ABC):
    """
    Abstract base class for all payment methods
    Demonstrates abstraction and polymorphism
    """
    
    def __init__(self, amount):
        self._amount = amount
        self._payment_id = None
        self._timestamp = None
        self._status = "PENDING"
    
    @abstractmethod
    def process_payment(self):
        """Process the payment - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_payment_method(self):
        """Get payment method name"""
        pass
    
    def get_amount(self):
        return self._amount
    
    def get_payment_id(self):
        return self._payment_id
    
    def get_status(self):
        return self._status
    
    def get_timestamp(self):
        return self._timestamp
    
    def _generate_payment_id(self):
        """Generate unique payment ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"PAY{timestamp}"
    
    def __str__(self):
        return f"Payment of Rs.{self._amount:.2f} via {self.get_payment_method()}"


class CashPayment(Payment):
    """
    Cash payment implementation
    Demonstrates polymorphism
    """
    
    def __init__(self, amount, cash_received):
        super().__init__(amount)
        self.__cash_received = cash_received
        self.__change = 0
    
    def process_payment(self):
        """Process cash payment"""
        if self.__cash_received < self._amount:
            self._status = "FAILED"
            raise ValueError(f"Insufficient cash. Need Rs.{self._amount:.2f}, received Rs.{self.__cash_received:.2f}")
        
        self.__change = self.__cash_received - self._amount
        self._payment_id = self._generate_payment_id()
        self._timestamp = datetime.now()
        self._status = "SUCCESS"
        
        return {
            'payment_id': self._payment_id,
            'amount': self._amount,
            'cash_received': self.__cash_received,
            'change': self.__change,
            'status': self._status
        }
    
    def get_payment_method(self):
        return "Cash"
    
    def get_change(self):
        return self.__change
    
    def __str__(self):
        return f"Cash Payment: Rs.{self._amount:.2f} | Change: Rs.{self.__change:.2f}"


class CardPayment(Payment):
    """
    Card payment (Credit/Debit) implementation
    Demonstrates polymorphism
    """
    
    def __init__(self, amount, card_number, card_holder, cvv):
        super().__init__(amount)
        self.__card_number = self.__mask_card_number(card_number)
        self.__card_holder = card_holder
        self.__cvv = cvv
    
    def __mask_card_number(self, card_number):
        """Mask card number for security"""
        if len(card_number) < 4:
            return "****"
        return "****-****-****-" + card_number[-4:]
    
    def process_payment(self):
        """Process card payment"""
        # Simulate card validation
        if len(self.__cvv) != 3:
            self._status = "FAILED"
            raise ValueError("Invalid CVV")
        
        # Simulate payment processing
        self._payment_id = self._generate_payment_id()
        self._timestamp = datetime.now()
        self._status = "SUCCESS"
        
        return {
            'payment_id': self._payment_id,
            'amount': self._amount,
            'card_number': self.__card_number,
            'card_holder': self.__card_holder,
            'status': self._status
        }
    
    def get_payment_method(self):
        return "Card"
    
    def __str__(self):
        return f"Card Payment: Rs.{self._amount:.2f} | Card: {self.__card_number}"

class WalletPayment(Payment):
    """
    Digital wallet payment implementation
    Demonstrates polymorphism
    """
    
    def __init__(self, amount, wallet_type, phone_number):
        super().__init__(amount)
        self.__wallet_type = wallet_type  # esewa, khalti etc.
        self.__phone_number = phone_number
        self.__transaction_id = None
    
    def process_payment(self):
        """Process wallet payment"""
        # Validate phone number
        if len(self.__phone_number) != 10:
            self._status = "FAILED"
            raise ValueError("Invalid phone number")
        
        # Simulate wallet payment processing
        self._payment_id = self._generate_payment_id()
        self._timestamp = datetime.now()
        self.__transaction_id = f"{self.__wallet_type[:3].upper()}{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._status = "SUCCESS"
        
        return {
            'payment_id': self._payment_id,
            'amount': self._amount,
            'wallet_type': self.__wallet_type,
            'phone_number': self.__phone_number,
            'transaction_id': self.__transaction_id,
            'status': self._status
        }
    
    def get_payment_method(self):
        return f"Wallet ({self.__wallet_type})"
    
    def __str__(self):
        return f"Wallet Payment: Rs.{self._amount:.2f} | {self.__wallet_type}"


class PaymentProcessor:
    """
    Payment processor class
    Demonstrates Strategy Pattern
    """
    
    def __init__(self):
        self.__payment_history = []
    
    def process(self, payment):
        """
        Process any payment type
        Demonstrates polymorphism - works with any Payment subclass
        """
        try:
            result = payment.process_payment()
            self.__payment_history.append(payment)
            return result
        except Exception as e:
            return {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def get_payment_history(self):
        return self.__payment_history
    
    def get_total_processed(self):
        """Get total amount processed"""
        return sum(p.get_amount() for p in self.__payment_history if p.get_status() == "SUCCESS")
    
    def generate_payment_receipt(self, payment):
        """Generate payment receipt"""
        receipt = "\n" + "=" * 50 + "\n"
        receipt += " " * 15 + "PAYMENT RECEIPT\n"
        receipt += "=" * 50 + "\n"
        receipt += f"Payment ID: {payment.get_payment_id()}\n"
        receipt += f"Method: {payment.get_payment_method()}\n"
        receipt += f"Amount: Rs.{payment.get_amount():.2f}\n"
        receipt += f"Status: {payment.get_status()}\n"
        receipt += f"Date/Time: {payment.get_timestamp().strftime('%d-%m-%Y %H:%M:%S')}\n"
        
        # Add specific details based on payment type
        if isinstance(payment, CashPayment):
            receipt += f"Change: Rs.{payment.get_change():.2f}\n"
        elif isinstance(payment, UPIPayment):
            receipt += f"Transaction Ref: {payment.get_transaction_ref()}\n"
        
        receipt += "=" * 50 + "\n"
        return receipt