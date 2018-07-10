from .models import *
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
from random import randint

def update_clusters():
    print("updating clusters")
    num_reviews = Review.objects.count()
    update_step = ((num_reviews/100)+1) * 5
    if num_reviews % update_step > 0: # using some magic numbers here, sorry...
        print("are we in if")
        # Create a sparse matrix from user reviews
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_color_ids = set(map(lambda x: x.color.id, Review.objects.only("color")))
        num_users = len(list(all_user_names))
        ratings_m = dok_matrix((num_users, max(all_color_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                user_obj = User.objects.get(username=user_review.user_name)
                user = User_Profile.objects.get(user=user_obj)
                user_cgs = user.liked_color_groups.all()
                cgs_of_c = user_review.color.color_groups_set.all()

                user_cgs_ids = [cg.id for cg in user_cgs]
                cgs_of_c_ids = [cg.id for cg in cgs_of_c]
                #print(user_cgs_ids)
                #print(cgs_of_c_ids)
                mutual = []
                for u in user_cgs_ids:
                    for c in cgs_of_c_ids:
                        if u == c and u not in mutual:
                            mutual.append(u)

                #print(mutual)
                if len(mutual)==0:
                    all_list = list(all_color_ids)
                    rand = randint(0,len(all_list))
                    mutual.append(all_list[rand])
                ratings_m[i,user_review.color.id] = mutual[0]
        
        #print(ratings_m.tocsr())

        
        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())
        
        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before refering to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))



