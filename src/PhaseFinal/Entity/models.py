from structure.FileHandler import FileHandler


class Models(object):
    __fields__ = ["id", ]
    __page__ = 0

    def __model__(self, data):
        i = 0
        for field in self.__fields__:
            if i < len(data):
                self.__setattr__(field, data[i])
            else:
                self.__setattr__(field, None)
            i += 1

    @classmethod
    def __getData__(cls):
        # TODO storage name should be defined in conf file
        storage = FileHandler("data")
        dataIterator = storage.read_page()
        data = []

        data = dataIterator.next()
        i = 0
        while (data[i] != cls.__name__):
            i += 2
        cls.__page__ = int(data[i+1])
        data = storage.read_page(int(data[i+1])).next()
        return data

    def __save__(self):
        storage = FileHandler("data")
        data = self.__getData__()
        instances = []
        lastID = 0
        print data
        for i in range(0, len(data)/len(self.__fields__)):
            instance = self.__class__()
            instance.__model__(data[i*len(self.__fields__):])
            instances.append(instance)
            if int(instance.id) > lastID:
                lastID = int(instance.id)
        if not hasattr(self, "id"):
            self.id = lastID+1
            instances.append(self)
        else:
            for i in instances:
                if (i.id == self.id):
                    i = self
                    break
        newData = []
        for instance in instances:
            newData.extend([
                instance.__getattribute__(j) for j in self.__fields__
            ])
        print newData
        storage.write_page(newData, self.__page__)
