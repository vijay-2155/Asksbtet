from django.urls import path
from . import views
urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('verify_otp/', views.verify_otp_view, name="verify_otp"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]

