CREATE VIEW `de` AS
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
    `cp`.`confirmed_new` AS `confirmed_new`,
    `cp`.`death_new` AS `death_new`,
    `cp`.`death_rate` AS `death_rate`,
    `cp`.`growth_rate` AS `growth_rate`
from
    (
        `covid` `c`
        join `covid_prep_it` `cp` on((`c`.`report_date` = `cp`.`report_date`))
    )
where
    (
        (`c`.`country_region` = 'Germany')
        and isnull(`c`.`province_state`)
    )