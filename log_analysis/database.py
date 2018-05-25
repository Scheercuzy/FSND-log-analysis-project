import psycopg2


class DBConnection:
    def __init__(self):
        self.dbname = 'news'

    def __enter__(self):
        self.conn = psycopg2.connect("dbname=%s" % (self.dbname,))
        return self.conn

    def __exit__(self, *args):
        self.conn.close()
