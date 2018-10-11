#coding:utf-8 
#file: findfat6.py

import tkinter
import tkinter.messagebox,tkinter.simpledialog
import os,os.path
import threading

rubbishExt=['.tmp','.bak','.old','.wbk','.xlk','._mp','.log','.gid','.chk','.syd','.$$$','.@@@','.~*']

class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        
        #创建菜单
        menu = tkinter.Menu(self.root)

        #创建“系统”子菜单
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="关于...",command = self.MenuAbout)
        submenu.add_separator() 
        submenu.add_command(label="退出", command = self.MenuExit)
        menu.add_cascade(label="系统", menu=submenu)
        
        #创建“清理”子菜单
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="扫描垃圾文件", command = self.MenuScanRubbish)
        submenu.add_command(label="删除垃圾文件", command = self.MenuDelRubbish)
        menu.add_cascade(label="清理", menu=submenu)

        #创建“查找”子菜单
        submenu = tkinter.Menu(menu, tearoff=0) 
        submenu.add_command(label="搜索大文件", command = self.MenuScanBigFile)  
        submenu.add_separator()             
        submenu.add_command(label="按名称搜索文件", command = self.MenuSearchFile)
        menu.add_cascade(label="搜索", menu=submenu)

        self.root.config(menu=menu)
        
        #创建标签，用于显示状态信息
        self.progress = tkinter.Label(self.root,anchor = tkinter.W,
            text = '状态',bitmap = 'hourglass',compound = 'left')
        self.progress.place(x=10,y=370,width = 480,height = 15)

        #创建列表框，显示文件列表
        self.flist = tkinter.Text(self.root)
        self.flist.place(x=10,y = 10,width = 480,height = 350)
        
        #为列表框添加垂直滚动条
        self.vscroll = tkinter.Scrollbar(self.flist)
        self.vscroll.pack(side = 'right',fill = 'y')
        self.flist['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.flist.yview

    #“关于”菜单
    def MenuAbout(self):
        tkinter.messagebox.showinfo("Window“减肥”",
            "这是使用Python编写的Windows优化程序。\n欢迎使用并提出宝贵意见！")

    #"退出"菜单
    def MenuExit(self):
        self.root.quit();

    #"扫描垃圾文件"菜单
    def MenuScanRubbish(self):
        result = tkinter.messagebox.askquestion("Window“减肥”","扫描垃圾文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("Window“减肥”","马上开始扫描垃圾文件！")
        #self.ScanRubbish()
        self.drives =GetDrives()
        t=threading.Thread(target=self.ScanRubbish,args=(self.drives,))
        t.start()

    #"删除垃圾文件"菜单
    def MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("Window“减肥”","删除垃圾文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("Window“减肥”","马上开始删除垃圾文件！")
        self.drives =GetDrives()
        t=threading.Thread(target=self.DeleteRubbish,args=(self.drives,))
        t.start()       
    
    #"搜索大文件"菜单
    def MenuScanBigFile(self):
        s = tkinter.simpledialog.askinteger('Window“减肥”','请设置大文件的大小(M)')
        t=threading.Thread(target=self.ScanBigFile,args=(s,))
        t.start()   
    
    #"按名称搜索文件"菜单
    def MenuSearchFile(self):
        result = tkinter.messagebox.askquestion("Window“减肥”","按名称搜索文件将需要较长的时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("Window“减肥”","马上开始按名称搜索文件！")
    
    #扫描垃圾文件
    def ScanRubbish(self,scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root,dirs,files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] == '':  #若文件无扩展名
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >=0:  #扩展名在垃圾文件扩展名列表中
                                fname = os.path.join(os.path.abspath(root),fil)
                                filesize += os.path.getsize(fname)
                                if total % 15 == 0:
                                    self.flist.delete(0.0,tkinter.END)
                                
                                l = len(fname)
                                if l > 50:
                                    fname = os.name[:25] + '...' + fname[l - 25:l]
                                self.flist.insert(tkinter.END,fname + '\n')
                                self.progress['text'] = fname
                                total += 1  #计数
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass
        self.progress['text'] = "找到 %s 个垃圾文件，共占用 %.2f M 磁盘空间" % (total,filesize/1024/1024)

    #删除垃圾文件
    def DeleteRubbish(self,scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root,dirs,files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] == '':  #若文件无扩展名
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >=0:  #扩展名在垃圾文件扩展名列表中
                                fname = os.path.join(os.path.abspath(root),fil)
                                filesize += os.path.getsize(fname)

                                try:
                                    os.remove(fname)    #删除文件
                                    l = len(fname)
                                    if l > 50:
                                        fname = fname[:25] + '...' + fname[l-25:l]
                                    
                                    if total % 15 == 0:
                                        self.flist.delete(0.0,tkinter.END)

                                    self.flist.insert(tkinter.END,'Deleted '+ fname + '\n')
                                    self.progress['text'] = fname
                                    
                                    total += 1  #计数
                                except:                 #不能删除，则跳过
                                    pass                                
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass
        self.progress['text'] = "删除 %s 个垃圾文件，收回 %.2f M 磁盘空间" % (total,filesize/1024/1024)   
    
    #搜索大文件
    def ScanBigFile(self,filesize):
        total = 0
        filesize = filesize * 1024 * 1024
        for drive in GetDrives():
            for root,dirs,files in os.walk(drive):
                for fil in files:
                    try:
                        fname = os.path.abspath(os.path.join(root,fil))                     
                        fsize = os.path.getsize(fname)

                        self.progress['text'] = fname   #在状态标签中显示每一个遍历的文件
                        if fsize >= filesize:                           
                            total += 1                      
                            self.flist.insert(tkinter.END, '%s，[%.2f M]\n' % (fname,fsize/1024/1024))                           
                    except:
                        pass
        self.progress['text'] = "找到 %s 个超过 %s M 的大文件" % (total,filesize/1024/1024)

    def MainLoop(self):
        self.root.title("Window“减肥”")
        self.root.minsize(500,400)
        self.root.maxsize(500,400)
        self.root.mainloop()

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