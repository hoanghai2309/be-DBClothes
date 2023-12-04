
from .views import EmployeeListCreateAPIView, EmployeeRetrieveUpdateDestroyAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NhanvienbanhangViewSet

router = DefaultRouter()
router.register(r'nhanvienbanhang', NhanvienbanhangViewSet, basename='nhanvienbanhang')


urlpatterns = [
    path('', include(router.urls)),
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<str:manhanvien>/', EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-retrieve-update-destroy'),
]
