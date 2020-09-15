import math
import random
from backend.orderDB import conn
equityNames = list(('Apple', 'Microsoft', 'IBM', 'Xerox', 'Pixar'))


# the equities class
class equity:
    # constructor for the equity objects
    def __init__(self, name, price, batchSize, trend, isin):
        self.name = name
        self.price = price
        self.batchSize = batchSize
        self.trend = bool(trend)
        self.isin = isin

    def PrintAtrributes(self):
        print(self.name + ' ' + self.price + ' ' + self.batchSize + ' ' + self.trend)

    # to be called when a transaction is performed to update the spot price
    def UpdatePrice(self, newPrice):
        self.price = newPrice

    # function to be called when a new order is generated
    # decreases the remaining batch size
    # when batch depleted generates a pseudorandom batch size and randomly changes the trend
    def DecrementBatchSize(self):
        if self.batchSize > 1:
            self.batchSize = self.batchSize - 1
        else:
            self.batchSize = random.randint(3, 10)
            self.trend = random.getrandbits(1)


equityCursor = conn.cursor()

# creating the list of the equity objects
equityList = list()
equityList.append(equity('Apple', 700, 5, 1, 'APPLE1984'))
equityCursor.execute('''INSERT INTO Securities_Index values(?, ?, ?, ?);''', ('APPLE1984', 'Apple', 'Stock', 700))
conn.commit()
equityList.append(equity('Microsoft', 500, 4, 1, 'MIC1990'))
equityCursor.execute('''INSERT INTO Securities_Index values(?, ?, ?, ?);''', ('MIC1990', 'Microsoft', 'Stock', 500))
conn.commit()
equityList.append(equity('IBM', 350, 5, 0, 'IBM1950'))
equityCursor.execute('''INSERT INTO Securities_Index values(?, ?, ?, ?);''', ('IBM1950', 'IBM', 'Stock', 350))
conn.commit()
equityList.append(equity('Xerox', 200, 3, 0, 'XER1960'))
equityCursor.execute('''INSERT INTO Securities_Index values(?, ?, ?, ?);''', ('XER1960', 'Xerox', 'Stock', 200))
conn.commit()
equityList.append(equity('Pixar', 550, 7, 1, 'PIX1991'))
equityCursor.execute('''INSERT INTO Securities_Index values(?, ?, ?, ?);''', ('PIX1991', 'Pixar', 'Stock', 550))
conn.commit()

# function to retrieve the attributes of a particular equity
def GetEquityAttributes(find):
    resultList = list()
    for i in equityList:
        if i.name == find:
            resultList.append(i.price)
            resultList.append(i.batchSize)
            resultList.append(i.trend)
            return resultList


# function to decrement the batch size of the equity when a new order is generated
def UpdateBatchSize(find):
    for i in equityList:
        if i.name == find:
            i.DecrementBatchSize()
            break


# function to update equity price when trade occurs
def UpdateEquityPrice(find, newPrice):
    for i in equityList:
        if i.name == find:
            i.UpdatePrice(newPrice)
            break


def GetRandomPrice(find):
    for i in equityList:
        if i.name == find:
            minLimit = 0.9 * i.price
            maxLimit = 1.1 * i.price
            m = math.ceil(minLimit / 0.05)
            n = math.floor(maxLimit / 0.05)
            resultPrice = (random.randint(m, n) * 0.05)
            resultPrice = float("{:.2f}".format(resultPrice))
            return resultPrice
