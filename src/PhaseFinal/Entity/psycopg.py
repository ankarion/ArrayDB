import psycopg2


class Connection(object):
    def getConnection(self):
        conn = None
        try:
            conn = psycopg2.connect(
                "dbname='library'"
                "user='anthony'"
                "password='masterkey'"
                "host='localhost'"
                )
            print 'connected'
        except:
            print "can't connect to db"
        return(conn)
