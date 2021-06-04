from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect                            # for loading http response
from django.contrib import  messages                                                                        # for informing the form about some error or giving message
from django.contrib.auth.models import (User, auth)                                                         # for verifying users
from django.shortcuts import render, redirect                                                               # for rendering the template http file
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Messages, UserStatus, Groups
from django.http import JsonResponse
import datetime, json
# from django.forms.models import model_to_dict

# Create your views here.
def registerUser(request):
    if(request.method == "POST"):
        login_name = request.POST['loginName']
        email = request.POST['email']
        userPassword = request.POST['loginpass']
        confirmPass = request.POST['confirmloginpass']

        if userPassword == confirmPass:
            if (User.objects.filter(username=login_name).exists()):                 
                messages.info(request, "Username must be unique", fail_silently=True)
                print("Username must be unique")
                return HttpResponseRedirect(reverse('loginUser'))

            elif (User.objects.filter(email=email).exists()):                       
                messages.info(request, "Email must be unique", fail_silently=True)
                print("Email must be unique")
                return HttpResponseRedirect(reverse('loginUser'))

            else:                                                                   
                if(userPassword.isalnum()):                                         
                    messages.info(request, "Password must be alphanumeric", fail_silently=True)
                    return HttpResponseRedirect(reverse('loginUser'))
                elif(len(userPassword) <8):                                         
                    messages.info(request, "Minimum 8 charechters required in Password", fail_silently=True)
                    return HttpResponseRedirect(reverse('loginUser'))
                else:                                                               
                    # print("regitsered with {} and {}".format(login_name, userPassword))
                    user = User.objects.create_user(username=login_name, password=userPassword, email=email)
                    user.save()
                    print("user created succesfuly")
                    # now logging in User
                    user = auth.authenticate(username=login_name, password=userPassword)
                    if user is not None:
                        auth.login(request, user)
                        print("user is verified")
                        return HttpResponseRedirect(reverse('chatwindow'))
                    else:
                        messages.info(request, "Login Failed, Please try again.")
                        return HttpResponseRedirect(reverse('loginUser'))

        else: 
            messages.info(request, "Password Doesn't Matched", fail_silently=True)
            return HttpResponseRedirect(reverse('loginUser'))
            
    else:
        return render(request, 'communication/login_signup.html')


# abhyam123@admin
def loginUser(request):
    if(request.method == "POST"):
        login_id = request.POST['loginid']
        password = request.POST['loginpass']

        user = auth.authenticate(username=login_id, password=password)
        if user is not None:
            auth.login(request, user)
            print("user is verified")
            return HttpResponseRedirect(reverse('chatwindow'))
        else:
            messages.info(request, "Invalid Credentials or user doesnot exsist")
            return HttpResponseRedirect(reverse('loginUser'))
    else:
        return render(request, 'communication/login_signup.html')

@login_required(login_url="/")
def logout(request):
    auth.logout(request)
    print("user loggedout successfully")
    return HttpResponseRedirect(reverse('loginUser'))


@login_required(login_url="/")
def chat(request):
    _owner = request.user.username
    _user = request.GET.get('user', None)
    _groupId = request.GET.get("groupId", None)

    all_users = User.objects.all()
    all_groups = Groups.objects.all().filter(groupStatus=True)
    # all_user_status = UserStatus.objects.all()
    
    return render(request, "communication/chat.html", context={"allUsers": all_users, "allGroups": all_groups, "sessionOwner": _owner})


@login_required(login_url="/")
def getChatUserInfo(request):
    _owner = request.user.username
    _user = request.POST.get('user', None)

    if _user != _owner:
        print("recipt user is ", _user)
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

            return JsonResponse({"sessionOwner": _owner, "reader": _user, "onGroup": False, "groupId": 123, "currentTimestamp": user_status.timestamp})

        else:
            return JsonResponse({"message": "please provide a valid username to chat with"}, safe=False)
    else:
        return JsonResponse({"message": "you can not talk to yourself, please mention name of ther user to chat with"}, safe=False)


