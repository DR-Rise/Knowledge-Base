from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import colorchooser
import PyPDF2
from os import listdir
from os.path import isfile, join
from PIL import ImageTk,Image
from tkPDFViewer import tkPDFViewer as pdf
import os
import docx2txt




root = Tk()
root.title('KB')
root.iconbitmap("icon.ico")
root.geometry("1500x850+50+50")


########################################################################################################################
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create Frame for X Scrollbar
sec = Frame(main_frame)
sec.pack(fill=X,side=BOTTOM)



myCanavas = Canvas(main_frame)
myCanavas.pack(side= LEFT, fill=BOTH, expand=1)

x_scrollbar = ttk.Scrollbar(sec,orient=HORIZONTAL,command=myCanavas.xview)
x_scrollbar.pack(side=BOTTOM,fill=X)

my_scrollbar1 = ttk.Scrollbar(main_frame, orient=VERTICAL, command=myCanavas.yview)
my_scrollbar1.pack(side=RIGHT, fill=Y)

myCanavas.configure(yscrollcommand=my_scrollbar1.set)
myCanavas.configure(xscrollcommand=x_scrollbar.set)

myCanavas.bind('<Configure>', lambda e:myCanavas.configure(scrollregion = myCanavas.bbox("all")))

second_frame = Frame(myCanavas)
myCanavas.create_window((0,0), window=second_frame, anchor="nw")

my_frame = Frame(second_frame)
my_frame.grid(row=0,column=1,columnspan=4)
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)


first_frame = Frame(second_frame)
first_frame.grid(row=0,column=0,padx=(10,30))

########################################################################################################################
global Size_Font
global my_fg
global theme
global color_changed
color_changed =False


def color():
    global my_fg
    global color_changed
    my_fg = colorchooser.askcolor()
    color_changed = True




def Font():
    global Size_Font
    global theme
    top = Toplevel()
    top.title("Font")
    top.iconbitmap("font.ico")

    Theme_list = ["Helvetica", "Terminal", "System", "Roman", "Adobe Arabic", "Narkisim"]
    theme = StringVar()
    theme.set("Theme Fonts")
    theme_drop = OptionMenu(top, theme, *Theme_list)
    theme_drop.grid(row=0,column=0,padx=(30,30))


    Size_Font =  Scale(top, from_=8, to=72, orient=HORIZONTAL)
    Size_Font.grid(row=0,column=1, padx=(30,30))

    color_btn = Button(top,text="Pick a Font Color",command=color)
    color_btn.grid(row=0, column=2, padx=(30,30),pady=20)

    edit_btn = Button(top,text=" Edit Font ",command=get_Font)
    edit_btn.grid(row=1, column=0,columnspan=3,ipadx=150, padx=(20, 30), pady=(40,30))


def get_Font():
    global color_changed
    global Size
    global my_fg
    global theme
    Size = str(Size_Font.get())

    if color_changed:
        my_text.config(font=(theme.get(), Size), fg=my_fg[1])
    else:
        my_text.config(font=(theme.get(), Size), fg=my_fg)






#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
global my_img
global my_label
global isExist
global waspdf
waspdf= False
global v2
v2 = Label()
isExist=False
my_img = ImageTk.PhotoImage(Image.open("D:/Studies/img2.jpg"))

my_label = Label(my_frame,image=my_img)



########################################################################################################################
def get_extn(filename):
    return filename[filename.rfind('.') + 1:]

