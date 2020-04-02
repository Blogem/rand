CREATE VIEW `covid_hosp_nl_prep` AS
select
    `c`.`Datum` AS `Datum`,
(`c`.`Aantal` - `cl`.`Aantal`) AS `Nieuw`,
(
        (`c`.`Aantal` - `cl`.`Aantal`) / (`cl`.`Aantal` - `cll`.`Aantal`)
    ) AS `Groeifactor`
from
    (
        (
            `covid_hosp_nl` `c`
            left join `covid_hosp_nl` `cl` on(
                (`cl`.`Datum` = (`c`.`Datum` + interval -(1) day))
            )
        )
        left join `covid_hosp_nl` `cll` on(
            (
                `cll`.`Datum` = (`c`.`Datum` + interval -(2) day)
            )
        )
    )