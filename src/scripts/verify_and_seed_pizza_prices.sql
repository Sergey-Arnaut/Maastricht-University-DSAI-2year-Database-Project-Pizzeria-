

USE our_little_secret;



INSERT INTO Ingredient (name, price_per_unit, vegan, vegetarian, allergen, allergen_type, amount, unit)
VALUES
('Tomato Sauce',        0.50,  TRUE,  TRUE,  FALSE, NULL, '100', 'g'),
('Mozzarella Cheese',   1.20,  FALSE, TRUE,  TRUE,  'milk', '100', 'g'),
('Pepperoni',           1.80,  FALSE, FALSE, TRUE,  'pork', '50',  'g'),
('Mushrooms',           1.00,  TRUE,  TRUE,  FALSE, NULL, '70',   'g'),
('Ham',                 2.00,  FALSE, FALSE, TRUE,  'pork', '60',  'g'),
('Pineapple',           1.00,  TRUE,  TRUE,  FALSE, NULL, '80',   'g'),
('Olives',              1.20,  TRUE,  TRUE,  FALSE, NULL, '40',   'g'),
('Onions',              0.70,  TRUE,  TRUE,  FALSE, NULL, '50',   'g'),
('Bell Peppers',        1.00,  TRUE,  TRUE,  FALSE, NULL, '60',   'g'),
('Chicken',             2.20,  FALSE, FALSE, TRUE,  'poultry', '70','g'),
('Basil',               0.30,  TRUE,  TRUE,  FALSE, NULL, '10',   'g'),
('Garlic',              0.40,  TRUE,  TRUE,  FALSE, NULL, '15',   'g')
ON DUPLICATE KEY UPDATE price_per_unit = VALUES(price_per_unit);

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


INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'margherita' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'margherita','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'margherita','M','Basil',0.2) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'pepperoni' n,'L' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'pepperoni','L','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'pepperoni','L','Pepperoni',1.0) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'hawaiian' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'hawaiian','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'hawaiian','M','Ham',1.0 UNION ALL
      SELECT 'hawaiian','M','Pineapple',1.0) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'vegetarian' n,'L' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'vegetarian','L','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'vegetarian','L','Mushrooms',1.0 UNION ALL
      SELECT 'vegetarian','L','Bell Peppers',1.0 UNION ALL
      SELECT 'vegetarian','L','Onions',0.7 UNION ALL
      SELECT 'vegetarian','L','Olives',0.6) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'supreme' n,'XL' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'supreme','XL','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'supreme','XL','Pepperoni',0.8 UNION ALL
      SELECT 'supreme','XL','Ham',0.8 UNION ALL
      SELECT 'supreme','XL','Mushrooms',1.0 UNION ALL
      SELECT 'supreme','XL','Bell Peppers',1.0 UNION ALL
      SELECT 'supreme','XL','Onions',0.7 UNION ALL
      SELECT 'supreme','XL','Olives',0.6) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'bbq chicken' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'bbq chicken','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'bbq chicken','M','Chicken',1.0 UNION ALL
      SELECT 'bbq chicken','M','Onions',0.7) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'mushroom' n,'S' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'mushroom','S','Mozzarella Cheese',1.5 UNION ALL
      SELECT 'mushroom','S','Mushrooms',1.2 UNION ALL
      SELECT 'mushroom','S','Garlic',0.2) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'four cheese' n,'L' s,'Tomato Sauce' ing,0.5 q UNION ALL
      SELECT 'four cheese','L','Mozzarella Cheese',2.5 UNION ALL
      SELECT 'four cheese','L','Garlic',0.2) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'vegan special' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'vegan special','M','Mushrooms',1.0 UNION ALL
      SELECT 'vegan special','M','Bell Peppers',1.0 UNION ALL
      SELECT 'vegan special','M','Onions',0.7 UNION ALL
      SELECT 'vegan special','M','Olives',0.6 UNION ALL
      SELECT 'vegan special','M','Basil',0.2) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'meat lovers' n,'XL' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'meat lovers','XL','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'meat lovers','XL','Pepperoni',1.0 UNION ALL
      SELECT 'meat lovers','XL','Ham',1.0 UNION ALL
      SELECT 'meat lovers','XL','Chicken',1.0) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);

INSERT INTO Pizza_Ingredients (pizza_id, ingredient_id, quantity)
SELECT p.pizza_id, i.ingredient_id, v.q
FROM (SELECT 'маргарита' n,'M' s,'Tomato Sauce' ing,1.0 q UNION ALL
      SELECT 'маргарита','M','Mozzarella Cheese',2.0 UNION ALL
      SELECT 'маргарита','M','Basil',0.2) v
JOIN Pizza p ON LOWER(TRIM(p.name))=v.n AND p.size=v.s
JOIN Ingredient i ON i.name=v.ing
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity);


SELECT p.pizza_id, p.name, p.size,
       COALESCE(SUM(pi.quantity),0) AS ing_rows
FROM Pizza p
LEFT JOIN Pizza_Ingredients pi ON pi.pizza_id = p.pizza_id
WHERE p.availability = TRUE
GROUP BY p.pizza_id, p.name, p.size
ORDER BY ing_rows, p.name;

SELECT pizza_id, pizza_name AS name, size, ingredients_cost, price_before_vat, final_price
FROM PizzaPriceView
ORDER BY name, size;
