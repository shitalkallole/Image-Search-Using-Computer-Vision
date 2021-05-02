import tkinter					 
import tkinter.ttk as ttk       #to use advanced widget
from tkinter import messagebox  #to use messagebox
from tkinter import filedialog  #to use file dialog

from PIL import Image,ImageTk
import PIL
import numpy as np

import FaceRecognitionModule as frm
import cv2

import os        				#used to create shortcut file

#List to store path to each source image selected in page 1
sourceImagesPath=[]
#Start of variables used for Second Window
SecondWindowGlobal=0							#object holds second window
lbl_Store_Setter=0								#variable for label used on second window
rb_Status_Setter=0								#variable for radio button select all and unselect all
rb_CopyOrShortcut_Status=0                      #tkinter variable for radio button copy and shortcut

canvasGlobal=0									#used for Scrolling function

#for dynamic check box purpose
controlVar=[]
dynamic_CheckButton=[]
dynamic_Fun=[]

#for dynamic picture purpose
dynamic_PicturePath=[]													#full path of each filtered Images
dynamic_PictureLoad=[]													#reference of 150 * 150 resized image which is shown in second window(iload)
dynamic_Picture=[]														#in label we use ImageTk object. for ImageTk (p) we use iload object (p=ImageTk.PhotoImage(iload))
dynamic_LabelForPicture=[]												#Storing label which contain image

totalFilteredPicture=0	#total picture in which person present
totalSelectedPicture=0  #total selected picture from given filtered picture which user want to export
selectedPictureStatus=0  #dynamically we are creating array

filteredImages=[] #list of all filtered images
filteredImagesNames=[] #list of all filtered images names
#End of var

#Definition of required function For Window-1
def initialize_SecondWindow_Function():
	global SecondWindowGlobal

	container.attributes("-disabled", 1)
	SecondWindow=tkinter.Toplevel()
	SecondWindow.protocol("WM_DELETE_WINDOW", destroy_SecondWindow_Function)#bind window close event to handler
	#SecondWindow=tkinter.Tk()

	w=SecondWindow.winfo_screenwidth()//2  #take width of screen
	h=SecondWindow.winfo_screenheight()//2 #take height of screen

	SecondWindow.minsize(820,685)       				  #window size
	SecondWindow.geometry("+{}+{}".format(w-410,h-360))   #left and upper space
	SecondWindow.resizable(0,0)						      #Remove maximize button
	SecondWindow.title("Export Images")

	SecondWindowGlobal=SecondWindow
	return SecondWindow


def destroy_SecondWindow_Function(arg=None):
	#reset all variables
	
	global controlVar
	global dynamic_CheckButton
	global dynamic_Fun

	global dynamic_PicturePath
	global dynamic_PictureLoad
	global dynamic_Picture
	global dynamic_LabelForPicture

	controlVar=[]
	dynamic_CheckButton=[]
	dynamic_Fun=[]

	dynamic_PicturePath=[]
	dynamic_PictureLoad=[]
	dynamic_Picture=[]
	dynamic_LabelForPicture=[]

	container.attributes("-disabled", 0)
	SecondWindowGlobal.destroy()