@login_required(login_url="/")
def getGroupChatInfo(request):
    print("served from group")
    _owner = request.user.username
    _group_id = request.POST.get("groupId", None)
    _group_name = request.POST.get("groupName", None)
    print(_group_id, _group_name)
    if (Groups.objects.filter(groupId=_group_id, groupName=_group_name).exists() and _group_id is not None):
        groupDetails = Groups.objects.filter(groupId=_group_id, groupName=_group_name)[0]

        if (groupDetails.groupStatus == False):
            return JsonResponse({"message": "This group is now deactivated due to some reason", "status": False}, safe=False)

        if UserStatus.objects.filter(onGroup=True, owner=_owner, groupId=_group_id).exists():
            user_status = UserStatus.objects.filter(owner=_owner, onGroup=True, groupId=_group_id)[0]
            user_status.reader = None
            user_status.onGroup = True
            user_status.groupId = _group_id
            user_status.timestamp = datetime.datetime.now()
            user_status.save()
        else:
            user_status = UserStatus.objects.create(owner=_owner, reader=None, onGroup=True, groupId=_group_id, timestamp=datetime.datetime.now())
            user_status.save()

        return JsonResponse({"sessionOwner": _owner, "reader": None, "onGroup": True, "groupId": _group_id, "groupProtection": groupDetails.protectedStatus, "currentTimestamp": user_status.timestamp}, safe=False)

    else:
        return JsonResponse({"message": "Please send the valid credentials of the group"}, safe=False)


@login_required(login_url="/")
def log_message(request):
    print("request value is ==>> ", request)
    if request.method == "POST":
        _owner = request.user.username
        _msg = request.POST.get("msg", "")
        _reader = request.POST.get("recipient", None)
        _group_flag = True if request.POST.get("groupFlag", False) == str("true") else False
        _group_id = None if (request.POST.get("group_id", None) == str('None') or request.POST.get("group_id", None) == str('')) else request.POST.get("group_id", None)
        _time_stamp = request.POST.get("currentStamp", datetime.datetime.now())

        # print("==========================================================", type(request.POST.get("groupFlag", False)))
        # print(_group_flag)
        # for chcking the status of groups as protected or open.
        # if group prtection flag is true then by default the message send in group will have approved status as false since the moderator has to approve the message status to be displayed on the group.
        if (_group_flag == True):
            print("group protection variable ", request.POST.get("group_protection", False))
            msg_approval_flag = False if request.POST.get("group_protection", False) == str("true") else True
        else:
            msg_approval_flag = True

        print("here owner is {} and message is {} {} {} {} {} ".format(_owner, _msg, _reader, _group_flag, _group_id, _time_stamp))
        message = Messages.objects.create(text=_msg, owner=_owner, timestamp=datetime.datetime.now(), recipient=_reader, isGroup=_group_flag, groupId=_group_id, approval_status=msg_approval_flag)
        try:
            message.save()
            print("message saved successfully")
        except :
            print("something happened and message is not saved to database")
        
        return JsonResponse({"message":"Message sent Successfully"}, safe=False)

    else:
        return JsonResponse({"message":"Please do post request to this link to perform the desire task i.e. to send your message"}, safe=False)
    # return HttpResponse("yes user is logged in and user is {}".format(request.user.username))



