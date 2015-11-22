from structure.FileHandler import FileHandler


class Models(object):
    __fields__ = ["id", ]
    __page__ = 0

    def __model__(self, data):
        # inserts data into the model
        # data - a list of data
        i = 0
        for field in self.__fields__:
            if i < len(data):
                self.__setattr__(field, data[i])
            else:
                self.__setattr__(field, None)
            i += 1

    @classmethod
    def __getData__(cls):
        # gets the data from file in list
        # TODO storage name should be defined in conf file
        storage = FileHandler("data")
        dataIterator = storage.read_page()
        data = []

        data = dataIterator.next()
        i = 0
        while ((i < len(data)) and (data[i] != cls.__name__)):
            i += 2
        if i >= len(data):
            print ("\n ERROR:table \""
                   "%s \" was not declared in this scope\n"
                   % cls.__name__)
            return
        cls.__page__ = int(data[i+1])
        data = storage.read_page(int(data[i+1])).next()
        return data

    @classmethod
    def __get__(cls, **kwargs):
        # returns filtered data as a list of instances
        data = cls.__getData__()
        instances = []
        for i in range(len(data)/len(cls.__fields__)):
            instance = cls()
            instance.__model__(data[len(cls.__fields__)*i:])
            instances.append(instance)
        for key in kwargs.keys():
            instances = filter(
                lambda x: x.__getattribute__(key) == kwargs[key],
                instances
            )
        return instances

    def __save__(self):
        # inserts an instance into file
        # or updates existing tuple if instance's id is specified
        # and it exists in file
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
