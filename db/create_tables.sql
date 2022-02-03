CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(64),
  `status` boolean DEFAULT 1,
  `is_author` boolean DEFAULT 0
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE `tests` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `author_id` bigint,
  `name` varchar(255),
  `answers` varchar(255),
  `count_tests` int,
  `test_time` int,
  `created_at` int,
  `status` boolean DEFAULT 1
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE `results` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `test_id` int,
  `user_id` bigint,
  `result_str` varchar(255),
  `correct_answers_count` int,
  `test_time` int
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;