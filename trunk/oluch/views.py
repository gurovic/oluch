# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext
import datetime
import settings
from oluch.models import Submit, Problem
from oluch.forms import SubmitForm, UserInfoForm


def choose_page(request):
    print Group.objects.get(name='Jury').user_set.all()
    if request.user in Group.objects.get(name='Jury').user_set.all():
        return HttpResponseRedirect('/statistics')
    else:
       return HttpResponseRedirect('/submit')
   

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')

def rate(request, submit_id, time):
    submit = Submit.objects.get(id=submit_id)
    if time == '1':
       submit.first_mark = int(request.POST["subm"]) if request.POST["subm"] != 'не оценивать' else -2
       submit.first_judge = request.user
    else:
        if request.POST["subm"] != u'не оценивать':     
            submit.final_mark = submit.second_mark = int(request.POST["subm"])
        else:
            submit.final_mark = submit.second_mark = -2
        submit.second_judge = request.user
    submit.save()
    return HttpResponseRedirect('/statistics')


def check(request, time, problem_id, submit_id=None):
    if submit_id is None:
        if time == '1':
            submit = Submit.objects.filter(problem__id=problem_id, first_mark=-2).latest('datetime')
            submit.first_mark=-1
        else:
            submit = Submit.objects.filter(problem__id=problem_id, first_mark__gt=-1, second_mark=-2).latest('datetime')	
            submit.second_mark=-1
        submit.save()
        return HttpResponseRedirect('/check/' + time + ('st/' if time == '1' else 'nd/') + str(problem_id) + '/' + str(submit.id))
    else:
        submit = Submit.objects.get(id=submit_id)
        if str(submit.file).split('.')[-1] in ['png', 'gif', 'jpeg', 'jpg']:
            is_picture = '1'
        else:
            is_picture = '0'
        return render(request, 'olymp/check.html', {
                'is_picture': is_picture,
                'submit': submit,
                'time': time,
                'marks': range(settings.max_mark + 1),
            })


def user_submited_problems(user):
    return Submit.objects.filter(author=user).values_list('problem__id', 'problem__number', 'problem__title').order_by('problem__sort_order')

def user_not_submited_problems(user):
    all = Problem.objects.all().values_list('id', 'number', 'title')
    submited = set(user_submited_problems(user))
    return [(item[0], item[1] + '. ' + item[2]) for item in all if item not in submited]

def submit(request):
    state, time = olymp_status()
    choices = user_not_submited_problems(request.user)
    submited = user_submited_problems(request.user)
    print submited
    if request.method == 'POST':
        form = SubmitForm(choices, request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            new_submit = Submit(author=request.user, file=request.FILES['file'], problem=Problem.objects.get(id=int(form.cleaned_data['problem'])))
            new_submit.save()
        return HttpResponseRedirect('/submit')
    elif choices:
        form = SubmitForm(choices)
        return render(request, 'olymp/submit.html', {
            'form': form,
            'submited': submited,
            'state': state,
            'time': time,
        })
    else:
        return render(request, 'olymp/submit.html', {
            'form': None,
            'submited': submited,
            'state': state,
            'time': time,
        })
    

def olymp_status():
    now = datetime.datetime.now()
    if now < settings.start:
        delta = settings.start - now
        return -1, str(delta).split('.')[0]
    elif now < settings.finish:
        delta = settings.finish - now
        return 0, str(delta).split('.')[0]
    else:
        return 1, 0
                

def submit_statistics():
    total = Submit.objects.count()
    zero = Submit.objects.filter(first_mark=-2).count() 
    first = Submit.objects.filter(first_mark__gt=-1, second_mark=-2).count() 
    second = Submit.objects.filter(second_mark__gt=-1).count() 
    return (total, zero, first, second)

def statistics(request):
    state, time = olymp_status()
    submits_stat = submit_statistics()
    problems = Problem.objects.all().order_by('id')
    problems_number = [Submit.objects.filter(problem=problem).count() for problem in Problem.objects.all().order_by('id')]
    problems_zero = [Submit.objects.filter(problem=problem, first_mark=-2).count() for problem in Problem.objects.all().order_by('id')]
    problems_first = [Submit.objects.filter(problem=problem, first_mark__gt=-1).filter(second_mark=-2).count() for problem in Problem.objects.all().order_by('id')]
    problems_second = [Submit.objects.filter(problem=problem, second_mark__gt=-1).count() for problem in Problem.objects.all().order_by('id')]
    problems_first_me = [Submit.objects.filter(problem=problem, first_mark__gt=-1, second_mark=-2).exclude(first_judge=request.user).count() for problem in Problem.objects.all().order_by('id')]
    probs = zip(problems, problems_number, problems_zero, problems_first, problems_first_me, problems_second)
    return render_to_response('olymp/statistics.html', {
                    'state': state,
                    'time': time,
                    'submits_count': submits_stat[0],
                    'zero_count': submits_stat[1],
                    'first_count': submits_stat[2],
                    'second_count': submits_stat[3],
                    'submits_zero_percent': 100 * submits_stat[1] // submits_stat[0],
                    'submits_first_percent': 100 * submits_stat[2] // submits_stat[0],
                    'submits_second_percent': 100 * submits_stat[3] // submits_stat[0],
                    'probs': probs,
                },
                context_instance=RequestContext(request)
            )

def results(request):
    problems = dict(zip(map(lambda x: x.id, Problem.objects.all()), range(2, settings.problems_number + 2)))
    results = dict()
    for user in User.objects.annotate(num=Count('submit')).filter(num__gt=0):
        results[user.id] = [0] + [user.last_name + ' ' + user.first_name] + [-3] * settings.problems_number
        submits = Submit.objects.filter(author=user).order_by('problem')
        for submit in submits:
            if submit.final_mark >= 0:
                results[user.id][problems[submit.problem.id]] = submit.final_mark
                results[user.id][0] += submit.final_mark
            elif submit.first_mark >= 0:
                results[user.id][problems[submit.problem.id]] = -1
            else:
                results[user.id][problems[submit.problem.id]] = -2

    res = sorted(results.values(), reverse=True) 
    results = [[r[1], r[0], r[2:]] for r in res] 
    return render_to_response('olymp/results.html', {
                               'results' : results,
                               'problems': Problem.objects.all(),
                                    },
                context_instance=RequestContext(request)
            )


def register(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password1, 
                        email=email)
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
            profile = user.userprofile
            profile.secondname = form.cleaned_data['secondname']
            profile.position = form.cleaned_data['position']
            profile.hours = form.cleaned_data['hours']
            profile.circles = form.cleaned_data['circles']
            profile.university = form.cleaned_data['university']
            profile.tel = form.cleaned_data['tel']
            profile.address = form.cleaned_data['address']
            profile.workplace = form.cleaned_data['workplace']
            profile.save()
 
            user = authenticate(username=username, password=password1)
            login(request, user)
            return HttpResponseRedirect('/submit')
    else: # If not POST
        form = UserInfoForm()

    return render_to_response('olymp/register.html', {
            'form': form,
        },
        context_instance=RequestContext(request)
    )