import pandas as pd
from django.core.management.base import BaseCommand, CommandError
#from django.db import models
from polls.models import *
from random import randint
import string
from polls.color import *
from sklearn.cluster import KMeans




class Command(BaseCommand):

	def add_argument(self, parser):
		pass

	def handle(self, *args, **options):
		self.update_color_clusters()

	def update_color_clusters(self, *args, **options):

		all_colors = Color.objects.all()
		color_groups = Color_Groups.objects.all()
		all_color_ids = list(map(lambda x: x.id, all_colors.only("id")))
		c_cg_list = []
		for color in all_colors:
			cgs = color.color_groups_set.all()
			for cg in cgs:
				c_cg_list.append((color.id,cg.id))

		data = {}
		data["color"] = []
		data["color_group"] = []
		data["count_c"] = []
		data["c_tend"] = []
		data["c_light"] = []
		data["c_satur"] = []
		for tupl in c_cg_list:
			c = Color.objects.get(id=tupl[0])
			cg = Color_Groups.objects.get(id=tupl[1])
			data["color"].append(tupl[0])
			data["color_group"].append(tupl[1])
			data["count_c"].append(cg.how_many_colors)
			data["c_tend"].append( 0 if c.color_tendency=="Red" else (1 if c.color_tendency=="Green" else (2 if c.color_tendency=="Blue" else 3) ) )
			data["c_light"].append( 1 if c.is_light else 0)
			data["c_satur"].append(1 if c.is_saturated else 0)
		#print(data)

		df = pd.DataFrame(data=data)
		#print(df)
		#num = int(df.iloc[[3000]]["color"])
		#print(num)
		k = int(len(color_groups) / 30 +1)
		kmeans = KMeans(n_clusters=k)
		clustering = kmeans.fit(df)

		Color_Cluster.objects.all().delete()
		new_clusters = {i: Color_Cluster(name=i) for i in range(k)}
		for cluster in new_clusters.values(): # clusters need to be saved before refering to users
			cluster.save()
		for i,cluster_label in enumerate(clustering.labels_):
			new_clusters[cluster_label].colors.add(Color.objects.get(id=df.iloc[[i]]["color"]))
			#print((i,cluster_label))
		print("Color clusters are updated")

