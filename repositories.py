import mysql.connector
from models import *

class MemberRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection
        
    def __del__(self):
        if self.connection:
            self.connection.close()

    def load(self, member_id: int) -> Member | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
                WHERE member_id = %s
            """
            params = (member_id,)
            
            cursor.execute(sql, params)
            if result := cursor.fetchone() is None:
                return None
            
            return Member(*result)
        
    def save(self, member: Member) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO members (name, email, phone, address, join_date)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = %s,
                    email = %s,
                    phone = %s,
                    address = %s
            """
            params = (
                member.name, member.email, member.phone, member.address, member.join_date,
                member.name, member.email, member.phone, member.address
            )
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def delete(self, member_id) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                DELETE FROM members
                WHERE member_id = %s
            """
            params = (member_id,)
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def commit(self):
        self.connection.commit()
        
    def rollback(self):
        self.connection.rollback()
        
    def load_all(self):
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
            """
            
            cursor.execute(sql)

            return tuple(
                Member(*row)
                for row in cursor.fetchall()
            )
            
    def load_by_email(self, email):
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
                WHERE email = %s
            """
            params = (email,)
            
            cursor.execute(sql, params)
            if result := cursor.fetchone() is None:
                return None
            
            return Member(*result)
        
class ProductRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection
        
    def __del__(self):
        if self.connection:
            self.connection.close()
            
    def load(self, product_id: int) -> Product | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products
                WHERE product_id = %s
            """
            params = (product_id,)
            
            cursor.execute(sql, params)
            if result := cursor.fetchone() is None:
                return None
            
            return Product(*result)
        
    def save(self, product: Product) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO products (name, price, stock, description, category)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = %s,
                    price = %s,
                    stock = %s,
                    description = %s,
                    category = %s
            """
            params = (
                product.name, product.price, product.stock, product.description, product.category,
                product.name, product.price, product.stock, product.description, product.category
            )
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def delete(self, product_id) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                DELETE FROM products
                WHERE product_id = %s
            """
            params = (product_id,)
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def commit(self):
        self.connection.commit()
        
    def rollback(self):
        self.connection.rollback()
        
    def load_all(self):
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products
            """
            
            cursor.execute(sql)
            
            return tuple(
                Product(row)
                for row in cursor.fetchall()
            )
            
        
class SaleRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection
        
    def __del__(self):
        if self.connection:
            self.connection.close()
            
    def load(self, sale_id: int) -> Sale | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM sales
                WHERE sale_id = %s
            """
            params = (sale_id,)
            
            cursor.execute(sql, params)
            if result := cursor.fetchone() is None:
                return None
            
            return Sale(*result)
        
    def save(self, sale: Sale) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO sales (member_id, product_id, quantity, sale_price, sale_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                sale.member_id, sale.product_id, sale.quantity, sale.sale_price, sale.sale_date
            )
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def delete(self, sale_id) -> int:
        with self.connection.cursor() as cursor:
            sql = """
                DELETE FROM sales
                WHERE sale_id = %s
            """
            params = (sale_id,)
            cursor.execute(sql, params)
            
            return cursor.rowcount
        
    def commit(self):
        self.connection.commit()
        
    def rollback(self):
        self.connection.rollback()
        
    def load_by_member_id(self, member_id) -> tuple:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM sales
                WHERE member_id = %s
            """
            params = (member_id,)
            
            cursor.execute(sql, params)
            return tuple(
                Sale(*row)
                for row in cursor.fetchall()
            )
            
    def load_all(self) -> tuple:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM sales
            """
            
            cursor.execute(sql)
            
            return tuple(
                Sale(*row)
                for row in cursor.fetchall()
            )
            