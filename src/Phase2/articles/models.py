from Entity.models import Models
from Entity.psycopg import Connection


class Articles(Models):
    __tableName__ = 'articles'

    def __init__(self):
        self.venue = ''
        self.id = 0
        self.year = 1900
        self.title = ''
        super(Articles, self).__init__()

    def __model__(self, data):
        article = Articles()
        article.id = data[0]
        article.venue = data[1] or ''
        article.year = data[2] or ''
        article.title = data[3] or ''
        return article

    def all(self):
        articles = self.get()
        return articles

    def get(self, id=None, venue=None, year=None, title=None, author=None, article=None):
        sql = 'select * from %s where true ' % self.__tableName__
        if id:
            sql += 'and id = %s ' % str(id)
        if venue:
            sql += 'and venue = \' %s \' ' % str(venue)
        if year:
            sql += 'and year = %s ' % str(year)
        if title:
            sql += 'and title = %s ' % str(title)
        if author:
            # TODO change aritcles.id to self.__tableName__
            sql += '''
                and exists(
                    select * from authorlists as al
                    where %s = al.author_id
                    and  al.article_id = articles.id
                )
            ''' % author
        if article:
            sql += '''
            and exists(
                select * from bibliographies as b
                where %s = b.reference_id
                and
                b.article_id = articles.id
            )
            ''' % article
        cur = Connection().getConnection()
        cur = cur.cursor()
        cur.execute(sql)
        articles = []
        for data in cur.fetchall():
            article = self.__model__(data)
            articles.append(article)
        return articles
