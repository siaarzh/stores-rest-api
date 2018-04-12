Implementation of 3 database types:
 - postgreSQL
 - OracleDB
 - SQLite3

Storing in oracle or postgresql needs special classes to deal with IO:
 - class Oracle
 - class PostGre

Each class needs to support a connection open/close, commit, request, requestmany
functions specific to each database's Python API:
(e.g. in Oracle:
    sql = "SELECT * FROM tablenamehere"
    or_cur = conn.cursor()
    or_cur.prepare(sql)
    or_cur.executemany(None, data)
    conn.commit()

 e.g. in postgreSQL:
    pg_cur = conn.cursor()
    sql = "SELECT * FROM tablenamehere"
    pg_cur.execute(sql)
    pg_cur.close()
)

SQLite3 database only needs a connection to a file on disk and commits directly
to  it. This means some IO is simpler but needs to ALSO be included in its OWN
CLASS.