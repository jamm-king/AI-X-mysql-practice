from datetime import datetime
from repositories import *

class MemberService:
    def __init__(
        self,
        member_repo: MemberRepository,
        product_repo: ProductRepository,
        sale_repo: SaleRepository
    ):
        self.member_repo = member_repo
        self.product_repo = product_repo
        self.sale_repo = sale_repo
        
    def register(
        self,
        name: str,
        email: str,
        phone: str,
        address: str
    ) -> int:
        join_date = datetime.now()
        
        new_member = Member(
            member_id = None,
            name = name,
            email = email,
            phone = phone,
            address = address,
            join_date = join_date
        )
        
        cnt = self.member_repo.save(new_member)
        
        self.member_repo.commit()
        
        return cnt
    
    def buy(self, member_id: int, product_id: int, quantity: int):
        if member := self.member_repo.load(member_id) is None:
            raise EntityNotFoundError.member_not_found(member_id)
        if product := self.product_repo.load(product_id) is None:
            raise EntityNotFoundError.product_not_found(product_id)
        if product.stock < quantity:
            raise ValueError(f"product stock is lower than quantity.")
        
        sale_price = product.price * quantity
        sale_date = datetime.now()
        new_sale = Sale(
            sale_id = None, 
            member_id = member.member_id,
            product_id = product.product_id,
            quantity = quantity,
            sale_price = sale_price,
            sale_date = sale_date
        )
        product.subtract_stock(quantity)
        
        try:
            self.product_repo.save(product)
            self.sale_repo.save(new_sale)       
        except mysql.connector.Error as e:
            self.product_repo.rollback()
            self.sale_repo.rollback()
            raise e
        
        self.product_repo.commit()
        self.sale_repo.commit()
        
    def purchase_list(self, member_id: int) -> tuple:
        if member := self.member_repo.load(member_id) is None:
            raise EntityNotFoundError.member_not_found(member_id)
        
        return self.sale_repo.load_by_member_id(member.member_id)
    
    def modify(
        self,
        member_id: int,
        name: str = None,
        email: str = None, 
        phone: str = None,
        address: str = None
    ) -> int:
        if member := self.member_repo.load(member_id) is None:
            raise EntityNotFoundError.member_not_found(member_id)
        
        member.modify(name, email, phone, address)
        
        cnt = self.member_repo.save(member)
        
        self.member_repo.commit()
        
        return cnt
    
    def retrieve_all(self) -> tuple:
        return self.member_repo.load_all()
    
    def retrieve_by_email(self, email) -> Member:
        return self.member_repo.load_by_email(email)
        
class ProductService:
    def __init__(
        self,
        member_repo: MemberRepository,
        product_repo: ProductRepository,
        sale_repo: SaleRepository
    ):
        self.member_repo = member_repo
        self.product_repo = product_repo
        self.sale_repo = sale_repo
        
    def register(
        self,
        name: str,
        price: int,
        stock: int,
        description: str,
        category: str
    ) -> int:
        new_product = Product(
            product_id = None,
            name = name,
            price = price,
            stock = stock,
            description = description,
            category = category
        )
        
        cnt = self.product_repo.save(new_product)
        
        self.product_repo.commit()
        
        return cnt
        
    def modify(
        self,
        product_id: int,
        name: str = None,
        price: int = None,
        stock: int = None,
        description: str = None,
        category: str = None
    ) -> int:
        if product := self.product_repo.load(product_id) is None:
            raise EntityNotFoundError.product_not_found(product_id)
        
        product.modify(name, price, stock, description, category)
        
        cnt = self.product_repo.save(product)
        
        self.product_repo.commit()
        
        return cnt
    
    def retrieve_all(self):
        return self.product_repo.load_all()
    
class SaleService:
    def __init__(
        self,
        member_repo: MemberRepository,
        product_repo: ProductRepository,
        sale_repo: SaleRepository
    ):
        self.member_repo = member_repo
        self.product_repo = product_repo
        self.sale_repo = sale_repo
        
    def retrieve_all(self) -> tuple:
        return self.sale_repo.load_all()
    
    def remove(self, sale_id: int) -> int:
        if self.sale_repo.load(sale_id) is None:
            raise EntityNotFoundError.sale_not_found(sale_id)
        
        cnt = self.sale_repo.delete(sale_id)
        
        self.sale_repo.commit()
        
        return cnt
        
class EntityNotFoundError(Exception):
    @classmethod
    def member_not_found(cls, member_id):
        return cls(f"member for id {member_id} is not found.")
    @classmethod
    def product_not_found(cls, product_id):
        return cls(f"product for id {product_id} is not found.")
    @classmethod
    def sale_not_found(cls, sale_id):
        return cls(f"sale for id {sale_id} is not found.")