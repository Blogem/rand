CREATE VIEW `covid_prep_de` AS
select
    `c`.`report_date` AS `report_date`,
(`c`.`confirmed` - `cl`.`confirmed`) AS `confirmed_new`,
(`c`.`death` - `cl`.`death`) AS `death_new`,
(`c`.`death` / `c`.`confirmed`) AS `death_rate`,
(
        (`c`.`confirmed` - `cl`.`confirmed`) / (`cl`.`confirmed` - `cll`.`confirmed`)
    ) AS `growth_rate`
from
    (
        (
            `covid` `c`
            left join `covid` `cl` on(
                (
                    (
                        `cl`.`report_date` = (`c`.`report_date` + interval -(1) day)
                    )
                    and (`cl`.`country_region` = `c`.`country_region`)
                )
            )
        )
        left join `covid` `cll` on(
            (
                (
                    `cll`.`report_date` = (`c`.`report_date` + interval -(2) day)
                )
                and (`cll`.`country_region` = `c`.`country_region`)
            )
        )
    )
where
    (`c`.`country_region` = 'Germany')