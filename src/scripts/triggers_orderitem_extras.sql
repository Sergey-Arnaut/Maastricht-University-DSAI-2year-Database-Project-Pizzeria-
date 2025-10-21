
DROP TRIGGER IF EXISTS bi_orderitem_extra_veg;
DELIMITER $$
CREATE TRIGGER bi_orderitem_extra_veg
BEFORE INSERT ON OrderItem
FOR EACH ROW
BEGIN
  IF NEW.pizza_id IS NOT NULL AND NEW.ingredient_id IS NOT NULL THEN
    DECLARE p_is_veg   BOOLEAN;
    DECLARE p_is_vegan BOOLEAN;
    DECLARE i_is_veg   BOOLEAN;
    DECLARE i_is_vegan BOOLEAN;

    SELECT is_vegetarian, is_vegan INTO p_is_veg, p_is_vegan
      FROM Pizza WHERE pizza_id = NEW.pizza_id;

    SELECT vegetarian, vegan INTO i_is_veg, i_is_vegan
      FROM Ingredient WHERE ingredient_id = NEW.ingredient_id;

    IF p_is_vegan AND (i_is_vegan = FALSE) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Vegan pizza cannot contain non-vegan extra ingredient';
    END IF;

    IF p_is_veg AND (i_is_veg = FALSE) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Vegetarian pizza cannot contain non-vegetarian extra ingredient';
    END IF;
  END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS bu_orderitem_extra_veg;
DELIMITER $$
CREATE TRIGGER bu_orderitem_extra_veg
BEFORE UPDATE ON OrderItem
FOR EACH ROW
BEGIN
  IF NEW.pizza_id IS NOT NULL AND NEW.ingredient_id IS NOT NULL THEN
    DECLARE p_is_veg   BOOLEAN;
    DECLARE p_is_vegan BOOLEAN;
    DECLARE i_is_veg   BOOLEAN;
    DECLARE i_is_vegan BOOLEAN;

    SELECT is_vegetarian, is_vegan INTO p_is_veg, p_is_vegan
      FROM Pizza WHERE pizza_id = NEW.pizza_id;

    SELECT vegetarian, vegan INTO i_is_veg, i_is_vegan
      FROM Ingredient WHERE ingredient_id = NEW.ingredient_id;

    IF p_is_vegan AND (i_is_vegan = FALSE) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Vegan pizza cannot contain non-vegan extra ingredient';
    END IF;

    IF p_is_veg AND (i_is_veg = FALSE) THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Vegetarian pizza cannot contain non-vegetarian extra ingredient';
    END IF;
  END IF;
END$$
DELIMITER ;



