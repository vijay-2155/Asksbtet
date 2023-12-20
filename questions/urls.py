from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('AskyourQuestion/', views.AskyourQuestion, name='AskyourQuestion'),
    path('Myquestions/', views.Myquestions, name="Myquestions"),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/submit_answer/', views.submit_answer, name='submit_answer'),
    path('notifications/', views.notifications, name='notifications')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

