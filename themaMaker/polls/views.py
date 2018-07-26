from django.shortcuts import render
from django.http import JsonResponse
import re
import webcolors
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

from polls.models import *
from polls import color
from .suggestions import update_clusters
from random import randint
from django.core.management import call_command
import cv2
from sklearn.cluster import KMeans
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


class apiView(APIView):

    authentication_classes = (TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print(request.user)
        usernames = [user.username for user in User.objects.all()]
        return JsonResponse({"users": usernames})

    def post(self, request, *args, **kwargs):
        operation = request.data["operation"]
        response = {}

        if operation == "login":
            uname = request.data["username"]
            passw = request.data["password"]
            print("posttayız")
            # print(request.data)
            print((uname,passw))

            s = LoginView()
            response = LoginView.login(s, uname,passw, request)

            cg_list = []
            if response["message"] == "done":
                try:
                    token = Token.objects.get(user=User.objects.get(username=uname))
                except:
                    token = Token.objects.create(user=User.objects.get(username=uname))
                response["token"] = token.key
                user_obj = User.objects.get(username=uname)
                user = User_Profile.objects.get(user=user_obj)
                cgs = user.liked_color_groups.all()
                for cg in cgs:
                    cols = cg.colors.all()
                    cols_id = cg.id
                    col_list = []
                    for c in cols:
                        col_list.append(c.color_id_hex)
                    cg_list.append({"id": cols_id, "list": col_list})

                response["liked_cg"] = cg_list

        elif operation == "recommend":
            print("recommendation operation")
            print(request.user)
            r = RecommendationView()
            return r.user_recommendation_list(request)

        elif operation == "dominantColors":
            print("dominantColors operation")
            print(request.user)
            print(request.data)
            print(request.data["photo"])
            instance = File(name_field=request.data["photo"].name, file_field=request.data["photo"])
            instance.save()
            u = UploadView()
            print(instance.file_field.name)
            cols = u.dominantColors(instance.file_field.name,5)
            colors = [webcolors.rgb_to_hex(tuple(t)) for t in cols]
            response["dominantColors"] = colors

        elif operation == "delete_cg":
            print("delete_cg operation")
            print(request.user)
            print(request.data)

            uname = request.user.username
            user_obj = User.objects.get(username=uname)
            user = User_Profile.objects.get(user=user_obj)
            cg_id = int(request.data["cg_id"])
            color_set = Color_Groups.objects.filter(id=cg_id)
            user.liked_color_groups.remove(color_set[0])
            cg_list = []
            cgs = user.liked_color_groups.all()
            for cg in cgs:
                cols = cg.colors.all()
                cols_id = cg.id
                col_list = []
                for c in cols:
                    col_list.append(c.color_id_hex)
                cg_list.append({"id": cols_id, "list": col_list})

            response["liked_cg"] = cg_list
            response["deleted"] = "true"
            #response["token"] = Token.objects.get(user=User.objects.get(username=uname))

        elif operation == "add_cg":
            print("add_cg operation")
            print(request.data)
            s = SaveView()
            s.add_cg_to_user(request.data["colors"], request.user.username)

            cg_list = []
            user = User_Profile.objects.get(user = request.user)
            cgs = user.liked_color_groups.all()
            for cg in cgs:
                cols = cg.colors.all()
                cols_id = cg.id
                col_list = []
                for c in cols:
                    col_list.append(c.color_id_hex)
                cg_list.append({"id": cols_id, "list": col_list})

            response["liked_cg"] = cg_list

        return JsonResponse(response)

class UploadView(View):

    def get(self, request):
        print("deneme sadece")
        return render(request,'more.html', {"files": "file_list" })

    def dominantColors(self,img,cluster=3):

        if img[:8] == "uploads/":
            img = cv2.imread('/Users/hande/Desktop/Project/themaMaker/' + img)
        else:
            #open image
            img = cv2.imread('/Users/hande/Desktop/Project/themaMaker/uploads/'+ img)

        if img is None:
            print("None img")
            return

        #convert to RGB from BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        #save image after operations
        #self.IMAGE = img

        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = cluster)
        kmeans.fit(img)

        #getting the colors as per dominance order
        colors = kmeans.cluster_centers_

        #save labels
        labels = kmeans.labels_

        return colors.astype(int)

    def post(self, request, *args, **kwargs):

        files=request.FILES.getlist("filee")
        file_list=[]
        for f in files:
            css_file_name = re.findall('.*\.css$', f.name)
            jpg_file_name = re.findall('.*\.jpg$|.*\.JPG$', f.name)

            if len(css_file_name) == 0 and len(jpg_file_name) == 0:
                return
            else:
                instance = File(name_field=f.name ,file_field=f)
                instance.save()

                if len(css_file_name)>0:
                    with open('/Users/hande/Desktop/Project/themaMaker/uploads/'+css_file_name[0], newline='') as myFile:
                        colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)

                    colors = [elem for elem in colors if (elem != "transparent")]

                    for x in range(0,len(colors)):
                        if ( colors[x][0] != '#'):
                            temp = webcolors.html5_parse_legacy_color(colors[x])
                            temp_r = str(hex(temp.red))[2:] if(len(str(hex(temp.red)))==4) else ('0'+ str(hex(temp.red))[2])
                            temp_g = str(hex(temp.green))[2:] if(len(str(hex(temp.green)))==4) else ('0'+ str(hex(temp.green))[2])
                            temp_b = str(hex(temp.blue))[2:] if(len(str(hex(temp.blue)))==4) else ('0'+ str(hex(temp.blue))[2])
                            colors[x] = '#' + temp_r + temp_g + temp_b

                        elif ( len(colors[x]) < 7 ):
                            temp_r = colors[x][1]
                            temp_g = colors[x][2]
                            temp_b = colors[x][3]
                            colors[x] = '#'+ temp_r + temp_r + temp_g + temp_g + temp_b + temp_b

                else:
                    cols = self.dominantColors(jpg_file_name[0], 5 )
                    colors = [webcolors.rgb_to_hex(tuple(t)) for t in cols]
                    #print(colors)

                color_no_list = list(range(len(colors)))
                print(instance.file_field.name)
                file_list.append({"name": f.name,"uploaded_fname": instance.file_field.path,"color_list":colors, "color_no_list": color_no_list })

        return render(request,'more.html', {"files": file_list })


