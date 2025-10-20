DROP VIEW IF EXISTS PizzaPriceView;

CREATE VIEW PizzaPriceView AS
SELECT
  p.pizza_id,
  p.name AS name,
  p.size AS size,
  ROUND(SUM(pi.quantity * i.price_per_unit), 2)               AS ingredients_cost,
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.40, 2)        AS price_no_vat,
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.40 * 1.09, 2) AS price_with_vat
FROM Pizza p
JOIN Pizza_Ingredients pi ON pi.pizza_id = p.pizza_id
JOIN Ingredient i         ON i.ingredient_id = pi.ingredient_id
WHERE p.availability = TRUE
GROUP BY p.pizza_id, p.name, p.size;
