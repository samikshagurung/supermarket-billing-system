"""
Main Supermarket Billing System
Demonstrates: All OOP concepts together
"""

import os
from datetime import datetime, timedelta
from product import GroceryProduct, ElectronicsProduct, ClothingProduct, HomeApplianceProduct
from customer import Customer, Membership
from billing import ShoppingCart, Bill, Coupon
from inventory import Inventory, InventoryReport
from payment import CashPayment, CardPayment, WalletPayment, PaymentProcessor


class SupermarketSystem:
    """
    Main supermarket billing system
    Demonstrates composition and orchestration of all components
    """
    
    def __init__(self):
        self.__inventory = Inventory()  # Singleton
        self.__customers = {}
        self.__bills = []
        self.__payment_processor = PaymentProcessor()
        self.__coupons = {}
        self.__current_customer = None
        self.__current_cart = None
        
        # Initialize system with sample data
        self.__initialize_system()
    
    def __initialize_system(self):
        """Initialize with sample products and coupons"""
        print("Initializing Supermarket System...")
        
        # Add Grocery Products
        self.__inventory.add_product(
            GroceryProduct("G001", "Rice (5kg)", 250.00, 50, 
                          datetime.now() + timedelta(days=30))
        )
        self.__inventory.add_product(
            GroceryProduct("G002", "Wheat Flour (10kg)", 400.00, 40,
                          datetime.now() + timedelta(days=25))
        )
        self.__inventory.add_product(
            GroceryProduct("G003", "Milk (1L)", 60.00, 100,
                          datetime.now() + timedelta(days=5))
        )
        self.__inventory.add_product(
            GroceryProduct("G004", "Bread", 40.00, 30,
                          datetime.now() + timedelta(days=3))
        )
        
        # Add Electronics Products
        self.__inventory.add_product(
            ElectronicsProduct("E001", "LED TV 32 inch", 15000.00, 10, 12)
        )
        self.__inventory.add_product(
            ElectronicsProduct("E002", "Smartphone", 12000.00, 15, 12)
        )
        self.__inventory.add_product(
            ElectronicsProduct("E003", "Bluetooth Speaker", 2500.00, 25, 6)
        )
        
        # Add Clothing Products
        self.__inventory.add_product(
            ClothingProduct("C001", "Men's T-Shirt", 499.00, 50, "L", "Nike")
        )
        self.__inventory.add_product(
            ClothingProduct("C002", "Women's Jeans", 1299.00, 30, "M", "Levi's")
        )
        self.__inventory.add_product(
            ClothingProduct("C003", "Kids Shirt", 399.00, 40, "S", "H&M")
        )
        
        # Add Home Appliances
        self.__inventory.add_product(
            HomeApplianceProduct("H001", "Refrigerator", 25000.00, 8, 5)
        )
        self.__inventory.add_product(
            HomeApplianceProduct("H002", "Washing Machine", 18000.00, 6, 4)
        )
        self.__inventory.add_product(
            HomeApplianceProduct("H003", "Microwave Oven", 7500.00, 12, 3)
        )
        
        # Add sample coupons
        self.__coupons["SAVE10"] = Coupon("SAVE10", "PERCENTAGE", 10, 1000)
        self.__coupons["FLAT200"] = Coupon("FLAT200", "FIXED", 200, 2000)
        self.__coupons["WELCOME50"] = Coupon("WELCOME50", "FIXED", 50, 500)
        
        # Add sample customers
        customer1 = Customer("C001", "Rajesh Kumar", "9876543210", "rajesh@email.com")
        customer1.set_membership(Membership("M001", "GOLD", 500))
        self.__customers["C001"] = customer1
        
        customer2 = Customer("C002", "Priya Sharma", "9876543211", "priya@email.com")
        customer2.set_membership(Membership("M002", "SILVER", 200))
        self.__customers["C002"] = customer2
        
        print("System initialized successfully!")
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print(" " * 15 + "SUPERMART BILLING SYSTEM")
        print("=" * 60)
        print("1.  Customer Registration")
        print("2.  Start Shopping (New Cart)")
        print("3.  View All Products")
        print("4.  Search Products")
        print("5.  View Cart")
        print("6.  Add to Cart")
        print("7.  Remove from Cart")
        print("8.  Generate Bill")
        print("9.  Process Payment")
        print("10. View Inventory Report")
        print("11. View Low Stock Alert")
        print("12. View Category Report")
        print("13. Customer Purchase History")
        print("14. Exit")
        print("=" * 60)
    
    def register_customer(self):
        """Register new customer"""
        print("\n--- Customer Registration ---")
        customer_id = input("Enter Customer ID: ")
        
        if customer_id in self.__customers:
            print("Customer already exists!")
            return
        
        name = input("Enter Name: ")
        phone = input("Enter Phone: ")
        email = input("Enter Email: ")
        
        customer = Customer(customer_id, name, phone, email)
        
        membership_choice = input("Would you like membership? (y/n): ").lower()
        if membership_choice == 'y':
            print("1. SILVER (5% discount)")
            print("2. GOLD (10% discount)")
            print("3. PLATINUM (15% discount)")
            mem_type = input("Choose membership type (1-3): ")
            
            membership_types = {'1': 'SILVER', '2': 'GOLD', '3': 'PLATINUM'}
            if mem_type in membership_types:
                membership = Membership(f"M{customer_id}", membership_types[mem_type])
                customer.set_membership(membership)
        
        self.__customers[customer_id] = customer
        print(f"\nCustomer registered successfully!")
        print(customer)
    
    def start_shopping(self):
        """Start new shopping session"""
        print("\n--- Start Shopping ---")
        customer_id = input("Enter Customer ID: ")
        
        if customer_id not in self.__customers:
            print("Customer not found! Please register first.")
            return
        
        self.__current_customer = self.__customers[customer_id]
        self.__current_cart = ShoppingCart()
        print(f"\nWelcome {self.__current_customer.get_name()}!")
        print("Cart created. You can now add products.")
    
    def view_all_products(self):
        """Display all available products"""
        products = self.__inventory.get_all_products()
        
        print("\n" + "=" * 80)
        print(" " * 30 + "PRODUCT CATALOG")
        print("=" * 80)
        print(f"{'ID':<8} {'Name':<30} {'Category':<15} {'Price':>10} {'Stock':>8}")
        print("-" * 80)
        
        for product in sorted(products, key=lambda p: p.get_product_id()):
            print(f"{product.get_product_id():<8} ", end="")
            print(f"{product.get_name():<30} ", end="")
            print(f"{product.get_category():<15} ", end="")
            print(f"Rs.{product.get_price():>9.2f} ", end="")
            print(f"{product.get_quantity():>8}")
        
        print("=" * 80)
    
    def search_products(self):
        """Search products by keyword"""
        keyword = input("Enter search keyword: ")
        results = self.__inventory.search_products(keyword)
        
        if not results:
            print("No products found!")
            return
        
        print(f"\nFound {len(results)} product(s):")
        print("-" * 60)
        for product in results:
            print(f"{product.get_product_id()}: {product.get_name()} - Rs.{product.get_price():.2f}")
    
    def view_cart(self):
        """View current shopping cart"""
        if self.__current_cart is None:
            print("No active cart! Please start shopping first.")
            return
        
        print(self.__current_cart)
    
    def add_to_cart(self):
        """Add product to cart"""
        if self.__current_cart is None:
            print("No active cart! Please start shopping first.")
            return
        
        product_id = input("Enter Product ID: ")
        product = self.__inventory.get_product(product_id)
        
        if product is None:
            print("Product not found!")
            return
        
        print(f"Selected: {product}")
        print(f"Available stock: {product.get_quantity()}")
        
        try:
            quantity = int(input("Enter quantity: "))
            
            if quantity > product.get_quantity():
                print(f"Insufficient stock! Only {product.get_quantity()} available.")
                return
            
            self.__current_cart.add_item(product, quantity)
            print(f"Added {quantity} x {product.get_name()} to cart!")
            
        except ValueError:
            print("Invalid quantity!")
    
    def remove_from_cart(self):
        """Remove product from cart"""
        if self.__current_cart is None or self.__current_cart.is_empty():
            print("Cart is empty!")
            return
        
        product_id = input("Enter Product ID to remove: ")
        self.__current_cart.remove_item(product_id)
        print("Product removed from cart!")
    
    def generate_bill(self):
        """Generate bill for current cart"""
        if self.__current_cart is None or self.__current_cart.is_empty():
            print("Cart is empty! Cannot generate bill.")
            return None
        
        # Create bill
        bill = Bill(self.__current_customer, self.__current_cart)
        
        # Ask for coupon
        apply_coupon = input("\nDo you have a coupon code? (y/n): ").lower()
        if apply_coupon == 'y':
            coupon_code = input("Enter coupon code: ").upper()
            if coupon_code in self.__coupons:
                coupon = self.__coupons[coupon_code]
                if bill.apply_coupon(coupon):
                    print(f"Coupon {coupon_code} applied successfully!")
                else:
                    print("Coupon not valid for this purchase.")
            else:
                print("Invalid coupon code!")
        
        # Print bill
        print(bill.print_bill())
        
        # Update inventory
        for item in self.__current_cart.get_items():
            product = item.get_product()
            product.reduce_quantity(item.get_quantity())
        
        # Store bill
        self.__bills.append(bill)
        self.__current_customer.add_to_history(bill)
        
        return bill
    
    def process_payment(self):
        """Process payment for the bill"""
        if not self.__bills:
            print("No bill to process!")
            return
        
        bill = self.__bills[-1]  # Get last bill
        amount = bill.get_final_amount()
        
        print(f"\nTotal Amount: Rs.{amount:.2f}")
        print("\nSelect Payment Method:")
        print("1. Cash")
        print("2. Card")
        print("3. Wallet")

        choice = input("Enter choice (1-3): ")

        try:
            payment = None
            
            if choice == '1':
                cash = float(input("Enter cash amount: "))
                payment = CashPayment(amount, cash)
            
            elif choice == '2':
                card_number = input("Enter card number: ")
                card_holder = input("Enter card holder name: ")
                cvv = input("Enter CVV: ")
                payment = CardPayment(amount, card_number, card_holder, cvv)
            
            elif choice == '3':
                upi_id = input("Enter UPI ID: ")
                payment = UPIPayment(amount, upi_id)
            
            elif choice == '4':
                wallet_type = input("Enter wallet type (PhonePe/Paytm/GooglePay): ")
                phone = input("Enter phone number: ")
                payment = WalletPayment(amount, wallet_type, phone)
            
            else:
                print("Invalid choice!")
                return
            
            # Process payment
            result = self.__payment_processor.process(payment)
            
            if result['status'] == 'SUCCESS':
                print("\n" + "=" * 50)
                print("PAYMENT SUCCESSFUL!")
                print("=" * 50)
                print(self.__payment_processor.generate_payment_receipt(payment))
                
                # Update membership points
                if self.__current_customer.get_membership():
                    self.__current_customer.get_membership().add_points(amount)
                    print(f"Loyalty points earned: {int(amount/100)}")
                
                # Clear cart after successful payment
                self.__current_cart = None
                self.__current_customer = None
                
            else:
                print(f"\nPAYMENT FAILED: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"Payment error: {str(e)}")
    
    def view_inventory_report(self):
        """View complete inventory report"""
        report = InventoryReport(self.__inventory)
        print(report.generate_stock_report())
    
    def view_low_stock_alert(self):
        """View low stock alert"""
        threshold = int(input("Enter stock threshold (default 10): ") or "10")
        report = InventoryReport(self.__inventory)
        print(report.generate_low_stock_alert(threshold))
    
    def view_category_report(self):
        """View category-wise report"""
        report = InventoryReport(self.__inventory)
        print(report.generate_category_report())
    
    def view_purchase_history(self):
        """View customer purchase history"""
        customer_id = input("Enter Customer ID: ")
        
        if customer_id not in self.__customers:
            print("Customer not found!")
            return
        
        customer = self.__customers[customer_id]
        history = customer.get_purchase_history()
        
        if not history:
            print("No purchase history found!")
            return
        
        print(f"\n--- Purchase History for {customer.get_name()} ---")
        print(f"Total Spent: Rs.{customer.get_total_spent():.2f}")
        print("\nBills:")
        
        for bill in history:
            print(f"Bill #{bill.get_bill_id()}: Rs.{bill.get_final_amount():.2f} on {bill.get_date_time().strftime('%d-%m-%Y')}")
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.register_customer()
            elif choice == '2':
                self.start_shopping()
            elif choice == '3':
                self.view_all_products()
            elif choice == '4':
                self.search_products()
            elif choice == '5':
                self.view_cart()
            elif choice == '6':
                self.add_to_cart()
            elif choice == '7':
                self.remove_from_cart()
            elif choice == '8':
                self.generate_bill()
            elif choice == '9':
                self.process_payment()
            elif choice == '10':
                self.view_inventory_report()
            elif choice == '11':
                self.view_low_stock_alert()
            elif choice == '12':
                self.view_category_report()
            elif choice == '13':
                self.view_purchase_history()
            elif choice == '14':
                print("\nThank you for using Supermart Billing System!")
                break
            else:
                print("Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")


def main():
    """Entry point of the application"""
    print("=" * 60)
    print(" " * 10 + "WELCOME TO SUPERMART BILLING SYSTEM")
    print("=" * 60)    
    system = SupermarketSystem()
    system.run()


if __name__ == "__main__":
    main()
