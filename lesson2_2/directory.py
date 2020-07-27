import os

class Simpledb:
    def __init__(self, filename, key, value):
        self.filename = filename
        self.key = key
        self.value = value
    def __repr__(self):
        return ('<' + self.__class__.__name__ +
        ' filename=' + str(self.filename) +
        ' key=' + str(self.key) +
        ' value=' + str(self.value) +
        '>')
    def insert(self):
        f = open(self.filename, 'a')
        f.write(self.key + '\t' + self.value + '\n')
        f.close
    def select_one(self):
        f = open(self.filename, 'r')
        for row in f:
            (k, v) = row.split('\t', 1)
            if k == self.key:
                return v[:-1]
        f.close()
    def delete(self):
        f = open(self.filename, 'r')
        result = open('result.txt.', 'w')
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k != self.key:
            result.write(row)
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.filename)
    def update(self):
        f = open(self.filename, 'r')
        result = open('result.txt', 'w')
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                result.write(key + '\t' + self.value + '\n')
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.filename)
