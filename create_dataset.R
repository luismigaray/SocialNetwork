dbGetQuery(con, "INSERT INTO cuentas_bbva (screen_name) VALUES ('DiarioSUR');")
dbGetQuery(con, "ALTER TABLE training_set ADD COLUMN clasification INT;")
dbGetQuery(con, "CREATE TABLE training_set AS (SELECT TOP 100 * FROM original_tweets);")