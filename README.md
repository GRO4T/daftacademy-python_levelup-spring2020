# Fastapi on Heroku web app
This app started as a part of Daftacademy Python course, but I've decided to spend some more time and improve her.
## Overview
App uses Fastapi for backend, PostgresSQL for database, and vue.js + Jinja2 for frontend.

## PostgreSQL
##### Chinook database info
* password: admin
* port: 5432
* name: chinook
* user: postgres
* host: 127.0.0.1 (localhost)
##### How to create local postgres database
```bash
psql -h host -p port -U role db_name < migration.sql
```

## SQLAlchemy
##### sqlacodegen (generating SQLAlchemy models)
```bash
sqlacodegen 'postgresql://postgres:admin@127.0.0.1:5432/chinook' > models.py
```

## Useful SQLs
##### Display all tables in the database with its row counts
source: https://gist.github.com/hugorodgerbrown/5084022
```sql
SELECT schemaname,relname,n_live_tup 
  FROM pg_stat_user_tables 
  ORDER BY n_live_tup DESC;
```
##### Display sum of all rows in the database
```sql
SELECT schemaname,SUM(n_live_tup) 
  FROM pg_stat_user_tables
  GROUP BY schemaname;
```

### May be important
12  main    5432 down   postgres /var/lib/postgresql/12/main /var/log/postgresql
/postgresql-12-main.log
