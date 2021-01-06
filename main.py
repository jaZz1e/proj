import tkinter as tk

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=40,height=40)
        self.pack()
        self.master = master
        # self.init_set()

if __name__=='__main__':
    root = tk.Tk()
    root.title('img2data')
    root.geometry('600x600')
    root.resizable(0,0)
    app = App(root)
    root.mainloop()