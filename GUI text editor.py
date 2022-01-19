from tkinter import *
from tkinter import filedialog as fd
from tkinter import font
from tkinter import colorchooser
import os, sys
import win32print
import win32api

root=Tk()
root.title("My Text-Editor")
root.geometry("1100x660")

#set variable for open file name
global open_file_name
open_file_name = False

#set variable for selected text( use in different block like function of cut_text,copy_text and paste_text)
global selected
selected= False

#create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

#Create Main Frame
my_frame=Frame(root)
my_frame.pack(pady=5)

#create our Scrollbar for the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT,fill=Y)

# Horizontal Scrollbar for text Box
hor_scroll = Scrollbar(my_frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)

#Create Text Box
#set undo=True  (for allowing undo)
#set wrap = none for continue scrolling toward Y-axis
my_text = Text(my_frame,width=97,height=25,font=("helvetica",16 ), selectbackground="yellow" , selectforeground="black", yscrollcommand=text_scroll.set, undo=True,wrap = "none", xscrollcommand=hor_scroll.set)
#selectbackground = to highligth selected text
my_text.pack()

#configure our Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

#create  Menu
My_menu=Menu(root)
root.config(menu=My_menu)

def new_file():    
    #Delete previous text
    my_text.delete("1.0",END) #start point(it is always 0.1) to last(END)

    #update title and status bar
    root.title("New File - TextPad!")
    status_bar.config(text="New File     ")

    global open_file_name
    open_file_name = False
    
def open_file():
    my_text.delete("1.0",END)
    #Grab Filename
    text_file=fd.askopenfilename(initialdir="F:/",title="My file opener",filetypes=(("Text Files","*.txt"),("HTML File","*.html"),("Python Files","*.py"),("All Files","*.*")))
  
    #check to see if there is a file open(for file name)
    if text_file:
        #make fiename global so we can access throughout the program
        #here is global declare ,so to update the value
        
        global open_file_name
        open_file_name = text_file
        status_bar.config(text=f'Save mode     ')
        
    #update title and Status bars
    name=text_file
    root.title(f'{name}  - TextPad')    # f is format()
    ch = name.rfind('/')
    name= name.replace(name,name[ch+1:])
    status_bar.config(text=f'Saved as: {name}     ')

    #Open the file
    text_file = open(text_file,'r')
    stuff = text_file.read()
    #Add file to text
    my_text.insert(END,stuff)
    #Closed the opened file
    text_file.close()

#create Save as file  
def save_as_file():
    text_file=fd.asksaveasfilename(defaultextension=".*", initialdir="C:/",title="save File", filetypes=(("Text File","*.txt"),("Python File","*.py"),("HTML File","*.html"),("All Files","*.*")))
    if text_file:
        #update status bars
        name = text_file
        
        root.title(f'{name}  - TextPad')    # f is format()
        ch = name.rfind('/')
        name= name.replace(name,name[ch+1:])
        status_bar.config(text=f'Saved as: {name}     ')

        
        #Save the file
        text_file = open(text_file,"w")
        text_file.write(my_text.get(1.0,END))
        #close the file
        text_file.close()

# Save File
def save_file():
    global open_file_name
    if open_file_name:
        text_file = open(open_file_name,"w") 
        text_file.write(my_text.get(1.0,  END))

        #close the file
        text_file.close()
        
        name = open_file_name
        ch = name.rfind('/')
        name= name.replace(name,name[ch+1:])
        status_bar.config(text=f'Saved: {name}     ')
        
    else:
        save_as_file()

# Print FIle
def print_file():
    #printer_name = win32print.GetDefaultPrinter()
    #status_bar.config(text=printer_name)

    #Grab file name
    file_to_print = fd.askopenfilename(initialdir="C:/",title="My file opener",filetypes=(("Text Files","*.txt"),("HTML File","*.html"),("Python Files","*.py"),("All Files","*.*")))

    if file_to_print:
        win32api.ShellExecute(0, "print" , file_to_print , None , "." , 0)

# Cut Text
def cut_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #Grab selected text from text box
            selected = my_text.selection_get()
            #delete selected text from text box
            my_text.delete("sel.first","sel.last")
            #clear anything in clipboard
            root.clipboard_clear()
            #append selected text in clipboard
            root.clipboard_append(selected)

