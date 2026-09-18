import re
from decimal import Decimal

class Customer:

    def __init__(self, customer_id: int, name: str, email: str):
        self.customer_id = customer_id
        self.name = self.validate_name(name)
        self.email = self.validate_email(email)

    @staticmethod
    def validate_name(name: str) -> str:
        if name is None or not name.strip():
            raise ValueError("Customer name is required.")
        return name.strip()

    @staticmethod
    def validate_email(email: str) -> str:
        if email is None or not email.strip():
            raise ValueError("Customer email is required.")

        email = email.strip()
        if re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email) is None:
            raise ValueError("Enter a valid email address, such as name@example.com.")

        return email

class RegularCustomer(Customer):    
        customer_type = "Regular" 

        def discount_rate(self):
         return Decimal("0.02")

class PremiumCustomer(Customer):
    customer_type = "Premium"

    def discount_rate(self):
        return Decimal("0.05")


class CorporateCustomer(Customer):
    customer_type = "Corporate"

    def discount_rate(self):
        return Decimal("0.07")        
 
