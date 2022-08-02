from http.client import HTTPResponse
from django.shortcuts import redirect, render
from .forms import *
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.db.models import Q
import string
import random

# Create your views here.

def get_random_code():
    string_length = 10 
    letters_digits = string.ascii_uppercase + string.digits 
    str = ''.join(random.choice(letters_digits) for i in range(string_length))
    return str

def register(request):
    registered = False
    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(userform.errors)
    else:
        userform = UserForm()
    return render(request, 'endterm/register.html',
                  {'userform': userform,
                    'registered': registered})

 
def update(request):
    if request.user.is_authenticated:
        updateuser = request.user
        print(updateuser)
        if request.method == 'POST':
            profile = UserProfileForm(data=request.POST)
            nickname = request.POST['nickname']
            photo = request.POST['photo']
            print(nickname, photo)
            if profile.is_valid():
                update, createdbool = AppUser.objects.get_or_create(user_id = updateuser.id)
                update.photo =photo
                update.nickname = nickname
                update.chat_code = get_random_code()
                update.save()
            else:
                print(profile.errors)
        else:
            profile = UserProfileForm()
    else:
        return HttpResponse("Your have not logged in, please to continue!")

    return render(request, 'endterm/update.html', {'updateForm': profile})

    

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../update')
            else:
                return HttpResponse("Log in failed, please check your username or password.")
        else:
            return HttpResponse("Invalid login.")
    else:
        return  render(request, 'endterm/login.html')

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('..')

