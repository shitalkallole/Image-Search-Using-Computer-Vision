import cv2
import os
import numpy as np

#Function to check how much match
#Arguments: faceRecognizer--> Object returned by trainRecognizer method
#			  predictImage--> Image of face to be compared
def prediction(faceRecognizer,predictImage):
	label,con=faceRecognizer.predict(predictImage)						#predict in-built method of recognizer
	return label,con 													#return label (which is 1 in any case) and confidence(which we use) in percentage


#Function to train Recognizer
#Arguments:  faceVector--> List which contain faces (Array)returned by prepareTrainingData method
#			labelVector--> List which contain label (Array)returned by prepareTrainingData method.Used for user convinient (like "1->name1,2->name2")
#						   In our case labelVector Conatain Only 1 coz we are only checking for 1 person.this must be passed as integer array
def trainRecognizer(faceVector,labelVector):	
	#print("Training Recognizer:start")						
	faceRecognizer=cv2.face.LBPHFaceRecognizer_create()					#We are using Linear Binary Pattern Histogram Algorithm for Face Recognition purppose
	faceRecognizer.train(faceVector,np.array(labelVector))				#train is in-built method used to train LBPH algorithm
	#print("Training Recognizer:end")
	return faceRecognizer												#return recognizer then recognizer used for prediction purpose


#Function for Training Recognizer
#Arguments: trainingDirectory--> contain Directory name where training images reside like="C:\\Users\\Shital\\Desktop\\pythonprograms\\train"
def prepareTrainingData(trainingImagesList):
	#print("Preparing training Data:start")	
	faceVector=[]														#List to hold face data
	labelVector=[]														#List to hold Label 
	errorCode=0
	errorInfo="Nothing"

	for fileName in trainingImagesList:						#for each image in directory.fileName hold name of each file present in directory
		sampleImage=cv2.imread(fileName)							#we read image
		faces,grayImage=faceDetection(sampleImage)					#faceDetection return faces(contain location of each face) and gray img(color->gray) 

		if(len(faces)==1):											#there must be only one face present in each training image
			#print("Found Face in training image of :"+fileName);
			roi=regionOfInterest(grayImage,faces[0])				#we take only face from original image
			resizedImage=resizeImage(roi)							#resized image to 300*300
			faceVector.append(resizedImage)							#add resized face to faceVector
			labelVector.append(1)									#add 1 to labelVector
		
	if(len(labelVector)>=10):											#at least 1 face we need to find from all training images
		return faceVector,labelVector,errorCode,errorInfo
	elif(len(labelVector)>=1):
		errorCode=1
		errorInfo="Training not done because atleat 10 sample images must be selected which must have single face and clear face in each file."	
		return 0,0,errorCode,errorInfo
	else:
		errorCode=2
		errorInfo="Training not done because face not found in all files or all file have more than 1 faces present."
		return 0,0,errorCode,errorInfo
#Function for Face Detection
#Arguments: sampleImage--> Original image passed for face detection
def faceDetection(sampleImage):
	faceCascade=cv2.CascadeClassifier("./data/haarcascade_frontalface_alt2.xml")	#load cascade (using Haar-Cascade or viola-jones algorithm)
	grayImage=cv2.cvtColor(sampleImage,cv2.COLOR_BGR2GRAY)							#convert image to gray coz cascade work on gray image
	faces=faceCascade.detectMultiScale(grayImage,scaleFactor=1.5,minNeighbors=5)	#return location of each face found in image i.e x,y,w,h
	return faces,grayImage															#returning location and gray image of original image	

#Function for cropping only face from whole image
#Arguments: grayImage--> grayImage passed from prepareTrainingData method
#				faces--> Contain location of faces,x=x-axis y=y-axis w=width h=height
def regionOfInterest(grayImage,faces):
	#for (x,y,w,h) in faces:												#For each face present in grayImage
	(x,y,w,h)=faces
	w=w-60															#For adjustment purpose we remove left 30 and right 30 so remove total 60
	x=x+30															#we add 30 so indirectly it return 30 from left(by default right side removed when we remove 60)
	endx=x+w     													#location of upper-right corner
	endy=y+h 														#location of below-left corner
	roi=grayImage[y:endy,x:endx] 									#extract only face from grayImage
	return roi       												#return face


#Function for resizing each face photo to 300*300.This will give u good results
#Arguments: roi--> regionOfFace returned by regionOfInterest method 
def resizeImage(roi):
	resized=cv2.resize(roi,(300,300))	
	if resized.size!=0:								#resize in-built method
		return resized 														#return resized image of face photo
	else:
		return 0


#Function for copying matched photos from scan Folder to rec folder
#Arguments: testingDirectory--> contain Directory name where testing images reside like="C:\\Users\\Shital\\Desktop\\pythonprograms\\test"
#			  faceRecognizer--> faceRecognizer object which is passed when calling prediction
def prepareTestingData(testingDirectory,faceRecognizer):
	#print("-------Testing started---------")
	filteredImagesNames=[]												#File name in which person present
	filteredImagesCount=0												#Count of total Files in which person present
	filteredImages=[]													#Actual image in which person present
	for fileName in os.listdir(testingDirectory):						#for each image in directory.fileName hold name of each file present in directory
		#print("Working for : "+fileName)
		if(fileName.endswith(".jpg") or fileName.endswith(".png")):		#only .jpg and .png allowed	
			imagePath=testingDirectory+"\\"+fileName					#we build full path to access image ex-"C:\\Users\\.."+"\\"+"first.jpg"
			testImage=cv2.imread(imagePath)							    #we read image
			if not testImage is None:
				faces,grayImage=faceDetection(testImage)					#faceDetection return faces(contain location of each face) and gray img(color->gray) 
				if(len(faces)>0):											#there must be more than zero face present in each testing image
					length=len(faces)										#length->variable store number of faces present in photo
					#print("  Number of faces in this file:",length)
					for tFaces in range(0,length): 							#for each face present in photo
						face=faces[tFaces] 									#storing data from array to variable face
						roi=regionOfInterest(grayImage,face)				#we take only face from original image
						resizedImage=resizeImage(roi)						#resized image to 300*300
						label,con=prediction(faceRecognizer,resizedImage)   #label is = 1 and con=confidence in percentage
						#print("  Confidence:",con)
						if con<41:
							#print("   Person Present in file "+fileName)
							filteredImagesNames.append(fileName)
							filteredImages.append(testImage)
							filteredImagesCount=filteredImagesCount+1
							break
		
	return filteredImages,filteredImagesNames,filteredImagesCount