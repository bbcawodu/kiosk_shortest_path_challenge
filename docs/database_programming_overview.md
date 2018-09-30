## Postgres Pros:
- Taken from: https://wiki.python.org/moin/PostgreSQL
  - Good compliance with SQL standards
  - Supports many SQL features
  - Foreign keys
  - Implements all SQL99 join types: inner join, left, right, full outer join, natural join
  - Subqueries
  - UNION and UNION ALL, INTERSECT and EXCEPT
  - Views
  - Triggers
  - Support for international character sets, multibyte character encodings, Unicode
  - Supports many languages for writing server-side functions/procedures and aggregates: Python, C, Perl, Tcl, PL/PgSQL, ...
  - ACID compliant
  - Support for rollback
  - Serializable transaction isolation
  - Multi-Version Concurrency Control (MVCC) for highly scalable concurrent applications

## Postgres Database Access from Python

### Drivers
Parts Taken from: http://crossbar.io/docs/Database-Programming-with-PostgreSQL/

- To access PostgreSQL from Python, you will need a database driver.
  There are multiple drivers (e.g. see here and here), however, the most commonly used is Psycopg.
- Psycopg can be used to access PostgreSQL from WAMP application components written in Python, and running under Twisted or asyncio.

Parts Taken from: https://pypi.python.org/pypi/psycopg2

- Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are
  the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share
  the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors
  and make a large number of concurrent “INSERT”s or “UPDATE”s.
- Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features
  client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many
  Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended
  and customized thanks to a flexible objects adaptation system.
  
### Create local db and connect it to project  
- First download Postgres for either mac or windows
- [Mac](http://postgresapp.com/)
- [Windows](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows)
- Follow installation guide and read docs on how to create a database and a user that is able to access that database
- Here is a short guide to creating database and user(FOR MAC):
    - Make sure postgres bin is added to your PATH environment variable and that the command 'which psql' works
    - Use 'createdb <database name>' to create a new postgress database on your local machine
    - Use 'psql <database name>' to open the postgres command line tool with a connection to your database
    - Once psql prompt is open, use the following command to create a postgres database user
        - "CREATE USER <username> WITH PASSWORD '<password>';"
    - Grant priviliges to access and write/read/etc. to your database with the following command.
        - "GRANT ALL PRIVILEGES ON DATABASE <database name> to <username>;"
    - Exit the postgres command line tool with the following command
        - '\q'
    - To access the database using a database url environment variable that is normally set by heroku when deployed,
      set it globally or locally by doing the following:
      - (PREFERRED METHOD) Configure virtual environment activate script to set and unset the PORT environment variable on
        activation and deactivation respectively
        - open venv/bin/activate
            - Add the folllowing the the end of the script:
                - export DATABASE_URL='postgres://<username>:<password>@localhost:<port>/<database name>'
                    - This sets the DATABASE_URL environment variable when the virtual environment activates
            - Add the following at the end of the deactivate () {} function
                - unset DATABASE_URL
                    - This unsets the DATABASE_URL environment variable when the virtual environment is deactivated
- You can now access the database programatically through psycopg2 using the DATABASE_URL environment variable

### Object-Relational Mapper database adapter
- I used alembic for DB schema creation / migration functionality and SQLAlchemy ORM Models to interact with the db.
    - [Alembic and SQLAlchemy Tutorial README](Alembic_SQLAlchemy_tutorial.md)
    - Docs: http://alembic.zzzcomputing.com/en/latest/
    - DB schema changes with Alembic through manual creation of migrations: http://alembic.zzzcomputing.com/en/latest/tutorial.html
    - DB schema changes with Alembic through auto generate migrations from SQLAlchemy ORM models:
        - Tutorial to create ORM models through SQLAlchemy: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
        - Tutorial to autogenerate migrations from SQLAlchemy models: http://alembic.zzzcomputing.com/en/latest/autogenerate.html
            
