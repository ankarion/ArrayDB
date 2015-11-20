class BPlusTree(object):

    def __init__(self, file="treeName.txt"):
        self.file = file
        file = open("data/{0}".format(file), "r")
        self.line = '\n'.join(file.readlines())
        file.close()

    def fromFile(self, tmp):
        line = self.line
        idpos = 0
        metaData = line.split()[1:]
        localLine = ''.join(line.split()[:1])
        if metaData:
            def d(x, y):
                return ''.join(
                    localLine[
                        int(metaData[x]):
                    ][
                        :int(metaData[y])
                    ]
                )
            while idpos+3 < len(metaData):
                tmp.insert(int(d(idpos, idpos+1)), d(idpos+2, idpos+3))
                idpos += 4
            return tmp

    def save(self, bPlusTree):
        metadata = []
        data = []
        pos = 0
        for i in bPlusTree.keys():
            metadata.append(pos)
            metadata.append(len(i.__str__()))
            pos += len(i.__str__())
            data.append(i.__str__())

            metadata.append(pos)
            metadata.append(len(bPlusTree.get(i).__str__()))
            pos += len(bPlusTree.get(i).__str__())
            data.append(bPlusTree.get(i).__str__())
        res = ''.join(data) + ' ' + ' '.join([str(i) for i in metadata])
        file = open("data/{0}".format(self.file), "w")
        file.writelines(res)
        file.close()
