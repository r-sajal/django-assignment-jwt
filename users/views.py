from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated 

import requests
from django.contrib.auth import login
from django.contrib.auth import authenticate
import collections 
import json

  
# Create your views here.

def verifytoken(currenttoken):
    print("------------------verify--------------------------")
    try:
        params = {'token':currenttoken}
        p = requests.post('http://localhost:8000/api-token-verify/', data=params)
        print(p.text)
        if p.text == currenttoken:
            return True
        else:
            return False
    except:
        return False

def converttorefresh(currenttoken):
    print("------------------refresh--------------------------")
    
    try:
        params = {'token':currenttoken}
        p = requests.post('http://localhost:8000/api-token-refresh/', data=params)
        print(p.text)
        tokennow = json.loads(p.text)['token']
        print(tokennow)
        return tokennow
    except:
        return None

    



def Showdata(request,*args):
    print("----------------------------------------Showdata-----------------------------------------------")

    
    new_token = None
    if len(args)>0:
        print(args)
        checktoken = converttorefresh(args[0])
        if checktoken!=None:
            new_token = checktoken
            print(new_token)
        else:
            redirect('/')
        


    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    givendata = response.json()
    new_dict = {}
    for i,j in enumerate(givendata):
        new_dict[i] = j
    
    return render(request, 'showdata.html',context =  {"context":new_dict,'token':new_token})


def loginpage(request):
    print("----------------------------------------loginpage-----------------------------------------------")
    return render(request,'userlogin.html')



def loginrequest(request):
    print("----------------------------------------loginrequest-----------------------------------------------")
    
    try:
        if(request.method == "POST"):

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            
            if user is not None:
                r = requests.post('http://127.0.0.1:8000/api-token-auth/', data={'username':username,'password':password})    
                r = json.loads(r.text)
                params = {'token':r['token']}
                print(params)

                p = requests.post('http://localhost:8000/api-token-verify/', data=params)
                print(p.text)
                if json.loads(p.text)['token'] == r['token']:
                    return Showdata(request,r['token'])
                    # return redirect('/showdata',{'currenttoken':r['token']})
            else:
                return redirect('/')  
        else:
            return redirect('/')
        
    except:
        return redirect('/')

def logout(request):
    return redirect('/')


def register(request):
    if(request.method == "POST"):
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            user = User.objects.create_user(username = username,password=password)
            user.save()
            r = requests.post('http://127.0.0.1:8000/api-token-auth/', data={'username':username,'password':password})    
            r = json.loads(r.text)
            print(type(r))

            params = {'token':r['token']}
                
            p = converttorefresh(r['token'])
            # print(p.text)

            if p!=None:
                return Showdata(request,p)

        except:
            return redirect('/register')
        # return render(request,'shop/')
        return Showdata(request)
    else:
        return render(request,'register.html')