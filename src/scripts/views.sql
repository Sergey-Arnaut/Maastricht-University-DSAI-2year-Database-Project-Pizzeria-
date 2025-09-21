-- views.sql
-- Представление для расчета цен пицц с ингредиентами
-- Создание представления для расчета цен пицц
CREATE OR REPLACE VIEW PizzaPriceView AS
SELECT
    p.pizza_id,
    p.name AS pizza_name,
    p.size,
    p.base_price,
    SUM(pi.quantity * i.price_per_unit) AS ingredients_cost,
    ROUND(SUM(pi.quantity * i.price_per_unit) * 1.5, 2) AS price_before_vat, -- Наценка 50%
    ROUND(SUM(pi.quantity * i.price_per_unit) * 1.5 * 1.2, 2) AS final_price -- +20% VAT
FROM Pizza p
JOIN Pizza_Ingredients pi ON p.pizza_id = pi.pizza_id
JOIN Ingredient i ON pi.ingredient_id = i.ingredient_id
GROUP BY p.pizza_id, p.name, p.size, p.base_price;
