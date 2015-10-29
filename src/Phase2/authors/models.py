from Entity.models import Models
from Entity.psycopg import Connection


class Authors(Models):
    __tableName__ = 'authors'

    def __init__(self):
        self.name = ''
        super(Authors, self).__init__()

    def __model__(self, data):
        authors = Authors()
        authors.id = data[0]
        authors.name = data[1] or ''
        return authors

    def all(self):
        authors = self.get()
        return authors

    def get(self, id=None, name=None, article=None):
        sql = 'select * from %s where true ' % self.__tableName__
        if id:
            sql += 'and id = %s ' % str(id)
        if name:
            sql += 'and name = \'%s\' ' % str(name)
        if article:
            # TODO change authors_id to self.__tableName__
            sql += '''
            and exists(
                select * from authorlists as al
                where\'%s\' = al.article_id
                and al.author_id = authors.id
            )
            ''' % article
        cur = Connection().getConnection()
        cur = cur.cursor()
        cur.execute(sql)
        authors = []
        for data in cur.fetchall():
            print data
            author = self.__model__(data)
            authors.append(author)
        return authors

    def save(self):
        if hasattr(self, 'id'):
            sql = '''
            update authors set (id,name)=({id}, '{name}')
            where id = {id};
            '''.format(name=self.name, id=self.id)
        else:
            sql = '''
            insert into authors(name) values('{name}');
            '''.format(name=self.name)
        cur = Connection().getConnection().cursor()
        print sql
        cur.execute(sql)
