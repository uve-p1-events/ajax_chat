from django.http import HttpResponse, HttpResponseRedirect                            # for loading http response
from django.contrib import  messages                            # for informing the form about some error or giving message
from django.contrib.auth.models import (User, auth)             # for verifying users
from django.shortcuts import render, redirect           # for rendering the template http file
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from .models import Messages
from django.http import JsonResponse
# from django.forms.models import model_to_dict

# Create your views here.
def registerUser(request):
    if(request.method == "POST"):
        login_name = request.POST['loginName']
        email = request.POST['email']
        userPassword = request.POST['loginpass']

        if (User.objects.filter(username=login_name).exists()):                 
            messages.info(request, "Username must be unique", fail_silently=True)
            print("Username must be unique")
            return HttpResponseRedirect(reverse('registerUser'))

        elif (User.objects.filter(email=email).exists()):                       
            messages.info(request, "Email must be unique", fail_silently=True)
            print("Email must be unique")
            return HttpResponseRedirect(reverse('registerUser'))

        else:                                                                   
            if(userPassword.isalnum()):                                         
                messages.info(request, "Password must be alphanumeric", fail_silently=True)
                return HttpResponseRedirect(reverse('registerUser'))
            elif(len(userPassword) <8):                                         
                messages.info(request, "Password must be of least 8 charechters in length", fail_silently=True)
                return HttpResponseRedirect(reverse('registerUser'))
            else:                                                               
                print("regitsered with {} and {}".format(login_name, userPassword))
                user = User.objects.create_user(username=login_name, password=userPassword, email=email)
                user.save()
                print("user created succesfuly")
                return HttpResponseRedirect(reverse('loginUser'))
               
        
    else:
        return render(request, 'communication/registeration.html')

# abhyam123@admin
def loginUser(request):
    print(request)
    if(request.method == "POST"):
        login_id = request.POST['loginid']
        password = request.POST['loginpass']

        print(login_id, password)
        user = auth.authenticate(username=login_id, password=password)
        print("user is ", user)
        if user is not None:
            auth.login(request, user)
            print("user is verified")
            return HttpResponseRedirect(reverse('chatwindow'))
        else:
            messages.info(request, "Invalid Credentials or user doesnot exsist")
            return HttpResponseRedirect(reverse('loginUser'))
    else:
        return render(request, 'communication/login.html')

def logout(request):
    auth.logout(request)
    print("user loggedout successfully")
    return HttpResponseRedirect(reverse('loginUser'))


@login_required(login_url="/")
def chat(request):
    return render(request, "communication/chat.html")


@login_required(login_url="/")
def log_message(request):
    if request.method == "POST":
        _owner = request.POST.get("owner", None)
        _msg = request.POST.get("msg", "")
        
        print("here owner is {} and message is {}".format(_owner, _msg))
        message = Messages.objects.create(text=_msg, owner=_owner, timestamp=datetime.datetime.now())
        try:
            message.save()
        except :
            print("something happened and message is not saved to database")
    
    return JsonResponse('hit', safe=False)
    # return HttpResponse("yes user is logged in and user is {}".format(request.user.username))


def get_all_chats(request):
    if request.user.is_authenticated:
        all_chats = []
        status = request.POST.get("typingStatus", False)
        _owner = request.POST.get("owner", False)

        s = Messages.objects.filter(owner=_owner)
        for t in s:
            t.status = False if status == str("false") else True
            t.save()

        chats = Messages.objects.all().order_by('-timestamp')[:20][::-1]

        for chat in chats:
            dict_object = chat.get_items_as_dict()
            # dict_object = model_to_dict(chat)
            all_chats.append(dict_object)
        # all_chats = model_to_dict(chats)

        print(list(all_chats))
        print("type of chat pbject is", type(all_chats))
        return JsonResponse(all_chats, safe=False)
    else:
        return HttpResponse("sigin first to see the message", content_type='application/json')


def test(request):
    return render(request, "communication/chatting.html")