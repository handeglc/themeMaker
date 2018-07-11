import matplotlib as mpl
mpl.use('TkAgg')

import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from polls.models import File
from polls.color import *

class Command(BaseCommand):
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def add_argument(self, parser):
        parser.add_argument('file', nargs='+', type=str, required=True)

    def handle(self, *args, **options):

        img = options['file']
        print(img)
        clusters = 5

        self.CLUSTERS = clusters
        self.IMAGE = img


        #print dominant colors
        colors = self.dominantColors()
        print(colors)
        return colors

    def dominantColors(self):
        
        #open image
        img = cv2.imread('/Users/hande/Desktop/Project/themaMaker/uploads/'+self.IMAGE)

        if img is not None:
            loaded = True
            cv2.imshow('Figure',img)
            cv2.waitKey(0)
        
        #convert to RGB from BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        
        #save image after operations
        self.IMAGE = img
        
        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(img)
        
        #getting the colors as per dominance order
        self.COLORS = kmeans.cluster_centers_
        
        #save labels
        self.LABELS = kmeans.labels_
        
        return self.COLORS.astype(int)



    
    
    
    
    



