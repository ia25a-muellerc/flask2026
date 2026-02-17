-- Drop existing tables to recreate with correct structure
DROP TABLE IF EXISTS customer_payment CASCADE;
DROP TABLE IF EXISTS customer_payment_data CASCADE;
DROP TABLE IF EXISTS customer_addres CASCADE;



CREATE TABLE IF NOT EXISTS salutation (
    salutation_id SERIAL PRIMARY KEY,
    salutation VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_addres (
    addres_id SERIAL PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_payment_data (
    payment_data_id SERIAL PRIMARY KEY,
    card_number VARCHAR(20) NOT NULL,
    expiry_date DATE NOT NULL,
    cvv VARCHAR(4) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_payment_twint (
    telon_number VARCHAR(20) PRIMARY KEY,
    twint_id VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_payment (
    payment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    salutation_id INT REFERENCES salutation(salutation_id),
    addres_id INT REFERENCES customer_addres(addres_id),
    payment_data_id INT REFERENCES customer_payment_data(payment_data_id)
);


CREATE TABLE IF NOT EXISTS contact_message (
    message_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS newsletter_subscription (
    subscription_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profile_information (
    profile_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    salutation_id INT REFERENCES salutation(salutation_id),
    addres_id INT REFERENCES customer_addres(addres_id),
    payment_data_id INT REFERENCES customer_payment_data(payment_data_id)
);

CREATE TABLE IF NOT EXISTS order_information (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES profile_information(profile_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_item (
    item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES order_information(order_id),
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS product_review (
    review_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    customer_id INT REFERENCES profile_information(profile_id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    shipping_address VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    canceled BOOLEAN NOT NULL
);