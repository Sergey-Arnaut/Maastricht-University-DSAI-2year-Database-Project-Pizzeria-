-- constraints_and_triggers.sql
-- Enforce DOB, vegetarian/vegan integrity, ingredient prices > 0, and global single-use discount codes.

-- 1) DOB must be 10+ years ago (or NULL)
ALTER TABLE Customer
  ADD CONSTRAINT chk_customer_dob_10y
  CHECK (date_of_birth IS NULL OR date_of_birth <= (CURDATE() - INTERVAL 10 YEAR));

-- 2) Ingredient price must be > 0 (strictly positive, per spec)
ALTER TABLE Ingredient
  MODIFY price_per_unit DECIMAL(10,2) NOT NULL CHECK (price_per_unit > 0);

-- 3) Discount code single-use globally (one redemption per code)
ALTER TABLE DiscountRedemption
  ADD UNIQUE KEY uq_discount_global (discount_id);

-- 4) Vegetarian/Vegan integrity on pizza composition
DROP TRIGGER IF EXISTS bi_pizza_ing_veg;
DELIMITER $$
CREATE TRIGGER bi_pizza_ing_veg
BEFORE INSERT ON Pizza_Ingredients
FOR EACH ROW
BEGIN
  DECLARE v_is_vegetarian BOOLEAN;
  DECLARE v_is_vegan BOOLEAN;
  DECLARE ing_veg BOOLEAN;
  DECLARE ing_vegan BOOLEAN;

  SELECT is_vegetarian, is_vegan INTO v_is_vegetarian, v_is_vegan
    FROM Pizza WHERE pizza_id = NEW.pizza_id;

  SELECT vegetarian, vegan INTO ing_veg, ing_vegan
    FROM Ingredient WHERE ingredient_id = NEW.ingredient_id;

  IF v_is_vegetarian AND (ing_veg = FALSE) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Vegetarian pizza cannot contain non-vegetarian ingredient';
  END IF;

  IF v_is_vegan AND (ing_vegan = FALSE) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Vegan pizza cannot contain non-vegan ingredient';
  END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS bu_pizza_ing_veg;
DELIMITER $$
CREATE TRIGGER bu_pizza_ing_veg
BEFORE UPDATE ON Pizza_Ingredients
FOR EACH ROW
BEGIN
  DECLARE v_is_vegetarian BOOLEAN;
  DECLARE v_is_vegan BOOLEAN;
  DECLARE ing_veg BOOLEAN;
  DECLARE ing_vegan BOOLEAN;

  SELECT is_vegetarian, is_vegan INTO v_is_vegetarian, v_is_vegan
    FROM Pizza WHERE pizza_id = NEW.pizza_id;

  SELECT vegetarian, vegan INTO ing_veg, ing_vegan
    FROM Ingredient WHERE ingredient_id = NEW.ingredient_id;

  IF v_is_vegetarian AND (ing_veg = FALSE) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Vegetarian pizza cannot contain non-vegetarian ingredient';
  END IF;

  IF v_is_vegan AND (ing_vegan = FALSE) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Vegan pizza cannot contain non-vegan ingredient';
  END IF;
END$$
DELIMITER ;
