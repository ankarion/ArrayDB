
class Student(object):
    i = 0

    def __init__(self, name="", address="", email=""):
        file = open("../data/Student.txt", "r")
        self.line = '\n'.join(file.readlines())
        file.close()

        Student.i += 1
        self.name = name
        self.nameHash = hash(name)
        self.address = address
        self.addressHash = hash(address)
        self.email = email
        self.emailHash = hash(email)
        self.id = Student.i

    def countHash(self):
        self.nameHash = hash(self.name)
        self.addressHash = hash(self.address)
        self.emailHash = hash(self.email)

    def __get__(self, idpos):
        line = self.line
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
            self.id = d(idpos, idpos+1)
            self.name = d(idpos+2, idpos+3)
            self.nameHash = hash(self.name)
            self.address = d(idpos+4, idpos+5)
            self.addressHash = hash(self.address)
            self.email = d(idpos+6, idpos+7)
            self.emailHash = hash(self.email)

    def __str__(self):
        return (
            "id=" + self.id +
            "; name=" + self.name +
            "; address=" + self.address +
            "; email=" + self.email
        )


class StudentHashTree(object):
    table = dict()

    def add(self, element):
        self.table.setdefault(
            element.nameHash, dict()
        ).setdefault(
            element.addressHash, dict()
        ).setdefault(
            element.email, []
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

    def getByDesignation(self, email):
        emailHash = hash(email)
        res = []
        for i in self.table.values():
            for j in i.values():
                for z in j.get(emailHash, []):
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
                        metadata.append(len(k.email.__str__()))
                        pos += len(k.email)
                        data.append(k.email)
        res = ''.join(data) + ' ' + ' '.join([str(i) for i in metadata])
        file = open("Student.txt", "w")
        file.writelines(res)
        file.close()

    def delete(self, element):
        condidates = self.table[element.nameHash][element.addressHash][element.emailHash]
        if element in condidates:
            condidates.remove(element)
