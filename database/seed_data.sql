-- 1. Insert Test Users
-- Using dummy password hashes (bcrypt style)
INSERT INTO users (username, email, password_hash, full_name, role, phone, balance) VALUES
('somchai_trek', 'somchai@example.com', '$2b$12$K.LO.X.vXG.X.vXG.X.vX.fakehash', 'Somchai Trekking', 'user', '081-222-3333', 5000.00),
('jane_camper', 'jane@example.com', '$2b$12$K.LO.X.vXG.X.vXG.X.vX.fakehash', 'Jane Doe', 'user', '089-111-2222', 1200.00),
('admin_pete', 'admin@camping.com', '$2b$12$K.LO.X.vXG.X.vXG.X.vX.fakehash', 'Admin Pete', 'admin', '088-888-8888', 0.00)
ON DUPLICATE KEY UPDATE username=VALUES(username);

-- 2. Insert User-Created Camps (Manual trips)
-- Getting IDs for users we just created
SET @user1 = (SELECT id FROM users WHERE username = 'somchai_trek');
SET @user2 = (SELECT id FROM users WHERE username = 'jane_camper');
SET @admin = (SELECT id FROM users WHERE username = 'admin_pete');

INSERT INTO camps (name, location, start_date, duration, price, slots, available_slots, description, contact, status, created_by) VALUES
('แคมป์ปิ้งดาวล้านดวง @เขาค้อ', 'เพชรบูรณ์', '2026-05-15', 3, 2500, 10, 8, 'นอนเต็นท์ชมดาว ก่อกองไฟตอนกลางคืน บรรยากาศสุดฟิน', 'Line: camp_pete', 'active', @admin),
('พายเรือคายัค เขื่อนเขาสก', 'สุราษฎร์ธานี', '2026-06-10', 2, 1800, 15, 12, 'ทริปพายเรือชมกุ้ยหลินเมืองไทย น้ำใสเย็นสบาย', '081-222-3333', 'active', @user1),
('เดินป่าพิชิตยอดดอยหลวงเชียงดาว', 'เชียงใหม่', '2026-11-20', 4, 4500, 8, 8, 'ทริปสุดโหดสำหรับสายลุย ชมพรรณไม้หายาก', '089-111-2222', 'active', @user2)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 3. Insert Bookings
-- Linking users to both Scraped camps and Manual camps
SET @camp1 = (SELECT id FROM camps WHERE name = 'แคมป์ปิ้งดาวล้านดวง @เขาค้อ');
SET @camp2 = (SELECT id FROM camps WHERE name = 'พายเรือคายัค เขื่อนเขาสก');
SET @scraped_camp = (SELECT id FROM camps WHERE created_by = 6 LIMIT 1);

INSERT INTO bookings (user_id, camp_id, status) VALUES
(@user1, @scraped_camp, 'confirmed'),
(@user1, @camp1, 'pending_payment'),
(@user2, @scraped_camp, 'confirmed'),
(@user2, @camp1, 'confirmed'),
(@user2, @camp2, 'cancelled')
ON DUPLICATE KEY UPDATE status=VALUES(status);
