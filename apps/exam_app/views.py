from django.shortcuts import render, redirect 
from .models import User, Appointment
from django.contrib import messages
from django.db import models 
import bcrypt
import datetime
from django.utils import timezone

def index(request):
    return render(request, 'exam_app/index.html')

def appointments(request):
    if 'id' not in request.session:
        messages.error(request, "Need to register or login")
        return redirect('/')
    
    user = User.objects.get(id=request.session['id'])
    date = datetime.date.today()
    now = timezone.now()
    appointments = Appointment.objects.exclude(date=date)
    todayapp = Appointment.objects.filter(date=date, user_id=request.session['id'])
    context = {
        "user": user,
        "now": now,
        "appointments": appointments,
        "todayapp": todayapp,
        "edit": "Edit",
        "delete": "Delete"

    }
    return render(request, 'exam_app/appointments.html', context)

def process(request):
    if request.method == "POST":
        res = User.objects.register(request.POST)

        if res['status']:
            request.session['id'] = res['data'].id
            return redirect('/appointments')

        else:
            for error in res['data']: 
                messages.error(request, error)

    return redirect('/')

def login(request):
    if request.method == "POST":
        res = User.objects.login(request.POST)

        if res['status']:
            request.session['id'] = res['data'].id
            return redirect('/appointments')
        else:
            messages.error(request, "Email or password invalid")
            return redirect('/')

def addappointment(request):
    if request.method == "POST":
        task = request.POST['task']
        date = request.POST['date']
        time = request.POST['time']
        user_list = User.objects.get(id=request.session['id'])

        Appointment.objects.create(task=task, date=date, time=time, user_id=user_list)
        

    return redirect('/appointments')

def editpage(request, id):

    context = { 
        "id": id,
        "appointment": Appointment.objects.get(id=id) 
    }
    return render(request, 'exam_app/display.html', context)    

def update(request, id):
    if request.method == "POST":
        app = Appointment.objects.get(id=id)
        app.task = request.POST['task']
        app.status = request.POST['status']
        app.save()
    return redirect('/appointments')

def delete(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect('/appointments')

def logout(request):
    request.session.flush()
    return redirect('/')