def initialize_UpperFrame_Function(upperFrame):

	global lbl_Store_Setter
	global rb_Status_Setter
	global rb_CopyOrShortcut_Status

	#start of store button
	btn_Store=ttk.Button(upperFrame,text="Browse Store Folder",command=btn_Store_Function)
	btn_Store.bind("<Return>",btn_Store_Function)			#to work on ENTER also
	btn_Store.place(x=10,y=10)

	lbl_Store_Setter=tkinter.StringVar()

	lbl_Store=ttk.Label(upperFrame,textvariable=lbl_Store_Setter,width=100,background="white",anchor="center")
	lbl_Store.place(x=150,y=10)

	#start of radio button of select all and unselect all
	rb_Status_Setter=tkinter.IntVar()
	rb_Status_Setter.set(1)

	rb_selectall=ttk.Radiobutton(upperFrame,text="Select All",value=1,variable=rb_Status_Setter,command=rb_Status_Function)
	rb_selectall.place(x=10,y=40)

	rb_unselectAll=ttk.Radiobutton(upperFrame,text="Unselect All",value=2,variable=rb_Status_Setter,command=rb_Status_Function)
	rb_unselectAll.place(x=150,y=40)

	#start of copy and shortcut radio button
	rb_CopyOrShortcut_Status=tkinter.IntVar()
	rb_CopyOrShortcut_Status.set(1)

	rb_copy=ttk.Radiobutton(upperFrame,text="Copy",value=1,variable=rb_CopyOrShortcut_Status)
	rb_copy.place(x=350,y=40)

	rb_shortcut=ttk.Radiobutton(upperFrame,text="shortcut",value=2,variable=rb_CopyOrShortcut_Status)
	rb_shortcut.place(x=450,y=40)


	#start of export and cancel button
	btn_Export=ttk.Button(upperFrame,text="Export",command=btn_Export_Function)
	btn_Export.bind("<Return>",btn_Export_Function)			#to work on ENTER also
	btn_Export.place(x=600,y=40)

	btn_CancelSecond=ttk.Button(upperFrame,text="Cancel",command=btn_Cancel_Second_Function)
	btn_CancelSecond.bind("<Return>",btn_Cancel_Second_Function)			#to work on ENTER also
	btn_CancelSecond.place(x=680,y=40)

def btn_Store_Function(arg=None):
	dirname=filedialog.askdirectory()
	lbl_Store_Setter.set(dirname)

def rb_Status_Function(arg=None):
	whichRadio=rb_Status_Setter.get()

	if(whichRadio==1):
		#selectAll 
		set_Function(1)
	else:
		#UnselectAll
		set_Function(0)

def set_Function(set):
	global totalSelectedPicture
	global totalFilteredPicture


	for cb in controlVar:
		cb.set(set)

	for i in range(0,totalFilteredPicture):
			selectedPictureStatus[i]=set

	if set==1:
		totalSelectedPicture=totalFilteredPicture
	else:
		totalSelectedPicture=0

	#print("filtered:",totalFilteredPicture)

def btn_Cancel_Second_Function(arg=None):
	destroy_SecondWindow_Function()

def btn_Export_Function(arg=None):
	global totalFilteredPicture
	global totalSelectedPicture

	shortcutornot=rb_CopyOrShortcut_Status.get()	#1.copy 2.Shortcut

	if totalSelectedPicture!=0:
		path=lbl_Store_Setter.get() 	
		if path!="":
			for i in range(0,totalFilteredPicture):
				if selectedPictureStatus[i]==1:
					if shortcutornot==1:
						finalPath=path+"\\filtered_"+filteredImagesNames[i]
						cv2.imwrite(finalPath,filteredImages[i])
					else:
						source=lbl_Dest_Setter.get()+"\\"+filteredImagesNames[i] #to get path of source image to create shortcut
						target=path+"\\shortcut_"+filteredImagesNames[i]
						os.symlink(source,target)	

			if shortcutornot==1:
				messagebox.showinfo("Information","Selected Images successfully copied to given folder.")
			else:
				messagebox.showinfo("Information","Shortcuts of Selected Images successfully created in given folder.")
		
		else:
			if shortcutornot==1:
				messagebox.showinfo("Information","Please select Folder where you want to copy selected images")
			else:
				messagebox.showinfo("Information","Please select Folder where you want to create shortcut of selected images")
	else:
		messagebox.showinfo("Information","Please select Images to Export")


