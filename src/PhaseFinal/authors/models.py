from Entity.models import Models


class Authors(Models):
    __fields__ = ["id", "name"]

    def all(self):
        authors = self.get()
        return authors

    @classmethod
    def get(cls, article=None, **kwargs):
        if article:
            pass
        authors = cls.__get__(**kwargs)
        return authors

    def save(self):
        self.__save__()
