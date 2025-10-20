-- seed_all_pizza_compositions.sql
-- Makes sure every pizza has ingredients so the computed price appears in PizzaPriceView.

USE our_little_secret;

-- 1) Ensure required ingredients exist (safe upsert)
INSERT INTO Ingredient (name, price_per_unit, vegan, vegetarian, allergen, allergen_type, amount, unit)
VALUES
('Tomato Sauce',        0.50,  TRUE,  TRUE,  FALSE, NULL, '100', 'g'),
('Mozzarella Cheese',   1.20,  FALSE, TRUE,  TRUE, 'milk', '100', 'g'),
('Pepperoni',           1.80,  FALSE, FALSE, TRUE, 'pork', '50',  'g'),
('Mushrooms',           1.00,  TRUE,  TRUE,  FALSE, NULL, '70',   'g'),
('Ham',                 2.00,  FALSE, FALSE, TRUE, 'pork', '60',  'g'),
('Pineapple',           1.00,  TRUE,  TRUE,  FALSE, NULL, '80',   'g'),
('Olives',              1.20,  TRUE,  TRUE,  FALSE, NULL, '40',   'g'),
('Onions',              0.70,  TRUE,  TRUE,  FALSE, NULL, '50',   'g'),
('Bell Peppers',        1.00,  TRUE,  TRUE,  FALSE, NULL, '60',   'g'),
('Chicken',             2.20,  FALSE, FALSE, TRUE, 'poultry', '70','g'),
('Basil',               0.30,  TRUE,  TRUE,  FALSE, NULL, '10',   'g'),
('Garlic',              0.40,  TRUE,  TRUE,  FALSE, NULL, '15',   'g')
ON DUPLICATE KEY UPDATE price_per_unit = VALUES(price_per_unit);

-- 2) Recreate the price view with the column names Django expects
DROP VIEW IF EXISTS PizzaPriceView;
CREATE VIEW PizzaPriceView AS
SELECT
  p.pizza_id,
  p.name                                   AS pizza_name,
  p.size                                   AS size,
  ROUND(SUM(pi.quantity * i.price_per_unit), 2)                 AS ingredients_cost,
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.40, 2)          AS price_before_vat,
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.40 * 1.09, 2)   AS final_price
FROM Pizza p
JOIN Pizza_Ingredients pi ON pi.pizza_id = p.pizza_id
JOIN Ingredient i         ON i.ingredient_id = pi.ingredient_id
WHERE p.availability = TRUE
GROUP BY p.pizza_id, p.name, p.size;

-- 3) Helper: upsert composition rows for a (name,size,ingredient,qty) set
--    Pattern used below: select pizza_id + ingredient_id by name, safe upsert quantities.

-- Margherita (M)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Margherita' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'Margherita','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Margherita','M','Basil',0.2) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Pepperoni (L)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Pepperoni','L','Tomato Sauce',1.0 UNION ALL
      SELECT 'Pepperoni','L','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Pepperoni','L','Pepperoni',1.0) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Hawaiian (M)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Hawaiian','M','Tomato Sauce',1.0 UNION ALL
      SELECT 'Hawaiian','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Hawaiian','M','Ham',1.0 UNION ALL
      SELECT 'Hawaiian','M','Pineapple',1.0) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Vegetarian (L)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Vegetarian','L','Tomato Sauce',1.0 UNION ALL
      SELECT 'Vegetarian','L','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Vegetarian','L','Mushrooms',1.0 UNION ALL
      SELECT 'Vegetarian','L','Bell Peppers',1.0 UNION ALL
      SELECT 'Vegetarian','L','Onions',0.7 UNION ALL
      SELECT 'Vegetarian','L','Olives',0.6) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Supreme (XL)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Supreme','XL','Tomato Sauce',1.0 UNION ALL
      SELECT 'Supreme','XL','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Supreme','XL','Pepperoni',0.8 UNION ALL
      SELECT 'Supreme','XL','Ham',0.8 UNION ALL
      SELECT 'Supreme','XL','Mushrooms',1.0 UNION ALL
      SELECT 'Supreme','XL','Bell Peppers',1.0 UNION ALL
      SELECT 'Supreme','XL','Onions',0.7 UNION ALL
      SELECT 'Supreme','XL','Olives',0.6) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- BBQ Chicken (M)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'BBQ Chicken','M','Tomato Sauce',1.0 UNION ALL
      SELECT 'BBQ Chicken','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'BBQ Chicken','M','Chicken',1.0 UNION ALL
      SELECT 'BBQ Chicken','M','Onions',0.7) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Mushroom (S)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Mushroom','S','Tomato Sauce',1.0 UNION ALL
      SELECT 'Mushroom','S','Mozzarella Cheese',1.5 UNION ALL
      SELECT 'Mushroom','S','Mushrooms',1.2 UNION ALL
      SELECT 'Mushroom','S','Garlic',0.2) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Four Cheese (L)  (simple stand-in: mozzarella + garlic)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Four Cheese','L','Tomato Sauce',0.5 UNION ALL
      SELECT 'Four Cheese','L','Mozzarella Cheese',2.5 UNION ALL
      SELECT 'Four Cheese','L','Garlic',0.2) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Vegan Special (M) (no dairy, veg only)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Vegan Special','M','Tomato Sauce',1.0 UNION ALL
      SELECT 'Vegan Special','M','Mushrooms',1.0 UNION ALL
      SELECT 'Vegan Special','M','Bell Peppers',1.0 UNION ALL
      SELECT 'Vegan Special','M','Onions',0.7 UNION ALL
      SELECT 'Vegan Special','M','Olives',0.6 UNION ALL
      SELECT 'Vegan Special','M','Basil',0.2) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Meat Lovers (XL)
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Meat Lovers','XL','Tomato Sauce',1.0 UNION ALL
      SELECT 'Meat Lovers','XL','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Meat Lovers','XL','Pepperoni',1.0 UNION ALL
      SELECT 'Meat Lovers','XL','Ham',1.0 UNION ALL
      SELECT 'Meat Lovers','XL','Chicken',1.0) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

-- Also give a composition to the Russian Маргарита (M) if present
INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'Маргарита' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'Маргарита','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'Маргарита','M','Basil',0.2) v
JOIN Pizza p ON p.name=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);
