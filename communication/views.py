from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect                            # for loading http response
from django.contrib import  messages                            # for informing the form about some error or giving message
from django.contrib.auth.models import (User, auth)             # for verifying users
from django.shortcuts import render, redirect           # for rendering the template http file
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Messages, UserStatus
from django.http import JsonResponse
import datetime, json
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
    _owner = request.user.username
    _user = request.GET.get('user', None)
    _groupId = request.GET.get("groupId", None)

    if _user is not None:
        print("served from user")
        if _user != _owner:
            if User.objects.filter(username=_user).exists():
                if UserStatus.objects.filter(owner=_owner, reader=_user, onGroup=False).exists():
                    user_status = UserStatus.objects.filter(owner=_owner, reader=_user, onGroup=False)[0]
                    user_status.reader = _user
                    user_status.onGroup = False
                    user_status.groupId = None
                    user_status.timestamp = datetime.datetime.now()
                    user_status.save()
                else:
                    user_status = UserStatus.objects.create(owner=_owner, reader=_user, onGroup=False, groupId=None, timestamp=datetime.datetime.now())
                    user_status.save()

                return render(request, "communication/chat.html", context={"sessionOwner": _owner, "reader": _user, "onGroup": False, "groupId": None, "currentTimestamp": user_status.timestamp})

            else:
                return render(request, "communication/chaterror.html", context={"msg": "please provide a valid username to chat with"})
        else:
            return render(request, "communication/chaterror.html", context={"msg": "you can not talk to yourself, please mention name of ther user to chat with"})

    elif _groupId is not None:
        print("served from group")
        if UserStatus.objects.filter(onGroup=True, owner=_owner, groupId=_groupId).exists():
            user_status = UserStatus.objects.filter(owner=_owner, onGroup=True, groupId=_groupId)[0]
            user_status.reader = None
            user_status.onGroup = True
            user_status.groupId = _groupId
            user_status.timestamp = datetime.datetime.now()
            user_status.save()
        else:
            user_status = UserStatus.objects.create(owner=_owner, reader=None, onGroup=True, groupId=_groupId, timestamp=datetime.datetime.now())
            user_status.save()

        return render(request, "communication/chat.html", context={"sessionOwner": _owner, "reader": None, "onGroup": True, "groupId": _groupId, "groupProtection": True, "currentTimestamp": user_status.timestamp})
    else:
        return render(request, "communication/chaterror.html", context={"msg": "please go to some valid page for either talking to user or in group"})



@login_required(login_url="/")
def log_message(request):
    if request.method == "POST":
        _owner = request.user.username
        _msg = request.POST.get("msg", "")
        _reader = request.POST.get("recipient", None)
        _group_flag = True if request.POST.get("groupFlag", False) == str("True") else False
        _group_id = None if request.POST.get("group_id", None) == str('None') else int(request.POST.get("group_id", None))
        _time_stamp = request.POST.get("currentStamp", datetime.datetime.now())

        # print("==========================================================", type(request.POST.get("groupFlag", False)))
        # print(_group_flag)
        # for chcking the status of groups as protected or open.
        # if group prtection flag is true then by default the message send in group will have approved status as false since the moderator has to approve the message status to be displayed on the group.
        if (_group_flag == True):
            msg_approval_flag = False if request.POST.get("group_protection", False) == str("True") else True
        else:
            msg_approval_flag = True

        print("here owner is {} and message is {} {} {} {} {} ".format(_owner, _msg, _reader, _group_flag, _group_id, _time_stamp))
        message = Messages.objects.create(text=_msg, owner=_owner, timestamp=datetime.datetime.now(), recipient=_reader, isGroup=_group_flag, groupId=_group_id, approval_status=msg_approval_flag)
        try:
            message.save()
            print("message saved successfully")
        except :
            print("something happened and message is not saved to database")
    
    return JsonResponse('hit', safe=False)
    # return HttpResponse("yes user is logged in and user is {}".format(request.user.username))


