from pymongo import MongoClient

conn = MongoClient('localhost', 27017)


class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def save_data(self):
        db = conn.gittrend
        db.col.remove()
        for data in self.datas:
            db.col.insert(data)
