from django.shortcuts import render
from authenticate.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from authenticate.models import UserProfile
from django.contrib.auth.models import User
import requests, json

def index(request):

    context_dict = {'boldmessage': "I am bold font from the context"}

    return render(request, 'authenticate/index.html', context_dict)


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()


            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'authenticate/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                context_dict = {}
                user_profile = UserProfile.objects.get(user=user.id)
                context_dict['user_profile'] = user_profile


                response_1 = send_otp(user_profile)
                context_dict['session_id'] = response_1['Details']
                if response_1['Status'] != 'Success':
                    raise Exception('NOT ABLE TO SEND OTP')

                return render(request, 'authenticate/verifyotp.html', context_dict)
            else:
                return HttpResponse("Your SelectDine account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'authenticate/login.html', {})

def after_pwd(request, user_profile_id):

        user_profile = UserProfile.objects.get(id=user_profile_id)
        return HttpResponseRedirect('/authenticate/login/' + str(user_profile.id) + '/')

def send_otp(user_profile):

    factor_url = "https://2factor.in/API/V1/0b03737f-08cb-11eb-9fa5-0200cd936042/SMS/+91" + str(user_profile.phone_no) + "/AUTOGEN"
    response_1 = requests.get(url=factor_url)
    activity_dict = json.loads(response_1.text)    #{"status":"SUCCESS/Failed", "details":"jsjsjsj"}
    return activity_dict

def otp_verification(request, user_profile_id):                 #phpone_no, otp, sesssion_id

    session_id = request.POST.get('session_id')
    otp = request.POST.get('otp')
    print(request)
    print("SESSION", session_id)
    print("otp", otp)
    user_profile = UserProfile.objects.get(id=user_profile_id)
    factor_url = "https://2factor.in/API/V1/0b03737f-08cb-11eb-9fa5-0200cd936042/SMS/VERIFY/" + str(session_id) + "/" + str(otp)
    print("808980980980980980980980980980980980909809")
    print(factor_url)
    print("808980980980980980980980980980980980909809")
    response_2 = requests.get(url=factor_url)
    activity_dict = json.loads(response_2.text)

    if activity_dict['Status'] == 'Success':
        user = User.objects.get(id=user_profile.user.id)
        print("user", user)
        username = user.username
        print("username", username)
        password = request.POST.get('password')
        print("password", password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/authenticate/')
    else:
        raise Exception("INVALID OTP")

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/authenticate/')