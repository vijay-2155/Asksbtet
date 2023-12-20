import json
from django.contrib import messages
import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from questions.models import Question, Branch


# Create your views here.


def index(request):
    user = request.user  # Get the current user
    if user.is_authenticated:
        branch = user.branch  # Get the branch from the user's profile
        questions = Question.objects.filter(stream=branch)
    else:
        # If the user is not authenticated, show all questions
        questions = Question.objects.all()

    context = {
        'questions': questions,
    }
    return render(request, 'index.html', context)


def branch(request):
    branches = Branch.objects.all()  # Retrieve all branches from the database
    context = {
        'branches': branches  # Pass the branches to the template context
    }
    return render(request, 'branch.html', context)


# Set your OpenAI API key here
api_key = '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'

openai.api_key = api_key


@login_required
def chatbot(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body)
        user_input = data.get('user_input')
        print(user_input)

        # Send the user's input to the OpenAI API and get the bot's response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=200  # Adjust as needed
        )

        bot_response = response.choices[0].text

        # Return the bot's response as JSON
        return JsonResponse({'bot_response': bot_response})

    return render(request, 'chatbot.html')


def each_branch(request, branch_name):
    # Retrieve questions related to the branch
    questions = Question.objects.filter(stream=branch_name)
    branch = Branch.objects.filter(short_form=branch_name)
    for i in branch:
        section = i
    context = {  # Pass the short form to the template
        'questions': questions,
        'section': section
    }

    return render(request, 'questions.html', context)


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Send an email
        subject = f'New contact form submission from {name}'
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['thoughtvijay@gmail.com']  # Replace with your email address

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, 'email sent successfully we will reach you back!')
        return render(request, 'contactus.html')  # Redirect to a success page

    return render(request, 'contactus.html')


def blog(request):
    return render(request,'blog.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def search_questions(request):
    query = request.GET.get('query', '')

    if query:
        # Modify this query to match your actual search criteria
        results = Question.objects.filter(title__icontains=query)[:10]

        # Create a list of dictionaries for each result
        results_list = [{'id': question.id, 'title': question.title} for question in results]

        return JsonResponse({'results': results_list})
    else:
        return JsonResponse({'results': []})
