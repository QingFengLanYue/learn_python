class cs:
    def __init__(self,name):
        self.name = name
    def cs1(self):
        print("hello words %s" %self.name)
    def cs2(self):
        pass

if __name__ == '__main__':
    b=cs('rob')
    b.cs1()
    b.name='www'
    b.cs1()
    b.cs2()


