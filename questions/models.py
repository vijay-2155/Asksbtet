from django.db import models
from django.utils import timezone
from django.urls import reverse

from authentication.models import CustomUser  # Import your user model here if needed


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user_expect = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the question to a user
    stream = models.CharField(max_length=50)  # You can replace this with your own choices
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    responses_via_email = models.BooleanField(default=True)
    answers = models.ManyToManyField('Answer', related_name='question_answers', blank=True)
    modified_at = models.DateTimeField(default=timezone.now)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        # Define the URL pattern name for the question detail view
        return reverse('question_detail', args=[str(self.id)])


class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='answer_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers', default=None)

    def __str__(self):
        return f"Answer by {self.user.email}"

    class Meta:
        ordering = ['-created_at']


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='branch_images/', null=True, blank=True)
    short_form = models.CharField(max_length=10)

    def __str__(self):
        return self.name
