SELECT `c`.`date` AS `date`
	,`c`.`intakeCount` AS `CurrentTotal`
	,`c`.`newIntake` AS `Nieuw`
	,(`c`.`newIntake` / `c1`.`newIntake`) AS `Groeifactor`
FROM (
	`covid_data`.`covid_ic_nl` `c` LEFT JOIN `covid_data`.`covid_ic_nl` `c1` ON ((`c1`.`date` = (`c`.`date` + interval - (1) day)))
	)

