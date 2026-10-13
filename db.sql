CREATE DATABASE IF NOT EXISTS practice;
USE practice;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS products;

CREATE TABLE IF NOT EXISTS members (
	member_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(200),
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_members	PRIMARY KEY(member_id),
    CONSTRAINT uq_email	UNIQUE(email)
);
CREATE TABLE IF NOT EXISTS products (
	product_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    description TEXT,
    category VARCHAR(50),
    CONSTRAINT pk_product_id	PRIMARY KEY(product_id),
    CONSTRAINT chk_price		CHECK(price >= 0),
    CONSTRAINT chk_stock		CHECK(stock >= 0)
);
CREATE TABLE IF NOT EXISTS sales (
	sale_id INT NOT NULL AUTO_INCREMENT,
    member_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    sale_date DATETIME NOT NULL,
    CONSTRAINT pk_sale_id		PRIMARY KEY(sale_id),
    CONSTRAINT fk_member_id		FOREIGN KEY(member_id) REFERENCES members(member_id),
    CONSTRAINT fk_product_id	FOREIGN KEY(product_id) REFERENCES products(product_id),
    CONSTRAINT chk_quantity		CHECK(quantity > 0),
    CONSTRAINT sale_price		CHECK(sale_price >= 0)
);

-- 회원 테스트 데이터
INSERT INTO members (name, email, phone, address, join_date)
VALUES
    ('김민수', 'minsu@example.com', '010-1234-5678', '서울시 강남구', '2026-01-05 10:00:00'),
    ('이지은', 'jieun@example.com', '010-2345-6789', '서울시 마포구', '2026-01-10 14:30:00'),
    ('박서준', 'seojun@example.com', '010-3456-7890', '부산시 해운대구', '2026-02-01 09:20:00'),
    ('최유진', 'yujin@example.com', NULL, NULL, '2026-02-15 16:00:00'),
    ('정하늘', 'haneul@example.com', '010-5678-9012', '대전시 유성구', '2026-03-01 11:10:00');

-- 상품 테스트 데이터
-- 재고 0, 가격 0, 선택 항목 NULL인 경우도 포함
INSERT INTO products (name, price, stock, description, category)
VALUES
    ('무선 마우스', 25000.00, 100, '저소음 무선 마우스', '전자기기'),
    ('기계식 키보드', 89000.00, 50, '적축 기계식 키보드', '전자기기'),
    ('USB-C 케이블', 9900.00, 200, '길이 1m 충전 케이블', '전자기기'),
    ('텀블러', 18000.00, 80, '500ml 스테인리스 텀블러', '생활용품'),
    ('노트', 3500.00, 150, 'A5 줄 노트', '문구'),
    ('볼펜 세트', 5000.00, 0, '검정 볼펜 5개 세트', '문구'),
    ('프로모션 스티커', 0.00, 300, '무료 증정용 스티커', '프로모션'),
    ('샘플 상품', 1000.00, 10, NULL, NULL);

-- 판매 테스트 데이터
-- member_id와 product_id는 위 INSERT로 생성된 ID 참조
-- sale_price는 판매 당시의 상품 1개 가격으로 가정
INSERT INTO sales (member_id, product_id, quantity, sale_price, sale_date)
VALUES
    (1, 1, 1, 25000.00, '2026-03-02 10:30:00'),
    (1, 3, 2, 9900.00,  '2026-03-02 10:30:00'),
    (2, 2, 1, 89000.00, '2026-03-03 14:20:00'),
    (2, 4, 1, 18000.00, '2026-03-04 11:00:00'),
    (3, 5, 3, 3500.00,  '2026-03-05 09:40:00'),
    (3, 1, 2, 23000.00, '2026-03-06 15:10:00'),
    (4, 4, 2, 16000.00, '2026-03-07 12:00:00'),
    (4, 7, 1, 0.00,     '2026-03-07 12:00:00'),
    (1, 2, 1, 85000.00, '2026-03-08 17:30:00'),
    (2, 5, 5, 3000.00,  '2026-03-09 13:15:00');

-- 판매 내역 확인
SELECT
    s.sale_id,
    m.name AS member_name,
    p.name AS product_name,
    s.quantity,
    s.sale_price,
    s.quantity * s.sale_price AS total_price,
    s.sale_date
FROM sales AS s
JOIN members AS m ON m.member_id = s.member_id
JOIN products AS p ON p.product_id = s.product_id
ORDER BY s.sale_date, s.sale_id;