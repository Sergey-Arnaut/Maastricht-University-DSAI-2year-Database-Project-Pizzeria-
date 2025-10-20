INSERT IGNORE INTO `Order` (customer_id, status, total_price, delivery_postal_code, delivery_person_id, order_timestamp) VALUES
(1, 'delivered', 25.99, '10001', 1, '2024-01-24 12:35:00'),
(2, 'delivered', 18.50, '10002', 2, '2024-01-24 13:50:00'),
(3, 'preparing', 32.75, '10003', 1, '2024-01-24 14:25:00'),
(1, 'out_for_delivery', 21.99, '10001', 3, '2024-01-24 15:15:00'),
(4, 'delivered', 28.30, '10004', 2, '2024-01-24 16:35:00'),
(1, 'delivered', 41.97, '10001', 1, '2024-01-24 18:00:00'),
(2, 'delivered', 63.96, '10002', 2, '2024-01-24 19:30:00'),
(3, 'delivered', 29.98, '10003', 3, '2024-01-25 17:45:00'),
(4, 'delivered', 67.95, '10004', 1, '2024-01-25 20:15:00'),
(5, 'delivered', 51.96, '10005', 2, '2024-01-26 19:00:00');

INSERT INTO OrderItem (order_id, pizza_id, pizza_quantity, item_current_price) VALUES
(22, 21, 2, 12.99),  -- 2x Margherita
(22, 23, 1, 14.99),  -- 1x Hawaiian
(23, 22, 1, 15.99),  -- 1x Pepperoni
(23, 21, 1, 12.99),  -- 1x Margherita
(24, 24, 1, 16.99),  -- 1x Vegetarian
(24, 25, 1, 19.99),  -- 1x Supreme
(25, 21, 1, 12.99),  -- 1x Margherita
(25, 26, 1, 15.99),  -- 1x BBQ Chicken
(26, 27, 2, 10.99),  -- 2x Mushroom
(26, 28, 1, 17.99),  -- 1x Four Cheese
(27, 21, 3, 12.99),  -- 3x Margherita
(28, 22, 4, 15.99),  -- 4x Pepperoni
(29, 23, 2, 14.99),  -- 2x Hawaiian
(30, 25, 3, 19.99),  -- 3x Supreme
(30, 21, 1, 12.99),  -- 1x Margherita
(31, 22, 2, 15.99),  -- 2x Pepperoni
(31, 24, 2, 16.99);  -- 2x Vegetarian

INSERT INTO Payment (order_id, amount, payment_method, status, payment_timestamp) VALUES
(22, 25.99, 'card', 'completed', '2024-01-24 12:30:00'),
(23, 18.50, 'cash', 'completed', '2024-01-24 13:45:00'),
(24, 32.75, 'online', 'pending', '2024-01-24 14:20:00'),
(25, 21.99, 'card', 'completed', '2024-01-24 15:10:00'),
(26, 28.30, 'cash', 'completed', '2024-01-24 16:30:00'),
(27, 41.97, 'card', 'completed', '2024-01-24 17:55:00'),
(28, 63.96, 'cash', 'completed', '2024-01-24 19:25:00'),
(29, 29.98, 'online', 'completed', '2024-01-25 17:40:00'),
(30, 67.95, 'card', 'completed', '2024-01-25 20:10:00'),
(31, 51.96, 'cash', 'completed', '2024-01-26 18:55:00');