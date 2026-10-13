from services import *

class MemberUsecase:
    def __init__(self, connector: MysqlConnector):
        self.db = connector
        
    def retrieve_member_by_email(self, email: str) -> Member:
        with self.db.get_connection() as connection:
            service = self._create_member_service(connection)
            return service.retrieve_by_email(email)
        
    def register_member(
        self,
        name: str,
        email: str,
        phone: str,
        address: str
    ) -> int:
        with self.db.get_connection() as connection:
            service = self._create_member_service(connection)
            return service.register(name, email, phone, address)
        
    def modify_member(
        self,
        member_id: int,
        name: str = None,
        email: str = None, 
        phone: str = None,
        address: str = None
    ) -> int:
        with self.db.get_connection() as connection:
            service = self._create_member_service(connection)
            return service.modify(member_id, name, email, phone, address)
        
    def buy_product(self, email: str, product_id: int, quantity: int):
        with self.db.get_connection() as connection:
            service = self._create_member_service(connection)
            return service.buy(email, product_id, quantity)
        
    def retrieve_purchase_list(self, email: str) -> tuple[SaleDetail, ...]:
        with self.db.get_connection() as connection:
            service = self._create_sale_service(connection)
            return service.retrieve_by_member_email(email)
        
    def retrieve_all_products(self) -> tuple[Product, ...]:
        with self.db.get_connection() as connection:
            service = self._create_product_service(connection)
            return service.retrieve_all()

    def _create_member_service(self, connection) -> MemberService:
        return MemberService(*self._create_supplies(connection))    
    
    def _create_product_service(self, connection) -> ProductService:
        return ProductService(*self._create_supplies(connection))
    
    def _create_sale_service(self, connection) -> SaleService:
        return SaleService(*self._create_supplies(connection))
    
    def _create_supplies(self, connection) -> tuple[MysqlTransaction, MemberRepository, ProductRepository, SaleRepository]:
        return MysqlTransaction(connection), MemberRepository(connection), ProductRepository(connection), SaleRepository(connection)

class AdminUsecase:
    def __init__(self, connector: MysqlConnector):
        self.db = connector
        
    def register_product(
        self,
        name: str,
        price: int,
        stock: int,
        description: str,
        category: str
    ) -> int:
        with self.db.get_connection() as connection:
            service = self._create_product_service(connection)
            return service.register(name, price, stock, description, category)
        
    def retrieve_all_purchases(self) -> tuple[SaleDetail, ...]:
        with self.db.get_connection() as connection:
            service = self._create_sale_service(connection)
            return service.retrieve_all()
        
    def retrieve_all_products(self) -> tuple[Product, ...]:
        with self.db.get_connection() as connection:
            service = self._create_product_service(connection)
            return service.retrieve_all()

    def modify_product(
        self,
        product_id: int,
        name: str = None,
        price: int = None,
        stock: int = None,
        description: str = None,
        category: str = None
    ) -> int:
        with self.db.get_connection() as connection:
            service = self._create_product_service(connection)
            return service.modify(product_id, name, price, stock, description, category)
        
    def remove_purchase(self, sale_id: int) -> int:
        with self.db.get_connection() as connection:
            service = self._create_sale_service(connection)
            return service.remove(sale_id)
            
    def _create_member_service(self, connection) -> MemberService:
            return MemberService(*self._create_supplies(connection))    
        
    def _create_product_service(self, connection) -> ProductService:
        return ProductService(*self._create_supplies(connection))
    
    def _create_sale_service(self, connection) -> SaleService:
        return SaleService(*self._create_supplies(connection))
    
    def _create_supplies(self, connection) -> tuple[MysqlTransaction, MemberRepository, ProductRepository, SaleRepository]:
        return MysqlTransaction(connection), MemberRepository(connection), ProductRepository(connection), SaleRepository(connection)