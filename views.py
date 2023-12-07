from MySQLdb import  OperationalError
from django.db.models import Max, Sum, Min
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from django.db.models import Prefetch
from django.db.models import Q
from datetime import datetime
from django.db import connection
from rest_framework import viewsets
from .models import Nhanvienbanhang, Donhang
from .serializers import NhanvienbanhangSerializer,QuanlySerializer
from django.db import connection, DatabaseError
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from .serializers import NhanvienSerializer, QuanlySerializer, NhanvienbanhangSerializer, NhanvienvanchuyenSerializer
from django.db.models import Max, Min

class EmployeeListCreateAPIView(ListCreateAPIView):
    queryset = Nhanvien.objects.all()
    serializer_class = NhanvienSerializer

    def create(self, request, *args, **kwargs):
        position = request.data.get('vitri', None)
        salary = int(request.data.get('luong', None))

        try:
            with connection.cursor() as cursor:
                cursor.callproc(
                    'CreateEmployee',
                    [
                        request.data.get('manhanvien'),
                        request.data.get('machinhanh'),
                        request.data.get('ten'),
                        salary,
                        request.data.get('tuoi'),
                        request.data.get('gioitinh'),
                        request.data.get('trangthai'),
                        position,
                        request.data.get('calamviec', None),
                        request.data.get('namkinhnghiem', None),
                        request.data.get('banglaixe', None),
                    ]
                )

                result = cursor.fetchone()

                if result[0] == 1:
                    # Error occurred in stored procedure
                    error_message = result[1]
                    if 'Salary of employee with position B or C must be lower than all position A employees'' salaries.' in error_message:
                        return Response({"detail": "Salary of employee with position A must be higher than all other employees' salaries."},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Fetch newly created employee data
            new_employee = Nhanvien.objects.get(manhanvien=request.data.get('manhanvien'))
            serialized_data = self.get_serializer(new_employee).data

            headers = self.get_success_headers(serialized_data)
            success_message = {"detail": "Employee created successfully."}
            return Response(success_message, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            success_message = {"detail": "Employee created successfully."}
            if str(e)=="'NoneType' object is not subscriptable": return Response(success_message, status=status.HTTP_201_CREATED)



from django.db import connection

class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # ... existing code ...
    queryset = Nhanvien.objects.all()
    serializer_class = NhanvienSerializer
    lookup_field = 'manhanvien'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        salary = int(request.data.get('luong', None))

        try:
            with connection.cursor() as cursor:
                cursor.callproc('UpdateEmployee', [instance.manhanvien, salary])
                # No need to fetch the result here, as the procedure doesn't return anything

            success_message = {"detail": "Employee updated successfully."}

            return super().update(request, *args, **kwargs)
        except DatabaseError as e:
            error_message = str(e)
            if "Salary of employee with position A must be higher than all other employees' salaries." in error_message:
                return Response(
                    {"detail": error_message},
                    status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST)




    def perform_destroy(self, instance):
        # ... existing code ...

        # Call the SQL delete procedure
        with connection.cursor() as cursor:
            cursor.callproc('DeleteEmployee', [instance.manhanvien])




class NhanvienbanhangViewSet(viewsets.ViewSet):
    queryset = Nhanvienbanhang.objects.all()

    def list(self, request):
        queryset = Nhanvienbanhang.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

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

    @action(detail=True, methods=['get', 'put'])
    def update_details(self, request, pk=None):
        nhanvienbanhang = Nhanvienbanhang.objects.get(manhanvien=pk)
        nhanvien = nhanvienbanhang.manhanvien

        if request.method == 'PUT':
            salary = request.data.get('luong')
            calamviec = request.data.get('calamviec')
            machinhanh = request.data.get('machinhanh')

            if salary is not None:
                min_salary_A = Nhanvien.objects.filter(vitri='A').aggregate(Min('luong'))['luong__min']
                if salary >= min_salary_A:
                    return Response(
                        {
                            "detail": "Salary of employee with position A must be higher than all other employees' salaries."},
                        status=status.HTTP_400_BAD_REQUEST)
                nhanvien.luong = salary
            if calamviec is not None:
                nhanvienbanhang.calamviec = calamviec
            if machinhanh is not None:
                chinhanh = Chinhanh.objects.get(machinhanh=machinhanh)
                nhanvien.machinhanh = chinhanh

            nhanvien.save()
            nhanvienbanhang.save()

            return Response({'status': 'details updated'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            # Return the current details of the employee
            data = {
                'manhanvien': nhanvien.manhanvien,
                'machinhanh': nhanvien.machinhanh.machinhanh,
                'ten': nhanvien.ten,
                'luong': nhanvien.luong,
                'calamviec': nhanvienbanhang.calamviec,
            }
            return Response(data, status=status.HTTP_200_OK)


from .serializers import DonhangSerializer, CouponSerializer

class DonhangViewSet(viewsets.ViewSet):
    queryset = Donhang.objects.all()
    def list(self, request):
        queryset = Donhang.objects.all()
        sodienthoai = request.query_params.get('sodienthoai', None)
        if sodienthoai is not None:
            queryset = Donhang.objects.filter(sodienthoai=sodienthoai)
        else:
            queryset = Donhang.objects.all()
        serializer = DonhangSerializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get', 'post'])
    def update_details(self, request, pk=None):
        donhang = Donhang.objects.get(madonhang=pk)
        tongtien = donhang.tongtien
        if request.method == 'POST':
            queryset = Coupon.objects.all()
            ma1 = request.data.get('ma1', None)
            ma2 = request.data.get('ma2', None)

            # Get the current date
            current_date = datetime.now().date()

            # Validate each coupon
            for ma in [ma for ma in [ma1, ma2] if ma is not None]:
                coupon = Coupon.objects.get(mauudai=ma)

                # Check if the coupon is already used
                if coupon.mauudai.tinhtrang == 1:
                    return Response({"error": f"Coupon {ma} has already been used."}, status=400)

                # Check if the coupon is within the valid date range
                if not (coupon.mauudai.batdau <= current_date <= coupon.mauudai.ketthuc):
                    return Response({"error": f"Coupon {ma} is not valid at this time."}, status=400)

                # Check if the order total meets the minimum requirement
                if tongtien < coupon.mauudai.sotientoithieu:
                    return Response({"error": f"Order total does not meet the minimum requirement for coupon {ma}."}, status=400)

            # Check if the two coupons are in conflict
            if ma1 is not None and ma2 is not None and Hanche.objects.filter(Q(mauudai=ma1, uudaihanche=ma2) | Q(mauudai=ma2, uudaihanche=ma1)).exists():
                return Response({"error": "The two coupons cannot be used together."}, status=400)

            # If all checks pass, apply the coupons and update the order total
            for ma in [ma for ma in [ma1, ma2] if ma is not None]:
                coupon = Coupon.objects.get(mauudai=ma)
                tongtien -= min(coupon.mucgiamgia * tongtien, coupon.mucgiamgiamax)
                coupon.mauudai.tinhtrang = 1
                coupon.madonhang=donhang
                coupon.mauudai.save()
                coupon.save()
            donhang.tinhtrang=1
            donhang.tongtien = tongtien
            donhang.save()

            return Response({"message": "Coupons applied successfully.", "new_total": tongtien},status=200)
        elif request.method == 'GET':
            if donhang.tinhtrang==1:
                return Response({"tinh trang":1})
            # Return the current details of the employee
            data = {
                'ma1': None,
                'ma2': None,
            }
            return Response(data, status=status.HTTP_200_OK)
