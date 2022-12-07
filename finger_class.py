import os
import cv2
from PIL import Image
import wsq
import numpy
import shutil
import sys

class FingerData:

  def __init__(self, dataDir, sampleDir, homeDir, mod):
    self.dir = dataDir
    self.sample = sampleDir
    self.home = homeDir
    self.modulo = int(mod)


  # Converts  images from WSQ format to PNG
  def sample_conversion(self, image, destination):
    self.destination = self.home + destination
    finger_image = Image.open(image)
    finger_image = finger_image.convert('L')

    try:
        os.mkdir(self.destination)
    except:
        print(destination+" folder exists.")

    finger_image.save(image + ".png")

    try:
      shutil.move(image + ".png", self.destination)
    except:
      os.remove(image+".png")
      sys.exit(image+" is already in "+ destination + " folder, delete and restart process")   
    

  # Compares sample file with fingerprint entries
  def scan(self):
    
    # Converting Sample File from WSQ to PNG and putting result
    # in a new folder, Sample
    self.sample_conversion(self.sample, "Sample")
    sampleFile = os.listdir(self.destination)   # assigning sample file a variable
    sampleFile = numpy.array(Image.open(self.destination+"/"+sampleFile[0]))
    best_score = 0.0

    # Group finger data into an array
    self.fileCount = len(os.listdir(self.dir))

    if (self.fileCount%self.modulo):
        splitNum = self.fileCount%self.modulo
    else:
        splitNum = (self.fileCount)/self.modulo 

    self.dataList = numpy.array_split(os.listdir(self.dir), splitNum)

    for i in range(len(self.dataList)):
      # print("Scanning Array: "+str(i))
      if (os.path.exists(self.home+"Temp")):
        shutil.rmtree(self.home+"Temp")

      for file in self.dataList[i]:
        filePath = self.dir+file
        self.sample_conversion(filePath, "Temp")

        filePath = self.home+"Temp/"+file+".png"
        dataFile = numpy.array(Image.open(filePath))

        # Matching Algorithm
        sift = cv2.SIFT_create()
        
        keypoints_1, descriptors_1 = sift.detectAndCompute(sampleFile, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(dataFile, None)

        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
                                                {}).knnMatch(descriptors_1, descriptors_2, k=2)

        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q. distance:
                match_points.append(p)

        keypoints = 0
        if len (keypoints_1) < len (keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)

        if len (match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file

        if best_score > 80.0:
          print("BEST MATCH: " + filename)
          print("SCORE: " + str(best_score))
          return