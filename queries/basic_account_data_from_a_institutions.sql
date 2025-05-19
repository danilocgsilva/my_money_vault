SET @institution_query = '?????';

SELECT
    `institutions`.`name`,
    `accounts`.`name` AS `account_name`,
    `account_metadata`.`metadata_key`,
    `account_metadata`.`metadata_value`
FROM `institutions` 
LEFT JOIN `accounts` ON institutions.id = accounts.institution_id
LEFT JOIN `account_metadata` ON accounts.id = account_metadata.account_id
WHERE `institutions`.`name` = @institution_query;
