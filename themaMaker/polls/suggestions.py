from .models import *
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
from random import randint
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
from statistics import mean

def update_clusters():
    print("updating clusters")
    num_cgs = Color_Groups.objects.count()
    update_step = ((num_cgs/100)+1) * 5
    if num_cgs % update_step > 0: # using some magic numbers here, sorry...
        print("are we in if")
        # Create a sparse matrix from user reviews
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_color_ids = list(map(lambda x: x.color.id, Review.objects.only("color")))
        num_users = len(list(all_user_names))
        ratings_m = dok_matrix((num_users, max(all_color_ids)+1), dtype=np.float32)
        all_cg = Color_Groups.objects.all()
        df = pd.DataFrame(columns=["user","cg_count","cg_tend","c_count"], index=list(range(0,num_users)))
        i=0;
        for user in all_user_names: # each user corresponds to a row, in the order of all_user_names
            user_obj = User.objects.get(username=user)
            user__ = User_Profile.objects.get(user=user_obj)
            user_cgs = user__.liked_color_groups.all()


            user_cgs_ids = [cg.id for cg in user_cgs]

            if len(user_cgs_ids)==0:
                df["cg_count"][i]=0
                df["user"][i]=user_obj.id
                df["cg_tend"][i] = -1
                df["c_count"][i] = -1
                i+=1
                continue;
            cg_dict ={} 
            cg_dict["cgid"]=[]
            cg_dict["cg_tend"]=[]
            cg_dict["c_count"]=[]
            for m in user_cgs_ids:
                cg_dict["cgid"].append(m)
                cg = Color_Groups.objects.get(id=m)
                tend = 0 if cg.group_tendency=="Red" else (1 if cg.group_tendency=="Green" else 2)
                cg_dict["cg_tend"].append(tend)
                cg_dict["c_count"].append(cg.how_many_colors)

            df["cg_count"][i]=len(cg_dict["cgid"])
            df["user"][i]=user_obj.id
            df["cg_tend"][i] = mean(cg_dict["cg_tend"])
            df["c_count"][i] = mean(cg_dict["c_count"])
            i+=1

        print(df)



        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(df)
        
        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before refering to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            #print(User.objects.get(id=df["user"][i]))
            new_clusters[cluster_label].users.add(User.objects.get(id=df["user"][i]))

        print("User clusters are updated")
