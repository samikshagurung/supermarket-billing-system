"""
Cart and Billing Module
Demonstrates: Composition, Aggregation, Association
"""

from datetime import datetime


class CartItem:
    """
    Individual item in shopping cart
    Demonstrates composition
    """
    
    def __init__(self, product, quantity):
        self.__product = product  # Composition - cart item contains product
        self.__quantity = quantity
    
    def get_product(self):
        return self.__product
    
    def get_quantity(self):
        return self.__quantity
    
    def set_quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.__quantity = quantity
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.__product.get_total_price(self.__quantity)
    
    def __str__(self):
        return f"{self.__product.get_name()} x {self.__quantity} = Rs.{self.get_subtotal():.2f}"


class ShoppingCart:
    """
    Shopping cart containing multiple items
    Demonstrates aggregation and composition
    """
    
    def __init__(self):
        self.__items = []  # Aggregation - cart contains multiple cart items
    
    def add_item(self, product, quantity):
        """Add product to cart"""
        # Check if product already in cart
        for item in self.__items:
            if item.get_product().get_product_id() == product.get_product_id():
                new_quantity = item.get_quantity() + quantity
                item.set_quantity(new_quantity)
                return
        
        # Add new item
        cart_item = CartItem(product, quantity)
        self.__items.append(cart_item)
    
    def remove_item(self, product_id):
        """Remove product from cart"""
        self.__items = [item for item in self.__items 
                       if item.get_product().get_product_id() != product_id]
    
    def update_quantity(self, product_id, quantity):
        """Update quantity of a product in cart"""
        for item in self.__items:
            if item.get_product().get_product_id() == product_id:
                item.set_quantity(quantity)
                return True
        return False
    
    def get_items(self):
        return self.__items
    
    def get_total(self):
        """Calculate cart total"""
        return sum(item.get_subtotal() for item in self.__items)
    
    def clear(self):
        """Empty the cart"""
        self.__items.clear()
    
    def is_empty(self):
        return len(self.__items) == 0
    
    def __str__(self):
        if self.is_empty():
            return "Cart is empty"
        
        cart_str = "Shopping Cart:\n"
        cart_str += "-" * 50 + "\n"
        for item in self.__items:
            cart_str += str(item) + "\n"
        cart_str += "-" * 50 + "\n"
        cart_str += f"Total: Rs.{self.get_total():.2f}"
        return cart_str


class Bill:
    """
    Bill/Invoice class
    Demonstrates composition and association
    """
    
    _bill_counter = 1000  # Class variable for bill numbering
    
    def __init__(self, customer, cart):
        self.__bill_id = Bill._bill_counter
        Bill._bill_counter += 1
        
        self.__customer = customer  # Association - bill associated with customer
        self.__items = cart.get_items().copy()  # Copy of cart items
        self.__date_time = datetime.now()
        self.__subtotal = cart.get_total()
        self.__discount_amount = 0
        self.__tax_amount = 0
        self.__final_amount = 0
        
        self.__calculate_bill()
    
    def __calculate_bill(self):
        """Calculate final bill with discounts and tax"""
        # Apply membership discount if applicable
        discount_percentage = 0
        if self.__customer.get_membership():
            discount_percentage = self.__customer.get_membership().get_discount()
        
        self.__discount_amount = self.__subtotal * discount_percentage
        
        # Calculate tax (GST 5%)
        taxable_amount = self.__subtotal - self.__discount_amount
        self.__tax_amount = taxable_amount * 0.05
        
        # Calculate final amount
        self.__final_amount = taxable_amount + self.__tax_amount
    
    def get_bill_id(self):
        return self.__bill_id
    
    def get_customer(self):
        return self.__customer
    
    def get_items(self):
        return self.__items
    
    def get_date_time(self):
        return self.__date_time
    
    def get_subtotal(self):
        return self.__subtotal
    
    def get_discount_amount(self):
        return self.__discount_amount
    
    def get_tax_amount(self):
        return self.__tax_amount
    
    def get_final_amount(self):
        return self.__final_amount
    
    def apply_coupon(self, coupon):
        """Apply coupon for additional discount"""
        if coupon.is_valid(self.__subtotal):
            additional_discount = coupon.get_discount_amount(self.__subtotal)
            self.__discount_amount += additional_discount
            self.__final_amount -= additional_discount
            return True
        return False
    
    def print_bill(self):
        """Generate formatted bill"""
        bill_str = "\n" + "=" * 60 + "\n"
        bill_str += " " * 20 + "SUPERMART INVOICE" + " " * 23 + "\n"
        bill_str += "=" * 60 + "\n"
        bill_str += f"Bill No: {self.__bill_id:05d}" + " " * 20
        bill_str += f"Date: {self.__date_time.strftime('%d-%m-%Y %H:%M')}\n"
        bill_str += "-" * 60 + "\n"
        bill_str += f"Customer: {self.__customer.get_name()}\n"
        bill_str += f"Phone: {self.__customer.get_phone()}\n"
        
        if self.__customer.get_membership():
            bill_str += f"Membership: {self.__customer.get_membership().get_membership_type()}\n"
        
        bill_str += "=" * 60 + "\n"
        bill_str += f"{'Item':<25} {'Qty':>5} {'Price':>10} {'Total':>10}\n"
        bill_str += "-" * 60 + "\n"
        
        for item in self.__items:
            product = item.get_product()
            bill_str += f"{product.get_name():<25} "
            bill_str += f"{item.get_quantity():>5} "
            bill_str += f"{product.get_price():>10.2f} "
            bill_str += f"{item.get_subtotal():>10.2f}\n"
        
        bill_str += "=" * 60 + "\n"
        bill_str += f"{'Subtotal:':<50} Rs.{self.__subtotal:>10.2f}\n"
        
        if self.__discount_amount > 0:
            bill_str += f"{'Discount:':<50} Rs.{self.__discount_amount:>10.2f}\n"
        
        bill_str += f"{'Tax (GST 5%):':<50} Rs.{self.__tax_amount:>10.2f}\n"
        bill_str += "=" * 60 + "\n"
        bill_str += f"{'TOTAL AMOUNT:':<50} Rs.{self.__final_amount:>10.2f}\n"
        bill_str += "=" * 60 + "\n"
        bill_str += " " * 15 + "Thank you for shopping with us!\n"
        bill_str += "=" * 60 + "\n"
        
        return bill_str


class Coupon:
    """
    Coupon/Promo code class
    Demonstrates encapsulation
    """
    
    def __init__(self, code, discount_type, discount_value, min_purchase=0, expiry_date=None):
        self.__code = code
        self.__discount_type = discount_type  # 'PERCENTAGE' or 'FIXED'
        self.__discount_value = discount_value
        self.__min_purchase = min_purchase
        self.__expiry_date = expiry_date
    
    def get_code(self):
        return self.__code
    
    def is_valid(self, purchase_amount):
        """Check if coupon is valid"""
        if self.__expiry_date and datetime.now() > self.__expiry_date:
            return False
        if purchase_amount < self.__min_purchase:
            return False
        return True
    
    def get_discount_amount(self, purchase_amount):
        """Calculate discount amount"""
        if self.__discount_type == 'PERCENTAGE':
            return purchase_amount * (self.__discount_value / 100)
        else:  # FIXED
            return self.__discount_value
    
    def __str__(self):
        if self.__discount_type == 'PERCENTAGE':
            return f"{self.__code}: {self.__discount_value}% off (Min: Rs.{self.__min_purchase})"
        else:
            return f"{self.__code}: Rs.{self.__discount_value} off (Min: Rs.{self.__min_purchase})"