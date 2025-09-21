-- =============================================
-- Pizza Delivery Database Schema
-- =============================================

USE our_little_secret;

-- Таблица Customers
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    gender ENUM('male', 'female', 'other'),
    email VARCHAR(255) UNIQUE NOT NULL,
    postal_code VARCHAR(12),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_postal_code (postal_code)
);

-- Таблица Delivery Persons
CREATE TABLE IF NOT EXISTS DeliveryPerson (
    delivery_person_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    number_of_orders INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00 CHECK (rating >= 0 AND rating <= 5),
    availability BOOLEAN DEFAULT TRUE,
    current_position VARCHAR(255),
    delivery_postal_code VARCHAR(12),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_availability (availability),
    INDEX idx_rating (rating)
);

-- Таблица Discount Codes
CREATE TABLE IF NOT EXISTS DiscountCode (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    discount_code VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255), -- если требуется аутентификация
    discount_value INT NOT NULL CHECK (discount_value > 0),
    discount_type ENUM('percent', 'value') NOT NULL,
    valid_from DATE,
    valid_until DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_discount_code (discount_code),
    INDEX idx_is_active (is_active)
);

-- Таблица Ingredients
CREATE TABLE IF NOT EXISTS Ingredient (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL CHECK (price_per_unit >= 0),
    vegan BOOLEAN DEFAULT FALSE,
    vegetarian BOOLEAN DEFAULT TRUE,
    allergen BOOLEAN DEFAULT FALSE,
    allergen_type VARCHAR(100),
    amount VARCHAR(20),
    unit VARCHAR(20) DEFAULT 'g',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_name (name),
    INDEX idx_allergen (allergen)
);

-- Таблица Pizzas
CREATE TABLE IF NOT EXISTS Pizza (
    pizza_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    size ENUM('S', 'M', 'L', 'XL', 'XXL') NOT NULL DEFAULT 'M',
    availability BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255),
    base_price DECIMAL(10,2) NOT NULL CHECK (base_price > 0),
    description TEXT,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_pizza_name_size (name, size),
    INDEX idx_availability (availability)
);

-- Таблица Pizza Ingredients (связь многие-ко-многим)
CREATE TABLE IF NOT EXISTS Pizza_Ingredients (
    pizza_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity DECIMAL(8,2) NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (pizza_id, ingredient_id),
    FOREIGN KEY (pizza_id) REFERENCES Pizza(pizza_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id) ON DELETE CASCADE,

    INDEX idx_pizza_id (pizza_id),
    INDEX idx_ingredient_id (ingredient_id)
);

-- Таблица Desserts
CREATE TABLE IF NOT EXISTS Dessert (
    dessert_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    sugar_free BOOLEAN DEFAULT FALSE,
    gluten_free BOOLEAN DEFAULT FALSE,
    milk_free BOOLEAN DEFAULT FALSE,
    description TEXT,
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_dessert_name (name),
    INDEX idx_availability (availability)
);

-- Таблица Drinks
CREATE TABLE IF NOT EXISTS Drink (
    drink_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    milk_free BOOLEAN DEFAULT TRUE,
    sugar_free BOOLEAN DEFAULT FALSE,
    volume_ml INT CHECK (volume_ml > 0),
    is_alcoholic BOOLEAN DEFAULT FALSE,
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_drink_name (name),
    INDEX idx_availability (availability)
);

-- Таблица Menus
CREATE TABLE IF NOT EXISTS Menu (
    menu_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    valid_from DATE,
    valid_until DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_is_active (is_active)
);

-- Таблица Menu Items
CREATE TABLE IF NOT EXISTS MenuItems (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_id INT NOT NULL,
    product_id INT NOT NULL,
    product_type ENUM('pizza', 'drink', 'dessert') NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (menu_id) REFERENCES Menu(menu_id) ON DELETE CASCADE,
    UNIQUE INDEX idx_menu_product (menu_id, product_id, product_type),

    INDEX idx_menu_id (menu_id),
    INDEX idx_product_type (product_type)
);

-- Таблица Orders
CREATE TABLE IF NOT EXISTS `Order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'preparing', 'baking', 'ready', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0),
    delivery_postal_code VARCHAR(12) NOT NULL,
    delivery_person_id INT,
    estimated_delivery_time DATETIME,
    actual_delivery_time DATETIME,
    discount_id INT,
    discount_amount DECIMAL(10,2) DEFAULT 0 CHECK (discount_amount >= 0),
    payment_id INT,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (delivery_person_id) REFERENCES DeliveryPerson(delivery_person_id),
    FOREIGN KEY (discount_id) REFERENCES DiscountCode(discount_id),

    INDEX idx_customer_id (customer_id),
    INDEX idx_status (status),
    INDEX idx_order_timestamp (order_timestamp)
);

-- Таблица Order Items
CREATE TABLE IF NOT EXISTS OrderItem (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    pizza_id INT,
    ingredient_id INT, -- для дополнительных ингредиентов
    pizza_quantity INT DEFAULT 1 CHECK (pizza_quantity > 0),
    drink_id INT,
    drink_quantity INT DEFAULT 0 CHECK (drink_quantity >= 0),
    dessert_id INT,
    dessert_quantity INT DEFAULT 0 CHECK (dessert_quantity >= 0),
    item_current_price DECIMAL(10,2) NOT NULL CHECK (item_current_price >= 0),
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (pizza_id) REFERENCES Pizza(pizza_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id),
    FOREIGN KEY (drink_id) REFERENCES Drink(drink_id),
    FOREIGN KEY (dessert_id) REFERENCES Dessert(dessert_id),

    INDEX idx_order_id (order_id),
    INDEX idx_pizza_id (pizza_id)
);

-- Таблица Payments
CREATE TABLE IF NOT EXISTS Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    payment_method ENUM('card', 'cash', 'online') NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'refunded', 'cancelled') DEFAULT 'pending',
    payment_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    refund_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),

    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_payment_timestamp (payment_timestamp)
);

-- Таблица Discount Redemptions
CREATE TABLE IF NOT EXISTS DiscountRedemption (
    redemption_id INT AUTO_INCREMENT PRIMARY KEY,
    discount_id INT NOT NULL,
    customer_id INT NOT NULL,
    order_id INT NOT NULL,
    redeemed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (discount_id) REFERENCES DiscountCode(discount_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),

    UNIQUE INDEX idx_discount_order (discount_id, order_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_redeemed_at (redeemed_at)
);



