-- insert_sample_data.sql

INSERT IGNORE INTO Pizza (name, size, availability, image_url, base_price) VALUES
('Margherita', 'M', TRUE, NULL, 12.99),
('Pepperoni', 'L', TRUE, NULL, 15.99),
('Hawaiian', 'M', TRUE, NULL, 14.99),
('Vegetarian', 'L', TRUE, NULL, 16.99),
('Supreme', 'XL', TRUE, NULL, 19.99),
('BBQ Chicken', 'M', TRUE, NULL, 15.99),
('Mushroom', 'S', TRUE, NULL, 10.99),
('Four Cheese', 'L', TRUE, NULL, 17.99),
('Vegan Special', 'M', TRUE, NULL, 16.99),
('Meat Lovers', 'XL', TRUE, NULL, 21.99);

INSERT IGNORE INTO Ingredient (name, price_per_unit, vegan, vegetarian, allergen, allergen_type, amount, unit) VALUES
('Tomato Sauce', 0.5, TRUE, TRUE, FALSE, NULL, '100', 'g'),
('Mozzarella Cheese', 1.2, FALSE, TRUE, FALSE, NULL, '100', 'g'),
('Pepperoni', 1.8, FALSE, FALSE, TRUE, 'Pork', '50', 'g'),
('Mushrooms', 1.0, TRUE, TRUE, FALSE, NULL, '70', 'g'),
('Ham', 2.0, FALSE, FALSE, TRUE, 'Pork', '60', 'g'),
('Pineapple', 1.0, TRUE, TRUE, FALSE, NULL, '80', 'g'),
('Olives', 1.2, TRUE, TRUE, FALSE, NULL, '40', 'g'),
('Onions', 0.7, TRUE, TRUE, FALSE, NULL, '50', 'g'),
('Bell Peppers', 1.0, TRUE, TRUE, FALSE, NULL, '60', 'g'),
('Chicken', 2.2, FALSE, FALSE, TRUE, 'Poultry', '70', 'g'),
('Basil', 0.3, TRUE, TRUE, FALSE, NULL, '10', 'g'),
('Garlic', 0.4, TRUE, TRUE, FALSE, NULL, '15', 'g');

INSERT IGNORE INTO Customer (first_name, last_name, phone_number, gender, email, postal_code, date_of_birth) VALUES
('John', 'Smith', '+1234567890', 'male', 'john.smith@email.com', '10001', '1985-03-15'),
('Emma', 'Johnson', '+1234567891', 'female', 'emma.johnson@email.com', '10002', '1990-07-22'),
('Michael', 'Brown', '+1234567892', 'male', 'michael.brown@email.com', '10003', '1988-11-30'),
('Sarah', 'Davis', '+1234567893', 'female', 'sarah.davis@email.com', '10004', '1992-05-14'),
('David', 'Wilson', '+1234567894', 'male', 'david.wilson@email.com', '10005', '1987-09-08'),
('Lisa', 'Miller', '+1234567895', 'female', 'lisa.miller@email.com', '10006', '1991-12-03'),
('James', 'Taylor', '+1234567896', 'male', 'james.taylor@email.com', '10007', '1986-08-19'),
('Jennifer', 'Anderson', '+1234567897', 'female', 'jennifer.anderson@email.com', '10008', '1993-02-25'),
('Robert', 'Thomas', '+1234567898', 'male', 'robert.thomas@email.com', '10009', '1989-06-12'),
('Maria', 'Jackson', '+1234567899', 'female', 'maria.jackson@email.com', '10010', '1994-10-07');

INSERT IGNORE INTO DeliveryPerson (first_name, last_name, number_of_orders, rating, availability, current_position, delivery_postal_code) VALUES
('Alex', 'Rodriguez', 15, 4.8, TRUE, NULL, '10001-10005'),
('Jessica', 'Martinez', 22, 4.9, TRUE, NULL, '10006-10010'),
('Daniel', 'Garcia', 18, 4.7, TRUE, NULL, '10001-10010');

INSERT IGNORE INTO Drink (name, price, milk_free, sugar_free, volume_ml, is_alcoholic, availability) VALUES
('Coca-Cola', 2.50, TRUE, FALSE, 330, FALSE, TRUE),
('Sprite', 2.50, TRUE, FALSE, 330, FALSE, TRUE),
('Water', 1.50, TRUE, TRUE, 500, FALSE, TRUE),
('Orange Juice', 3.00, TRUE, FALSE, 250, FALSE, TRUE),
('Beer', 4.50, TRUE, FALSE, 500, TRUE, TRUE),
('Iced Tea', 2.80, TRUE, FALSE, 330, FALSE, TRUE),
('Lemonade', 3.20, TRUE, FALSE, 400, FALSE, TRUE),
('Coffee', 2.00, FALSE, FALSE, 200, FALSE, TRUE),
('Red Bull', 3.50, TRUE, FALSE, 250, FALSE, TRUE),
('Mineral Water', 1.80, TRUE, TRUE, 500, FALSE, TRUE);

INSERT IGNORE INTO Dessert (name, price, sugar_free, gluten_free, milk_free, availability) VALUES
('Tiramisu', 4.50, FALSE, FALSE, FALSE, TRUE),
('Chocolate Cake', 3.80, FALSE, FALSE, FALSE, TRUE),
('Cheesecake', 4.20, FALSE, FALSE, FALSE, TRUE),
('Fruit Salad', 3.00, TRUE, TRUE, TRUE, TRUE),
('Ice Cream', 2.50, FALSE, TRUE, FALSE, TRUE),
('Apple Pie', 3.50, FALSE, FALSE, FALSE, TRUE),
('Brownie', 2.80, FALSE, FALSE, FALSE, TRUE),
('Panna Cotta', 4.00, FALSE, TRUE, FALSE, TRUE),
('Chocolate Mousse', 3.70, FALSE, TRUE, FALSE, TRUE),
('Fruit Tart', 3.90, FALSE, FALSE, FALSE, TRUE);

INSERT IGNORE INTO Menu (menu_name, is_active, valid_from, valid_until) VALUES
('Main Menu', TRUE, '2024-01-01', '2024-12-31'),
('Summer Specials', TRUE, '2024-06-01', '2024-08-31'),
('Vegetarian Menu', TRUE, '2024-01-01', '2024-12-31');

INSERT INTO MenuItems (menu_id, product_id, product_type, display_order) VALUES
-- Main Menu
(1, 1, 'pizza', 1), (1, 2, 'pizza', 2), (1, 3, 'pizza', 3),
(1, 1, 'drink', 1), (1, 2, 'drink', 2), (1, 3, 'drink', 3),
(1, 1, 'dessert', 1), (1, 2, 'dessert', 2),
-- Summer Specials
(2, 3, 'pizza', 1), (2, 6, 'pizza', 2),
(2, 4, 'drink', 1), (2, 6, 'drink', 2),
(2, 4, 'dessert', 1), (2, 9, 'dessert', 2),
-- Vegetarian Menu
(3, 1, 'pizza', 1), (3, 4, 'pizza', 2), (3, 7, 'pizza', 3),
(3, 3, 'drink', 1), (3, 10, 'drink', 2),
(3, 4, 'dessert', 1), (3, 10, 'dessert', 2);