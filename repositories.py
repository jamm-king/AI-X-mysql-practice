import mysql.connector
from models import *

class MemberRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection

    def load(self, member_id: int) -> Member | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
                WHERE member_id = %s
            """
            params = (member_id,)
            
            cursor.execute(sql, params)
            if (result := cursor.fetchone()) is None:
                return None
            
            return Member(*result)
        
    def save(self, member: Member) -> int:
        with self.connection.cursor() as cursor:
            if member.member_id is None:
                sql = """
                    INSERT INTO members (name, email, phone, address, join_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (member.name, member.email, member.phone, member.address, member.join_date)
            else:
                sql = """
                    UPDATE members
                    SET
                        name = %s,
                        phone = %s,
                        address = %s
                    WHERE member_id = %s
                """
                params = (member.name, member.phone, member.address, member.member_id)
                
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
        
    def load_all(self) -> tuple[Member, ...]:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
            """
            
            cursor.execute(sql)

            return tuple(
                Member(*row)
                for row in cursor.fetchall()
            )
            
    def load_by_email(self, email) -> Member | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM members
                WHERE email = %s
            """
            params = (email,)
            
            cursor.execute(sql, params)
            if (result := cursor.fetchone()) is None:
                return None
            
            return Member(*result)
        
class ProductRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection
            
    def load(self, product_id: int) -> Product | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products
                WHERE product_id = %s
            """
            params = (product_id,)
            
            cursor.execute(sql, params)
            if (result := cursor.fetchone()) is None:
                return None
            
            return Product(*result)
        
    def save(self, product: Product) -> int:
        with self.connection.cursor() as cursor:
            if product.product_id is None:
                sql = """
                    INSERT INTO products (name, price, stock, description, category)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (
                    product.name, product.price, product.stock,
                    product.description, product.category
                )
            else:
                sql = """
                    UPDATE products
                    SET
                        name = %s,
                        price = %s,
                        stock = %s,
                        description = %s,
                        category = %s
                    WHERE product_id = %s
                """
                params = (
                    product.name, product.price, product.stock, 
                    product.description, product.category, product.product_id
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
        
    def load_all(self) -> tuple[Product, ...]:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM products
            """
            
            cursor.execute(sql)
            
            return tuple(
                Product(*row)
                for row in cursor.fetchall()
            )
            
        
class SaleRepository:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self.connection = connection
            
    def load(self, sale_id: int) -> Sale | None:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM sales
                WHERE sale_id = %s
            """
            params = (sale_id,)
            
            cursor.execute(sql, params)
            if (result := cursor.fetchone()) is None:
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
        
    def load_by_member_id(self, member_id: int) -> tuple[SaleDetail, ...]:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT
                    s.sale_id, m.name AS member_name, p.name AS product_name,
                    s.quantity, s.sale_price, s.sale_date
                FROM sales AS s
                JOIN members AS m ON m.member_id = s.member_id
                JOIN products AS p ON p.product_id = s.product_id
                WHERE s.member_id = %s
                ORDER BY s.sale_date DESC, s.sale_id DESC
            """
            params = (member_id,)
            
            cursor.execute(sql, params)
            return tuple(
                SaleDetail(*row)
                for row in cursor.fetchall()
            )
            
    def load_all(self) -> tuple[SaleDetail, ...]:
        with self.connection.cursor() as cursor:
            sql = """
                SELECT
                    s.sale_id, m.name AS member_name, p.name AS product_name,
                    s.quantity, s.sale_price, s.sale_date
                FROM sales AS s
                JOIN members AS m ON m.member_id = s.member_id
                JOIN products AS p ON p.product_id = s.product_id
                ORDER BY s.sale_date DESC, s.sale_id DESC
            """
            
            cursor.execute(sql)
            
            return tuple(
                SaleDetail(*row)
                for row in cursor.fetchall()
            )
            
