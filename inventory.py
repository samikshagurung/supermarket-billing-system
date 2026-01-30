"""
Inventory Management Module
Demonstrates: Encapsulation, Singleton Pattern
"""


class Inventory:
    """
    Inventory management system
    Implements Singleton pattern - only one inventory instance
    """
    
    __instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        """Initialize inventory only once"""
        if self.__initialized:
            return
        
        self.__products = {}  # Dictionary to store products {product_id: product}
        self.__initialized = True
    
    def add_product(self, product):
        """Add new product to inventory"""
        product_id = product.get_product_id()
        if product_id in self.__products:
            raise ValueError(f"Product with ID {product_id} already exists")
        self.__products[product_id] = product
    
    def remove_product(self, product_id):
        """Remove product from inventory"""
        if product_id not in self.__products:
            raise ValueError(f"Product with ID {product_id} not found")
        del self.__products[product_id]
    
    def get_product(self, product_id):
        """Get product by ID"""
        if product_id not in self.__products:
            return None
        return self.__products[product_id]
    
    def search_products(self, keyword):
        """Search products by name"""
        keyword = keyword.lower()
        results = []
        for product in self.__products.values():
            if keyword in product.get_name().lower():
                results.append(product)
        return results
    
    def get_all_products(self):
        """Get all products"""
        return list(self.__products.values())
    
    def get_products_by_category(self, category):
        """Get all products in a category"""
        return [p for p in self.__products.values() if p.get_category() == category]
    
    def update_stock(self, product_id, quantity):
        """Update product stock quantity"""
        product = self.get_product(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")
        product.set_quantity(quantity)
    
    def check_low_stock(self, threshold=10):
        """Get products with low stock"""
        return [p for p in self.__products.values() if p.get_quantity() < threshold]
    
    def get_inventory_value(self):
        """Calculate total inventory value"""
        return sum(p.get_price() * p.get_quantity() for p in self.__products.values())
    
    def __str__(self):
        return f"Inventory contains {len(self.__products)} products"


class InventoryReport:
    """
    Generate inventory reports
    Demonstrates composition with Inventory
    """
    
    def __init__(self, inventory):
        self.__inventory = inventory
    
    def generate_stock_report(self):
        """Generate complete stock report"""
        report = "\n" + "=" * 80 + "\n"
        report += " " * 30 + "INVENTORY REPORT\n"
        report += "=" * 80 + "\n"
        
        products = self.__inventory.get_all_products()
        
        if not products:
            return report + "No products in inventory\n"
        
        report += f"{'ID':<8} {'Name':<30} {'Category':<15} {'Price':>10} {'Stock':>8}\n"
        report += "-" * 80 + "\n"
        
        for product in sorted(products, key=lambda p: p.get_product_id()):
            report += f"{product.get_product_id():<8} "
            report += f"{product.get_name():<30} "
            report += f"{product.get_category():<15} "
            report += f"{product.get_price():>10.2f} "
            report += f"{product.get_quantity():>8}\n"
        
        report += "=" * 80 + "\n"
        report += f"Total Products: {len(products)}\n"
        report += f"Total Inventory Value: Rs.{self.__inventory.get_inventory_value():.2f}\n"
        report += "=" * 80 + "\n"
        
        return report
    
    def generate_low_stock_alert(self, threshold=10):
        """Generate low stock alert"""
        low_stock = self.__inventory.check_low_stock(threshold)
        
        report = "\n" + "=" * 60 + "\n"
        report += " " * 20 + "LOW STOCK ALERT\n"
        report += "=" * 60 + "\n"
        
        if not low_stock:
            return report + "All products are well stocked\n"
        
        report += f"Products with stock below {threshold}:\n"
        report += "-" * 60 + "\n"
        
        for product in low_stock:
            report += f"{product.get_name():<40} Stock: {product.get_quantity():>3}\n"
        
        report += "=" * 60 + "\n"
        
        return report
    
    def generate_category_report(self):
        """Generate report by category"""
        report = "\n" + "=" * 60 + "\n"
        report += " " * 15 + "CATEGORY-WISE REPORT\n"
        report += "=" * 60 + "\n"
        
        products = self.__inventory.get_all_products()
        
        if not products:
            return report + "No products in inventory\n"
        
        # Group by category
        categories = {}
        for product in products:
            category = product.get_category()
            if category not in categories:
                categories[category] = []
            categories[category].append(product)
        
        for category, items in sorted(categories.items()):
            report += f"\n{category}:\n"
            report += "-" * 60 + "\n"
            total_value = sum(p.get_price() * p.get_quantity() for p in items)
            total_items = sum(p.get_quantity() for p in items)
            
            for product in items:
                report += f"  {product.get_name():<35} "
                report += f"Rs.{product.get_price():>8.2f} x {product.get_quantity():>3}\n"
            
            report += f"  Total Items: {total_items}, Total Value: Rs.{total_value:.2f}\n"
        
        report += "=" * 60 + "\n"
        
        return report