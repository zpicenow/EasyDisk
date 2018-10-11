#coding:utf-8 
#
import os,os.path,time
import tkinter
import tkinter.messagebox
import threading

p_file=[]

class Window:
    def __init__(self):
        self.root = tkinter.Tk()

        menu = tkinter.Menu(self.root)
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="关于...",command = self.MenuAbout)
        submenu.add_separator() 
        submenu.add_command(label="退出", command = self.MenuExit)
        menu.add_cascade(label="系统", menu=submenu)

        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="扫描垃圾文件", command = self.MenuScanRubbish )
        submenu.add_command(label="删除垃圾文件", command = self.MenuDelRubbish)
        menu.add_cascade(label="清理", menu=submenu)

        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="扫描大文件", command = self.MenuScanBigFile)  
        submenu.add_separator()             
        submenu.add_command(label="查找文件", command = self.MenuSearchFile)
        menu.add_cascade(label="查找", menu=submenu)

        self.root.config(menu=menu)
        
        self.progress = tkinter.Label(self.root,anchor = tkinter.W,text = '状态',bitmap = 'hourglass',compound = 'left')
        self.progress.place(x=10,y=370,width = 480,height = 15)


        #列表框，显示文件列表
        self.flist = tkinter.Listbox(self.root)
        self.flist.place(x=10,y = 10,width = 480,height = 350)
        
        #为列表框添加垂直滚动条
        self.vscroll = tkinter.Scrollbar(self.flist)
        self.vscroll.pack(side = 'right',fill = 'y')
        self.flist['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.flist.yview

    def MainLoop(self):
        self.root.title("Window“减肥”")
        self.root.minsize(500,400)
        self.root.maxsize(500,400)
        self.root.mainloop()

    #“关于”菜单
    def MenuAbout(self):
        tkinter.messagebox.showinfo("PyOptimize","这是使用Python编写的Windows优化程序。\n欢迎使用并提出宝贵意见！")


    #"退出"菜单
    def MenuExit(self):
        self.root.quit();
    
    #"扫描垃圾文件"菜单
    def MenuScanRubbish(self):
        result = tkinter.messagebox.askquestion("提示","扫描垃圾文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        self.drives =GetDrives()
        t=threading.Thread(target=self.ScanRubbish,args=(self.drives,))
        t.start()


    #"删除垃圾文件"菜单
    def MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("提示","删除垃圾文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("PyOptimize","马上开始删除垃圾文件！")
        self.DelRubbish()
    
    #"扫描大文件"菜单
    def MenuScanBigFile(self):
        result = tkinter.messagebox.askquestion("提示","扫描大文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("PyOptimize","马上开始扫描大文件！")
        #文件大小参考《Python标准库》P202(6.1.4)
    
    #"查找文件"菜单
    def MenuSearchFile(self):
        result = tkinter.messagebox.askquestion("提示","查找文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("PyOptimize","马上开始查找文件！")
        #文件时间参考《Python标准库》P202(6.1.4)
    
    def ScanRubbish(self,scanpath):
        filenumber = 0; #文件数量
        filesize = 0;   #文件大小
        for drive in scanpath:
            for root,dirs,files in os.walk(drive):
                for file in files:
                    try:
                        fname = os.path.join(os.path.abspath(root),file)
                        l = len(fname)
                        if l>60:
                            self.progress['text'] = fname[:30] + '...' + fname[l-30:l]
                        else:
                            self.progress['text'] = fname
                        filenumber += 1
                        filesize += os.path.getsize(fname)
                    except:
                        pass
        self.flist.insert(tkinter.END,"文件数量:"+str(filenumber))
        self.flist.insert(tkinter.END,"文件大小:"+str(filesize))


    def DelRubbish(self):
        pass
    
    def AddStrToEdit(self,s):
        pass
        #self.edit.insert(tkinter.END, 
        #title_small + twitter['message']+'\n')

    def threadtest(self):
        p_file.append("1")
        p_file.append("2")
        time.sleep(5)

#取得当前计算机的盘符
def GetDrives():
    drives=[]
    for i in range(65,91):
        vol = chr(i) + ':/'
        if os.path.isdir(vol):
            drives.append(vol)
    return tuple(drives)

if __name__ == "__main__" :
    window = Window()
    window.MainLoop()



'''
如果不使用这个方法,遍历同样能达到效果.不过使用 os.walk 方便很多了.这个方法返回的是一个三元tupple(dirpath, dirnames, filenames),
其中第一个为起始路径，
第二个为起始路径下的文件夹,
第三个是起始路径下的文件.
dirpath是一个string，代表目录的路径,
dirnames是一个list，包含了dirpath下所有子目录的名字,
filenames是一个list，包含了非目录文件的名字.这些名字不包含路径信息,如果需要得到全路径,需要使用 os.path.join(dirpath, name).


下面是我是自己用递归实现的遍历文件方法.
代码:
def listdir(leval,path):
    for i in os.listdir(path):
        print('|  '*(leval + 1) + i) 
        if os.path.isdir(path+i):
            listdir(leval+1, path+i)

path = 'c:'+os.sep+'ant'
#或者直接 path='C:/ant' 
print(path+os.sep)
listdir(0, path+os.sep)

'''