# Copy Text
def copy_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #Grab selected text from text box
            selected = my_text
            #clear anything in clipboard
            root.clipboard_clear()
            #append selected text in clipboard
            root.clipboard_append(selected)

# Paste Text
def paste_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.clipboard_get()
    #else block avoid to paste twice 
    else:
        if selected:
            #Get current position of cursor
            position= my_text.index(INSERT)
            my_text.insert(position, selected)

#Select all text
def select_all(e):
    # Add sel tag to select all text
    #my_text.tag_add("sel" , "1.0" , "end")
    my_text.tag_add("sel" , 1.0 , END)

# Clear all text
def clear_all():
    my_text.delete(1.0 , END)
# Bold Text
def bold_it():
    # Create our font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight = "bold")

    #Configure a tag
    my_text.tag_configure("bold", font = bold_font )

    #Define Current Tags
    current_tags = my_text.tag_names("sel.first")
    
    # If Statement to see if tag has been set
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")

# Italic Text
def italics_it():
    # Create our font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")

    #Configure a tag
    my_text.tag_configure("italic", font = italics_font )

    #Define Current Tags
    current_tags = my_text.tag_names("sel.first")
    
    # If Statement to see if tag has been set
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

#Change selected text color
def text_color():
    #Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=f"color : {my_color}")

        # Create our font
        color_font = font.Font(my_text, my_text.cget("font"))
        #Configure a tag
        my_text.tag_configure("colored", font = color_font , foreground=my_color)

        #Define Current Tags
        current_tags = my_text.tag_names("sel.first")
        # If Statement to see if tag has been set
        my_text.tag_add("colored", "sel.first", "sel.last")

# Change background color
def bg_color():
    #Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

#Change All Text color
def all_text_color():
    #Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)
        
#Add file menu
file_menu = Menu(My_menu,tearoff=0)
My_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save",command=save_file)  #,command=save_file
file_menu.add_command(label="Save As",command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Print",command=print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)

#Add edit menu
edit_menu = Menu(My_menu,tearoff=0)
My_menu.add_cascade(label="Edit ",menu=edit_menu)
edit_menu.add_command(label="Cut            ", command= lambda: cut_text(False), accelerator=" (Ctrl+x)") # In whole program inside lamda function we can pass anything like True or False or 1
edit_menu.add_command(label="Copy ", command= lambda: copy_text(False), accelerator=" (Ctrl+c)")
edit_menu.add_command(label="Paste", command= lambda: paste_text(False), accelerator=" (Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command = my_text.edit_undo, accelerator=" (Ctrl+z)")#it does not required binding
edit_menu.add_command(label="Redo", command = my_text.edit_redo, accelerator=" (Ctrl+y)")#beacause tkinter text widget has this already this operate it
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command = lambda : select_all(True), accelerator=" (Ctrl+a)")
edit_menu.add_command(label="Clear", command = clear_all, accelerator=" (Ctrl+y)")

#Add color menu
color_menu = Menu(My_menu,tearoff=0)
My_menu.add_cascade(label="Colors ",menu=color_menu)
color_menu.add_command(label="Selected Text ", command= text_color)
color_menu.add_command(label="All Text", command= all_text_color)
color_menu.add_command(label="Background", command =bg_color)

#create Button
#Bold Button
bold_button = Button(toolbar_frame, text = "Bold" , command = bold_it)
bold_button.grid(row=0, column = 0, sticky=W, padx = 5)

#Italic Button
italic_button = Button(toolbar_frame, text = "Italic" , command = italics_it)
italic_button.grid(row=0, column = 1 , padx = 5)

#Undo/Redo Button
undo_button = Button(toolbar_frame, text = "Undo" , command = my_text.edit_undo)
undo_button.grid(row=0, column = 2 , padx =5)

redo_button = Button(toolbar_frame, text = "Redo" , command = my_text.edit_redo)
redo_button.grid(row=0, column = 3 , padx =5)

#Text Color
color_text_button = Button(toolbar_frame , text = "Text color" , command=text_color)
color_text_button.grid(row = 0,column = 4 , padx=5)

#Edit Binding to Keyboard
root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

#Not neccesary
#Select Binding
root.bind("<Control-A>", select_all)
root.bind("<Control-a>", select_all)

#Add status to bottom
status_bar = Label( root , text="Welcome!         " , anchor=E)
status_bar.pack(fill=X , side = BOTTOM , ipady=15)

root.mainloop()
