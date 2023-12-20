from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from questions.models import Question, Branch
from .models import Answer


# Create your views here.


@login_required
def AskyourQuestion(request):
    if request.method == 'POST':
        stream = request.POST.get('stream')
        title = request.POST.get('question')
        description = request.POST.get('description')
        user_expect = request.POST.get('user-expecting')
        responses_via_email = request.POST.get('responses') == 'checkedValue'
        image = request.FILES.get('image')  # Use request.FILES to access uploaded files
        # Check if any of the required fields is empty
        if not stream or not title or not description:
            # Determine which field is empty and display an error message
            if not stream:
                messages.error(request, "Stream field is required.")
            if not title:
                messages.error(request, "Title field is required.")
            if not description:
                messages.error(request, "Description field is required.")
            # Redirect back to the form page
            return redirect('AskyourQuestion')
        try:
            Branch.objects.get(short_form=stream)
        except Branch.DoesNotExist:
            messages.error(request, "The selected stream does not exist.")
            return redirect('AskyourQuestion')

        # Check if the user is authenticated (you can replace this with your own logic)
        if request.user.is_authenticated:
            question = Question(
                stream=stream,
                title=title,
                description=description,
                user_expect=user_expect,
                responses_via_email=responses_via_email,
                image=image,
                user=request.user  # Assign the user who asked the question
            )
            question.save()

            messages.success(request, "Your question has been submitted successfully.")
            return redirect('Myquestions')  # Redirect to a success page

        else:
            messages.warning(request, "You must sign in to ask a question.")
            return redirect('signin')  # Redirect to the sign-in page if the user is not authenticated
    branches = Branch.objects.all()
    if branches:
        context = {
            'branches': branches
        }
    return render(request, 'question.html', context)


@login_required
def Myquestions(request):
    user = request.user  # Get the current user
    if user.is_authenticated:
        email = user.email
        questions = Question.objects.filter(user__email=email)
    if questions:
        context = {
            'questions': questions,
        }
        return render(request, 'myquestions.html', context)
    else:
        messages.warning(request, "you Did not Asked any questions till now")
        return render(request, 'myquestions.html')


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Retrieve answers related to the question using the question field
    answers = Answer.objects.filter(question=question)
    question.view_count += 1
    question.save()

    context = {
        'question': question,
        'answers': answers,  # Pass the answers queryset to the template
    }

    return render(request, 'answer.html', context)


def submit_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        answer_text = request.POST.get('answer')
        image = request.FILES.get('image')  # Uploaded image file

        if answer_text:
            # Create a new answer object
            answer = Answer(
                question_id=question_id,
                user=request.user,  # Assign the user who answered the question
                content=answer_text,  # Use the 'content' field for answer text
                image=image,  # Assign the uploaded image
            )
            answer.save()

            # Call the email notification function
            send_email_notification(
                sender_name=request.user.first_name,
                sender_college=request.user.college_name,
                question_title=question.title,
                answer_text=answer_text,
                question_url=request.build_absolute_uri(question.get_absolute_url()),
                recipient_email=question.user.email,
            )

            messages.success(request, 'Your Answer Submitted Successfully')
            # Redirect to the question detail page after answer submission
            return redirect('question_detail', question_id=question_id)
        else:
            # Handle invalid form submission (e.g., answer_text is empty)
            messages.error(request, "Please provide an answer to the question.")
            return redirect('question_detail', question_id=question_id)
    # Handle GET requests or invalid form submissions
    messages.error(request, 'Invalid Response!')
    return redirect('question_detail', question_id=question_id)


def send_email_notification(sender_name, sender_college, question_title, answer_text, question_url, recipient_email):
    # Create an email subject
    subject = f"{sender_name} has answered your question on AskSbtet"

    # Render the email body using the provided template
    email_message = render_to_string('email_notification.html', {
        'sender_name': sender_name,
        'sender_college': sender_college,
        'question_title': question_title,
        'answer_text': answer_text,
        'question_url': question_url,
    })

    send_mail(
        subject,
        email_message,
        'vijaykumartholeti2005@gmail.com',  # Replace with your email address or a custom sender
        [recipient_email],  # Replace with the recipient's email address
        fail_silently=False,  # Set to True to suppress errors if email sending fails
        html_message=email_message  # Enable HTML content in the email
    )


def notifications(request):
    return render(request, 'notifications.html')
