import pandas as pd


class ReadData:
    def __init__(self, file_name, **kwargs):
        self.file_name = 'data/' + file_name
        self.sep = kwargs.get('sep', False)
        self.columns = kwargs.get('columns', False)

    def read_txt(self):
        print(self.file_name, self.sep, self.columns)
        reader = pd.read_csv(self.file_name, sep=self.sep, dtype=str, header=None, engine='python')
        reader.columns = self.columns
        return reader

    def read_csv(self):
        reader = pd.read_csv(self.file_name, dtype=str)
        return reader

    def read_excel(self):
        reader = pd.read_excel(self.file_name, sheet_name='Sheet1')
        reader = reader.fillna(method='pad')
        return reader

    def read_database(self):
        pass

    def read_check(self):
        if self.file_name.endswith('.txt'):
            print('解析 txt')
            return self.read_txt()
        elif self.file_name.endswith('.csv'):
            print('解析 csv')
            return self.read_csv()
        elif self.file_name.endswith('.excel'):
            print('解析 excel')
            return self.read_excel()


def file_deal(file_name, sep=None, columns=None):
    read = ReadData(file_name, sep=sep, columns=columns)
    return read.read_check()


x = file_deal('localtion.txt', sep='!#~', columns=columns)
print(x)
