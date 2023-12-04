from django.db.models import Max, Sum
from django.db.models.functions import datetime
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from django.db.models import Prefetch


from rest_framework import viewsets
from .models import Nhanvienbanhang, Donhang
from .serializers import NhanvienbanhangSerializer

class EmployeeListCreateAPIView(ListCreateAPIView):
    queryset = Nhanvien.objects.all()
    serializer_class = NhanvienSerializer

    def create(self, request, *args, **kwargs):
        position = request.data.get('vitri', None)
        salary = int(request.data.get('luong', None))
        if position == 'A':
            # Create Nhanvien instance
            nhanvien_serializer = self.get_serializer(data=request.data)
            nhanvien_serializer.is_valid(raise_exception=True)
            nhanvien_instance = nhanvien_serializer.save()
            if salary is not None:
                max_salary = Nhanvien.objects.exclude(vitri='A').aggregate(Max('luong'))['luong__max']
                if salary <= max_salary:
                    return Response({"detail": "Salary of employee with position A must be higher than all other employees' salaries."},
                                    status=status.HTTP_400_BAD_REQUEST)
            # Create Nhanvienbanhang instance
            nhanvienbanhang_data = {
                'manhanvien': nhanvien_instance.manhanvien,
                'machinhanh': nhanvien_instance.machinhanh.machinhanh,
                'namkinhnghiem': request.data.get('namkinhnghiem', None)
            }
            Quanly_serializer = QuanlySerializer(data=nhanvienbanhang_data)
            Quanly_serializer.is_valid(raise_exception=True)
            Quanly_serializer.save()

            headers = self.get_success_headers(nhanvien_serializer.data)
            return Response(nhanvien_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        elif position == 'B':
            # Create Nhanvien instance
            nhanvien_serializer = self.get_serializer(data=request.data)
            nhanvien_serializer.is_valid(raise_exception=True)
            nhanvien_instance = nhanvien_serializer.save()

            # Create Nhanvienbanhang instance
            nhanvienbanhang_data = {
                'manhanvien': nhanvien_instance.manhanvien,
                'calamviec': request.data.get('calamviec', None)
            }
            nhanvienbanhang_serializer = NhanvienbanhangSerializer(data=nhanvienbanhang_data)
            nhanvienbanhang_serializer.is_valid(raise_exception=True)
            nhanvienbanhang_serializer.save()

            headers = self.get_success_headers(nhanvien_serializer.data)
            return Response(nhanvien_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        elif position == 'C':
            # Create Nhanvien instance
            nhanvien_serializer = self.get_serializer(data=request.data)
            nhanvien_serializer.is_valid(raise_exception=True)
            nhanvien_instance = nhanvien_serializer.save()

            # Create Nhanvienbanhang instance
            Nhanvienvanchuyen_data = {
                'manhanvien': nhanvien_instance.manhanvien,
                'banglaixe': request.data.get('banglaixe', None)
            }
            Nhanvienvanchuyen_serializer = NhanvienvanchuyenSerializer(data=Nhanvienvanchuyen_data)
            Nhanvienvanchuyen_serializer.is_valid(raise_exception=True)
            Nhanvienvanchuyen_serializer.save()

            headers = self.get_success_headers(nhanvien_serializer.data)
            return Response(nhanvien_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        else:
            error_message = "Invalid position entered. Please provide a valid position (A, B, or C)."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Nhanvien.objects.all()
    serializer_class = NhanvienSerializer
    lookup_field = 'manhanvien'

    def update(self, request, *args, **kwargs):
        position = request.data.get('vitri', None)
        salary = int(request.data.get('luong', None))

        if position == 'A' and salary is not None:
            # Check if the salary is higher than all other employees' salaries
            max_salary = Nhanvien.objects.exclude(vitri='A').aggregate(Max('luong'))['luong__max']
            if salary <= max_salary:
                return Response({"detail": "Salary of employee with position A must be higher than all other employees' salaries."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


    def perform_destroy(self, instance):
        if instance.trangthai == '0':
            # If trangthai is 0, delete the instance
            instance.delete()
        else:
            # If trangthai is not 0, set trangthai to 2
            instance.trangthai = '2'
            instance.save()



class NhanvienbanhangViewSet(viewsets.ViewSet):
    queryset = Nhanvienbanhang.objects.all()

    def list(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        queryset = self.queryset
        data = []
        for nhanvien in queryset:
            if start_date is not None and end_date is not None:
                donhangs = Donhang.objects.filter(manhanvien=nhanvien, ngaytaodon__range=[start_date, end_date])
            else:
                donhangs = Donhang.objects.filter(manhanvien=nhanvien)
            total = donhangs.aggregate(Sum('tongtien'))['tongtien__sum']
            data.append({
                'manhanvien': nhanvien.manhanvien.manhanvien,
                'machinhanh': nhanvien.manhanvien.machinhanh.machinhanh,
                'ten': nhanvien.manhanvien.ten,
                'luong': nhanvien.manhanvien.luong,
                'calamviec': nhanvien.calamviec,
                'tongtien': total or 0,
            })
        return Response(data)

    @action(detail=True, methods=['put'])
    def update_details(self, request, pk=None):
        nhanvienbanhang = Nhanvienbanhang.objects.get(manhanvien=pk)
        nhanvien = nhanvienbanhang.manhanvien

        luong = request.data.get('luong')
        calamviec = request.data.get('calamviec')
        machinhanh = request.data.get('machinhanh')

        if luong is not None:
            nhanvien.luong = luong
        if calamviec is not None:
            nhanvienbanhang.calamviec = calamviec
        if machinhanh is not None:
            chinhanh = Chinhanh.objects.get(machinhanh=machinhanh)
            nhanvien.machinhanh = chinhanh

        nhanvien.save()
        nhanvienbanhang.save()

        return Response({'status': 'details updated'}, status=status.HTTP_200_OK)