class LoginView(View):

    def liked_cg(self, request):
        c = {};
        c["liked_cg"]=[]
        if request.user.is_authenticated:
            #c["liked_cg"]
            cg_list =[]
            user_nname = request.user.username
            user_obj = User.objects.get(username = user_nname)
            user = User_Profile.objects.get(user = user_obj)
            cgs = user.liked_color_groups.all()
            for cg in cgs:
                cols = cg.colors.all()
                cols_id = cg.id
                col_list = []
                for c in cols:
                    col_list.append(c)
                cg_list.append({"id": cols_id, "list" :col_list})

            c = {"liked_cg":cg_list}
        return c

    def get(self, request):
        c = self.liked_cg(request)

        return render(request,'login.html',c)

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        return JsonResponse(self.login(username,password,request))

    def login(self, username, password, request):
        c = {}
        user = User.objects.filter(username= username)
        if user.count() == 0:
            c["message"] = "There is not such a user with username: "+ username
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                #c = self.liked_cg(request)
                print(c)
                c["message"] = "done"
                print(c)
                #return render(request,'index.html',c)
            else:
                c["message"] = "Your username or password is wrong, try again!"
                #return render(request,'login.html',c)
        return c


def logout_view(request):
    logout(request)
    return JsonResponse({"successfully_logged_out": "yes"})

