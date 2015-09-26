import inspect
import psycopg2


class Models(object):
    __tableName__ = 'Not implemented yet!'

    def __init__(self):
        attributes = inspect.getmembers(
            self, lambda x: not(inspect.isroutine(x))
        )
        no_magic = [str(x[0]) for x in attributes if not(x[0].startswith('__'))]
        params = 's.'+', s.'.join(no_magic)
        select = (
            "select {params} \n"
            "from {tableName} as s "
            )
        self.__sql__ = select.format(
            params=params,
            tableName=self.__tableName__
        )

    def __str__(self):
        return (self.__sql__)

    def __finilize__(self):
        try:
            conn = psycopg2.connect(
                "dbname='library'"
                "user='anthony'"
                "password='masterkey'"
                "host='localhost'"
            )
        except:
            print "can't connect to db"
        cur = conn.cursor()
        return cur.execute(self.__sql__)

    def __save__(self):
        attributes = inspect.getmembers(
            self, lambda x: not(inspect.isroutine(x))
        )
        no_magic = [
            str(x[0]) for x in attributes
            if (
                not(x[0].startswith('__'))
                and self.__getattribute__(x[0])
            )
        ]
        params = ','.join(no_magic)

        self.__sql__ = 'insert into {tableName}( {params}) values({paramsValues})'.format(
            tableName=self.__tableName__,
            params=params,
            paramsValues='\''+'\', \''.join(
                [str(self.__getattribute__(x)) for x in no_magic]
            )
        )
        return self.__finilize__()
