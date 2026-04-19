from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User





def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        # ✅ validation
        if not email or not password or not phone:
            return render(request, "signup.html", {"error": "All fields required"})

        if User.objects.filter(username=email).exists():
            return render(request, "signup.html", {"error": "User already exists"})

        # ✅ create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # ✅ save phone in profile
        user.profile.phone = phone
        user.profile.save()

        # ✅ login
        login(request, user)

        # ✅ redirect
        return redirect("/")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/signup/")

from django.shortcuts import render, redirect
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        return redirect('/contact/?success=1')

    success = request.GET.get('success') == '1'
    return render(request, 'corev_contact.html', {'success': success})