from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib import auth
from .models import Ticket

import datetime
import json
import random

from .run_code import run_code, TestCase


# user = User.objects.create_user('inarchus', 'inarchus@gmail.com', 'asdf1234')


@login_required
def view_codesite(request):
    template = loader.get_template('code_template.html')
    context = {'static': '/', 'username': request.user.username}
    return HttpResponse(template.render(context, request))


def prettify_title(s):
    if len(s) > 0:
        return (s[0].upper() + s[1:]).replace('_', ' ')
    else:
        return s


class Field:
    def __init__(self, name, field_type, value):
        self.name = name
        self.field_type = field_type
        self.value = value


@login_required
def view_tracker(request):
    template = loader.get_template('ticket_tracker.html')
    user_tickets = Ticket.objects.filter(user=request.user.username)
    # print(user_tickets)
    # print([prettify_title(x.name) for x in Ticket._meta.fields])
    context = {'static': '/',
               'username': request.user.username,
               'values': [],
               'tickets': user_tickets,
               'next_id': 0,
               'tracker': ['Create User Database', 'Create Code Site', 'Create Submit Functionality', 'Create Grade Spreadsheet', 'Create Ticket System', 'Create Email Manifest', 'Create code testing functionality', 'Create unit tests']}
    # [[prettify_title(x.name), 'input'] for x in Ticket._meta.fields],
    context['fields'] = [Field('Id', 'fixed', 0), Field('User', 'fixed', request.user.username), Field('status', 'fixed', 'Creating...'),
                         Field('Description', 'input', ''), Field('Creation date', 'fixed', datetime.datetime.now().strftime("%Y:%M:%D")),
                         Field('Response', 'fixed', 'Awaiting Submission'), Field('Type', 'input', '')]

    return HttpResponse(template.render(context, request))


@login_required
def view_grades(request):
    template = loader.get_template('grades.html')
    context = {'static': '/', 'username': request.user.username, 'grade_categories': ['Exams', 'Homework', 'Labs', 'Lectures', 'Projects', 'Etc', 'Overall']}
    # here get from the database of grades, but for now, generate random assignments and grades
    grades = {}
    for category in context['grade_categories']:
        if category != 'Overall':
            grades[category] = {}
            num_assignments = random.randint(0, 50)
            for x in range(1, num_assignments + 1):
                grades[category][category + str(x)] = {}
                grades[category][category + str(x)]['total'] = random.choice([10, 50, 75, 100, 125, 200])
                grades[category][category + str(x)]['score'] = random.randint(0, grades[category][category + str(x)]['total'])
                grades[category][category + str(x)]['comments'] = ''
        else:
            pass
    context['grades'] = grades
    # encrypt the grades before sending them, but for now just send it.

    return HttpResponse(template.render(context, request))


@login_required
def submit_ticket(request):
    print('ticket submitted')
    if request.method == "POST":
        print(json.loads(request.body))
        print(Ticket.objects.filter(user=request.user.username))
    return HttpResponse('blah blah blah', content_type='html')


@login_required
def settings_page(request):
    template = loader.get_template('settings.html')
    context = {'static': '/', 'username': request.user.username}
    return HttpResponse(template.render(context, request))


def login_page(request):
    # print(request.username, request.password)
    context = {'static': '/', 'user_not_recognized': False}
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        # user = User.objects.create_user(, request.POST['username'] + '@umbc.edu', )
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            request.session['member_id'] = user.username
            return redirect('/')
        else:
            context['user_not_recognized'] = True

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


@login_required
def code_submit(request):
    the_body = request.body.decode('utf-8')
    the_code = json.loads(the_body)
    print(the_code)
    # need to load which problem_id is submitted and then load and run the test cases for that.
    results = run_code(the_code['code'], TestCase())
    return HttpResponse(results)


def logout_page(request):
    context = {'static': '/', 'username': request.user.username}
    logout(request)
    template = loader.get_template('logout.html')
    return HttpResponse(template.render(context, request))
