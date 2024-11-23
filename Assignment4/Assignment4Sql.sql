-- PostgreSQL: Create Table
CREATE TABLE Product (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    DeliveryPrice REAL,
    Description VARCHAR(8000)
);

-- Insert 5 records
INSERT INTO Product (Name, DeliveryPrice, Description)
VALUES
    ('Laptop', 800.50, 'A powerful laptop with 16GB RAM'),
    ('Phone', 500.00, 'A smartphone with AMOLED display'),
    ('Tablet', 300.00, 'A compact tablet with long battery life'),
    ('Headphones', 50.99, 'Wireless over-ear headphones'),
    ('Smartwatch', 150.25, 'A smartwatch with fitness tracking features');