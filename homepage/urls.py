from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('branches', views.branch, name='branch'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('each_branch/<str:branch_name>/', views.each_branch, name='each_branch'),
    path('contactus/', views.contactus, name='contactus'),
    path('blog/', views.blog, name='blog'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search_questions, name='search_questions_api'),

]
