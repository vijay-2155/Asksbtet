import random
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from authentication.models import CustomUser
from questions.models import Branch


# Function to generate a random 6-digit OTP


def generate_otp():
    return str(random.randint(100000, 999999))


# Function to send OTP via email
def send_otp_email(to_email, otp_code):
    subject = 'OTP Verification for Your Account'
    message = f'Your OTP code is: {otp_code}\n\nThis OTP code is valid for a limited time.'
    from_email = 'thoughtvijay@gmail.com'  # Use a valid email address
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)


# Signup view
def signup(request):
    if request.method == 'POST':
        # Get data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user-type')
        college_name = request.POST.get('college-name')
        branch = request.POST.get('branch')
        try:
            Branch.objects.get(short_form=branch)
        except Branch.DoesNotExist:
            messages.error(request, "The selected stream does not exist.")
            return redirect('signup')
        # Perform basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with this email address already exists.")
            return redirect('signup')
        request.session['signup_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password1': password1,
            'user_type': user_type,
            'college_name': college_name,
            'branch': branch,
        }
        # Generate an OTP
        otp = generate_otp()
        # Send OTP via email
        send_otp_email(email, otp)

        # Store the OTP in the session
        request.session['otp'] = otp

        # Redirect to OTP verification page
        return redirect('verify_otp')  # Create a 'verify_otp' URL pattern for the verification page
    branches = Branch.objects.all()
    if branches:
        context = {
            'branches': branches
        }
    return render(request, 'signup.html',context)


# OTP verification view
def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')
        print(entered_otp)
        stored_otp = request.session.get('otp')
        print(stored_otp)
        if entered_otp == stored_otp:
            # OTP is valid, proceed with user creation and data storage
            form_data = request.session.get('signup_data', {})
            first_name = form_data.get('first_name')
            last_name = form_data.get('last_name')
            email = form_data.get('email')
            password1 = form_data.get('password1')
            user_type = form_data.get('user_type')
            college_name = form_data.get('college_name')
            branch = form_data.get('branch')
            # Create a new user instance
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            # Set the user_type attribute on the user instance
            user.user_type = user_type
            user.college_name = college_name
            user.branch = branch

            # Save the user instance to persist the changes
            user.save()

            # Clear the OTP and Signup from the session
            del request.session['otp']
            del request.session['signup_data']
            messages.success(request, 'Account created successfully !!')
            # Redirect to a success page or login page
            return redirect('signin')  # Replace with the URL name of your success page

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def signin(request):
    if request.method == 'POST':
        # Get the user's input from the form
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        # Authenticate the user against your CustomUser model
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            if next_url:
                # Redirect to the URL stored in the 'next' parameter
                return redirect(next_url)
            return redirect('index')  # Replace 'dashboard' with the URL name of your dashboard page
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    # Render the sign-in form
    return render(request, 'signin.html')


def user_logout(request):
    logout(request)
    return redirect('index')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            # Generate a password reset token
            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create a reset link
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[uid, token]))

            # Send the reset email
            # Email subject and message
            subject = 'Password Reset'
            message = (f'Hello User yes we got a request for your password reset Click the following link to reset your'
                       f'password: {reset_link}'
                       )

            # Email from address (sender) and recipient
            from_email = 'Asksbtet@gmail.com'  # Replace with your email
            recipient_list = [email]

            # Send the reset email with the reset link
            send_mail(subject, message, from_email, recipient_list)

            # Provide a success message
            messages.success(request, 'A password reset link has been sent to your email address.')
            return redirect('signin')

        else:
            # Provide an error message
            messages.error(request, 'No user with that email address exists.')
            return redirect('forgot_password')

    return render(request, 'forget_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, allow the user to reset the password
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                new_password = request.POST.get('password1')
                user.set_password(new_password)
                user.save()
                # Provide a success message
                messages.success(request, 'Password reset successfully.')
                return redirect('signin')
        return render(request, 'change_password.html')

    # If the token is invalid, provide an error message or redirect to an error page
    messages.error(request, 'Invalid password reset link.')
    return redirect('forgot_password')