def open_Directory(value):
    global isExist
    global Read_btn
    global my_label
    global v2
    global waspdf
    extn = get_extn(value)
    if extn == "txt":

        my_scrollbar.config(command=my_text.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_text.pack(pady=20,ipadx=300)
        v2.grid_forget()
        my_label.destroy()
        text_file = open(value, 'r', encoding='cp850', errors='ignore')
        stuff = text_file.read()
        my_text.delete("1.0", END)
        my_text.insert(END, stuff)
        text_file.close()
        Read_btn.grid(row=1, column=2, pady=20, ipadx=150)
        print("txt btn")

    elif extn == "docx":
        my_scrollbar.config(command=my_text.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_text.pack(pady=20, ipadx=300)
        v2.grid_forget()
        my_label.destroy()
        stuff = docx2txt.process(value)
        my_text.delete("1.0", END)
        my_text.insert(END, stuff)
        Read_btn.grid(row=1, column=2, pady=20, ipadx=150)
        print("docx btn")



    elif extn == "pdf":
        if value:
            my_text.pack_forget()
            my_label.destroy()
            v1=pdf.ShowPdf()
            v2=v1.pdf_view(second_frame,pdf_location=open(value,"r"),width=77,height=100)
            v2.grid(row=0, column=1, pady=(0,0))
            Read_btn.grid(row=0, column=2,padx=30, pady=20, ipadx=150)
            waspdf = True
            print("pdf btn")

    elif extn == "jpg" or extn =="GIF" or extn =="png" or extn =="svg" or extn =="jpeg":
        if value:
            global my_img
            v2.grid_forget()
            my_label.destroy()
            my_img = ImageTk.PhotoImage(Image.open(value))
            my_label = Label(second_frame, image=my_img)
            my_scrollbar.pack_forget()
            my_text.pack_forget()
            my_label.grid(row=0, column=1)
            Read_btn.grid(row=1, column=1, pady=20, ipadx=150)

            print("jpg btn")



    else:
        pass

########################################################################################################################

def Select_directory():
    global isExist
    global first_frame
    global Read_btn
    global v2
    global my_label
    global waspdf
    mypath = filedialog.askdirectory(initialdir="D:/Studies", title="Get Directory")

    if mypath:
        v2.grid_forget()
        my_label.destroy()
        first_frame.destroy()
        first_frame = LabelFrame(second_frame, text=mypath, fg="BLUE")
        first_frame.grid(row=0, column=0, padx=(10, 30))
        my_text.delete("1.0", END)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for index in range(0, len(onlyfiles) ):
            Radiobutton(first_frame, text=onlyfiles[index], variable=File, value=mypath+"/"+onlyfiles[index]).pack(anchor=SW)
        my_text.insert(END," Select a File ....\n")
        my_text.pack(pady=20, ipadx=300)

        if not isExist:
            Read_btn = Button(second_frame, text="Open File", command=lambda: open_Directory(File.get()))
            Read_btn.grid(row=1 , column=3,pady=20, ipadx=150)
            print("slct dir btn")
            isExist = True

        if waspdf:
            Read_btn.grid(row=1, column=3, pady=20, ipadx=150)
            waspdf=False

        #open_Directory_btn.config(state=DISABLED)
    else:
        pass


########################################################################################################################

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

########################################################################################################################

def save_file():
    text_file = filedialog.asksaveasfilename(initialdir="D:/Studies", title="Save Text File",filetypes=(("Text File","*.txt"),("All","*.*"),))
    if text_file:
        text_file = open(text_file,'w')
        text_file.write(my_text.get("1.0", END))
        text_file.close()
        my_text.delete(1.0, END)
    else:
        pass


########################################################################################################################
File = StringVar()
File.set("*")



Size = '16'
my_fg = "Black"
theme = "Adobe Arabic"

my_text = Text(my_frame, width=40, height=20, font=(theme, Size),fg=my_fg)
my_scrollbar.config(command= my_text.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_text.pack(pady=20,ipadx=300)

########################################################################################################################

my_menu = Menu(second_frame)
root.config(menu=my_menu)

#Create a menu items
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="Open Directory",command=Select_directory)
file_menu.add_separator()
file_menu.add_command(label="Open File",command=open_file)
file_menu.add_command(label="New File",command=lambda:my_text.delete("1.0", END))
file_menu.add_command(label="Save File",command=save_file)

view_menu = Menu(my_menu)
my_menu.add_cascade(label="View",menu=view_menu)
view_menu.add_command(label="Font",command=Font)

exit_menu = Menu(my_menu)
my_menu.add_command(label="Exit",command=quit)

root.mainloop()