CREATE VIEW `covid_china` AS
select
    'aggregate' AS `file`,
    `covid`.`report_date` AS `report_date`,
    NULL AS `fips`,
    NULL AS `city`,
    NULL AS `province_state`,
    'China' AS `country_region`,
    max(`covid`.`last_update`) AS `last_update`,
    NULL AS `lat`,
    NULL AS `lon`,
    sum(`covid`.`confirmed`) AS `confirmed`,
    sum(`covid`.`death`) AS `death`,
    sum(`covid`.`recovered`) AS `recovered`,
    sum(`covid`.`active`) AS `active`,
    NULL AS `combined_key`
from
    `covid`
where
    (
        `covid`.`country_region` in ('Mainland China', 'China')
    )
group by
    `covid`.`report_date`
order by
    `covid`.`report_date`