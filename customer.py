"""
Customer Module - Customer management with membership
Demonstrates: Encapsulation, Composition
"""


class Customer:
    """
    Customer class with membership support
    Demonstrates encapsulation
    """
    
    def __init__(self, customer_id, name, phone, email):
        self.__customer_id = customer_id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__membership = None  # Composition - can have a membership
        self.__purchase_history = []
    
    # Getters
    def get_customer_id(self):
        return self.__customer_id
    
    def get_name(self):
        return self.__name
    
    def get_phone(self):
        return self.__phone
    
    def get_email(self):
        return self.__email
    
    def get_membership(self):
        return self.__membership
    
    def get_purchase_history(self):
        return self.__purchase_history
    
    # Setters
    def set_phone(self, phone):
        self.__phone = phone
    
    def set_email(self, email):
        self.__email = email
    
    def set_membership(self, membership):
        """Composition - associate a membership with customer"""
        self.__membership = membership
    
    def add_to_history(self, bill):
        """Add bill to purchase history"""
        self.__purchase_history.append(bill)
    
    def get_total_spent(self):
        """Calculate total amount spent by customer"""
        return sum(bill.get_final_amount() for bill in self.__purchase_history)
    
    def __str__(self):
        membership_status = "Member" if self.__membership else "Non-Member"
        return f"Customer: {self.__name} ({membership_status})"


class Membership:
    """
    Membership class for loyalty program
    Demonstrates encapsulation and composition
    """
    
    MEMBERSHIP_TYPES = {
        'SILVER': {'discount': 0.05, 'min_purchase': 1000},
        'GOLD': {'discount': 0.10, 'min_purchase': 5000},
        'PLATINUM': {'discount': 0.15, 'min_purchase': 10000}
    }
    
    def __init__(self, membership_id, membership_type, points=0):
        if membership_type not in self.MEMBERSHIP_TYPES:
            raise ValueError(f"Invalid membership type: {membership_type}")
        
        self.__membership_id = membership_id
        self.__membership_type = membership_type
        self.__points = points
    
    def get_membership_id(self):
        return self.__membership_id
    
    def get_membership_type(self):
        return self.__membership_type
    
    def get_points(self):
        return self.__points
    
    def get_discount(self):
        """Get membership discount percentage"""
        return self.MEMBERSHIP_TYPES[self.__membership_type]['discount']
    
    def add_points(self, amount):
        """Add loyalty points (1 point per 100 rupees spent)"""
        self.__points += int(amount / 100)
    
    def redeem_points(self, points):
        """Redeem points for discount (1 point = 1 rupee)"""
        if points > self.__points:
            raise ValueError("Insufficient points")
        self.__points -= points
        return points
    
    def upgrade_membership(self, total_spent):
        """Auto-upgrade membership based on spending"""
        if total_spent >= self.MEMBERSHIP_TYPES['PLATINUM']['min_purchase']:
            self.__membership_type = 'PLATINUM'
        elif total_spent >= self.MEMBERSHIP_TYPES['GOLD']['min_purchase']:
            self.__membership_type = 'GOLD'
        elif total_spent >= self.MEMBERSHIP_TYPES['SILVER']['min_purchase']:
            self.__membership_type = 'SILVER'
    
    def __str__(self):
        return f"{self.__membership_type} Membership (Points: {self.__points})"