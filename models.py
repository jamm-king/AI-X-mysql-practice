from dataclasses import dataclass

@dataclass
class Member:
    member_id: int
    name: str
    email: str
    phone: str
    address: str
    join_date: str
    
    def __str__(self):
        return f"{self.member_id:<5} {self.name:<5} {self.email if self.email else "N/A":<20} {self.phone if self.phone else "N/A":<15} {self.address if self.address else "N/A"}"
    
    def modify(
        self,
        name: str = None,
        email: str = None,
        phone: str = None,
        address: str = None
     ):
        if name is None: name = self.name
        if email is None: email = self.email
        if phone is None: phone = self.phone
        if address is None: address = self.address
        
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
    
@dataclass
class Product:
    product_id: int
    name: str
    price: int
    stock: int
    description: str
    category: str
    
    def __str__(self):
        return f"{self.product_id:<5} {self.name:<10} {self.price:<7} {self.stock:<5} {self.category if self.category else "N/A"}"
    
    def subtract_stock(self, quantity):
        self.stock -= quantity
        
    def modify(
        self,
        name: str = None,
        price: int = None,
        stock: int = None,
        description: str = None,
        category: str = None
    ):
        if name is None: name = self.name
        if price is None: price = self.price
        if stock is None: stock = self.stock
        if description is None: description = self.description
        if category is None: category = self.category
        
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
        self.category = category
    
@dataclass
class Sale:
    sale_id: int
    member_id: int
    product_id: int
    quantity: int
    sale_price: int
    sale_date: int
    
    def __str__(self):
        return f"{self.sale_id:<5} {self.member_id:<5} {self.product_id:<5} {self.quantity:<5} {self.sale_price:<10} {self.sale_date}"