def initialize_BelowFrame_Function(belowFrame,filteredImagesCount,filteredImagesNames):
	global canvasGlobal	#using this global variable while destroying this second window

	scroll=ttk.Scrollbar(belowFrame)
	scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)

	can=tkinter.Canvas(belowFrame,yscrollcommand=scroll.set,width=800,height=585)
	can.pack(side=tkinter.LEFT)


	belowContainer=ttk.Frame(can)
	can.create_window((0,0),window=belowContainer,anchor='nw')
	belowContainer.bind("<Configure>",forScrolling_Function)

	scroll.config(command=can.yview)

	canvasGlobal=can 

	#start of adding checkbox and image
	totalPic=filteredImagesCount
	
	#variable creation to each check button
	for i in range(0,totalPic):
		var=tkinter.IntVar()
		var.set(1)
		controlVar.append(var)

	#function creation to each check button
	for i in range(0,totalPic):
		def handle(e,i=i):
			 return checkButton_Function(e,i)
		f=handle
		dynamic_Fun.append(f)

	#append names of file which are filtered so that we can display them on second window
	buildPath=lbl_Dest_Setter.get()			#get path name i.e from source label

	for imageName in filteredImagesNames:
		finalPath=buildPath+"\\"+imageName
		dynamic_PicturePath.append(finalPath)
	
	#start of Adding widget dynamically
	ans=totalPic//5
	rem=totalPic%5
	currentPicture=0
	currentCheck=0
	rowVal=-1
	if ans !=0:
		for i in range(0,ans):
			rowVal=rowVal+1
			for j in range(0,5):

				cb=ttk.Checkbutton(belowContainer,text=str(currentCheck+1),variable=controlVar[currentCheck])#attach different var to each checkbutton
				cb.bind('<Button-1>',dynamic_Fun[currentCheck])#attach different function to each checkbutton
				cb.grid(row=rowVal,column=j,padx=5,pady=5)
				dynamic_CheckButton.append(cb)
				currentCheck=currentCheck+1

			rowVal=rowVal+1
			for j in range(0,5):

				iload=Image.open(dynamic_PicturePath[currentPicture])
				iload=iload.resize((150,150),PIL.Image.ANTIALIAS)
				p=ImageTk.PhotoImage(iload)
				img=ttk.Label(belowContainer,image=p)
				img.grid(row=rowVal,column=j,padx=5,pady=5)
				dynamic_PictureLoad.append(iload)
				dynamic_Picture.append(p)
				dynamic_LabelForPicture.append(img)

				currentPicture=currentPicture+1

	if rem !=0:
		rowVal=rowVal+1
		for i in range(0,rem):

			cb=ttk.Checkbutton(belowContainer,text=str(currentCheck+1),variable=controlVar[currentCheck])
			cb.bind('<Button-1>',dynamic_Fun[currentCheck])
			cb.grid(row=rowVal,column=i,padx=5,pady=5)
			dynamic_CheckButton.append(cb)
			currentCheck=currentCheck+1

		rowVal=rowVal+1
		for i in range(0,rem):
			
			iload=Image.open(dynamic_PicturePath[currentPicture])
			iload=iload.resize((150,150),PIL.Image.ANTIALIAS)
			p=ImageTk.PhotoImage(iload)
			img=ttk.Label(belowContainer,image=p)
			img.grid(row=rowVal,column=i,padx=5,pady=5)
			dynamic_PictureLoad.append(iload)
			dynamic_Picture.append(p)
			dynamic_LabelForPicture.append(img)		

			currentPicture=currentPicture+1

	#for handling which picture selected and how many 
	global totalSelectedPicture
	global selectedPictureStatus
	global totalFilteredPicture

	selectedPictureStatus=np.ones(totalPic,int)
	totalSelectedPicture=totalPic
	totalFilteredPicture=totalPic
	#print("total selected pic:",totalSelectedPicture)	

def forScrolling_Function(event):
    canvasGlobal.configure(scrollregion=canvasGlobal.bbox("all"))


#to check which image selected
def checkButton_Function(event,number):
	global totalSelectedPicture
	if(selectedPictureStatus[number]==1):
		selectedPictureStatus[number]=0
		totalSelectedPicture=totalSelectedPicture-1
	else:
		selectedPictureStatus[number]=1
		totalSelectedPicture=totalSelectedPicture+1

	#print("total:",totalSelectedPicture)
	#print("checkbox:",number+1)
	#print("status:",selectedPictureStatus[number])
	#print("-------------------------")
#end of required function for window-2

#Start of Required function for window-1
def btn_Source_Function(arg=None):
	global sourceImagesPath

	sourceImagesPath=[] 		#initially make it empty
	multipleFile=filedialog.askopenfilenames(filetypes=(("jpeg file","*.jpg"),("png files","*.png")));

	totalSelectedSourceImage=len(multipleFile)
	lbl_Source_Setter.set(str(totalSelectedSourceImage)+" Images Selected")

	for filename in multipleFile:
		sourceImagesPath.append(filename)	
                                      
def btn_Dest_Function(arg=None):
	dirname=filedialog.askdirectory()
	lbl_Dest_Setter.set(dirname)

