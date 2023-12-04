from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nhanvien.urls')),  # replace 'your_app_name' with the actual name of your app
]
