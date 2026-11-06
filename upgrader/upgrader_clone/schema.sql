-- ============================================
-- СХЕМА БАЗЫ ДАННЫХ ДЛЯ UPGRADER CLONE
-- Выполни этот код в MySQL (Workbench, HeidiSQL, консоль)
-- ============================================

CREATE DATABASE IF NOT EXISTS upgrader_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE upgrader_db;

-- Таблица пользователей
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 5000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица скинов
CREATE TABLE skins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    tier ENUM('Consumer','Industrial','Mil-Spec','Restricted','Classified','Covert','Contraband') DEFAULT 'Mil-Spec',
    wear VARCHAR(50) DEFAULT 'Field-Tested',
    price DECIMAL(12,2) NOT NULL,
    image_url VARCHAR(255) DEFAULT 'https://via.placeholder.com/300x200/2a2a2a/ffffff?text=Skin',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Инвентарь пользователей
CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skin_id INT NOT NULL,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skin_id) REFERENCES skins(id) ON DELETE CASCADE
);

-- Маркет (продажа/покупка скинов между игроками)
CREATE TABLE market_listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    inventory_id INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    status ENUM('active','sold','cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id) ON DELETE CASCADE
);

-- История апгрейдов
CREATE TABLE upgrade_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    input_skin_id INT,
    output_skin_id INT,
    win TINYINT(1) DEFAULT 0,
    chance DECIMAL(5,2),
    cost DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- СТАРТОВЫЕ СКИНЫ (примерные картинки-заглушки)
-- ============================================
-- Если хочешь свои картинки, замени image_url на прямую ссылку на картинку.
INSERT INTO skins (name, tier, wear, price, image_url, description) VALUES
('AK-47 | Redline', 'Classified', 'Field-Tested', 4500.00, 'https://via.placeholder.com/320x220/8b0000/ffffff?text=AK-47+Redline', 'Классическая красно-чёрная скина'),
('AWP | Dragon Lore', 'Covert', 'Factory New', 150000.00, 'https://via.placeholder.com/320x220/4b0082/ffffff?text=AWP+Dragon+Lore', 'Легендарная снайперская винтовка'),
('M4A4 | Howl', 'Contraband', 'Factory New', 80000.00, 'https://via.placeholder.com/320x220/8b0000/ffffff?text=M4A4+Howl', 'Запрещённый рев — редчайшая скина'),
('Glock-18 | Fade', 'Restricted', 'Minimal Wear', 3500.00, 'https://via.placeholder.com/320x220/ff69b4/ffffff?text=Glock-18+Fade', 'Яркий градиентный пистолет'),
('Karambit | Doppler', 'Covert', 'Factory New', 60000.00, 'https://via.placeholder.com/320x220/008080/ffffff?text=Karambit+Doppler', 'Нож карамбит с расцветкой Doppler'),
('USP-S | Kill Confirmed', 'Classified', 'Field-Tested', 12000.00, 'https://via.placeholder.com/320x220/2f4f4f/ffffff?text=USP-S+Kill+Confirmed', 'Стильный пистолет USP-S');
