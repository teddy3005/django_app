from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from .models import *
import bcrypt
from django.db.models import Count, Sum

# Create your views here.

def index(request):
    return render(request, 'pokes/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validation(request.POST)
        if 'user' in errors:
            request.session['currentuser']=errors['user']
            
            return redirect('/dashboard')
        else:
            for register,error in errors.iteritems():
                messages.error(request, error, extra_tags=register)
            return redirect('/index2')
    else:
        return redirect('/index2')

def new(request):
    return render(request, 'pokes/index2.html')

def login(request):
    if request.method == 'POST':
        checklogin = User.objects.loginvalidation(request.POST)
        if "user" in checklogin:
            request.session['currentuser']= checklogin["user"]
            request.session["idk"]= "logged in"
            return redirect('/dashboard')
        else:
            for tag, error in checklogin.iteritems():
                messages.error(request, error, extra_tags=tag)
                return redirect('/main')
    else:
        return redirect('/main')

def success(request):
    if 'currentuser' in request.session:
        showuser= request.session['currentuser']
        context={
            'currentuser':showuser,
            'total_pokers':User.objects.filter(id=request.session['currentuser'].id).annotate(counter=Count("receiverspoke__pokes")),
            'opokes':User.objects.exclude(id=request.session['currentuser'].id).annotate(counter=Sum("receiverspoke__pokes")),
            'my_pokes':Pokes.objects.filter(receiver=request.session['currentuser'].id),
        }
        return render(request, 'pokes/success.html',context)
    else:
        return redirect ('/main')

def poke_process(request):
    senderid = User.objects.get(id=request.session['currentuser'].id)
    receiverid = User.objects.get(id=request.POST['receiver'])
    poke_check = Pokes.objects.filter(sender=senderid, receiver=receiverid)

    if not poke_check:
        Pokes.objects.create(sender=senderid, receiver=receiverid, pokes=1)
        return redirect ('/dashboard')
    
    else:
        poke_check[0].pokes += 1
        poke_check[0].save()
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/')