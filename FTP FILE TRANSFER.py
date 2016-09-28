#Created by Callibrator
#Using python 3.x
#callibrator21@gmail.com


from tkinter import *
from ftplib import FTP
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring

class ftpclass():
    def __init__(self):
        self.relogin = False
        self.curdata = ''
        self.username = ''
        self.password = ''
        self.host = ''
        self.prevcwd = []
        
    def connect(self,user,passwd,host):
        self.username = user
        self.password = passwd
        self.client = FTP(host)
        self.host = host
        self.relogin = True
        self.client.login(user,passwd)
        self.getcwd()

        
    def getcwd(self):
        self.curdata = self.client.nlst()
        
        
    def relog(self):
        if self.relogin == False:
            showinfo('FTP','You must login at least 1 time to relog')
            return 0
        self.client = FTP(self.host)
        self.client.login(self.username,self.password)
        self.getcwd()
        self.prevcwd = []
        
    def download(self,file):
        local = open(file,'wb')
        self.client.retrbinary('RETR '+file,local.write,1024)
        local.close()
        showinfo('FTP','File succesfully Downloaded')

    def unpload(self):
        file = askopenfilename()        
        name = file.split('/')[-1]
        local = open(file,'rb')
        self.client.storbinary('STOR '+name,local,1024)
        local.close()
        showinfo('FTP','File succesfully unploaded')
    def changecwd(self,dr):
        self.client.cwd(dr)
        self.getcwd()
    def mkdir(self):
        dr = askstring('FTP','Enter the name of the folder')
        try:
          self.client.mkd(dr)
        except:
          showinfo('Error','Unable to create Directory on the remote server')
        
        
root = Tk()
root.title('FTP File Transfer')

global f
f= ftpclass()

conframe = Frame(root)
conframe.pack()

Label(conframe,text='Host: ').pack(side=LEFT)
hosttext = Entry(conframe)
hosttext.pack(side=LEFT)
hosttext.insert(0,'127.0.0.1')

Label(conframe,text='Username: ').pack(side=LEFT)
username = Entry(conframe)
username.pack(side=LEFT)


Label(conframe,text='Password: ').pack(side=LEFT)
password = Entry(conframe,show='*')
password.pack(side=LEFT)



dataframe = Frame(root)
dataframe.pack(expand=YES,fill=BOTH)

data = Listbox(dataframe)
data.pack(side=LEFT,fill=BOTH,expand=YES)

botframe = Frame(root)
botframe.pack()

def conn(host,user,passwd,lst):
    try:
     f.connect(user,passwd,host)
     lst.delete(0,END)
     for i in range(len(f.curdata)):
        lst.insert(i,f.curdata[i])

    except:
       showerror('Error','Somthing didn\'t go well :/')
       
def recon(lst):
    try:
        lst.delete(0,END)
        f.relog()
        for i in range(len(f.curdata)):
            lst.insert(i,f.curdata[i])

    except:
        showerror('Error','Somthing didn\'t go well :/')

def changecwd(dr,lst):
    try:
        lst.delete(0,END)
        f.prevcwd.append(f.client.pwd())
        f.changecwd(dr)
        
        for i in range(len(f.curdata)):
            lst.insert(i,f.curdata[i])
            
    except:
        showerror('Error','Somthing didn\'t go well :/')

def prevcwd(lst):
    try:
        dr = f.prevcwd[-1]
        lst.delete(0,END)
        f.prevcwd.remove(dr)
        f.changecwd(dr)
        
        for i in range(len(f.curdata)):
            lst.insert(i,f.curdata[i])
    except IndexError:
        showerror('Error','You alredy are in the home directory')
            
    except:
        showerror('Error','Somthing didn\'t go well :/')



def unpload(lst):
    try:
       f.unpload()
       f.getcwd()
       lst.delete(0,END)
       for i in range(len(f.curdata)):
           lst.insert(i,f.curdata[i])
    except:
       showerror('Error','Somthing didn\'t go well :/')


def makedir(lst):
    try:
      f.mkdir()
      f.getcwd()
      lst.delete(0,END)
      for i in range(len(f.curdata)):
           lst.insert(i,f.curdata[i])
    except:
      showerror('Error','Somthing didn\'t go well')
       
Button(botframe,text='Download',command=lambda:f.download(data.get(data.curselection(),data.curselection())[0])).pack(side=LEFT)
Button(botframe,text='Unpload',command=lambda:unpload(data)).pack(side=LEFT)
Button(botframe,text='Change CWD',command=lambda:changecwd(data.get(data.curselection(),data.curselection())[0],data)).pack(side=LEFT)
Button(botframe,text='Previus CWD',command=lambda:prevcwd(data)).pack(side=LEFT)
Button(botframe,text='Create Directory',command=lambda:makedir(data)).pack(side=LEFT)
Button(botframe,text='Up Directory',command=lambda:changecwd('..',data)).pack(side=LEFT)
Button(conframe,text='Log in',command=lambda:conn(hosttext.get(),username.get(),password.get(),data)).pack(side=LEFT)
Button(conframe,text='Relog in',command=lambda:recon(data)).pack(side=LEFT)

root.mainloop()
