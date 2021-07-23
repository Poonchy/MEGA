import Resources.imports as res
TOKEN = res.os.environ.get("TOKEN")
def openConn():
    conn = res.pymysql.connect(
        host=res.os.environ.get("HOST"),
        user=res.os.environ.get("USER"),
        password=res.os.environ.get("PASSWORD"),
        database=res.os.environ.get("DATABASE"),
        charset='utf8mb4'
    )
    cursor = conn.cursor(res.pymysql.cursors.DictCursor)
    return conn, cursor
def queryTable(command):
    conn, cursor = openConn()
    cmd = command
    cursor.execute(cmd)
    conn.commit()
    query = cursor.fetchall()
    conn.close()
    return query
def insert(table, columns, values):
    cmd = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
    queryTable(cmd)
def select(whatToSelect, table, column, value):
    cmd = "SELECT %s FROM %s WHERE %s = '%s';" % (whatToSelect, table, column, value)
    query = queryTable(cmd)
    try:
        return query[0]
    except:
        return {}
def update(table, selector, selectorValue, column, columnValue):
    cmd = "UPDATE %s SET %s = '%s' WHERE %s = '%s';" % (table, column, columnValue, selector, selectorValue)
    queryTable(cmd)
def delete(table, selector, selectorValue):
    cmd = "DELETE FROM %s WHERE %s = '%s';" % (table, selector, selectorValue)
    queryTable(cmd)