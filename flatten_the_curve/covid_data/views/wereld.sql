CREATE VIEW `wereld` AS
select
    `c`.`file` AS `file`,
    `c`.`report_date` AS `report_date`,
    `c`.`fips` AS `fips`,
    `c`.`city` AS `city`,
    `c`.`province_state` AS `province_state`,
    `c`.`country_region` AS `country_region`,
    `c`.`last_update` AS `last_update`,
    `c`.`lat` AS `lat`,
    `c`.`lon` AS `lon`,
    `c`.`confirmed` AS `confirmed`,
    `c`.`death` AS `death`,
    `c`.`recovered` AS `recovered`,
    `c`.`active` AS `active`,
    `c`.`combined_key` AS `combined_key`,
(`c`.`confirmed` - `cl`.`confirmed`) AS `confirmed_new`,
(`c`.`death` - `cl`.`death`) AS `death_new`,
(`c`.`death` / `c`.`confirmed`) AS `death_rate`,
(
        (`c`.`confirmed` - `cl`.`confirmed`) / (`cl`.`confirmed` - `cll`.`confirmed`)
    ) AS `growth_rate`
from
    (
        (
            `covid_world` `c`
            left join `covid_world` `cl` on(
                (
                    `cl`.`report_date` = (`c`.`report_date` + interval -(1) day)
                )
            )
        )
        left join `covid_world` `cll` on(
            (
                `cll`.`report_date` = (`c`.`report_date` + interval -(2) day)
            )
        )
    )