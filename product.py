"""
Product Module - Base classes for all products in the supermarket
Demonstrates: Encapsulation, Abstraction, Inheritance
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Product(ABC):
    """
    Abstract base class for all products
    Demonstrates abstraction and encapsulation
    """
    
    def __init__(self, product_id, name, price, quantity):
        self.__product_id = product_id  # Private attribute (encapsulation)
        self.__name = name
        self.__price = price
        self.__quantity = quantity
    
    # Getter methods (encapsulation)
    def get_product_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__name
    
    def get_price(self):
        return self.__price
    
    def get_quantity(self):
        return self.__quantity
    
    # Setter methods (encapsulation with validation)
    def set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price
    
    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.__quantity = quantity
    
    def reduce_quantity(self, amount):
        """Reduce stock quantity"""
        if amount > self.__quantity:
            raise ValueError(f"Insufficient stock! Only {self.__quantity} available")
        self.__quantity -= amount
    
    @abstractmethod
    def calculate_discount(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_category(self):
        """Abstract method to get product category"""
        pass
    
    def get_total_price(self, quantity):
        """Calculate total price after discount"""
        discount = self.calculate_discount()
        return self.__price * quantity * (1 - discount)
    
    def __str__(self):
        return f"{self.__name} (ID: {self.__product_id}) - Rs.{self.__price:.2f}"


class GroceryProduct(Product):
    """
    Grocery products - perishable items
    Demonstrates inheritance and polymorphism
    """
    
    def __init__(self, product_id, name, price, quantity, expiry_date):
        super().__init__(product_id, name, price, quantity)
        self.__expiry_date = expiry_date
    
    def get_expiry_date(self):
        return self.__expiry_date
    
    def calculate_discount(self):
        """Polymorphism - override parent method"""
        # Check if near expiry (within 7 days)
        days_to_expiry = (self.__expiry_date - datetime.now()).days
        if days_to_expiry <= 3:
            return 0.30  # 30% discount
        elif days_to_expiry <= 7:
            return 0.15  # 15% discount
        return 0.05  # 5% regular discount
    
    def get_category(self):
        return "Grocery"
    
    def is_expired(self):
        """Check if product is expired"""
        return datetime.now() > self.__expiry_date


class ElectronicsProduct(Product):
    """
    Electronics products with warranty
    Demonstrates inheritance and polymorphism
    """
    
    def __init__(self, product_id, name, price, quantity, warranty_months):
        super().__init__(product_id, name, price, quantity)
        self.__warranty_months = warranty_months
    
    def get_warranty_months(self):
        return self.__warranty_months
    
    def calculate_discount(self):
        """Polymorphism - different discount logic"""
        # Electronics have higher discount on bulk purchase
        return 0.10  # 10% standard discount
    
    def get_category(self):
        return "Electronics"


class ClothingProduct(Product):
    """
    Clothing products with size and brand
    Demonstrates inheritance and polymorphism
    """
    
    def __init__(self, product_id, name, price, quantity, size, brand):
        super().__init__(product_id, name, price, quantity)
        self.__size = size
        self.__brand = brand
    
    def get_size(self):
        return self.__size
    
    def get_brand(self):
        return self.__brand
    
    def calculate_discount(self):
        """Polymorphism - seasonal discount"""
        return 0.20  # 20% discount on clothing
    
    def get_category(self):
        return "Clothing"


class HomeApplianceProduct(Product):
    """
    Home appliances with energy rating
    Demonstrates inheritance
    """
    
    def __init__(self, product_id, name, price, quantity, energy_rating):
        super().__init__(product_id, name, price, quantity)
        self.__energy_rating = energy_rating
    
    def get_energy_rating(self):
        return self.__energy_rating
    
    def calculate_discount(self):
        """Energy-efficient products get extra discount"""
        base_discount = 0.08
        if self.__energy_rating >= 4:
            return base_discount + 0.05  # Extra 5% for 4+ star rating
        return base_discount
    
    def get_category(self):
        return "Home Appliance"