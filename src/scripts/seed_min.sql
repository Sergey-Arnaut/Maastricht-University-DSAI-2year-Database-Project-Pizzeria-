-- Минимальные данные для проверки VIEW

-- 1) Ингредиенты
INSERT INTO Ingredient (name, price_per_unit, vegan, vegetarian, allergen, allergen_type, amount, unit)
VALUES
  ('Моцарелла', 1.20, FALSE, TRUE,  TRUE,  'milk', '100', 'g'),
  ('Томат',     0.40, TRUE,  TRUE,  FALSE, NULL,   '100', 'g'),
  ('Базилик',   0.20, TRUE,  TRUE,  FALSE, NULL,   '10',  'g')
ON DUPLICATE KEY UPDATE price_per_unit = VALUES(price_per_unit);

-- 2) Пицца (важно: base_price > 0 из-за CHECK)
INSERT INTO Pizza (name, size, availability, base_price, is_vegetarian, is_vegan)
VALUES ('Маргарита', 'M', TRUE, 7.99, TRUE, FALSE)
ON DUPLICATE KEY UPDATE availability = VALUES(availability),
                        base_price   = VALUES(base_price),
                        is_vegetarian= VALUES(is_vegetarian),
                        is_vegan     = VALUES(is_vegan);

-- 3) Состав пиццы
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
VALUES
  ( (SELECT pizza_id     FROM Pizza      WHERE name='Маргарита' AND size='M' LIMIT 1),
    (SELECT ingredient_id FROM Ingredient WHERE name='Томат'     LIMIT 1), 1.0 ),
  ( (SELECT pizza_id     FROM Pizza      WHERE name='Маргарита' AND size='M' LIMIT 1),
    (SELECT ingredient_id FROM Ingredient WHERE name='Моцарелла' LIMIT 1), 2.0 ),
  ( (SELECT pizza_id     FROM Pizza      WHERE name='Маргарита' AND size='M' LIMIT 1),
    (SELECT ingredient_id FROM Ingredient WHERE name='Базилик'   LIMIT 1), 0.2 )
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

