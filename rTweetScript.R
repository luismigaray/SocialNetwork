## load rtweet and RPostgreSQL
library("rtweet")
library("RPostgreSQL")

# load PostgreSQL driver
drv = dbDriver("PostgreSQL") 

# create a connection
con = dbConnect(drv, dbname = "twitterBBVA", host = "127.0.0.1", port = 5432, 
                user = "m.soto.montesinos", password = "XXXXXX")

##Twitter keys and tokens for the authentication.
#api_key <- "api_key" 
#api_secret_key <- "api_secret_key" 
#access_token <- "2733355629-access_token" 
#access_token_secret <- "access_token_secret"
## authenticate via web browser
## authenticate via web browser
#token <- create_token(
#  app = "TwitterBBVA",
#  consumer_key = api_key,
#  consumer_secret = api_secret_key,
#  access_token = access_token,
#  access_secret = access_token_secret)

#Download teets.
rt <-  search_tweets("BBVA", n = 10000, include_rts = FALSE)

#write the teewts into the data base.
dbWriteTable(con,'original_tweets',rt, row.names=FALSE, append=TRUE)

#Llamamos al script de primera fase de limpieza.
source("primeraLimpieza.R")