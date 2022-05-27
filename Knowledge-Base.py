from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import PyPDF2
from os import listdir
from os.path import isfile, join
from tkPDFViewer import tkPDFViewer as pdf
import os



root = Tk()
root.title('KB')
root.iconbitmap("icon.ico")
root.geometry("1500x850")



main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)



myCanavas = Canvas(main_frame)
myCanavas.pack(side= LEFT, fill=BOTH, expand=1)

my_scrollbar1 = ttk.Scrollbar(main_frame, orient=VERTICAL, command=myCanavas.yview)
my_scrollbar1.pack(side=RIGHT, fill=Y)

myCanavas.configure(yscrollcommand=my_scrollbar1.set)
myCanavas.bind('<Configure>', lambda e:myCanavas.configure(scrollregion = myCanavas.bbox("all")))

second_frame = Frame(myCanavas)
myCanavas.create_window((0,0), window=second_frame, anchor="nw")

my_frame = Frame(second_frame)
my_frame.grid(row=0,column=1,columnspan=4)
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

first_frame = Frame(second_frame)
first_frame.grid(row=0,column=0,padx=(10,30))

########################################################################################################################
def get_extn(filename):
    return filename[filename.rfind('.') + 1:]


def open_Directory(value):
    extn = get_extn(value)
    if extn == "txt":
        text_file = open(value, 'r', encoding='cp850', errors='ignore')
        stuff = text_file.read()
        my_text.delete("1.0", END)
        my_text.insert(END, stuff)
        text_file.close()

    elif extn == "pdf":
        if value:

            my_text.delete("1.0", END)
            pdf_file = PyPDF2.PdfFileReader(value)
            page = pdf_file.getPage(1)
            page_content = page.extract_text()
            my_text.insert(1.0, page_content)

    else:
        pass


def Select_directory():
    global first_frame
    first_frame.destroy()

    mypath = filedialog.askdirectory(initialdir="D:/Studies", title="Get Directory")
    first_frame = LabelFrame(second_frame, text=mypath, fg="BLUE")
    first_frame.grid(row=0, column=0, padx=(10, 30))
    if mypath:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for index in range(0, len(onlyfiles) ):
            my_text.insert(END, mypath+"/"+onlyfiles[index]+"\n")
            Radiobutton(first_frame, text=onlyfiles[index], variable=File, value=mypath+"/"+onlyfiles[index]).pack(anchor=SW)
        if File:
            open_Directory(File.get())
        Read_btn = Button(second_frame, text="Read File", command=lambda:open_Directory(File.get()))
        Read_btn.grid(row=1 , column=3,pady=20)
        #open_Directory_btn.config(state=DISABLED)
    else:
        pass



def open_file():

    text_file = filedialog.askopenfilename(initialdir="D:/Studies", title="Open Text File",filetypes=(("All","*.*"),("Text File","*.txt"),("PDF File","*.pdf")))
    extn = get_extn(text_file)
    if extn == "txt":
        text_file = open(text_file, 'r',encoding='cp850',errors='ignore')
        stuff = text_file.read()
        my_text.delete("1.0", END)
        my_text.insert(END, stuff)
        text_file.close()

    elif extn == "pdf":
        if text_file:
            my_text.delete("1.0", END)
            pdf_file = PyPDF2.PdfFileReader(text_file)
            page = pdf_file.getPage(0)
            page_content = page.extract_text()
            my_text.insert(1.0, page_content)
    else:
        pass


def save_txt():
    text_file = filedialog.asksaveasfilename(initialdir="D:/Studies", title="Save Text File",filetypes=(("Text File","*.txt"),("All","*.*"),))
    if text_file:
        text_file = open(text_file,'w')
        text_file.write(my_text.get("1.0", END))
        text_file.close()
        my_text.delete(1.0, END)
    else:
        pass



File = StringVar()
File.set("*")






my_text = Text(my_frame, width=40, height=20, font=("Helvetica", 16))
my_scrollbar.config(command= my_text.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)



my_text.pack(pady=20,ipadx=300)



open_btn = Button(second_frame, text="Open File", command=open_file)
open_btn.grid(row=1 , column=0,pady=20,padx=(30,0))

save_btn = Button(second_frame, text="Save File", command=save_txt)
save_btn.grid(row=1 , column=1,pady=20)

open_Directory_btn = Button(second_frame, text="Open Directory",command=Select_directory)
open_Directory_btn.grid(row=1 , column=2,pady=20)




root.mainloop()