CREATE TABLE `user`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `avatar_url` VARCHAR(150) DEFAULT '',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE `teams`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `owner_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE `UsersToTeams`(
    `user_id` BIGINT UNSIGNED NOT NULL,
    `team_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `team_id`)
);
CREATE TABLE `desk`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `owner_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE `projects`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `team_id` BIGINT UNSIGNED NOT NULL,
    `desk_id` BIGINT UNSIGNED NOT NULL,
    `owner_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE `section`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `desk_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `order` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE `ticket`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL,
    `task` TEXT NOT NULL,
    `priority` ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'medium',
    `complexity` INT NOT NULL DEFAULT 1,
    `section_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
ALTER TABLE
    `teams` ADD CONSTRAINT `teams_owner_id_foreign` FOREIGN KEY(`owner_id`) REFERENCES `user`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `UsersToTeams` ADD CONSTRAINT `userstoteams_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `UsersToTeams` ADD CONSTRAINT `userstoteams_team_id_foreign` FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `desk` ADD CONSTRAINT `desk_owner_id_foreign` FOREIGN KEY(`owner_id`) REFERENCES `user`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_team_id_foreign` FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_desk_id_foreign` FOREIGN KEY(`desk_id`) REFERENCES `desk`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_owner_id_foreign` FOREIGN KEY(`owner_id`) REFERENCES `user`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `section` ADD CONSTRAINT `section_desk_id_foreign` FOREIGN KEY(`desk_id`) REFERENCES `desk`(`id`) ON DELETE CASCADE;
ALTER TABLE
    `ticket` ADD CONSTRAINT `ticket_section_id_foreign` FOREIGN KEY(`section_id`) REFERENCES `section`(`id`) ON DELETE CASCADE;

-- Create indexes for better performance
CREATE INDEX `idx_user_email` ON `user`(`email`);
CREATE INDEX `idx_projects_owner` ON `projects`(`owner_id`);
CREATE INDEX `idx_projects_team` ON `projects`(`team_id`);
CREATE INDEX `idx_section_desk` ON `section`(`desk_id`);
CREATE INDEX `idx_ticket_section` ON `ticket`(`section_id`);