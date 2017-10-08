# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from .models import Student
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
import allauth.account.views
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, EmailAddress


def student_detail(request):
    print()
    get_all_students = SocialAccount.objects.all()
    print(get_all_students[0])
    print(request.user.id)
    print(user_signed_up)
    print()
    print(request.user)
    print(user_logged_in)
    # print(get_all_students[0].extra_data)
    context = get_all_students[0].extra_data
    return HttpResponse(context)
