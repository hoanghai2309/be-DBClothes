# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Chinhanh(models.Model):
    machinhanh = models.CharField(db_column='MaChiNhanh', primary_key=True, max_length=3)  # Field name made lowercase.
    tenchinhanh = models.CharField(db_column='TenChiNhanh', max_length=20)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=10, blank=True, null=True)  # Field name made lowercase.
    duong = models.CharField(db_column='Duong', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quanhuyen = models.CharField(db_column='QuanHuyen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    thanhpho = models.CharField(db_column='ThanhPho', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chinhanh'


class Coupon(models.Model):
    mucgiamgia = models.FloatField(db_column='MucGiamGia', blank=True, null=True)  # Field name made lowercase.
    mucgiamgiamax = models.IntegerField(db_column='MucGiamGiaMax', blank=True, null=True)  # Field name made lowercase.
    mauudai = models.OneToOneField('Uudai', models.DO_NOTHING, db_column='MaUuDai', primary_key=True)  # Field name made lowercase.
    madonhang = models.ForeignKey('Donhang', models.DO_NOTHING, db_column='MaDonHang', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'coupon'



class Donhang(models.Model):
    manhanvien = models.ForeignKey('Nhanvienbanhang', models.DO_NOTHING, db_column='MaNhanVien')  # Field name made lowercase.
    madonhang = models.CharField(db_column='MaDonHang', primary_key=True, max_length=15)  # Field name made lowercase.
    machinhanh = models.ForeignKey(Chinhanh, models.DO_NOTHING, db_column='MaChiNhanh', blank=True, null=True)  # Field name made lowercase.
    tinhtrang = models.IntegerField(db_column='TinhTrang', blank=True, null=True)  # Field name made lowercase.
    ngaytaodon = models.DateField(db_column='NgayTaoDon')  # Field name made lowercase.
    tongtien = models.IntegerField(db_column='TongTien', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='SoDienThoai', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donhang'


class Khachhang(models.Model):
    sodienthoai = models.CharField(db_column='SoDienThoai', primary_key=True, max_length=10)  # Field name made lowercase.
    diemtichluy = models.IntegerField(db_column='DiemTichLuy')  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=1, blank=True, null=True)  # Field name made lowercase.
    duong = models.CharField(db_column='Duong', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quanhuyen = models.CharField(db_column='QuanHuyen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    thanhpho = models.CharField(db_column='ThanhPho', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'khachhang'


class Nhanvien(models.Model):
    manhanvien = models.CharField(db_column='MaNhanVien', primary_key=True, max_length=4)  # Field name made lowercase.
    machinhanh = models.ForeignKey(Chinhanh, models.DO_NOTHING, db_column='MaChiNhanh')  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=50)  # Field name made lowercase.
    luong = models.IntegerField(db_column='Luong', blank=True, null=True)  # Field name made lowercase.
    tuoi = models.IntegerField(db_column='Tuoi', blank=True, null=True)  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GioiTinh', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vitri = models.CharField(db_column='Vitri', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nhanvien'


class Nhanvienbanhang(models.Model):
    manhanvien = models.OneToOneField(Nhanvien, models.DO_NOTHING, db_column='MaNhanVien', primary_key=True)  # Field name made lowercase.
    calamviec = models.CharField(db_column='CaLamViec', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nhanvienbanhang'


class Nhanvienvanchuyen(models.Model):
    manhanvien = models.OneToOneField(Nhanvien, models.DO_NOTHING, db_column='MaNhanVien', primary_key=True)  # Field name made lowercase.
    banglaixe = models.CharField(db_column='BangLaiXe', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nhanvienvanchuyen'


class Quanly(models.Model):
    manhanvien = models.OneToOneField(Nhanvien, models.DO_NOTHING, db_column='MaNhanVien', primary_key=True)  # Field name made lowercase.
    machinhanh = models.ForeignKey(Chinhanh, models.DO_NOTHING, db_column='MaChiNhanh', blank=True, null=True)  # Field name made lowercase.
    namkinhnghiem = models.IntegerField(db_column='NamKinhNghiem', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quanly'


class Uudai(models.Model):
    mauudai = models.CharField(db_column='MaUuDai', primary_key=True, max_length=8)  # Field name made lowercase.
    mahanche = models.ForeignKey('self', models.DO_NOTHING, db_column='MaHanChe', blank=True, null=True)  # Field name made lowercase.
    sotientoithieu = models.IntegerField(db_column='SoTienToiThieu', blank=True, null=True)  # Field name made lowercase.
    tinhtrang = models.IntegerField(db_column='TinhTrang', blank=True, null=True)  # Field name made lowercase.
    batdau = models.DateField(db_column='BatDau')  # Field name made lowercase.
    ketthuc = models.DateField(db_column='KetThuc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'uudai'
