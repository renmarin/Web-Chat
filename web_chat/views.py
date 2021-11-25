from datetime import datetime
from django.utils import timezone

from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator


from django.views import View
from .models import Chat
from .forms import SignUpIn, Tok, DelaySend, ChooseRoom

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# todo  copy forms from older projects              +
# todo  create html pages for reg/loging            +
# todo  create view for reg/loging                  +
# todo  implement token-based authentication:
# https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
# todo  use token for accessing chat?:
# https://hashnode.com/post/using-django-drf-jwt-authentication-with-django-channels-cjzy5ffqs0013rus1yb9huxvl


class RegisterUser(View):
    def get(self, request):
        form = SignUpIn()
        self.context = {
            'SignUpIn': form,
        }
        return render(request, 'web_chat/RegisterUser.html', self.context)


    def post(self, request):
        if 'username' in request.POST and 'password' in request.POST:
            self.username = request.POST['username']
            self.password = request.POST['password']
            user = User.objects.create_user(username=self.username, password=self.password)
            messages.info(request, f"Account for {self.username} is created!")
            return HttpResponseRedirect(reverse('web_chat:login'))


class LogIn(View):

    def get(self, request):

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('web_chat:choosechat'))

        form = SignUpIn()
        self.context = {
            'SignUpIn': form,
        }
        return render(request, 'web_chat/login.html', self.context)

    def post(self, request):
        if 'username' in request.POST and 'password' in request.POST:
            self.username = request.POST['username']
            self.password = request.POST['password']
            self.user = authenticate(request, username=self.username, password=self.password)
            if self.user is not None:
                login(request, self.user)
                request.session['username'] = self.username
                return HttpResponseRedirect(reverse('web_chat:choosechat'))
            else:
                # Return an 'invalid login' error message.
                raise Http404("Invalid login")


class LogOut(View):
    def get(self, request):
        logout(request)
        messages.info(request, f"Loged out!")
        return HttpResponseRedirect(reverse('web_chat:login'))


class ChooseChatRoom(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.form = ChooseRoom()
        self.context = {
            'username': request.session.get('username'),
            'ChooseRoom': self.form,
        }
        return render(request, 'web_chat/choose_room.html', self.context)

    def post(self, requset):
        self.room = requset.POST['room'].replace(" ", "_")
        return HttpResponseRedirect(reverse('web_chat:chat', args=(self.room,)))


class ChatRoom(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, room_name):

        username = request.session.get('username', 'Anon')
        # messages = Chat.objects.all()
        # hide future (delayed) messages
        messages = Chat.objects.messages = Chat.objects.filter(
            date__lte=timezone.now(),
            room=room_name,
        ).all()
        messages_paginator = Paginator(messages, 10)
        page_num = request.GET.get('page')
        page = messages_paginator.get_page(page_num)

        context = {
            'username': username,
            'page_list': page.object_list[::-1],
            'page': page,
            'DelaySend': DelaySend(),
            'room_name': room_name,
        }

        return render(request, 'web_chat/chat.html', context)

    # Delay message
    def post(self, request, room_name):
        if 'date' in request.POST and 'time' in request.POST and 'message' in request.POST:
            date = request.POST['date']
            time = request.POST['time']
            date_time = date + ' ' + time  # 2021-11-30 11:11
            if request.POST['anon'] == 'Anon':
                username = 'Anon'
            else:
                username = request.session.get('username', 'Anon')
            # return HttpResponse(date_time)
            datetime_object = datetime.strptime(date_time, '%Y-%m-%d  %H:%M')
            if datetime_object < datetime.now():
                messages.info(request, "Can't send message in past")
                return HttpResponseRedirect(reverse('web_chat:chat', args=(room_name,)))
            else:
                chat = Chat.objects.create(
                    name=username,
                    message=request.POST['message'],
                    date=date_time,
                    room=room_name,
                )
                chat.save()
                return HttpResponseRedirect(reverse('web_chat:chat', args=(room_name,)))
