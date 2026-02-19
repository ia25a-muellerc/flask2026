DROP TABLE IF EXISTS order_item CASCADE;
DROP TABLE IF EXISTS product_review CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS customer_payment CASCADE;
DROP TABLE IF EXISTS payment_method CASCADE;
DROP TABLE IF EXISTS profile_information CASCADE;
DROP TABLE IF EXISTS newsletter_subscription CASCADE;
DROP TABLE IF EXISTS contact_message CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS customer_address CASCADE;
DROP TABLE IF EXISTS salutation CASCADE;
DROP TABLE IF EXISTS orders CASCADE;

CREATE TABLE customer_address (
    address_id SERIAL PRIMARY KEY,
    street VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS salutation (
    salutation_id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL
);

CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salutation_id INT REFERENCES salutation(salutation_id),
    address_id INT REFERENCES customer_address(address_id)
);

CREATE TABLE payment_method (
    payment_method_id SERIAL PRIMARY KEY,
    method VARCHAR(50) NOT NULL
);

CREATE TABLE customer_payment (
    customer_payment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address_id INT REFERENCES customer_address(address_id),
    payment_method_id INT REFERENCES payment_method(payment_method_id)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    shipping_address VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    customer_id INT REFERENCES customer(customer_id),
    customer_payment_id INT REFERENCES customer_payment(customer_payment_id),
    canceled BOOLEAN NOT NULL
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2)
);



CREATE TABLE contact_message (
    message_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    message TEXT,
    customer_id INT REFERENCES customer(customer_id)
);

CREATE TABLE product_review (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(product_id),
    customer_id INT REFERENCES customer(customer_id),
    rating INT,
    review_text TEXT
);


