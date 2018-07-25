#import pandas as pd
from django.core.management.base import BaseCommand, CommandError
#from django.db import models
from polls.models import *
from django.contrib.auth.models import User
from random import randint,choice
import string
from polls.color import *
import re
#from django.contrib.auth import authenticate
#filename = 'color_data.csv'

#dataframe = pd.read_csv(filename)

#dataframe[]


 
class Command(BaseCommand):
    help = 'Command to do........'

    def read_color_sets(self,filename):

        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            color_list = []
            cols = line.split(" ")
            for c in cols:
                if len(c)>7: #get rid of the nev line
                    c = c[:7]
                the_color = Color.objects.filter(color_id_hex=c)
                if the_color.count() == 0:
                    #print(c)
                    new_color = Color(color_id_hex=c, is_light= color_is_light(c), is_saturated = color_is_saturated(c), color_tendency=color_tendency(c))
                    new_color.save()
                    color_list.append(new_color)
                else:
                    color_list.append(the_color[0])
            color_hex_list =[c.color_id_hex for c in color_list]
            cg = Color_Groups(how_many_colors=len(color_list), group_tendency=cg_group_tendency(color_hex_list))
            cg.save()
            print(color_list)
            for col in color_list:
                print(col)
                cg.colors.add(col)
            print(cg)

    def read_color_sets_rgb(self,filename):
        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            color_list = []
            cols = line.split(" ")
            for c in cols:
                if c[-1] != ")":
                    c = c[:len(c)-1]
                #print(c)
                color_rgb = re.match('rgb\(([0-9]*),([0-9]*),([0-9]*)\)', c)
                r = int(color_rgb.group(1))
                g = int(color_rgb.group(2))
                b = int(color_rgb.group(3))
                hex_col = convert_rgb_to_hex(r,g,b)
                print((r,g,b))
                print(hex_col)
                the_color = Color.objects.filter(color_id_hex=hex_col)
                if the_color.count() == 0:
                    # print(c)
                    new_color = Color(color_id_hex=hex_col, is_light=color_is_light(hex_col), is_saturated=color_is_saturated(hex_col),
                                      color_tendency=color_tendency(hex_col))
                    new_color.save()
                    color_list.append(new_color)
                else:
                    color_list.append(the_color[0])
            color_hex_list = [c.color_id_hex for c in color_list]
            print(color_hex_list)
            cg = Color_Groups(how_many_colors=len(color_list), group_tendency=cg_group_tendency(color_hex_list))
            cg.save()
            print(color_list)
            for col in color_list:
                print(col)
                cg.colors.add(col)
            print(cg)

    def assign_cg_to_users(self):
        all_users = User_Profile.objects.all()
        all_cgs = Color_Groups.objects.all()
        used_cgs = []

        for user in all_users:
            limit = randint(3,10)
            for i in range(0,limit):
                random_cg_id = randint(1,len(all_cgs))
                if random_cg_id not in used_cgs:
                    used_cgs.append(random_cg_id)
                    cg = Color_Groups.objects.filter(id=random_cg_id)
                    user.liked_color_groups.add()
                print((random_cg_id,used_cgs))

        for cg in all_cgs:
            if cg.id not in used_cgs:
                random_user_id = randint(1,len(all_users))
                user = User_Profile.objects.get(user_id = random_user_id)
                user.liked_color_groups.add(cg)


    def random_color(self):
        limit = Color.objects.count()
        c = Color.objects.filter(id=randint(0,limit))
        while (c.count() == 0):
            c = Color.objects.filter(id=randint(0,limit))
        return c[0]

    def id_generator(self,size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(choice(chars) for _ in range(size))

    def cg_creator(self):
        cg_list = []
        for i in range(1,100):
            #create cg
            k = randint(1,15)
            #color_obj_list = [self.random_color() for ik in range(0,k)]
            color_list = [self.random_color().color_id_hex for ik in range(0,k)]
            cg = Color_Groups(how_many_colors=len(color_list), group_tendency=cg_group_tendency(color_list))
            cg.save()
            for c in color_list:
                col = Color.objects.filter(color_id_hex = c)
                cg.colors.add(col[0])

            cg_list.append(cg)

        print(cg_list)

        users = User_Profile.objects.all()
        for user in users:
            k =randint(1,5)
            for i in range(1,k):
                user.liked_color_groups.add(cg_list[randint(1, len(cg_list)-1)])


    def add_some_data(self):
        limit = Color.objects.count()
        k =randint(1,limit)

        new_users = [self.id_generator() for i in range(0,k)]

        cg_list = []
        for i in range(1,10):
            #create cg
            k = randint(1,10)
            color_obj_list = [self.random_color() for i in range(0,k)]
            color_list = [self.random_color().color_id_hex for i in range(0,k)]
            cg = Color_Groups(how_many_colors=len(color_list), group_tendency=cg_group_tendency(color_list))
            cg.save()
            for c in color_obj_list:
                cg.colors.add(c)

            cg_list.append(cg)

        print(cg_list)

        for user_name in new_users:
            #create users
            user_obj = User.objects.create_user(username=user_name, email=None, password='1234abcd')
            user_obj.save()
            user = User_Profile(user=user_obj)
            user.save()


            k =randint(1,20)
            for i in range(1,k):
                user.liked_color_groups.add(cg_list[randint(1, len(cg_list)-1)])

    def delete_same_color_groups(self):
        cgs=Color_Groups.objects.all()
        for cg1 in cgs:
            cg1L = set(cg1.colors.all())
            #print(cg1L)
            for cg2 in cgs:
                cg2L = set(cg2.colors.all())
                if cg1L == cg2L and cg1.id > cg2.id:
                    print(cg2.id)
                    #cg2.delete()


    def add_argument(self, parser):
        pass


    def handle(self, *args, **options):
        #try:
            # your logic here
        print("I am here")
        #self.assign_cg_to_users()
        #self.delete_same_color_groups()
        '''self.read_color_sets("colorset4_clean.txt")
        self.read_color_sets("colorset_5.txt")
        self.read_color_sets("colorset_5_small.txt")
        #self.cg_creator()
        self.read_color_sets_rgb("colorset_4.txt")'''
