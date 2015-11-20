class Employee(object):
    i = 0

    def __init__(self, name="", address="", designation="", file="Employee.txt"):
        file = open("data/{0}".format(file), "r")
        self.line = '\n'.join(file.readlines())
        file.close()

        Employee.i += 1
        self.name = name
        self.nameHash = hash(name)
        self.address = address
        self.addressHash = hash(address)
        self.designation = designation
        self.designationHash = hash(designation)
        self.id = Employee.i

    def countHash(self):
        self.nameHash = hash(self.name)
        self.addressHash = hash(self.address)
        self.designationHash = hash(self.designation)

    def __getitem__(self, idpos):
        line = self.line
        idpos *= 8
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
            tmp = Employee()
            tmp.id = d(idpos, idpos+1)
            tmp.name = d(idpos+2, idpos+3)
            tmp.nameHash = hash(tmp.name)
            tmp.address = d(idpos+4, idpos+5)
            tmp.addressHash = hash(tmp.address)
            tmp.designation = d(idpos+6, idpos+7)
            tmp.designationHash = hash(tmp.designation)
            return tmp

    def __str__(self):
        return (
            "id=" + self.id +
            "; name=" + self.name +
            "; address=" + self.address +
            "; designation=" + self.designation
        )


class EmployeeHashTree(object):
    table = dict()

    def add(self, element):
        self.fileName = element.file
        self.table.setdefault(
            element.nameHash, dict()
        ).setdefault(
            element.addressHash, dict()
        ).setdefault(
            element.designationHash, []
        ).append(element)

    def getByName(self, name):
        nameHash = hash(name)
        res = []
        for i in self.table.get(nameHash, {}).values():
            for j in i.values():
                for z in j:
                    res.append(z)
        return res

    def getByAddress(self, address):
        addressHash = hash(address)
        res = []
        for i in self.table.values():
            for j in i.get(addressHash, {}).values():
                for z in j:
                    res.append(z)
        return res

    def getByDesignation(self, designation):
        designationHash = hash(designation)
        res = []
        for i in self.table.values():
            for j in i.values():
                for z in j.get(designationHash, []):
                    res.append(z)
        return res

    def save(self):
        data = []
        metadata = []
        pos = 0
        for i in self.table.values():
            for j in i.values():
                for z in j.values():
                    for k in z:
                        metadata.append(pos)
                        metadata.append(len(k.id.__str__()))
                        pos += len(k.id.__str__())
                        data.append(k.id.__str__())
                        metadata.append(pos)
                        metadata.append(len(k.name.__str__()))
                        pos += len(k.name)
                        data.append(k.name)
                        metadata.append(pos)
                        metadata.append(len(k.address.__str__()))
                        pos += len(k.address)
                        data.append(k.address)
                        metadata.append(pos)
                        metadata.append(len(k.designation.__str__()))
                        pos += len(k.designation)
                        data.append(k.designation)
        res = ''.join(data) + ' ' + ' '.join([str(i) for i in metadata])
        file = open("data/{0}".format(self.fileName), "w")
        file.writelines(res)
        file.close()

    def delete(self, element):
        condidates = self.table[element.nameHash][element.addressHash][element.designationHash]
        if element in condidates:
            condidates.remove(element)
