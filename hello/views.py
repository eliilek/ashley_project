from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe
import requests
import os
from models import *
import random
import copy

# Create your views here.
def index(request):
    return render(request, 'index.html')

def session(request):
    if request.method == "POST":
        request.session['user'] = request.POST['firstname'].upper() + " " + request.POST['lastname'].upper()
        request.session['admin'] = False
        try:
            existing_user = Subject.objects.get(name=request.session['user'])
            return redirect(existing_user)
        except:
            new_user = Subject(name=request.session['user'], phase=1, training=True)
            new_user.save()
            return redirect(new_user)
    else:
        if 'user' in request.session:
            return HttpResponse(request.session['user'].title())
        return HttpResponse("Failure!")

def subject(request, subid):
    try:
        sub = Subject.objects.get(id=subid)
    except:
        return HttpResponse("Oops! This page is looking for a subject that we don't have any info for.<br>Please return to the landing page and enter a name.")

    response_list = ResponseBlock.objects.filter(subject_id=subid)

    return render(request, 'subject.html', {'subject': sub, 'response_list':response_list, 'admin': True})
    #return HttpResponse("Captured id: " + subid + "<br>Captured name: " + sub.name.title())

def response_set(request, responseid):
    try:
        response_block = ResponseBlock.objects.get(responseid)
    except:
        return HttpResponse("Oops! This page is looking for a response set that hasn't been recorded.")

    return render(request, 'response_set.html', {'response_block': response_block})

def myself(request):
    if not 'user' in request.session:
        return HttpResponse("Oops! You haven't told us your name!<br>Please return to the landing page and enter a name.")
    try:
        sub = Subject.objects.get(name=request.session['user'])
    except:
        return HttpResponse("Oops! This page is looking for a subject that we don't have any info for.<br>Please return to the landing page and enter a name.")

    response_list = ResponseBlock.objects.filter(subject_id=sub.id)

    return render(request, 'subject.html', {'subject': sub, 'response_list': response_list, 'admin': False})

def trial(request):
    if request.method == "POST" and 'subject' in request.POST.keys():
        sub = request.POST['subject']
    elif 'user' in request.session.keys() and not request.session['admin']:
        sub = request.session['user']
    else:
        return HttpResponse("I couldn't identify the user you're trying to start a trial for.")
    subject = Subject.objects.get(name=sub)
    try:
        symbol_set = random.choice(SymbolSet.objects.filter(phase=subject.phase))
    except:
        return HttpResponse("I have no symbol sets for this phase.")
    if subject.phase % 2 == 0:
        training = False
    else:
        training = True
    single_sets = SingleSet.objects.filter(symbol_set=symbol_set).filter(training=training)
    trial = []
    for i in range(symbol_set.block_size / len(single_sets)):
        for current_set in single_sets:
            temp = SingleSetUnpacker(current_set)
            options_list = temp.options.split(",")
            random.shuffle(options_list)
            temp.left_option = temp.symbol_set + "_" + options_list[0]
            temp.center_option = temp.symbol_set + "_" + options_list[1]
            temp.right_option = temp.symbol_set + "_" + options_list[2]
            temp.options = (",".join(options_list))
            trial.append(temp)
    random.shuffle(trial)
    new_block = ResponseBlock(subject=subject, phase=subject.phase, training=training, symbol_set=symbol_set, complete=False)
    new_block.save()
    for i in len(trial):
        new_response = Response(block=new_block, modifier=trial[i].modifier, stimulus=trial[i].stimulus, options=trial[i].options, correct_response=trial[i].correct_response)
        trial[i].response_id = new_response.id
        new_response.save()

    return render(request, 'trial.html', {'trial': mark_safe(json.dumps(trial)), 'feedback': training})

class SingleSetUnpacker(object):
    def __init__(self, single_set):
        self.symbol_set = single_set.symbol_set.name
        self.stimulus = self.symbol_set + "_" + single_set.stimulus
        self.modifier = single_set.get_modifier_display()
        self.options = single_set.options
        self.training = single_set.training
        self.correct_response = single_set.correct_response

def edit_subject(request, subid):
    return HttpResponse("Pass")
