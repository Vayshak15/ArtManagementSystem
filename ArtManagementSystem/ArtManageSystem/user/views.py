from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect

# Create your views here.

User = get_user_model()


def signup(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()

        if not username:
            errors['username'] = "Username field required"
        elif len(username) <= 7:
            errors['username'] = "Atleast 8 characters"
        else:
            is_used = User.objects.filter(username=username).exists()
            if is_used:
                errors['username'] = "Username already taken!"

        if not password1:
            errors['password1'] = "password required"
        elif len(password1) <= 7:
            errors['password1'] = "password must contains 8 characters with numbers"
        if not password2:
            errors['password2'] = "Re enter your password!"
        if password1 and password2 and password1 != password2:
            errors['password1'] = "password not match!!!"

        if not email:
            errors['email'] = "Email flied required"
        else:
            is_used = User.objects.filter(email=email).exists()
            if is_used:
                errors['email'] = "This email already taken!!!"
        if not first_name:
            errors[first_name] = "Firstname first is required"
        is_valid = len(errors.keys()) == 0
        if is_valid:
            user = User.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )

            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect('/?signup=sucessfull')
    context = {
        'errors': errors
    }
    return render(request, 'signup.html',context)
