class FileHandler(object):
    page_size = 10  # symbols

    def __init__(self, name):
        self.url = "data/"+name+".txt"
        with open(self.url, buffering=10) as f:
            self.page_size = int(f.read().split()[0])

    def __repr__(self):
        return self.url

    def read_page(self, _offset=0):
        offset = len(self.page_size.__str__())+1+_offset*self.page_size
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
                            ]
                        )
                    yield res

    def write_page(self, data, page_number=0):
        metaData = []
        pos = 0
        for i in range(0, len(data)):
            metaData.append(pos)
            metaData.append(len(data[i]))
            pos += len(data[i])
        data = ''.join(data)
        metaData = " "+' '.join([str(i) for i in metaData])
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
