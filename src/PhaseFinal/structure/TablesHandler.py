from FileHandler import FileHandler


class TablesHandler(object):
    @classmethod
    def createTable(cls, model):
        # write a model to the file
        storage = FileHandler("data")
        page = []

        # TODO warp in try-except
        page = storage.read_page().next()

        tablePage = len(page)/2 + 1  # 2 is a numer of fields in Table entity
        page.append(model.__name__)
        page.append(tablePage)
        storage.write_page(page)
        storage.write_page(["null", ], tablePage, True)

    @classmethod
    def updateTable(cls, model):
        # find the model table in file and rewrite it
        pass

    @classmethod
    def deleteTable(cls, model):
        # find the model table and delete it
        pass


