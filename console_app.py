from db import MysqlConfig
from services import *

class ConsoleApp():
    def __init__(
        self,
        member_service: MemberService,
        product_service: ProductService,
        sale_service: SaleService
    ):
        self.member_service = member_service
        self.product_service = product_service
        self.sale_service = sale_service
        
    def main_app(self):
        while True:
            match self.select_user():
                case -1: continue
                case 0: break
                case 1: self.member_app()
                case 2: self.admin_app()
                
    def member_app(self):
        while True:
            match self.select_member_function():
                case -1: continue
                case 0: break
                case 1: self.register_member()
                case 2: self.modify_member()
                case 3: self.buy_product()
                case 4: self.retrieve_purchase_list()
                
    def admin_app(self):
        while True:
            match self.select_admin_function():
                case -1: continue
                case 0: break
                case 1: self.register_product
                case 2: self.retrieve_all_purchases
                case 3: self.remove_purchase
                    
    def register_member(self):
        self.print_line()
        print("[회원 등록]")
        name = input("이름: ")
        email = input("이메일: ")
        phone = input("연락처: ")
        address = input("주소: ")
        
        try:
            self.member_service.register(name, email, phone, address)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("회원 기능으로 돌아갑니다.")
            
    def modify_member(self):
        self.print_line()
        print("[회원 수정]")
        email = input("이메일: ")
        if member := self.member_service.retrieve_by_email(email) is None:
            print("이메일이 일치하는 회원이 없습니다:", email)
            print("회원 기능으로 돌아갑니다.")
            return       
        
        print("수정 값을 입력하세요.")
        name = input("이름: ")
        phone = input("연락처: ")
        address = input("주소: ")
        
        try:
            self.member_service.modify(name, email, phone, address)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("회원 기능으로 돌아갑니다.")
            
    def buy_product(self):
        self.print_line()
        print("상품 구매")
        email = input("이메일을 입력해주세요: ")
        
        if member := self.member_service.retrieve_by_email(email) is None:
            print("이메일이 일치하는 회원이 없습니다:", email)
            print("회원 기능으로 돌아갑니다.")
            return
        
        products = self.product_service.retrieve_all()
        if len(products) == 0:
            print("등록된 상품이 없습니다.")
            print("회원 기능으로 돌아갑니다.")
            return
        print("|상품 목록|")
        self.show_data(products)
        
        try:  
            product_id = int(input("구매하실 상품 번호를 입력해주세요: "))
        except Exception as e:
            self.wrong_input()
            print("회원 기능으로 돌아갑니다.")
            return
        
        try:
            product, = filter(
                lambda product: product.product_id == product_id,
                products
            )
        except ValueError as e:
            print("입력하신 상품 번호에 해당하는 상품이 없습니다.")
            print("회원 기능으로 돌아갑니다.")
            return
        
        try:
            quantity = int(input("구매하실 상품 수량을 입력해주세요: "))
        except ValueError as e:
            self.wrong_input()
            print("회원 기능으로 돌아갑니다.")
            return
            
        try:
            self.member_service.buy(member.member_id, product.product_id, quantity)
        except:
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            
        print(f"상품 구매가 완료됐습니다: {product.name} {quantity}개")
        print("회원 기능으로 돌아갑니다.")
        
    def retrieve_purchase_list(self):
        self.print_line()
        print("[구매 목록 조회]")
        sales = self.member_service.retrieve_all()
        
        if len(sales) == 0:
            print("구매 내역이 없습니다.")
        else:
            self.show_data(sales)
        print("회원 기능으로 돌아갑니다.")
        
    
        
    def select_user(self) -> int:
        self.print_line()
        print("[사용자 선택]")
        print("1. 회원\n2. 관리자\n0. 종료")
        
        n = int(input("입력: "))
        if not self.validate_input(n, 0, 2):
            self.wrong_input()
            return -1
        
        return n
    
    def register_product(self):
        self.print_line()
        print("[상품 등록]")
        name = input("이름: ")
        price = int(input("가격: "))
        stock = int(input("재고: "))
        description = input("주소: ")
        category = input("카테고리: ")
        
        try:
            self.product_service.register(name, price, stock, description, category)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            
    def retrieve_all_purchases(self):
        self.print_line()
        print("[전체 판매 목록 조회]")
        sales = self.product_service.retrieve_all()
        if len(sales) == 0:
            print("판매 내역이 없습니다.")
            print("관리자 기능으로 돌아갑니다.")
            return
        
        for sale in sales:
            print(sale)
        print("관리자 기능으로 돌아갑니다.")
        
    def modify_product(self):
        self.print_line()
        print("[상품 수정]")
        products = self.product_service.retrieve_all()
        if len(products) == 0:
            print("등록된 상품이 없습니다.")
            print("관리자 기능으로 돌아갑니다.")
            return
        
        print("|상품 목록|")
        for product in products:
            print(product)
        
        product_id = int(input("수정할 상품 번호를 입력하세요: "))
        try:
            product, = filter(
                lambda product: product.product_id == product_id,
                products
            )
        except ValueError as e:
            print("입력하신 상품 번호와 일치하는 상품이 없습니다:", product_id)
            print("관리자 기능으로 돌아갑니다.")
            return
        
        print("수정값을 입력하세요.")
        name = input("이름: ")
        price = int(input("가격: "))
        stock = int(input("재고: "))
        description = input("설명: ")
        category = input("카테고리: ")
        
        try:
            self.product_service.modify(product.product_id, name, price, stock, description, category)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("관리자 기능으로 돌아갑니다.")
        
    def remove_purchase(self):
        self.print_line()
        print("[판매 내역 삭제]")
        sales = self.sale_service.retrieve_all()
        if len(sales) == 0:
            print("판매 내역이 없습니다.")
            print("관리자 기능으로 돌아갑니다.")
            return
        
        print("|판매 내역|")
        for sale in sales:
            print(sale)
        
        sale_id = int(input("삭제할 판매 번호를 입력하세요: "))
        try:
            sale, = filter(
                lambda sale: sale.sale_id == sale_id,
                sales
            )
        except ValueError as e:
            print("입력하신 판매 번호와 일치하는 판매 정보 없습니다:", sale_id)
            print("관리자 기능으로 돌아갑니다.")
            return

        try:
            self.sale_service.remove(sale.sale_id)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("관리자 기능으로 돌아갑니다.")
    
    def select_member_function(self):
        self.print_line()
        print("[회원 기능]")
        print("1. 회원 등록\n2. 회원 수정\n3. 상품 구매\n4. 구매 목록 조회\n0. 나가기")
        
        n = int(input("입력: "))
        if not self.validate_input(n, 0, 4):
            self.wrong_input()
            return -1
        
        return n
    
    def select_admin_function(self):
        self.print_line()
        print("[관리자 기능]")
        print("1. 상품 등록\n2. 전체 판매 목록 조회\n3. 상품 수정\n4. 판매 내역 삭제\n0. 나가기")

        n = int(input("입력: "))
        if not self.validate_input(n, 0, 4):
            self.wrong_input()
            return -1
        
        return n
    
    def show_data(self, data):
        self.print_line()
        for d in data:
            print(d)
        
    def validate_input(self, n, min, max) -> bool:
        if not isinstance(n, int):
            return False
        if n < min:
            return False
        if n > max:
            return False
        
        return True
    
    def wrong_input(self):
        print("잘못된 입력입니다.")
        
    def print_line(self):
        print("--------------------------------------")
    
if __name__ == '__main__':
    member_repo = MemberRepository(MysqlConfig.get_connection())
    product_repo = ProductRepository(MysqlConfig.get_connection())
    sale_repo = SaleRepository(MysqlConfig.get_connection())
    
    member_service = MemberService(member_repo, product_repo, sale_repo)
    product_service = ProductService(member_repo, product_repo, sale_repo)
    sale_service = SaleService(member_repo, product_repo, sale_repo)
    
    app = ConsoleApp(member_service, product_service, sale_service)
    app.main_app()