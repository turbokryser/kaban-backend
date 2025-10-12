CREATE TABLE `user`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `team_id` BIGINT NULL
);
CREATE TABLE `ticket`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL,
    `task` TEXT NOT NULL,
    `priority` ENUM('') NOT NULL,
    `complexity` INT NOT NULL,
    `setcion_id` BIGINT NOT NULL
);
CREATE TABLE `desk`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` BIGINT NOT NULL,
    `team` BIGINT NOT NULL,
    `owner_id` BIGINT NOT NULL
);
CREATE TABLE `section`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `desk_id` BIGINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `order` INT NOT NULL
);
CREATE TABLE `teams`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `owner_id` BIGINT NOT NULL
);
CREATE TABLE `projects`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `team_id` BIGINT NOT NULL,
    `desk_id` BIGINT NOT NULL,
    `owner_id` BIGINT NOT NULL,
    `new_column` BIGINT NOT NULL
);
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_team_id_foreign` FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`);
ALTER TABLE
    `section` ADD CONSTRAINT `section_desk_id_foreign` FOREIGN KEY(`desk_id`) REFERENCES `desk`(`id`);
ALTER TABLE
    `teams` ADD CONSTRAINT `teams_owner_id_foreign` FOREIGN KEY(`owner_id`) REFERENCES `user`(`id`);
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_desk_id_foreign` FOREIGN KEY(`desk_id`) REFERENCES `desk`(`id`);
ALTER TABLE
    `projects` ADD CONSTRAINT `projects_new_column_foreign` FOREIGN KEY(`new_column`) REFERENCES `user`(`id`);
ALTER TABLE
    `user` ADD CONSTRAINT `user_team_id_foreign` FOREIGN KEY(`team_id`) REFERENCES `teams`(`id`);
ALTER TABLE
    `desk` ADD CONSTRAINT `desk_owner_id_foreign` FOREIGN KEY(`owner_id`) REFERENCES `user`(`id`);
ALTER TABLE
    `ticket` ADD CONSTRAINT `ticket_setcion_id_foreign` FOREIGN KEY(`setcion_id`) REFERENCES `section`(`id`);