from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe
import requests
import os
from models import *
import random
import copy
from django.forms.models import model_to_dict
from datetime import timedelta

# Create your views here.
def index(request):
    used_ids = list(Subject.objects.all().values_list('pk', flat=True).order_by('-pk'))
    if len(used_ids) != 0:
        return render(request, 'index.html', {"used_ids": used_ids})
    else:
        return render(request, 'index.html')

def session(request):
    if request.method == "POST":
        try:
            existing_user = Subject.objects.get(pk=request.POST['subid'])
            request.session['user'] = request.POST['subid']
            new_session_length = SessionLength(subject=existing_user, trials=0)
            new_session_length.save()
            request.session['session_length'] = new_session_length.pk
            return redirect('myself')
        except:
            return redirect('/adminhello/subject/add')
    else:
        if 'user' in request.session:
            try:
                return redirect(Subject.objects.get(pk=request.session['user']))
            except:
                pass
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
        response_block = ResponseBlock.objects.get(id=responseid)
    except:
        return HttpResponse("Oops! This page is looking for a response set that hasn't been recorded.")
    responses = Response.objects.filter(block=response_block)
    return render(request, 'response_set.html', {'response_block': response_block, 'responses': responses})

def myself(request):
    if not 'user' in request.session:
        return HttpResponse("Please return to the landing page and enter a subject ID.")
    try:
        sub = Subject.objects.get(pk=request.session['user'])
    except:
        return HttpResponse("Oops! This page is looking for a subject that we don't have any info for.<br>Please return to the landing page and enter a name.")

    response_list = ResponseBlock.objects.filter(subject=sub)

    return render(request, 'subject.html', {'subject': sub, 'response_list': response_list, 'admin': False})

def trial(request):
    if request.method == "POST" and 'subject' in request.POST.keys():
        sub = request.POST['subject']
    elif 'user' in request.session.keys():
        sub = request.session['user']
    else:
        return HttpResponse("I couldn't identify the user you're trying to start a trial for.")
    subject = Subject.objects.get(pk=sub)
    try:
        symbol_set = random.choice(SymbolSet.objects.filter(phase=subject.phase))
    except:
        return HttpResponse("I have no symbol sets for this phase.")
    single_sets = SingleSet.objects.filter(symbol_set=symbol_set).filter(training=subject.training)
    trial = []
    for i in range(symbol_set.block_size / len(single_sets)):
        for current_set in single_sets:
            options_list = []
            options_list.append(current_set.option_1)
            options_list.append(current_set.option_2)
            options_list.append(current_set.option_3)
            random.shuffle(options_list)

            temp_dict = model_to_dict(current_set)
            temp_dict["symbol_set"] = current_set.symbol_set.name
            temp_dict["left"] = model_to_dict(options_list[0])
            temp_dict["left"]["image"] = temp_dict["left"]["image"].url
            print temp_dict["left"]["image"]
            temp_dict["center"] = model_to_dict(options_list[1])
            temp_dict["center"]["image"] = temp_dict["center"]["image"].url
            temp_dict["right"] = model_to_dict(options_list[2])
            temp_dict["right"]["image"] = temp_dict["right"]["image"].url
            trial.append(temp_dict)
    random.shuffle(trial)
    new_block = ResponseBlock(subject=subject, phase=subject.phase, symbol_set=symbol_set, complete=False)
    new_block.save()
    for i in range(len(trial)):
        stimulus = Symbol.objects.get(pk=trial[i]["stimulus"])
        trial[i]["stimulus"] = Symbol.objects.get(pk=trial[i]["stimulus"]).image.url
        option_1 = Symbol.objects.get(pk=trial[i]["option_1"])
        option_2 = Symbol.objects.get(pk=trial[i]["option_2"])
        option_3 = Symbol.objects.get(pk=trial[i]["option_3"])
        new_response = Response(block=new_block, modifier=trial[i]["modifier"], stimulus=stimulus, option_1=option_1, option_2=option_2, option_3=option_3, correct_response=trial[i]["correct_response"])
        new_response.save()
        trial[i]["response_id"] = new_response.pk

    session_length = SessionLength.objects.get(pk=request.session['session_length'])
    session_length.trials += 1
    session_length.save()

    return render(request, 'trial.html', {'trial': mark_safe(json.dumps(trial)), 'feedback': subject.training})

def report_results(request):
    if request.method != "POST":
        return HttpResponse("You have reached this page in error. If you want to begin a trial, return to the subject view page.")
    block = ""
    json_object = json.loads(request.body)
    if len(json_object) < int(json_object['trial_length']) + 1:
        try:
            db_response = Response.objects.get(id=json_object[0].response_id)
            block = db_response.block
            block.delete()
        except:
            print "Delete failed"
        return redirect("/myself")
    for response in json_object:
        try:
            db_response = Response.objects.get(id=json_object[response]['response_id'])
            db_response.response_time = timedelta(milliseconds=json_object[response]['response_time'])
            db_response.given_response = json_object[response]['given_response']
            db_response.save()
            if block == "":
                block = db_response.block
                block.complete = True
                block.save()
        except:
            pass
    try:
        return redirect(block)
    except:
        return redirect("/myself")

def edit_subject(request, subid):
    try:
        sub = Subject.objects.get(pk=subid)
        return render(request, 'subject_edit.html', {'subject': sub})
    except:
        return HttpResponse("I couldn't find the user you're trying to edit.")

def phase_view(request, subid):
    try:
        sub = Subject.objects.get(pk=subid)
    except:
        return HttpResponse("I couldn't find the user you're trying to view.")

    response_list = ResponseBlock.objects.filter(subject=sub)
    phases = Phase.objects.all()

    table_data = {}
    for phase in phases:
        temp = response_list.filter(phase=phase)
        if temp.exists():
            trial_count = len(temp)
            trial_cor = 0
            total_duration = 0
            for block in temp:
                responses = block.response_set.all()
                block_count = len(responses)
                cor_count = 0.0
                block_duration = 0
                for response in responses:
                    cor_count += response.correct()
                    total_duration += response.get_response_time()
                if (not phase.passing_accuracy_percentage) or (cor_count/block_count >= phase.passing_accuracy_percentage):
                    if (not phase.passing_time) or (block_duration <= phase.get_passing_time()):
                        trial_cor += 1
                total_duration += block_duration
            table_data[str(phase)] = {'count':trial_count, 'passing':trial_cor, 'total_duration':total_duration}

    return render(request, 'phase_view.html', {'table_data':table_data, 'subject':sub})
