from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from .models import URLShortener
import datetime

# Create your views here.

def redirect_to_long_url(request, shorturl):
	#Redirect to Long URL: Note: Only happens on unauthenticated user when url_visible_to length is zero; Otherwise authentication required
	try:
		url_to_go = URLShortener.objects.get(uuid=shorturl)
	except URLShortener.DoesNotExist:
		return HttpResponseNotFound('<h1>Page not found</h1>')
	if(url_to_go.users_visible_to.count() > 0):
		#import pdb; pdb.set_trace()
		if(url_to_go.users_visible_to.all().filter(id=request.user.id).count()!=1):
			return HttpResponseForbidden('<h2>Response400:This URL Shortener is not for You</h2>')
	url_to_go.visits+=1
	#import pdb; pdb.set_trace()
	url_to_go.save()
	if(url_to_go.longurl[:7] != "http://"):
		return HttpResponseRedirect("http://"+url_to_go.longurl)
	else:
		return HttpResponseRedirect(url_to_go.longurl)

def create_short_url(request):
	#Create Short URL Post Request
	toggle_invalid_user=False
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		longurl = request.POST['longurl']
		try:
			exp_hours = int(request.POST['expiry-hours'])
		except ValueError:
			exp_hours=0
		try:
			exp_days = int(request.POST['expiry-days'])
		except ValueError:
			exp_days=0
		try:
			exp_mins = int(request.POST['expiry-minutes'])
		except ValueError:
			exp_mins=1
		expiry = datetime.datetime.now() + datetime.timedelta(days=exp_days, hours=exp_hours, minutes=exp_mins)
		userslist = [x.strip() for x in request.POST['userlist'].split(",")]
		new_tiny_url = URLShortener(longurl=longurl, created_by=request.user, create_date=datetime.datetime.now(), end_date=expiry, visits=0)
		new_tiny_url.save()
		toggle = False
		if(not(len(userslist)==0 or (len(userslist)==1 and userslist[0]==''))):
			for usernm in userslist:
				try:
					user_to_add = User.objects.get(username=usernm)
					new_tiny_url.users_visible_to.add(user_to_add)
					toggle = True	
				except User.DoesNotExist:
					pass
			if(toggle):	
				user_to_add = User.objects.get(username=request.user.username)
				new_tiny_url.users_visible_to.add(user_to_add)
				new_tiny_url.save()
			#new_tiny_url = URLShortener(longurl=longurl, created_by=request.user, create_date=datetime.datetime.now(), end_date=expiry, visits=0, users_visible_to=users_visible)
	return redirect('home')


def home_page(request):
	#Create Short URL Post Request
	if not request.user.is_authenticated:
		return redirect('login')
	else:
		timenow = datetime.datetime.now()
		all_urls = URLShortener.objects.filter(end_date__gte=timenow).filter(created_by=request.user)
		return render(request, 'home.html', {'all_urls':all_urls, 'time_now':timenow })



def login_form_view(request):
	if(request.method == 'POST'):
		#form = UserLoginForm()
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		return render(request, 'login.html', {'toggle':True})
	return render(request, 'login.html', {'toggle':False})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})		

def logout_view(request):
    logout(request)
    return redirect('home')