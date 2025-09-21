-- Пересчёт цены пиццы из состава
CREATE OR REPLACE VIEW PizzaPriceView AS
SELECT
  p.pizza_id,
  p.name,
  p.size,
  ROUND(SUM(pi.quantity * i.price_per_unit), 2)                  AS ingredients_cost,
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.30, 2)           AS price_no_vat,     -- наценка 30%
  ROUND(SUM(pi.quantity * i.price_per_unit) * 1.30 * 1.21, 2)    AS price_with_vat    -- НДС 21%
FROM Pizza p
JOIN Pizza_Ingredients pi ON pi.pizza_id = p.pizza_id
JOIN Ingredient i         ON i.ingredient_id = pi.ingredient_id
WHERE p.availability = TRUE
GROUP BY p.pizza_id, p.name, p.size;