def delete_cg_view(request):
    user_nname = request.user.username
    user_obj = User.objects.get(username = user_nname)
    user = User_Profile.objects.get(user = user_obj)
    cg_id = int(request.POST["id"])
    color_set = Color_Groups.objects.filter(id=cg_id)
    user.liked_color_groups.remove(color_set[0])
    return JsonResponse({"saved": "deleted"})

def show_cg_view(request):
    colors_list = []
    if(request.method == 'POST'):
        cg_id = request.POST["id"]
        cg = Color_Groups.objects.filter(id=cg_id)
        if(cg.count() != 0):
            colors = cg[0].colors.all()
            colors_list = [c.color_id_hex for c in colors]
    return JsonResponse({"colors": colors_list})


class SaveView(View):

    def get_color_hex_list(self,request):
        data = request.POST.get("datas",None);

        colors = re.findall(r'favcolor=%23([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9])',data, re.DOTALL) #color hexes but without "#"
        colors_hex = [ "#"+elem for elem in colors] #add '#' to the beginning of the color codes
        for color_hex in colors_hex:
            database_color = Color.objects.filter(color_id_hex=color_hex)
            if database_color.count() == 0:
                color_dic = {"color_id_hex": color_hex,"color_tendency": color.color_tendency(color_hex), "is_light": color.color_is_light(color_hex), "is_saturated":color.color_is_saturated(color_hex)}
                c = Color(**color_dic)
                c.save()
            else:
                c = database_color[0]
        return colors_hex

    def add_cg_to_user(self, colors_hex, username):
        color_set = Color_Groups(how_many_colors=len(colors_hex), group_tendency=color.cg_group_tendency(colors_hex))
        color_set.save()
        for color_hex in colors_hex:
            database_color = Color.objects.filter(color_id_hex=color_hex)
            if database_color.count() == 0:
                color_dic = {"color_id_hex": color_hex, "color_tendency": color.color_tendency(color_hex),
                             "is_light": color.color_is_light(color_hex),
                             "is_saturated": color.color_is_saturated(color_hex)}
                c = Color(**color_dic)
                c.save()
            else:
                c = database_color[0]
            color_set.colors.add(c)

        all_cgs = Color_Groups.objects.all()
        for cg in all_cgs:
            if set(color_set.colors.all()) == set(cg.colors.all()) and cg.id != color_set.id:
                color_set.delete()
                color_set = cg

        user_obj = User.objects.get(username=username)
        user = User_Profile.objects.get(user=user_obj)
        users_sets = user.liked_color_groups.all()
        print(color_set)
        if color_set not in users_sets:
            user.liked_color_groups.add(color_set)

    def post(self, request, *args, **kwargs):

        colors_hex = self.get_color_hex_list(request)

        if request.user.is_authenticated:
            user_nname = request.user.username
            self.add_cg_to_user(colors_hex, user_nname)

        #update_clusters()
        return JsonResponse({"done": "data","refresh": "yes"})


class SignUpView(View):
    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']

        taken_name = User.objects.filter(username=username)

        if taken_name.count() == 0:
            user_obj = User.objects.create_user(username=username,email=None,password=password)
            user_obj.save()
            user = User_Profile(user=user_obj)
            user.save()
            us = authenticate(request, username=username, password=password)
            login(request, us)
            return JsonResponse({"saved": "registered"})

        else:
            return JsonResponse({"saved": "same_name_taken"})