def get_all_chats(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            all_chats = []
            typing_status_users_list = []
            status = request.POST.get("typingStatus", False)
            _owner = request.user.username
            _reader = request.POST.get("recipient", None)
            _group_flag = True if request.POST.get("groupFlag", False) == str("True") else False
            _group_id = None if request.POST.get("group_id", None) == str('None') else int(request.POST.get("group_id", None))
            _time_stamp = request.POST.get("currentStamp", datetime.datetime.now())

            print("========>>>>>>>>>>>>here owner is {} and message is {} {} {} {} ".format(_owner, _reader, _group_flag, _group_id, _time_stamp))

            update_typing_status = UserStatus.objects.filter(owner=_owner)[0]
            update_typing_status.typing_status = False if status == str("false") else True
            update_typing_status.reader = _reader
            update_typing_status.onGroup = _group_flag
            update_typing_status.groupId = _group_id
            update_typing_status.timestamp = datetime.datetime.now()
            update_typing_status.save()

            if _group_flag:
                chats = Messages.objects.all().filter(isGroup=True, groupId=_group_id, approval_status=True).order_by('-timestamp')[:20][::-1]
                typing_status = UserStatus.objects.all().filter(onGroup=True, groupId=_group_id, typing_status=True)
                print("chat is ==============>>>>>>>>", chats)
                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    all_chats.append(dict_object)

                for s in typing_status:
                    typing_obj = s.get_status()
                    typing_status_users_list.append(typing_obj)

                print(list(typing_status_users_list))
                return JsonResponse({"chats": all_chats, "typing_status": typing_status_users_list, "group_flag": True}, safe=False)

            else:
                chats = Messages.objects.all().filter(isGroup=False, owner=_owner, recipient=_reader).union(Messages.objects.all().filter(isGroup=False, owner=_reader, recipient=_owner)).order_by('-timestamp')[:20][::-1]
                # print("chat is ==============>>>>>>>>", chats)
                typing_status = UserStatus.objects.all().filter(onGroup=False, owner=_reader)[0]

                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    all_chats.append(dict_object)

                print(list(all_chats))
                return JsonResponse({"chats": all_chats, "typing_status": typing_status.get_typing_status(), "group_flag": False}, safe=False)

        else:
            return JsonResponse({"message": "sigin first to see the message"}, safe=False)
    
    else:
        return JsonResponse({"message": "Please do request with a valid request type and verified account to get the service"}, safe=False)


def load_previous_messages(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            all_chats = []
            msg_data = json.loads(request.POST.get("dataObject"))
            # print(msg_data['id'], msg_data['text'])
            _owner = request.user.username
            _reader = request.POST.get("recipient", None)
            _group_flag = True if request.POST.get("groupFlag", False) == str("True") else False
            _group_id = None if request.POST.get("group_id", None) == str('None') else int(request.POST.get("group_id", None))

            if _group_flag:
                chats = Messages.objects.all().filter(isGroup=True, groupId=_group_id, timestamp__lte=msg_data['normal_timestamp'], approval_status=True).order_by('-timestamp')[:20][::-1]
         
                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    # dict_object = model_to_dict(chat)
                    all_chats.append(dict_object)
            
                return JsonResponse({"chats": all_chats, "group_flag": True}, safe=False)

            else:
                chats = Messages.objects.all().filter(isGroup=False, owner=_owner, recipient=_reader, timestamp__lte=msg_data['normal_timestamp']).union(Messages.objects.all().filter(isGroup=False, owner=_reader, recipient=_owner, timestamp__lte=msg_data['normal_timestamp'])).order_by('-timestamp')[:20][::-1]

                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    # dict_object = model_to_dict(chat)
                    all_chats.append(dict_object)

                print(list(all_chats))
                return JsonResponse({"chats": all_chats, "group_flag": False}, safe=False)


            # return JsonResponse({"message": "sent successfully"}, safe=False)
        else:
            return HttpResponse("sigin first to see the message")
    
    else:
        return HttpResponse("Please do a post request with verified account to get the service")

@login_required(login_url="/")
def pre_moderation_view(request):
    _owner = request.user.username
    _groupId = request.GET.get("groupId", None)
    _msgs_per_page = request.GET.get("msgLimit", 20)

    if _groupId is not None:
        group_ids = _groupId.split('+')
        for ids in range(len(group_ids)):
            if group_ids[ids] == "":
                del group_ids[ids]

        print(group_ids)
        return render(request, "communication/preModeratorView.html", context={"groupIds": group_ids, "msgLimit":_msgs_per_page, "sessionOwner": _owner})
    else:
        return HttpResponse("Please provide group Ids to look into which.")


def get_pre_moderator_chats(request):
    if request.method == "POST":
        if (request.user.is_authenticated and request.user.is_staff):
            msg_limit = int(request.POST.get("msgLimit", 20))
            group_ids_list = json.loads(request.POST.get("groupIds", None))
            all_chats = []
            
            print("grop listy is ", group_ids_list)
            print("integer is ", int(group_ids_list[0]))
            chats = Messages.objects.all().filter(isGroup=True, groupId=int(group_ids_list[0]), approval_status=False).order_by('timestamp')
            for i in range(1, len(group_ids_list)):
                if (len(chats)>=msg_limit):
                    print("i am going to break and the length of chats is", len(chats))
                    break
                chats = chats.union(Messages.objects.all().filter(isGroup=True, groupId=int(group_ids_list[i]), approval_status=False).order_by('timestamp'))
                    
            for chat in chats:
                dict_object = chat.get_items_as_dict()
                all_chats.append(dict_object)

            print(all_chats)
            print("length of chats is ", len(chats))
            return JsonResponse({"chats": all_chats}, safe=False)

        else:
            return JsonResponse({"message": "sigin first to load the group messages"}, safe=False)
    
    else:
        return JsonResponse({"message": "Please do request with a valid request type and verified account to get the service"}, safe=False)


def approve_pre_moderator_msgs(request):
    if request.method == "POST":
        if (request.user.is_authenticated and request.user.is_staff):
            msg_data = json.loads(request.POST.get("msg_data", None))
            print("=============================\n", msg_data)
            for msg in msg_data:
                msg_delete_status = msg.get("deleteStatus", False)
                if msg_delete_status:
                    chat = Messages.objects.get(isGroup=True, groupId=int(msg.get("group_id", 0)), approval_status=False, id__exact=msg["id"])
                    print(chat)
                    chat.delete()
                    continue
                msg_approval_status = msg.get("status", False)
                if msg_approval_status:
                    chat = Messages.objects.get(isGroup=True, groupId=int(msg.get("group_id", 0)), approval_status=False, id__exact=msg["id"])
                    chat.approval_status = True
                    chat.save()

            return JsonResponse({"message": "Approval message list executed succssfully"}, safe=False)

        else:
            return JsonResponse({"message": "sigin first to load the group messages"}, safe=False)
    
    else:
        return JsonResponse({"message": "Please do request with a valid request type and verified account to approve the messages"}, safe=False)
    
    # return render(request, "communication/preModeratorView.html", context={"sessionOwner": _owner})

    
    # if _groupId is not None:
    #     group_ids = _groupId.split(',')
    #     print("served from group")
    #     chats = Messages.objects.all().filter(isGroup=True, groupId=_group_id, approval_status=True).order_by('-timestamp')[:20][::-1]
    #     typing_status = UserStatus.objects.all().filter(onGroup=True, groupId=_group_id, typing_status=True)
    #     # print("chat is ==============>>>>>>>>", chats)
    #     for chat in chats:
    #         dict_object = chat.get_items_as_dict()
    #         all_chats.append(dict_object)

    #     for s in typing_status:
    #         typing_obj = s.get_status()
    #         typing_status_users_list.append(typing_obj)

    #     print(list(typing_status_users_list))
    #     return JsonResponse({"chats": all_chats, "typing_status": typing_status_users_list, "group_flag": True}, safe=False)
        # if UserStatus.objects.filter(onGroup=True, owner=_owner, groupId=_groupId).exists():
        #     user_status = UserStatus.objects.filter(owner=_owner, onGroup=True, groupId=_groupId)[0]
        #     user_status.reader = None
        #     user_status.onGroup = True
        #     user_status.groupId = _groupId
        #     user_status.timestamp = datetime.datetime.now()
        #     user_status.save()
        # else:
        #     user_status = UserStatus.objects.create(owner=_owner, reader=None, onGroup=True, groupId=_groupId, timestamp=datetime.datetime.now())
        #     user_status.save()

        # return render(request, "communication/chat.html", context={"sessionOwner": _owner, "reader": None, "onGroup": True, "groupId": _groupId, "currentTimestamp": user_status.timestamp})
    # else:
    #     return render(request, "communication/chaterror.html", context={"msg": "please go to some valid page for either talking to user or in group"})
        


    # if request.method == "POST":
    #     if request.user.is_staff:
    #         all_chats = []
    #         msg_data = json.loads(request.POST.get("dataObject"))
    #         # print(msg_data['id'], msg_data['text'])
    #         _owner = request.user.username
    #         _reader = request.POST.get("recipient", None)
    #         _group_flag = True if request.POST.get("groupFlag", False) == str("True") else False
    #         _group_id = None if request.POST.get("group_id", None) == str('None') else int(request.POST.get("group_id", None))

    #         if _group_flag:
    #             chats = Messages.objects.all().filter(isGroup=True, groupId=_group_id, timestamp__lte=msg_data['normal_timestamp']).order_by('-timestamp')[:20][::-1]
         
    #             for chat in chats:
    #                 dict_object = chat.get_items_as_dict()
    #                 # dict_object = model_to_dict(chat)
    #                 all_chats.append(dict_object)
            
    #             return JsonResponse({"chats": all_chats, "group_flag": True}, safe=False)

    #         else:
    #             chats = Messages.objects.all().filter(isGroup=False, owner=_owner, recipient=_reader, timestamp__lte=msg_data['normal_timestamp']).union(Messages.objects.all().filter(isGroup=False, owner=_reader, recipient=_owner, timestamp__lte=msg_data['normal_timestamp'])).order_by('-timestamp')[:20][::-1]

    #             for chat in chats:
    #                 dict_object = chat.get_items_as_dict()
    #                 # dict_object = model_to_dict(chat)
    #                 all_chats.append(dict_object)

    #             print(list(all_chats))
    #             return JsonResponse({"chats": all_chats, "group_flag": False}, safe=False)


    #         return JsonResponse({"message": "sent successfully"}, safe=False)
    #     else:
    #         return HttpResponse("sigin first to see the message", content_type='application/json')
    
    # else:
    #     return HttpResponse("Please do a post request with verified account to get the service", content_type='application/json')

