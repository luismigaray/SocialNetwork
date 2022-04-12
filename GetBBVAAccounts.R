## Cargamos RPostgreSQL
library("RPostgreSQL")

#Eliminamos los Tweets que pertenecen a alguna cuenta BBVA
dbGetQuery(con, "SELECT COUNT(*) FROM test;")
dbGetQuery(con, "DELETE FROM test WHERE EXISTS (SELECT * FROM cuentas_bbva WHERE cuentas_bbva.screen_name = test.screen_name);")
dbGetQuery(con, "SELECT COUNT(*) FROM test;")