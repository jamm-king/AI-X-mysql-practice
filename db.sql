DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sales;

CREATE TABLE IF NOT EXISTS members (
	member_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    adress VARCHAR(200),
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
)