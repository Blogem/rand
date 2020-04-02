CREATE TABLE `covid` (
  `file` varchar(255) DEFAULT NULL,
  `report_date` date DEFAULT NULL,
  `fips` int(11) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `province_state` varchar(255) DEFAULT NULL,
  `country_region` varchar(255) DEFAULT NULL,
  `last_update` varchar(255) DEFAULT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lon` decimal(11,8) DEFAULT NULL,
  `confirmed` int(11) DEFAULT NULL,
  `death` int(11) DEFAULT NULL,
  `recovered` int(11) DEFAULT NULL,
  `active` int(11) DEFAULT NULL,
  `combined_key` varchar(255) DEFAULT NULL,
  KEY `report_date` (`report_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;