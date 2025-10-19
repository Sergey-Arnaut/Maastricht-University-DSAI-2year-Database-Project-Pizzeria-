-- Один активный код на 15%
INSERT INTO DiscountCode (discount_code, password, discount_value, discount_type, valid_from, valid_until, is_active)
VALUES ('HELLO15', NULL, 15, 'percent', CURDATE() - INTERVAL 1 DAY, CURDATE() + INTERVAL 30 DAY, TRUE)
ON DUPLICATE KEY UPDATE is_active=VALUES(is_active), valid_until=VALUES(valid_until);

-- Курьеры на индексы 62150 и 62110
INSERT INTO DeliveryPerson (first_name, last_name, number_of_orders, rating, availability, current_position, delivery_postal_code)
VALUES
('Mike','Rider', 0, 4.80, TRUE, 'N50.85,E5.69', '62150'),
('Jane','Swift', 1, 4.95, TRUE, 'N50.85,E5.70', '62150'),
('Bob','Calm',  0, 4.50, TRUE, 'N50.85,E5.65', '62110')
ON DUPLICATE KEY UPDATE availability=VALUES(availability);
