SET @institution_query = '???';
SET @metadata_1 = '???';
SET @metadata_2 = '???';

SELECT
    `institutions`.`name`,
    `accounts`.`name` AS `account_name`,
    (
        SELECT
            am.metadata_value
        FROM account_metadata AS am
        LEFT JOIN accounts AS a ON am.account_id = a.id
        LEFT JOIN institutions AS i ON a.institution_id = i.id
        WHERE i.name = @institution_query AND am.metadata_key = @metadata_1
    ) as `@metadata_1`
    ,(
        SELECT
            am.metadata_value
        FROM account_metadata AS am
        LEFT JOIN accounts AS a ON am.account_id = a.id
        LEFT JOIN institutions AS i ON a.institution_id = i.id
        WHERE i.name = @institution_query AND am.metadata_key = @metadata_2
    ) as `@metadata_2`
FROM `institutions` 
LEFT JOIN `accounts` ON institutions.id = accounts.institution_id
WHERE `institutions`.`name` = @institution_query;

