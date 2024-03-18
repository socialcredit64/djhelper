#https://www.youtube.com/watch?v=qw_XHRJP-vc 8:25
#https://dev.to/highcenburg/getting-the-tempo-of-a-song-using-librosa-4e5b
#https://www.youtube.com/watch?v=reJ8kTqQsTY 5:18
#https://www.sqlitetutorial.net/sqlite-python/creating-database/
#https://docs.python.org/3/library/dialog.html#tkinter.filedialog.askopenfile

#how to print contents of a database in sqlite?

import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
import os
import librosa
import sqlite3
from pathlib import Path
import subprocess
#initialize some variables
text1 = "Folder Path: "
songs = ""
type = "folder/file"

filelist=list()

# A database using sqlite
conn = sqlite3.connect("songs.db")
c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS songs(
        song_name   TEXT,
        bpm         REAL
)""")

def openFile():
    global currentDirectory
    global type
    global currentRawPath
    global folderPath
    global stringtd


    type = "file"

    currentDirectory = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Wave files", "*.wav"), ("MP3 files", "*.mp3")))
    folderPath = os.path.dirname(currentDirectory)
    currentRawPath = currentDirectory
    folderPath = os.path.normpath(folderPath)
    
    displayDirectory = Label(mainScreen, text = text1+currentDirectory)
    displayDirectory.grid(row=2 , column=1, columnspan=5)

    stringtd=os.path.normpath(str(currentDirectory))
    #to get rid of the directory before the file
    stringtd=stringtd.replace(str(folderPath)+"\\", "")
    print("stringtd:",stringtd)
    print("currentdirectory:",currentDirectory)
    print("folder:",folderPath)

    '''folderPath is the path of the folder to the file. stringtd is going to be the song name without path marks. currentDirectory is the path to the file'''



def openFolder():
    

    #a variable that is not a parameter for the function must be written like this to be accessed by it.
    global currentDirectory
    global text1
    global listOfFiles
    global songs
    global stringtd
    global filelist
    global type

    type = "folder"
    currentDirectory = filedialog.askdirectory()
    #turn \ to /
    currentDirectory = os.path.normpath(currentDirectory)+"\\"
    
    for td in Path(currentDirectory).iterdir():
        
        stringtd=os.path.normpath(str(td))
        
        #to get rid of the directory before the file
        stringtd=stringtd.replace(str(currentDirectory), "")
        
        #print(currentDirectory)

        if str(td)[-3:]=="wav" or str(td)[-3:]=="mp3":
            filelist.append(td)
        print(stringtd)
        
        '''if len(stringtd)>50:
            stringtd=stringtd[0:47]+"..."
        songs = songs + str(stringtd) + "\n"'''
    #print(songs)

    '''listOfFiles=Text(mainScreen, height = 500, width = 400)
    listOfFiles.grid(row=6, column=1, columnspan=5)
    listOfFiles.insert(tk.END, "Songs in the folder:\n"+ songs)'''
            
        
        

        
    displayDirectory = Label(mainScreen, text = text1+currentDirectory)
    displayDirectory.grid(row=2 , column=1, columnspan=5)





def doNothing():
    x=1

def setLimit():
    global low
    global high
    global correctvalues #bool
    try:
       

        low=int(low_entry.get())
        high=int(high_entry.get())

        print(str(low)+"\n"+str(high))
    except:
        print("no")
        low_entry.delete(0, tk.END)
        high_entry.delete(0, tk.END)
        
        error_label=tk.Label(mainScreen, text="must be numbers")
        error_label.grid(row=2+3,column=5)
    else:
        if low<high:
            correctvalues=True
            
            error_label= tk.Label(mainScreen, text="Values Set!")
            error_label.grid(row=2+3,column=5)
            print("c")
        else:
            low_entry.delete(0, tk.END)
            high_entry.delete(0, tk.END)
            
            error_label=tk.Label(mainScreen, text="numbers must make sense")
            error_label.grid(row=2+1,column=5)
        

def sort():
    global stringtd

    if type=="folder":
        for td in filelist:
            y, sr = librosa.load(td)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

            #display the song name and BPM on screen

            stringtd=os.path.normpath(str(td))
            stringtd=stringtd.replace(str(currentDirectory), "")

            print("Songname: "+str(stringtd)+", Tempo: {:.2f}".format(tempo)) 
            song_data = (stringtd, int(tempo))
            c.execute("INSERT INTO songs (song_name, bpm) VALUES (?, ?)", song_data)
            #if the correct values arent given then the bpm cannot be categorized
            if correctvalues is None:
                break
            if correctvalues==True:
                if tempo<low:
                    print( "Low Bpm")
                if tempo>high:
                    print( "High Bpm")



    if type=="file":
        y, sr = librosa.load(currentRawPath)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        print("Songname: "+str(stringtd)+", Tempo: {:.2f}".format(tempo))
        song_data = (stringtd, int(tempo))
        c.execute("INSERT INTO songs (song_name, bpm) VALUES (?, ?)", song_data)
        #if the correct values arent given then the bpm cannot be categorized  
        if correctvalues==True:
            if tempo<low:
                print( "Low Bpm")
            if tempo>high:
                print( "High Bpm")




    


# create a tkinter window
root = tk.Tk()

profilePage = Frame(root, width=800, height=1000, style="profilePage.TFrame")
mainScreen = Frame(root, width=800, height=1000, style="mainScreen.TFrame")
mainScreen.grid()
mainScreen.grid_propagate(False)

# Open window having dimension 100x100  
root.geometry('1000x800')
#set first screen to main screen
mainScreen.lift()

mainScreen.grid(row=0, column=0)
profilePage.grid(row=0, column=0)

#Main Menu Widgets
newFolder_button = Button(mainScreen, text = 'Import File', command = openFile)
importFolder_button = Button(mainScreen, text = "Import Folder", command = openFolder)




# Display directory label



newFolder_button.grid(row = 1, column = 1, padx = 10, pady = 10)
importFolder_button.grid(row = 1, column = 2, padx = 10, pady = 10)





#value
low_label=tk.Label(mainScreen, text = "Highest BPM for low:")
low_label.grid(row=3+3,column=3)
low_entry=tk.Entry(mainScreen)
low_entry.grid(row=4+3,column=3)



high_label=tk.Label(mainScreen, text = "Lowest BPM for high:")
high_label.grid(row=7+3,column=3)
high_entry=tk.Entry(mainScreen)
high_entry.grid(row=8+3,column=3)

setLimit = tk.Button(mainScreen, text="set thresholds", command=setLimit)
setLimit.grid(row=4+3,column=4)


#displaying files on screen
'''listOfFiles=Text(mainScreen, height = 20, width = 50)
listOfFiles.grid(row=6, column=1, columnspan=5, pady=30)
listOfFiles.insert(tk.END, "Songs in the folder: "+ songs)
listOfFiles.config(state=DISABLED)'''


#analyze bpm

analyze_button = tk.Button(mainScreen,text="分析", command=sort)
analyze_button.grid(row=10+3,column=3)




























#Profile Menu
l_username = Label(profilePage, text = "Bobson6464", font = ("Arial", 25))
l_username.grid(row = 0, column = 3, padx = 10, pady = 10)







root.title("DJTool")
root.resizable(False, False)
root.mainloop()

conn.commit()
conn.close()