def userProfile(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_info = AppUser.objects.get(user = current_user)
        user_email = current_user.email
        user_photo = user_info.photo
        user_nickname = user_info.nickname
        user_chat_code = user_info.chat_code
        return render(request, 'endterm/userProfile.html',{'nickname': user_nickname, 
                        'photo': user_photo, 'email': user_email, 'user_chat_code':user_chat_code})

def viewuser(request, user_id):
    user_info = AppUser.objects.get(user_id = user_id)
    user_photo = user_info.photo
    user_nickname = user_info.nickname
    user_id = user_info.id
    return render(request, 'endterm/viewuser.html',{'nickname': user_nickname, 'photo': user_photo, 'user_id': user_id})


def searchUser(request, *args, **kwargs):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        if query:
            qset = (Q(email__icontains=query))
            results = User.objects.filter(qset).distinct()
        else:
            results = User.objects.all()
        return render(request, "endterm/search.html", {"results": results,"query": query})
    else:
        return HTTPResponse("You must log in to search users.")
    
def send(request):
    fromUser = request.user
    if request.method == 'POST':
        user_id = request.POST['user_id']
        toUser = User.objects.get(id=user_id)
        friendreq, createbool = friendReq.objects.get_or_create(FromUser = fromUser, ToUser = toUser)
        friendreq.save()
        if createbool:
            return render(request, 'endterm/search.html')
        else:
            return HttpResponse("You have sent the request already! Please wait the respone!")
    else:
        return render(request, 'endterm/send.html')
def checkRequest(request):
    current_user = request.user
    friend_requests = friendReq.objects.filter(ToUser =current_user)
    if request.method == 'POST':
        accepting = request.POST['request_id']
        accpeting_request = friendReq.objects.get(id = accepting)

        accepter = accpeting_request.ToUser
        accepter_friendlist, created= friends.objects.get_or_create(user = accepter)
        sender = accpeting_request.FromUser
        sender_freindlist, created= friends.objects.get_or_create(user = sender)
        sender = User.objects.get(id = sender.id)

        accepter_friendlist.friend.add(sender)
        sender_freindlist.friend.add(accepter)
        accpeting_request.delete()
        return HttpResponse("Accepted Successfully!")
    else:
        requests_id = []
        senders_id = []
        senders_nickname = []
        for req_obj in friend_requests:
            requests_id.append(req_obj.id)
            senders_id.append(req_obj.FromUser)
            sendersAppUser = AppUser.objects.get(user = req_obj.FromUser)
            senders_nickname.append(sendersAppUser.nickname)
        requester_data = zip(requests_id , senders_id, senders_nickname)
        return render(request, 'endterm/checkRequest.html', {'requester_data': requester_data})
        
def friendlist(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            try:
                removing = request.POST['remove_id']
                deleted = User.objects.get(user = removing)
                deleted_q = friends.objects.get(user = current_user)
                deleted_q.friend.remove(deleted)
                deleted_side_q = friends.objects.get(user = deleted)
                deleted_side_q.friend.remove(current_user)
                return HttpResponse("Remove Successfully!")
            except Exception:
                return HttpResponse("The removing met some error, please try again or check your id input.")
        else:
            try: 
                friend_list = friends.objects.get(user = current_user)
                friends_nicknames = []
                friends_photo = []
                friends_usernames = []
                friends_emails = []
                firends_chat_code = []
                friends_ids = friend_list.friend.all()
                friend_ids_toRemove = []
                for friend in friends_ids: 
                    friend_user_info = User.objects.get(id = friend.id)
                    friends_usernames.append(friend_user_info.username)
                    friends_emails.append(friend_user_info.email)
                    friend_ids_toRemove.append(friend_user_info.id)
                    friend_info = AppUser.objects.get(user = friend_user_info)
                    friends_nicknames.append(friend_info.nickname)
                    friends_photo.append(friend_info.photo)
                    firends_chat_code.append(friend_info.chat_code)

                friends_context = zip(friends_usernames, friends_emails, friends_nicknames, friends_photo, firends_chat_code, friend_ids_toRemove)
                print(friend_list)
                return render(request, 'endterm/friendlist.html', {'friends_context': friends_context})
            except Exception:
                return HttpResponse('Please search a user and add a friend first to continue!')




def roomchat_enter(request):
    return render(request, 'endterm/roomchat_enter.html')

def roomchat(request, room_name):
    currrent_user = request.user
    user_nickname = AppUser.objects.get(user = currrent_user)
    user_nickname = user_nickname.nickname
    return render(request, 'endterm/roomchat.html', {'room_name': room_name, 'username': user_nickname})

def get_friends_id(current_user):
    friend_list = friends.objects.get(user = current_user)
    friends_nicknames = []
    friends_photo = []
    friend_ids = []
    friends_ids = friend_list.friend.all()
    for friend in friends_ids: 
        friend_ids.append(friend.id)
        friend_user_info = User.objects.get(id = friend.id)
        friend_info = AppUser.objects.get(user = friend_user_info)
        friends_nicknames.append(friend_info.nickname)
        friends_photo.append(friend_info.photo)
    friends_context = zip(friend_ids, friends_nicknames, friends_photo)
    return friends_context 

def user_post(request):
    if request.user.is_authenticated:
        current_user = request.user
        poster_info = AppUser.objects.get(user = current_user)
        if request.method == 'POST':
            postform = postForm(data = request.POST)
            text = request.POST['text']
            mediaFile1 = request.POST['mediaFile1']
            mediaFile2 = request.POST['mediaFile2']
            mediaFile3 = request.POST['mediaFile3']
            if postform.is_valid():
                post_q = userPost.objects.create(poster = poster_info, text= text)
                if mediaFile1:
                    post_q.mediaFile1 = mediaFile1
                if mediaFile2:
                    post_q.mediaFile2 = mediaFile2
                if mediaFile3:
                    post_q.mediaFile3 = mediaFile3
                post_q.save()
            return render (request, 'endterm/post.html', {'postForm': postform})
            
        else:
            try:
                post_query = userPost.objects.none() 
                user_nicknames = []
                user_texts = []
                post_image1 = []
                post_image2 = []
                post_image3 = []
                friends_info = get_friends_id(current_user)
                for id, nickname,photo in friends_info :
                    posted = userPost.objects.filter(poster_id = id)
                    post_query = post_query | posted
                my_post = userPost.objects.filter(poster = poster_info)
                post_query = post_query | my_post
                post_query.order_by('-id')
                for post_single in post_query:
                    poster_nickname_query = AppUser.objects.get(id = post_single.poster_id)
                    user_nicknames.append(poster_nickname_query.nickname)
                    user_texts.append(post_single.text)
                    post_image1.append(post_single.mediaFile1)
                    post_image2.append(post_single.mediaFile2)
                    post_image3.append(post_single.mediaFile3)
                data = zip(user_nicknames,user_texts, post_image1, post_image2, post_image3)
                return render (request, 'endterm/post.html', {'postForm': postForm, "data": data })
            except Exception:
                return HttpResponse('Please search a user and add a friend first to continue!')
    else:
        return HttpResponse('You needs to login to post!')

def index(request):
    users_nickname = []
    users_comment = []
    commnets = publicChat.objects.all()
    commnets.order_by('-id')
    for single in commnets:
        appuser_q = AppUser.objects.get(user = single.user_id)
        users_nickname.append(appuser_q.nickname)
        users_comment.append(single.comment)
    data = zip(users_nickname, users_comment)
    comment_form = publicChatForm()
    
    if request.user.is_authenticated:
        current_user = request.user
        poster_info = AppUser.objects.get(user = current_user)
        comment_form = publicChatForm(data = request.POST)
        if request.method == 'POST':
            if comment_form.is_valid():
                comment_content = request.POST['comment']
                comment_q = publicChat.objects.create(user = poster_info, comment = comment_content)
                comment_q.save()
            return HttpResponseRedirect('..')
        else:
            return render(request, 'endterm/index.html', {'comment_form': comment_form, 'data': data})
    else:
        return render(request, 'endterm/index.html', {'comment_form': comment_form, 'data': data})
