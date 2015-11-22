from Entity.models import Models

from authors.models import Authors


class Articles(Models):
    __fields__ = ["id", "venue", "year", "title"]

    @classmethod
    def all(self):
        articles = self.get()
        return articles

    @classmethod
    def get(cls, author_id=None, article_id=None,
            limit=None, offset=None,
            **kwargs):
        articles = cls.__get__(**kwargs)
        if author_id:
            authors_articles = AuthorLists.get(id=author_id)
            articles = articles.filter(
                lambda x: x.id in authors_articles,
                articles
            )
        if article_id:
            references = References.get(id=article_id)
            articles = filter(
                lambda x: x.id in references,
                articles
            )
        if offset:
            articles = articles[offset:]
        if limit:
            articles = articles[:limit]
        return articles

    def save(self, **kwargs):
        print kwargs
        self.__save__()

    def authors(self, **kwargs):
        return Authors.get(article=self.id, **kwargs)


class AuthorLists(Models):
    __fields__ = ["article_id", "author_id"]

    @classmethod
    def get(cls, **kwargs):
        return cls.__get__(**kwargs)


class References(Models):
    __fields__ = ["article_id", "reference_id"]

    @classmethod
    def get(cls, **kwargs):
        return cls.__get__(**kwargs)