def btn_Scan_Function(arg=None):#when Enter pressed arg passed like -<KeyPress event state=Mod1 keysym=Return keycode=13 char='\r' x=69 y=24> (So we dont want to receive)
	global filteredImages
	global filteredImagesNames
	global sourceImagesPath


	sourceData=lbl_Source_Setter.get()
	destData=lbl_Dest_Setter.get()

	
	if(sourceData!="" and destData!=""):
		if(len(sourceImagesPath)>9):
		
			faceVector,labelVector,errorCode,errorInfo=frm.prepareTrainingData(sourceImagesPath)

			if errorCode==0:
				filteredImagesCount=0

				faceRecognizer=frm.trainRecognizer(faceVector,labelVector)
				filteredImages,filteredImagesNames,filteredImagesCount = frm.prepareTestingData(destData,faceRecognizer)

					
				if(filteredImagesCount!=0):
					SecondWindow=initialize_SecondWindow_Function()
					
					upperFrame=ttk.Frame(SecondWindow,width=820,height=100)
					upperFrame.grid(row=0)

					belowFrame=ttk.Frame(SecondWindow,width=820,height=585)
					belowFrame.grid(row=1)

					initialize_UpperFrame_Function(upperFrame)
					initialize_BelowFrame_Function(belowFrame,filteredImagesCount,filteredImagesNames)

				else:
					messagebox.showinfo("Information","No Images Found for given Person")

			else:
				messagebox.showinfo("Information",errorInfo);
		else:
			messagebox.showinfo("Information","Please select Atleast 10 images of person")
				
	else:
		if(sourceData=="" and destData==""):
			messagebox.showinfo("Information","Please select Source Images and Scan Folder")
		elif(sourceData==""):
			messagebox.showinfo("Information","Please select Source Images")
		else:
			messagebox.showinfo("Information","Please select Scan Folder")
	
	
def btn_Cancel_Function(arg=None):
	container.quit()
#End of Required function for window-1

#Create Container to hold widget
#fw -> First Window
#Start of Program
container=tkinter.Tk()

w=container.winfo_screenwidth()//2  #take width of screen
h=container.winfo_screenheight()//2 #take height of screen

container.minsize(600,300)       				   #window size
container.geometry("+{}+{}".format(w-300,h-150))   #left and upper space
container.resizable(0,0)						   #Remove maximize button
container.title("Image Scanner")				   #Set Title
#container.withdraw()  for hiding purpose

#Configure Style
style=ttk.Style()
style.configure("fw.TButton",width=25)

#Create Widget
lbl_Atleast=ttk.Label(container,text="Please Select Atleast 10 images (Source Images) of Person in which only he/she present and face is clear",width=93,background="white")
lbl_Atleast.place(x=27,y=5)

btn_Source=ttk.Button(container,text="Browse Source Images",style="fw.TButton",command=btn_Source_Function)
btn_Source.bind("<Return>",btn_Source_Function)			#to work on ENTER also
btn_Source.place(x=27,y=42)
	
lbl_Source_Setter=tkinter.StringVar()
lbl_Dest_Setter=tkinter.StringVar()

lbl_Source=ttk.Label(container,textvariable=lbl_Source_Setter,width=60,background="white",anchor="center")
lbl_Source.place(x=197,y=42)

btn_Dest=ttk.Button(container,text="Browse Scan Folder",style="fw.TButton",command=btn_Dest_Function)
btn_Dest.bind("<Return>",btn_Dest_Function)
btn_Dest.place(x=27,y=92)

	
lbl_Dest=ttk.Label(container,textvariable=lbl_Dest_Setter,width=60,background="white",anchor="center")
lbl_Dest.place(x=197,y=92)

btn_Scan=ttk.Button(container,text="Scan",style="fw.TButton",command=btn_Scan_Function)
btn_Scan.bind("<Return>",btn_Scan_Function)
btn_Scan.place(x=197,y=142)

btn_Cancel=ttk.Button(container,text="Cancel",style="fw.TButton",command=btn_Cancel_Function)
btn_Cancel.bind("<Return>",btn_Cancel_Function)
btn_Cancel.place(x=403,y=142)

#Infinite loop to take action on event
container.mainloop()
#end of Program
