#task: figure out how to switch between pages
#https://www.youtube.com/watch?v=qw_XHRJP-vc 8:25
#https://dev.to/highcenburg/getting-the-tempo-of-a-song-using-librosa-4e5b
#https://www.youtube.com/watch?v=reJ8kTqQsTY 5:18

import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
import os
import librosa

from pathlib import Path
#initialize some variables
text1 = "Folder Path: ";




def openFolder():
    global currentDirectory;
    global text1;
    global listOfFiles;
    global thestring
    
    filelist=list();
    
    currentDirectory = filedialog.askdirectory()
    
    for td in Path(currentDirectory).iterdir():
        print(td);
        filelist.append(td);
        thestring = str(td) + "\n"

    listOfFiles=Text(mainScreen, height = 500, width = 400, text = thestring)
    listOfFiles.grid()
            
        
        

        
    displayDirectory = Label(mainScreen, text = text1+currentDirectory)
    displayDirectory.grid(row=2 , column=3, padx = 5)




    

def doNothing():
    x=1

def setLimit():
    global low
    global middle
    global high
    global correctvalues #bool
    try:
       

        low=int(low_entry.get())
        middle=int(middle_entry.get())
        high=int(high_entry.get())

        print(str(low)+"\n"+str(middle)+"\n"+str(high))
    except:
        print("no")
        low_entry.delete(0, tk.END)
        middle_entry.delete(0, tk.END)
        high_entry.delete(0, tk.END)
        error_label=tk.Label(mainScreen, text="must be numbers")
        error_label.grid(row=2,column=5)
    else:
        if low<middle and middle<high:
            correctvalues=True
            error_label.delete()
        else:
            low_entry.delete(0, tk.END)
            middle_entry.delete(0, tk.END)
            high_entry.delete(0, tk.END)
            error_label=tk.Label(mainScreen, text="numbers must make sense")
            error_label.grid(row=2,column=5)
        
        


    


# create a tkinter window
root = tk.Tk()

profilePage = Frame(root, width=800, height=1000, style="profilePage.TFrame")
mainScreen = Frame(root, width=800, height=1000, style="mainScreen.TFrame")
mainScreen.grid()

# Open window having dimension 100x100  
root.geometry('1000x800')
#set first screen to main screen
mainScreen.lift()

mainScreen.grid(row=0, column=0)
profilePage.grid(row=0, column=0)

#Main Menu Widgets
new_folder = Button(mainScreen, text = 'New Folder', command = doNothing)
import_folder = Button(mainScreen, text = "Import Folder", command = lambda: openFolder())



profile = Button(mainScreen, text = "Profile", command = lambda: profilePage.lift())
print("testing", text1)
# Display directory label

displayDirectory = Label(mainScreen, text = text1)
displayDirectory.grid(row=2, column=1, padx=10, pady=10)

new_folder.grid(row = 1, column = 1, padx = 10, pady = 10)
import_folder.grid(row = 1, column = 2, padx = 10, pady = 10)
profile.grid(row = 0, column = 3, padx = 10, pady = 10)




#value
low_label=tk.Label(mainScreen, text = "Highest BPM for low:")
low_label.grid(row=3,column=3)
low_entry=tk.Entry(mainScreen)
low_entry.grid(row=3,column=4)

middle_label=tk.Label(mainScreen, text = "Highest BPM for medium:")
middle_label.grid(row=3,column=5)
middle_entry=tk.Entry(mainScreen)
middle_entry.grid(row=3,column=6)

high_label=tk.Label(mainScreen, text = "Lowest BPM for high:")
high_label.grid(row=3,column=7)
high_entry=tk.Entry(mainScreen)
high_entry.grid(row=3,column=8)




setLimit = tk.Button(mainScreen, text="set thresholds", command=setLimit)
setLimit.grid(row=4,column=5)





























#Profile Menu
l_username = Label(profilePage, text = "Bobson6464", font = ("Arial", 25))
l_username.grid(row = 0, column = 3, padx = 10, pady = 10)


'''#calling opening filesystem code 
button = Button(text="Open",command=openFile())
button.pack()'''


'''# Directory
directory = "test"
  
# Parent Directory path
parent_dir = "C:/"

# Path
path = os.path.join(parent_dir, directory)

os.mkdir(path)
print("Directory '% s' created" % directory) '''

root.title("DJTool")
root.resizable(False, False)
root.mainloop()


