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
songdisplay = ""
type = "folder/file"

filelist=list()

# A database using sqlite
conn = sqlite3.connect("songs.db")
c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS songs(
        song_name   TEXT,
        bpm         REAL
)""")

c.execute('SELECT * FROM songs')

rows = c.fetchall()

print("db contents: ")
for row in rows:
    print(row)

def openFile():
    global currentDirectory
    global type
    global currentRawPath
    global folderPath
    global stringtd
    global songdisplay

    listOfFiles.delete("1.0", tk.END)
    type = "file"
    songdisplay=""
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

    if len(stringtd)>20:
        stringtd = stringtd[:20]+"\n"+stringtd[20:]

    listOfFiles.insert(tk.END, "Song selected:\n"+ stringtd)
    

    '''folderPath is the path of the folder to the file. stringtd is going to be the song name without path marks. currentDirectory is the path to the file'''



def openFolder():
    

    #a variable that is not a parameter for the function must be written like this to be accessed by it.
    global currentDirectory
    global text1
    global listOfFiles
    global songdisplay
    global stringtd
    global filelist
    global type
    

    #resetting folder-specific values
    
    
    listOfFiles.delete("1.0", tk.END)

    songdisplay=""
    type = "folder"
    filelist = []

    #open filesystem
    currentDirectory = filedialog.askdirectory()
    #turn \ to /
    currentDirectory = os.path.normpath(currentDirectory)+"\\"
    
    for td in Path(currentDirectory).iterdir():
        
        
        


        #checking for right file type
        if str(td)[-3:]=="wav" or str(td)[-3:]=="mp3":

            stringtd=os.path.normpath(str(td))
        
            #to get rid of the directory before the file
            stringtd=stringtd.replace(str(currentDirectory), "")
            
            #adding the song name to display screen, but not too long
            
            if len(stringtd)>20:
                stringtd = stringtd[:20]+"\n"+stringtd[20:]
            
            filelist.append(stringtd)

            print("openFolder()",stringtd)
    
    #wrote this at a later time, didnt write this line in the for loop above to maintain readability
    for item in filelist:
        songdisplay=songdisplay+item+"\n"+"\n"
        

        

        
        
        
    
    
    
    listOfFiles.insert(tk.END, "Songs in the folder:\n"+ songdisplay)
    

            
        
        

        
    displayDirectory = Label(mainScreen, text = text1+currentDirectory)
    displayDirectory.grid(row=2 , column=1, columnspan=5)


def shorten(string):
    if len(string)>20:
        return string[:20]+"\n"+string[20:]

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
        low_entry.delete(0, tk.END)
        high_entry.delete(0, tk.END)
        
        error_label=tk.Label(mainScreen, text="must be numbers")
        error_label.grid(row=2+3,column=5)
    else:
        if low<high:
            correctvalues=True
            
            error_label= tk.Label(mainScreen, text="Values Set!")
            error_label.grid(row=2+3,column=5)
        else:
            low_entry.delete(0, tk.END)
            high_entry.delete(0, tk.END)
            
            error_label=tk.Label(mainScreen, text="numbers must make sense")
            error_label.grid(row=2+1,column=5)
        

def sort():
    global stringtd
    
    bpmclass = "none"
    if type=="folder":
        listOfFiles.delete("1.0","end")
        index = 0
        result = ""
        
        for td in filelist:
            
            stringtd=os.path.normpath(str(td))
            stringtd=stringtd.replace(str(currentDirectory), "")
            #check if exists in database
            c.execute("SELECT bpm FROM songs WHERE song_name = ?", (stringtd,))

            bpmfromdb = str(c.fetchone())
            print("fetchone",bpmfromdb)

            if c.fetchone() is not None: #exists already
                bpmfromdb = bpmfromdb[1:-2]
                if float(bpmfromdb)<low:
                    bpmclass="low bpm"
                if float(bpmfromdb)>low and float(bpmfromdb)<high:
                    bpmclass="medium bpm"
                if float(bpmfromdb)>high:
                    bpmclass="high bpm"

                result = result+"Songname: "+shorten(str(stringtd))+", "+str("\n"+", Tempo: "+bpmfromdb+" "+bpmclass+"\n")

            else:
                #calculate bpm
                y, sr = librosa.load(td)
                tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

                #categorize bpm 
                if correctvalues==True:
                    if tempo<low:
                        print( "Low Bpm")
                        bpmclass="low bpm"
                    if tempo>low and tempo<high:
                        print( "Medium Bpm")
                        bpmclass="medium bpm"
                    if tempo>high:
                        print( "High Bpm")
                        bpmclass="high bpm"
                
                #display
                result = result+"Songname: "+shorten(str(stringtd))+", Tempo: {:.2f}".format(tempo)

                print("Songname: "+str(stringtd)+", Tempo: {:.2f}".format(tempo)) 
            

                #store in database    
                song_data = (stringtd, int(tempo))
                c.execute("INSERT INTO songs (song_name, bpm) VALUES (?, ?)", song_data)
    
        #end of for each loop
        listOfFiles.insert(tk.END,result)
        index+=1



    if type=="file":
        
    
        #check if exists in database
        c.execute("SELECT bpm FROM songs WHERE song_name = ?", (stringtd,))
        
        bpmfromdb = str(c.fetchone())
        print("fetchone",bpmfromdb)

        if c.fetchone() is not None: #exists already
            bpmfromdb = bpmfromdb[1:-2]

            if float(bpmfromdb)<low:
                bpmclass="low bpm"
            if float(bpmfromdb)>low and float(bpmfromdb)<high:
                bpmclass="medium bpm"
            if float(bpmfromdb)>high:
                bpmclass="high bpm"

            print("got from database",bpmfromdb)
            listOfFiles.insert(tk.END, str("\n, Tempo: "+bpmfromdb+" "+bpmclass+"\n"))
        
        else:
            #calculate bpm
            y, sr = librosa.load(currentRawPath)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            print("Songname: "+str(stringtd)+", Tempo: {:.2f}".format(tempo))
            

            #categorize bpm 
            if correctvalues==True:
                if tempo<low:
                    print( "Low Bpm")
                    bpmclass="low bpm"
                if tempo>low and tempo<high:
                    print( "Medium Bpm")
                    bpmclass="medium bpm"
                if tempo>high:
                    print( "High Bpm")
                    bpmclass="high bpm"

            #display and store
            listOfFiles.insert(tk.END, str("\n, Tempo: {:.2f}".format(tempo)+bpmclass+"\n"))
            song_data = (stringtd, int(tempo))
            c.execute("INSERT INTO songs (song_name, bpm) VALUES (?, ?)", song_data)
            

def showSystem():
    dirpath = filedialog.askdirectory(initialdir=currentDirectory)

            




    


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
showInSystem_button = Button(mainScreen, text = "Show in FileSystem", command = showSystem)

#display song data

listOfFiles=Text(mainScreen, height = 300, width = 55)
listOfFiles.place(x=500,y=130)





# Display directory label



newFolder_button.grid(row = 1, column = 1, padx = 10, pady = 10)
importFolder_button.grid(row = 1, column = 2, padx = 10, pady = 10)
showInSystem_button.grid(row = 1, column = 3, padx = 10, pady = 10)






#value
low_label=tk.Label(mainScreen, text = "Low BPM threshold:")
low_label.grid(row=3+3,column=3)
low_entry=tk.Entry(mainScreen)
low_entry.grid(row=4+3,column=3)



high_label=tk.Label(mainScreen, text = "High BPM threshold:")
high_label.grid(row=7+3,column=3)
high_entry=tk.Entry(mainScreen)
high_entry.grid(row=8+3,column=3)

setLimit = tk.Button(mainScreen, text="set values", command=setLimit)
setLimit.grid(row=4+3,column=4)





#analyze bpm

analyze_button = tk.Button(mainScreen,text="analyze", command=sort)
analyze_button.grid(row=10+3,column=3)




























#Profile Menu
l_username = Label(profilePage, text = "Bobson6464", font = ("Arial", 25))
l_username.grid(row = 0, column = 3, padx = 10, pady = 10)







root.title("DJHelper")
root.resizable(False, False)
root.mainloop()






conn.commit()
conn.close()
