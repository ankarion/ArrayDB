from Entity.models import Models


class Articles(Models):
    __fields__ = ["id", "venue", "year", "title"]

    @classmethod
    def all(self):
        articles = self.get()
        return articles

    @classmethod
    def get(cls, id=None, venue=None, year=None, title=None,
            author=None, article=None,
            limit=None, offset=None):
        data = cls.__getData__()
        articles = []
        for i in range(len(data)/4):
            article = cls()
            article.__model__(data[4*i:])
            articles.append(article)
        sql = "true"
        if id:
            articles = filter(lambda x: True if x.id == id else False, articles)
        if venue:
            articles = filter(lambda x: True if x.venue == venue else False, articles)
        if year:
            articles = filter(lambda x: True if x.year == year else False, articles)
        if title:
            articles = filter(lambda x: True if x.title == title else False, articles)
            sql += 'and title =\'%s\' ' % str(title)
        if author:
            # TODO change aritcles.id to self.__tableName__
            sql += '''
                and exists(
                    select * from authorlists as al
                    where '%s' = al.author_id
                    and  al.article_id = articles.id
                )
            ''' % author
        if article:
            sql += '''
            and exists(
                select * from bibliographies as b
                where '%s' = b.reference_id
                and
                b.article_id = articles.id
            )
            ''' % article
        if limit:
            sql += 'limit %s' % limit
        if offset:
            sql += 'offset %s' % offset
        return articles

    def save(self):
        self.__save__()