class RecommendationView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.POST["which"] == "locked_recom": #make recommendation according to locked colors
                print(request.POST["locked"])
                print("oki doki")
                return self.locked_recom(request)
                #return JsonResponse({'username': "",'color_list': ""})
            else:
                return self.user_recommendation_list(request)
        else:
            return JsonResponse({'username': "",'color_list': ""})

    def locked_recom(self,request):
        # get locked colors and process them
        s = SaveView()
        colors_hex = SaveView.get_color_hex_list(s,request)
        print(colors_hex)
        locked = request.POST["locked"]
        locked = list(filter(lambda x: (x != "[") and (x!="]") and (x !="'") and (x!=",") and (x!=" ") and (x!='"'), locked))
        locked_color_indexes = [int(t) for t in locked]
        print("locked_colors")
        print(locked_color_indexes)
        locked_colors = [colors_hex[t] for t in locked_color_indexes]
        print(locked_colors)

        # get clusters of clors
        clusters = []
        color_groups = []
        for c in locked_colors:
            if (Color.objects.filter(color_id_hex=c).count() != 0):
                color_obj = Color.objects.get(color_id_hex=c)
                color_cluster = set(color_obj.color_cluster_set.all())
                cgs = set(color_obj.color_groups_set.all())
                if len(color_cluster) == 0:
                    call_command('recom')
                    color_cluster = set(color_obj.color_cluster_set.all())
            else: #if the color doesn't exist in db
                color_obj = Color(color_id_hex = c, is_light= color.color_is_light(c), is_saturated= color.color_is_saturated(c), color_tendency = color.color_tendency(c))
                color_obj.save()
                call_command('recom')
                color_cluster = set(color_obj.color_cluster_set.all())

            clusters.append(color_cluster)
            color_groups.append(cgs)

        # find the common clusters
        mutual_clusters = set.intersection(*clusters)
        mutual_cgs = set.intersection(*color_groups)
        print("mutual clusters: --------------------------")
        print(mutual_clusters)

        print("mutual cgs: --------------------------")
        print(mutual_cgs)

        # if there is no mutual cluster, update color clusters
        if len(mutual_clusters) == 0:
            print(clusters)
            return self.user_recommendation_list(request)

        # get all the colors in mutual_clusters in nested list. !!! redundant work here fix later
        recommended_color_lists = [cluster.colors.all() for cluster in mutual_clusters]
        print("############################")
        print(recommended_color_lists)
        print("############################")
        candidate_list = recommended_color_lists[randint(0,len(recommended_color_lists)-1)]
        color_list_pre = [color.color_id_hex for color in candidate_list]

        #select random colors from the selected_cluster
        color_list = [color_list_pre[randint(0,len(color_list_pre)-1)] for i in range(0,5)]
        print(color_list)
        return JsonResponse({'username': request.user.username ,'color_list': color_list})


    def user_recommendation_list(self,request):
        # get request user reviewed colors
        user = User.objects.filter(username=request.user.username)
        if user.count() == 0:
            return JsonResponse({'username': request.user.username,'color_list': []})
        user_p = User_Profile.objects.filter(user=user[0])
        if user_p.count() == 0:
            return JsonResponse({'username': request.user.username, 'color_list': []})
        user_cgs = user_p[0].liked_color_groups.all()
        #user_reviews_color_ids = [cg.id for cg in user_cgs]

        # get request user cluster name (just the first one right now)
        try:
            #update_clusters()
            user_cluster_name = \
                User.objects.get(username=request.user.username).cluster_set.first().name
        except: # if no cluster assigned for a user, update clusters
            update_clusters()
            user_cluster_name = \
                User.objects.get(username=request.user.username).cluster_set.first().name

        # get usernames for other members of the cluster
        user_cluster_other_members = \
            Cluster.objects.get(name=user_cluster_name).users \
                .exclude(username=request.user.username).all()
        #other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))


        # get reviews by those users, excluding colors reviewed by the request user
        user_profiles = [User_Profile.objects.get(user=user) for user in user_cluster_other_members]
        color_groups = []
        [color_groups.append(up.liked_color_groups.all()) for up in user_profiles]

        quer = color_groups[randint(0,len(color_groups)-1)]
        chosen_cg = color_objs = quer[randint(0,len(quer)-1)]
        color_objs = chosen_cg.colors.all()
        color_list = [ c.color_id_hex for c in color_objs ]

        return JsonResponse(
            {'username': request.user.username,'color_list': color_list, 'cg_id': chosen_cg.id}
        )