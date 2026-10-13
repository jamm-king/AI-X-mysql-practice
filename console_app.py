from db import MysqlConnector
from usecases import *

class ConsoleApp():
    def __init__(
        self,
        member_usecase: MemberUsecase,
        admin_usecase: AdminUsecase,
    ):
        self.member_usecase = member_usecase
        self.admin_usecase = admin_usecase
        self.current_member_id = None
        
    def main_app(self):
        while True:
            match self.select_user():
                case -1: continue
                case 0: break
                case 1: self.member_app()
                case 2: self.admin_app()
                
    def member_app(self):
        # if not self.login():
        #     return
        
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
                case 1: self.register_product()
                case 2: self.retrieve_all_purchases()
                case 3: self.modify_product()
                case 4: self.remove_purchase()
                
    def login(self) -> bool:
        self.print_line()
        print("[로그인]")
        email = input("이메일: ")
        try:
            member = self.member_usecase.retrieve_member_by_email(email)
            if member is None:
                print("이메일이 일치하는 회원이 없습니다.")
                return False
        except EntityNotFoundError as e:
            print("이메일이 일치하는 회원이 없습니다.")
            return False
        except Exception as e:
            print("에러가 발생했습니다:", e)
            return False

        self.current_member_id = member.member_id
        return True
                    
    def register_member(self):
        self.print_line()
        print(f"[회원 등록]")
        name = input("이름: ")
        email = input("이메일: ")
        phone = input("연락처: ")
        address = input("주소: ")
        
        try:
            self.member_usecase.register_member(name, email, phone, address)
            print("등록이 완료됐습니다.")
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("회원 기능으로 돌아갑니다.")
            
    def modify_member(self):
        self.print_line()
        print("[회원 수정]")
        email = input("이메일: ")
        try:
            member = self.member_usecase.retrieve_member_by_email(email)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            return

        if member is None:
            print("이메일이 일치하는 회원이 없습니다:", email)
            print("회원 기능으로 돌아갑니다.")
            return       
        
        print("수정 값을 입력하세요.")
        name = input("이름: ")
        phone = input("연락처: ")
        address = input("주소: ")
        
        try:
            self.member_usecase.modify_member(member.member_id, name, email, phone, address)
            print("수정이 완료됐습니다.")
        except Exception as e:
            print("에러가 발생했습니다:", e)
            
        print("회원 기능으로 돌아갑니다.")
            
    def buy_product(self):
        self.print_line()
        print("[상품 구매]")
        try:
            products = self.member_usecase.retrieve_all_products()
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            return
        if len(products) == 0:
            print("등록된 상품이 없습니다.")
            print("회원 기능으로 돌아갑니다.")
            return
        print("|상품 목록|")
        self.show_data(products)
        
        try:  
            email = input("이메일을 입력해주세요: ")
            product_id = int(input("구매하실 상품 번호를 입력해주세요: "))
            quantity = int(input("구매하실 상품 수량을 입력해주세요: "))
        except ValueError as e:
            self.wrong_input()
            print("회원 기능으로 돌아갑니다.")
            return
            
        try:
            self.member_usecase.buy_product(email, product_id, quantity)
        except EntityNotFoundError as e:
            msg, = e.args
            if "member" in msg:
                print("이메일이 일치하는 회원이 없습니다:", email)
                print("회원 기능으로 돌아갑니다.")
                return
            elif "product" in msg:
                print("입력하신 상품 번호에 해당하는 상품이 없습니다.")
                print("회원 기능으로 돌아갑니다.")
                return
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            return
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            return
            
        print(f"상품 구매가 완료됐습니다")
        print("회원 기능으로 돌아갑니다.")
        
    def retrieve_purchase_list(self):
        self.print_line()
        print("[구매 목록 조회]")
        email = input("이메일을 입력해주세요: ")
            
        try:
            sales = self.member_usecase.retrieve_purchase_list(email)
        except EntityNotFoundError as e:
            print("이메일이 일치하는 회원이 없습니다.")
            print("회원 기능으로 돌아갑니다.")
            return
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("회원 기능으로 돌아갑니다.")
            return
        
        if len(sales) == 0:
            print("구매 내역이 없습니다.")
        else:
            self.show_data(sales)
        print("회원 기능으로 돌아갑니다.")
        
    def select_user(self) -> int:
        self.print_line()
        print("[사용자 선택]")
        print("1. 회원\n2. 관리자\n0. 종료")
        
        try:
            n = int(input("입력: "))
        except ValueError as e:
            self.wrong_input()
            return -1
        if not self.validate_input(n, 0, 2):
            self.wrong_input()
            return -1
        
        return n
    
    def register_product(self):
        self.print_line()
        print("[상품 등록]")
        try:
            name = input("이름: ")
            price = int(input("가격: "))
            stock = int(input("재고: "))
            description = input("설명: ")
            category = input("카테고리: ")
        except ValueError:
            self.wrong_input()
            print("관리자 기능으로 돌아갑니다.")
            return
        
        try:
            self.admin_usecase.register_product(name, price, stock, description, category)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            
    def retrieve_all_purchases(self):
        self.print_line()
        print("[전체 판매 목록 조회]")
        try:
            sales = self.admin_usecase.retrieve_all_purchases()
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            return
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
        try:
            products = self.admin_usecase.retrieve_all_products()
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            return
        if len(products) == 0:
            print("등록된 상품이 없습니다.")
            print("관리자 기능으로 돌아갑니다.")
            return
        
        print("|상품 목록|")
        for product in products:
            print(product)
        
        try:
            product_id = int(input("수정할 상품 번호를 입력하세요: "))
        except ValueError as e:
            self.wrong_input()
            print("관리자 기능으로 돌아갑니다.")
            return

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
        try:
            name = input("이름: ")
            price = int(input("가격: "))
            stock = int(input("재고: "))
            description = input("설명: ")
            category = input("카테고리: ")
        except ValueError:
            self.wrong_input()
            print("관리자 기능으로 돌아갑니다.")
            return
        
        try:
            self.admin_usecase.modify_product(product.product_id, name, price, stock, description, category)
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            return

        print("수정 완료했습니다.")
        print("관리자 기능으로 돌아갑니다.")
        
    def remove_purchase(self):
        self.print_line()
        print("[판매 내역 삭제]")
        try:
            sales = self.admin_usecase.retrieve_all_purchases()
        except Exception as e:
            print("에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            return
        if len(sales) == 0:
            print("판매 내역이 없습니다.")
            print("관리자 기능으로 돌아갑니다.")
            return
        
        print("|판매 내역|")
        self.show_data(sales)
        
        try:
            sale_id = int(input("삭제할 판매 번호를 입력하세요: "))
        except ValueError as e:
            self.wrong_input()
            print("관리자 기능으로 돌아갑니다.")
            return

        try:
            self.admin_usecase.remove_purchase(sale_id)
        except EntityNotFoundError as e:
            print("입력하신 판매 번호와 일치하는 판매 정보 없습니다:", sale_id)
            print("관리자 기능으로 돌아갑니다.")
            return
        except Exception as e:
            print("알 수 없는 에러가 발생했습니다:", e)
            print("관리자 기능으로 돌아갑니다.")
            return
            
        print("삭제 완료했습니다.")
        print("관리자 기능으로 돌아갑니다.")
    
    def select_member_function(self):
        self.print_line()
        print("[회원 기능]")
        print("1. 회원 등록\n2. 회원 수정\n3. 상품 구매\n4. 구매 목록 조회\n0. 나가기")
        
        try:
            n = int(input("입력: "))
        except ValueError as e:
            self.wrong_input()
            return -1
        if not self.validate_input(n, 0, 4):
            self.wrong_input()
            return -1
        
        return n
    
    def select_admin_function(self):
        self.print_line()
        print("[관리자 기능]")
        print("1. 상품 등록\n2. 전체 판매 목록 조회\n3. 상품 수정\n4. 판매 내역 삭제\n0. 나가기")

        try:
            n = int(input("입력: "))
        except ValueError as e:
            self.wrong_input()
            return -1
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
    connector = MysqlConnector()
    
    member_usecase = MemberUsecase(connector)
    admin_usecase = AdminUsecase(connector)
    
    app = ConsoleApp(member_usecase, admin_usecase)
    app.main_app()