def get_all_chats(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            all_chats = []
            typing_status_users_list = []
            status = request.POST.get("typingStatus", False)
            _owner = request.user.username
            _reader = request.POST.get("recipient", None)
            _group_flag = True if request.POST.get("groupFlag", False) == str("true") else False
            # print("=======>>>>>>>>>>.", request.POST.get("group_id", None))
            # print("=======>>>>>>>>>>.group flag ", request.POST.get("groupFlag", None))
            _group_id = None if (request.POST.get("group_id", None) == str('None') or request.POST.get("group_id", None) == str('')) else request.POST.get("group_id", None)
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

                # for s in typing_status:
                #     typing_obj = s.get_status()
                #     typing_status_users_list.append(typing_obj)

                # print(list(typing_status_users_list))
                return JsonResponse({"chats": all_chats, "group_flag": True}, safe=False)

            else:
                chats = Messages.objects.all().filter(isGroup=False, owner=_owner, recipient=_reader).union(Messages.objects.all().filter(isGroup=False, owner=_reader, recipient=_owner)).order_by('-timestamp')[:20][::-1]
                # print("chat is ==============>>>>>>>>", chats)

                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    all_chats.append(dict_object)
                # print(list(all_chats))    
            
                try:
                    typing_status = UserStatus.objects.all().filter(onGroup=False, owner=_reader, reader=_owner)[0]
                    return JsonResponse({"chats": all_chats, "typing_status": typing_status.get_typing_status(), "group_flag": False}, safe=False)
                except:
                    print("Owner with user name {} does not yet started to talk to the guy with name {}".format(_reader, _owner))   
                    return JsonResponse({"chats": all_chats, "typing_status": False, "group_flag": False}, safe=False)

        else:
            return JsonResponse({"message": "sigin first to see the message"}, safe=False)
    
    else:
        return JsonResponse({"message": "Please do request with a valid request type and verified account to get the service"}, safe=False)



def load_previous_messages(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            all_chats = []
            msg_data = json.loads(request.POST.get("dataObject"))
            _owner = request.user.username
            _reader = request.POST.get("recipient", None)
            _group_flag = True if request.POST.get("groupFlag", False) == str("True") else False
            _group_id = None if request.POST.get("group_id", None) == str('None') else request.POST.get("group_id", None)

            if _group_flag:
                chats = Messages.objects.all().filter(isGroup=True, groupId=_group_id, timestamp__lte=msg_data['normal_timestamp'], approval_status=True).order_by('-timestamp')[:20][::-1]
         
                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    all_chats.append(dict_object)
            
                return JsonResponse({"chats": all_chats, "group_flag": True}, safe=False)

            else:
                chats = Messages.objects.all().filter(isGroup=False, owner=_owner, recipient=_reader, timestamp__lte=msg_data['normal_timestamp']).union(Messages.objects.all().filter(isGroup=False, owner=_reader, recipient=_owner, timestamp__lte=msg_data['normal_timestamp'])).order_by('-timestamp')[:20][::-1]

                for chat in chats:
                    dict_object = chat.get_items_as_dict()
                    all_chats.append(dict_object)

                print(list(all_chats))
                return JsonResponse({"chats": all_chats, "group_flag": False}, safe=False)

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
                continue

            group_ids[ids] = str(group_ids[ids])

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
            print("integer is ", group_ids_list[0])
            chats = Messages.objects.all().filter(isGroup=True, groupId=group_ids_list[0], approval_status=False).order_by('timestamp')
            for i in range(1, len(group_ids_list)):
                if (len(chats)>=msg_limit):
                    print("i am going to break and the length of chats is", len(chats))
                    break
                chats = chats.union(Messages.objects.all().filter(isGroup=True, groupId=group_ids_list[i], approval_status=False).order_by('timestamp'))
                    
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
            for msg in msg_data:
                msg_delete_status = msg.get("deleteStatus", False)
                if msg_delete_status:
                    chat = Messages.objects.get(isGroup=True, groupId=msg.get("group_id", 0), approval_status=False, id__exact=msg["id"])
                    print(chat)
                    chat.delete()
                    continue
                msg_approval_status = msg.get("status", False)
                if msg_approval_status:
                    chat = Messages.objects.get(isGroup=True, groupId=msg.get("group_id", 0), approval_status=False, id__exact=msg["id"])
                    chat.approval_status = True
                    chat.save()

            return JsonResponse({"message": "Approval message list executed succssfully"}, safe=False)

        else:
            return JsonResponse({"message": "sigin first to load the group messages"}, safe=False)
    
    else:
        return JsonResponse({"message": "Please do request with a valid request type and verified account to approve the messages"}, safe=False)