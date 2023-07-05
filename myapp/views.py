from django.shortcuts import render, redirect, HttpResponse
from .models import Caretaker, Careseeker
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


# Create your views here.
def home(request):
    return render(request, 'home.html')


def all_members(request):
    if request.user.is_authenticated and request.user.user_type == "caretaker":
        all_users = Careseeker.objects.all()
        return render(request, 'all_careseekers.html', {'all_users': all_users})

    elif request.user.is_authenticated and request.user.user_type == "careseeker":
        all_users = Caretaker.objects.all()
        return render(request, 'all_caretakers.html', {'all_users': all_users})

    else:
        return HttpResponse('User is not authenticated')


"""
def all_caretakers(request):
    if request.user.is_authenticated:
        all_users = Caretaker.objects.all()
        return render(request, 'all_caretakers.html', {'all_users': all_users})
    else:
        return HttpResponse('User is not authenticated')
"""

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        caretaker = authenticate(request, email=email, password=password, is_caretaker=True)
        if caretaker is not None:
            login(request, caretaker)
            return redirect('all_members')

        careseeker = authenticate(request, email=email, password=password, is_careseeker=True)
        if careseeker is not None:
            login(request, careseeker)
            return redirect('all_members')

        messages.info(request, "Invalid email or password")
        return redirect('login_view')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


def caretaker_register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        ID_card = request.POST.get('ID_card')
        profession = request.POST.get('profession')
        objective = request.POST.get('objective')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = 'caretaker'

        if password1 == password2:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                messages.info(request, "Your email already exists. Please log in.")
                return redirect('caretaker_register')
            else:
                caretaker = Caretaker(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    gender=gender,
                    age=age,
                    phone=phone,
                    experience=experience,
                    id_card_number=ID_card,
                    profession=profession,
                    objective=objective,
                    image=image,
                    password=make_password(password1),
                    user_type=user_type
                )
                caretaker.save()
                messages.info(request, "Congratulations! You are already registered!")
                return redirect('login_view')

        messages.info(request, "Please check your password confirmation!")

    return render(request, 'caretaker_register.html')


def careseeker_register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        order = request.POST.get('order')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = 'careseeker'

        if password1 == password2:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                messages.info(request, "Your email already exists. Please log in.")
                return redirect('careseeker_register')
            else:
                careseeker = Careseeker(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    gender=gender,
                    age=age,
                    phone=phone,
                    state=state,
                    city=city,
                    address=address,
                    order=order,
                    image=image,
                    password=make_password(password1),
                    user_type=user_type
                )
                careseeker.save()
                messages.info(request, "Congratulations! You are already registered!")
                return redirect('login_view')

        messages.info(request, "Please check your password confirmation!")

    return render(request, 'careseeker_register.html')


def user_profile(request):
    if request.user.is_authenticated and request.user.user_type == "caretaker":
        my_user = Caretaker.objects.get(careuser_ptr_id=request.user.id)
        return render(request, 'user_data.html', {'my_user': my_user})
    elif request.user.is_authenticated and request.user.user_type == "careseeker":
        my_user = Careseeker.objects.get(careuser_ptr_id=request.user.id)
        return render(request, 'user_data.html', {'my_user': my_user})
    else:
        return HttpResponse("can't found user")


def about_us(request):
    return render(request, 'about_us.html')


def services(request):
    return render(request, 'services.html')


"""        if Caretaker.objects.get(email=email, password=password):
            user = Caretaker.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            all_users = Caretaker.objects.all()
            return render(request, 'all_careseekers.html', {'all_users': all_users})
        elif Careseeker.objects.get(email=email, password=password):
            user = Careseeker.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('all_caretakers')

        messages.info("password or email is incorrect")
"""
