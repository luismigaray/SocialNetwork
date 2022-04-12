## Cargamos RPostgreSQL
library("RPostgreSQL")

#Eliminamos los Tweets que pertenecen a alguna cuenta BBVA
dbGetQuery(con, "DELETE FROM original_tweets WHERE EXISTS (SELECT * FROM cuentas_bbva WHERE cuentas_bbva.screen_name = original_tweets.screen_name);")

#Eliminamos los registros duplicados (mismo status_id)
dbGetQuery(con, "ALTER TABLE original_tweets ADD COLUMN seq_id SERIAL PRIMARY KEY;")
dbGetQuery(con, "DELETE FROM original_tweets where seq_id in (SELECT A.seq_id FROM original_tweets A inner join original_tweets B on A.seq_id < B.seq_id
                 AND (A.status_id = B.status_id));")
dbGetQuery(con, "ALTER TABLE original_tweets DROP COLUMN seq_id;")

#Eliminar tweets que no estén en inglés o en español
dbGetQuery(con, "DELETE FROM original_tweets WHERE lang <> 'es' AND lang <> 'en';") 
#Contar los tweets
dbGetQuery(con, "SELECT COUNT(*) FROM original_tweets;")