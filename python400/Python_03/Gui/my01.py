from tkinter import *
from tkinter import messagebox


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.label02 = None
        self.entry01 = None
        self.label01 = None
        self.entry02 = None
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.label01 = Label(self, text='用户名')
        self.label01.pack()
        # Stringvar 变量绑定到指定的组件
        v1 = StringVar()
        self.entry01 = Entry(self, textvariable=v1)
        self.entry01.pack()

        self.label02 = Label(self, text='密码')
        self.label02.pack()
        # Stringvar 变量绑定到指定的组件
        v2 = StringVar()
        self.entry02 = Entry(self, textvariable=v2, show='*')
        self.entry02.pack()

        Button(self, text='登录', command=self.login).pack()

    def login(self):
        username = self.entry01.get()
        pwd = self.entry02.get()
        print(f'用户名:{username}')
        print(f'密码:{pwd}')
        if username == 'qw' and pwd == '123':
            messagebox.showinfo("登录界面", '登陆成功')
        else:
            messagebox.showinfo("登录界面", '登录失败,用户名或者密码错误！')


if __name__ == '__main__':
    root = Tk()
    root.geometry('600x230+200+300')
    app = Application(master=root)
    root.mainloop()
