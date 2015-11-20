from FileHandler import FileHandler


class TablesHandler(object):
    @classmethod
    def createTable(self, model):
        # write a model to the file
        storage = FileHandler("data")
        page = storage.read_page().next()
        page.append(model.__name__)
        storage.write_page(page)

    def updateTable(model):
        # find the model table in file and rewrite it
        pass

    def deleteTable(model):
        # find the model table and delete it
        pass
