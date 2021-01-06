import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
#from PIL import Image, ImageTk
from tkinter.simpledialog import askfloat,askinteger,askstring
from pandas.core.frame import DataFrame
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse, Circle


class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=400,height=300)
        self.pack()
        self.master = master

        self.var_init()

        #self.canvas = tk.Canvas()

        self.bt1 = tk.Button(master,text="加载数据",command=self.load_data,width=12)
        self.bt1.place(x=20,y=15)

        self.bt2 = tk.Button(master,text="计算",command=self.deal_data,width=12)
        self.bt2.place(x=120,y=15)

        self.bt5 = tk.Button(master,text="设置完毕\n点此继续",command=self.disp_cur,width=20,height=3)
        self.bt5.place(x=700,y=300)

        self.entry1 = tk.Entry(master,width=8)
        self.entry1.place(x=700,y=100)

        self.entry2 = tk.Entry(master,width=8)
        self.entry2.place(x=800,y=100)

        #self.bt3 = tk.Button(master,text="确定",command=self.update_fre,width=8)
        #self.bt3.place(x=750,y=130)

        self.label1 = tk.Label(master,text = '显示设置')
        self.label1.place(x=750,y=70)

        self.entry3 = tk.Entry(master,width=8)
        self.entry3.place(x=700,y=130)

        self.entry4 = tk.Entry(master,width=8)
        self.entry4.place(x=800,y=130)

        self.bt4 = tk.Button(master,text="确定",command=self.update_bof,width=8)
        self.bt4.place(x=750,y=160)

        #self.label2 = tk.Label(master,text = '设置范围')
        #self.label2.place(x=750,y=180)

        self.scale1 = tk.Scale(master,from_=2,to=100,orient=tk.HORIZONTAL,command=self.mod_linenum,width=10)
        self.scale1.set(50)
        self.scale1.place(x=750,y=200)
        
        self.label2 = tk.Label(master,text = '级别')
        self.label2.place(x=700,y=218)
        
        self.label3 = tk.Label(master,text = '频率')
        self.label3.place(x=670,y=100)

        self.label4 = tk.Label(master,text = '波数')
        self.label4.place(x=670,y=130)

        self.bt6 = tk.Button(master,text="添加模态",command=self.add_modal,width=12)
        self.bt7 = tk.Button(master,text="完成",command=self.set_done,width=12)
        self.bt8 = tk.Button(master,text="删除",command=self.del_modal,width=8)

        self.bt9 = tk.Button(master,text="导出数据",command=self.export_data,width=12)
        self.bt10 = tk.Button(master,text="加载数据",command=self.reload,width=12)

        self.label_author = tk.Label(master,text = '作者：Jazzie \n Email：jazzie@qq.com \n沈阳建筑大学 岳国栋副教授课题组')
        self.label_author.place(x=700,y=400)
        

        self.modal_list = tk.Listbox(master,width = 12)


        #self.bt6.place(x=20,y=15)

        #self.canvas_width = 700
        #self.canvas_height = 600
        #self.img_canvas = tk.Canvas(master,width=self.canvas_width,height=self.canvas_height,bg='white')

        #self.img_canvas.place(x=20,y=50)

    def var_init(self):
        self.origin_data = None
        self.Fs = None
        self.bof = None
        self.ori_w = None
        self.ori_h = None
        self.data_fft2_sh = None
        self.cur_img = None
        self.state_flag = 0
        self.f = None
        self.data_set_group = []
        self.data_set_xygroup = []
        self.data_set = []
        self.data_set_x = []
        self.data_set_y = []
        self.data_set_x_group = []
        self.data_set_y_group = []
        self.modal_index = 0

    def window1_init(self):
        
        self.var_init()

        if self.f is not None:
            plt.clf()
            self.canvas.draw()
            
        self.bt1.place(x=20,y=15)
        self.bt2.place(x=120,y=15)
        self.bt5.place(x=700,y=300)
        self.entry1.place(x=700,y=100)
        self.entry2.place(x=800,y=100)
        self.entry3.place(x=700,y=130)
        self.entry4.place(x=800,y=130)
        self.bt4.place(x=750,y=160)
        self.scale1.place(x=750,y=200)
        self.label1.place(x=750,y=70)
        self.label2.place(x=700,y=218)
        self.label3.place(x=670,y=100)
        self.label4.place(x=670,y=130)
        
        self.bt6.place_forget()
        self.bt8.place_forget()
        self.bt9.place_forget()
        self.bt7.place_forget()
        self.bt10.place_forget()
        self.modal_list.place_forget()
        self.modal_list.delete(0,'end')

    def window2_init(self):
        #self.canvas.place_forget()
        self.bt1.place_forget()
        self.bt2.place_forget()
        #self.bt3.place_forget()
        self.bt4.place_forget()
        self.bt5.place_forget()
        self.entry1.place_forget()
        self.entry2.place_forget()
        self.entry3.place_forget()
        self.entry4.place_forget()
        self.scale1.place_forget()
        self.label1.place_forget()
        self.label2.place_forget()
        self.label3.place_forget()
        self.label4.place_forget()
        
        self.bt6.place(x=20,y=15)
        self.bt8.place(x=800,y=100)
        self.bt9.place(x=120,y=15)
        self.bt10.place(x=220,y=15)
        self.modal_list.place(x=700,y=100)

        
    
    def load_data(self):

        
        
        data_path = filedialog.askopenfilename(filetypes=[('XLSX','xlsx')])
        if data_path != '':
            self.var_init()
            if self.f is not None:
                plt.clf()
                self.canvas.draw()

            self.origin_data = pd.read_excel(data_path,'Sheet1')
            print(self.origin_data.shape)
            messagebox.showinfo("Message","加载成功！")

    def deal_data(self):
        while self.Fs == None:
            self.Fs = askinteger("Message", "时间采样率(Hz)", minvalue=-9999999999, maxvalue=9999999999)
            if self.Fs == None:
                messagebox.showinfo("Warning","输入为空")
                
        while self.bof == None:
            self.bof = askinteger("Message", "空间采样率(1/m)", minvalue=-9999999999, maxvalue=9999999999)
            if self.bof == None:
                messagebox.showinfo("Warning","输入为空")
        try:
            self._2dfft()
        except:
            messagebox.showinfo("Warning","输入数据错误，请重新导入")
            return
        self.cur_img = self.data_fft2_sh
        self.create_img(self.cur_img)

    def _2dfft(self):
        #print(self.origin_data)
        data_fft2 = np.fft.fft2(self.origin_data)
        data_fft2_sh = abs(np.fft.fftshift(data_fft2)).T
        w,h = data_fft2_sh.shape
        data_fft2_sh = data_fft2_sh[w//2:,:h//2]
        self.data_fft2_sh = np.fliplr(data_fft2_sh)
        self.ori_w,self.ori_h = self.data_fft2_sh.shape

    def create_img(self,img_data):

        w,h = img_data.shape
        self.axisx = (np.linspace(0,1,self.ori_h)*self.Fs/2)[0:h]
        self.axisy = (np.linspace(0,1,self.ori_w)*np.pi*self.bof)[0:w]
        X,Y = np.meshgrid(self.axisx,self.axisy)
        self.f = plt.figure(figsize=(6.4,4.8),dpi=100)
        
        C = plt.contour(X,Y,img_data,self.scale1.get(),color='black',linewidth=1)
        #plt.plot([2,300000,9],[10,20,30])

             
        self.canvas = FigureCanvasTkAgg(self.f,self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=20,y=50)

        #toolbar =NavigationToolbar2Tk(self.canvas, self.master)
        #toolbar.update()
        #self.canvas._tkcanvas.place(x=20,y=50)
        
        cid = self.f.canvas.mpl_connect('button_press_event', self.onclick)
        
    def update_img(self,img_data):
        
        w,h = img_data.shape
        self.axisx = (np.linspace(0,1,self.ori_h)*self.Fs/2)[0:h]
        self.axisy = (np.linspace(0,1,self.ori_w)*np.pi*self.bof)[0:w]
        X,Y = np.meshgrid(self.axisx,self.axisy)
        plt.clf()
        C = plt.contour(X,Y,img_data,self.scale1.get(),color='black',linewidth=1)

        if len(self.data_set_x_group) != 0:
            for index in range(len(self.data_set_x_group)):
                plt.plot(self.data_set_x_group[index],self.data_set_y_group[index])
                plt.scatter(self.data_set_x_group[index],self.data_set_y_group[index])

        if len(self.data_set_x) != 0:
            plt.plot(self.data_set_x,self.data_set_y)
            plt.scatter(self.data_set_x,self.data_set_y)
            
        self.canvas.draw()
        

    def update_fre(self):
        #try:
        #    min_fre = int(self.entry1.get())
        #    max_fre = int(self.entry2.get())
        #except:
        #    messagebox.showinfo("Warning","请输入整数")

        #print(min_fre,max_fre,self.data_fft2_sh.shape)
        #print(min_fre//self.Fs*2*2//self.Fs,max_fre//self.Fs*2*2//self.Fs)

        #self.cur_img = self.data_fft2_sh[:,round(min_fre*2/self.Fs*self.ori_h):round(max_fre*2/self.Fs*self.ori_h)]
        #self.update_img(self.cur_img)
        pass

    def update_bof(self):
        try:
            min_fre = int(self.entry1.get())
            max_fre = int(self.entry2.get())
            min_bof = int(self.entry3.get())
            max_bof = int(self.entry4.get())
        except:
            messagebox.showinfo("Warning","请输入整数")
        self.cur_img = self.data_fft2_sh[round(min_bof/np.pi/self.bof*self.ori_w):round(max_bof/np.pi/self.bof*self.ori_w),round(min_fre*2/self.Fs*self.ori_h):round(max_fre*2/self.Fs*self.ori_h)]
        self.update_img(self.cur_img)
        
    def mod_linenum(self,pos):
        if self.cur_img is not None:
            self.update_img(self.cur_img)

    def disp_cur(self):
        self.state_flag = 1
        self.window2_init()


    def onclick(self,event):
        
        if self.state_flag == 1:
            pass
            #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %(event.button, event.x, event.y, event.xdata, event.ydata))
        if self.state_flag == 2:
            if event.xdata is not None and event.ydata is not None:
                self.data_set_x.append(event.xdata)
                self.data_set_y.append(event.ydata)
                self.data_set.append((event.xdata,event.ydata))
                self.update_img(self.cur_img)
            
            
        
    def add_modal(self):
        self.state_flag = 2
        self.bt6.place_forget()
        self.bt7.place(x=20,y=15)

    def set_done(self):
        self.state_flag = 1
        
        self.bt7.place_forget()
        self.bt6.place(x=20,y=15)

        self.data_set_x_group.append(self.data_set_x)
        self.data_set_y_group.append(self.data_set_y)

        self.data_set_x = []
        self.data_set_y = []

        self.data_set_group.append(self.data_set)
        self.data_set = []

        self.modal_index += 1
        modal_name = "模态"+str(self.modal_index)
        self.modal_list.insert('end',modal_name)

    def del_modal(self):

        if len(self.data_set_group) == 0:
            return

        del_index = self.modal_list.curselection()[0]
        print(del_index)
        del self.data_set_x_group[del_index]
        del self.data_set_y_group[del_index]
        del self.data_set_group[del_index]
        self.modal_list.delete(del_index)
        
        self.update_img(self.cur_img)

    def export_data(self):

        if len(self.data_set_group) == 0:
            messagebox.showinfo("Message","无模态输出")
            return

        csv_path = filedialog.asksaveasfilename(filetypes=[('CSV','csv')])
        frame_list = []
        for dotlist in self.data_set_group:
            data = DataFrame(dotlist)
            data = data
            frame_list.append(data)
        frame = frame_list[0]
        for i in range(len(frame_list)):
            if i >=1:
                frame = pd.concat([frame,frame_list[i]],axis=1)

        frame.to_csv (csv_path+'.csv' , encoding = "utf-8")

        frame_result = pd.DataFrame(data=self.data_fft2_sh)
        frame_result.to_csv(csv_path+'result'+'.csv' , encoding = "utf-8")

    def reload(self):
        self.window1_init()
        self.load_data()

        

    def display(self):
        pass
        
            
if __name__=='__main__':
    #matplotlib.use('TkAgg')
    root = tk.Tk()
    root.title('Draw Dispersion Curve')
    root.geometry('900x600')
    root.resizable(0,0)
    app = App(root)
    root.mainloop()
