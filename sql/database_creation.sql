production CREATE TABLE `production` (
	`production_key` bigint(20) NOT NULL AUTO_INCREMENT,
	`datetime` datetime(2) NOT NULL,
	`consumption` float NOT NULL,
	`production` float NOT NULL,
	PRIMARY KEY (`production_key`),
	KEY `datetime_idx` (`datetime`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8