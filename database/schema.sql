-- สร้างฐานข้อมูล
CREATE DATABASE IF NOT EXISTS camping_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE camping_db;

-- ตาราง users (สำหรับ login/register)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    phone VARCHAR(20),
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ตาราง camps
CREATE TABLE IF NOT EXISTS camps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE,
    duration INT,
    price INT,
    slots INT DEFAULT 20,
    available_slots INT DEFAULT 20,
    image_url TEXT,
    description TEXT,
    contact VARCHAR(255),
    facebook_link TEXT,
    status ENUM('active', 'full', 'ended', 'cancelled') DEFAULT 'active',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ตาราง bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    camp_id INT NOT NULL,
    status ENUM('pending_payment', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending_payment',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE CASCADE
);
