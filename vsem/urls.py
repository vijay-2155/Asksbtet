
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('questions/',include('questions.urls')),
    path('questions/', include('authentication.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)