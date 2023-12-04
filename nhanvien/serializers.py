from rest_framework import serializers
from .models import Nhanvien, Nhanvienbanhang, Nhanvienvanchuyen, Quanly

class NhanvienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nhanvien
        fields = '__all__'

class NhanvienbanhangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nhanvienbanhang
        fields = '__all__'

class NhanvienvanchuyenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nhanvienvanchuyen
        fields = '__all__'

class QuanlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quanly
        fields = '__all__'
