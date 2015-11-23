class FileHandler(object):
    page_size = 10  # 10 symbols in file for page_size

    def __init__(self, name):
        self.url = "data/"+name+".txt"
        with open(self.url, buffering=10) as f:
            self.page_size = int(f.read().split()[0])

    def __repr__(self):
        return self.url

    def read_page(self, _offset=0):
        assert type(_offset) is int, "page number is not an integer: %r" % _offset
        offset = len(self.page_size.__str__())+1+int(_offset)*int(self.page_size)
        tmp = 1
        while tmp:
            with open(self.url, buffering=self.page_size) as f:
                f.seek(offset)
                offset += self.page_size
                tmp = f.read(self.page_size)
                if tmp:
                    metaData = tmp.split()[1:]
                    data = ''.join(tmp.split()[:1])
                    res = []
                    for i in range(len(metaData)/2):
                        res.append(
                            data[
                                int(metaData[2*i]):
                            ][
                                :int(metaData[2*i+1])
                            ].replace("\s"," ")
                        )
                    yield res

    def write_page(self, data, page_number=0, __blank__=False):
        metaData = []
        pos = 0
        for i in range(0, len(data)):
            metaData.append(pos)
            data[i] = str(data[i]).replace(" ","\s")
            metaData.append(len(data[i]))
            pos += len(data[i])
        data = ''.join(data)
        if (not __blank__) and (data):
            metaData = " "+' '.join([str(i) for i in metaData])
        else:
            metaData = ""
        offset = len(self.page_size.__str__())+1
        if len(data)+len(metaData) < self.page_size:
            while len(data)+len(metaData) < self.page_size:
                data += " "
            with open(self.url, "r+", buffering=self.page_size) as f:
                f.seek(page_number*self.page_size+offset)
                f.write(data+metaData)
        else:
            # TODO: should handle cases when the data is larger than a page_size
            pass
