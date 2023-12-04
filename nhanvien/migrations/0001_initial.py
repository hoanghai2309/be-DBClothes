# Generated by Django 4.2.6 on 2023-12-03 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chinhanh',
            fields=[
                ('machinhanh', models.CharField(db_column='MaChiNhanh', max_length=3, primary_key=True, serialize=False)),
                ('tenchinhanh', models.CharField(db_column='TenChiNhanh', max_length=20)),
                ('sodienthoai', models.CharField(blank=True, db_column='SoDienThoai', max_length=10, null=True)),
                ('duong', models.CharField(blank=True, db_column='Duong', max_length=50, null=True)),
                ('quanhuyen', models.CharField(blank=True, db_column='QuanHuyen', max_length=50, null=True)),
                ('thanhpho', models.CharField(blank=True, db_column='ThanhPho', max_length=50, null=True)),
            ],
            options={
                'db_table': 'chinhanh',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nhanvien',
            fields=[
                ('manhanvien', models.CharField(db_column='MaNhanVien', max_length=4, primary_key=True, serialize=False)),
                ('ten', models.CharField(db_column='Ten', max_length=50)),
                ('luong', models.IntegerField(blank=True, db_column='Luong', null=True)),
                ('tuoi', models.IntegerField(blank=True, db_column='Tuoi', null=True)),
                ('gioitinh', models.CharField(blank=True, db_column='GioiTinh', max_length=1, null=True)),
                ('trangthai', models.CharField(blank=True, db_column='TrangThai', max_length=1, null=True)),
                ('vitri', models.CharField(db_column='Vitri', max_length=1)),
            ],
            options={
                'db_table': 'nhanvien',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nhanvienbanhang',
            fields=[
                ('manhanvien', models.OneToOneField(db_column='MaNhanVien', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='nhanvien.nhanvien')),
                ('calamviec', models.CharField(blank=True, db_column='CaLamViec', max_length=1, null=True)),
            ],
            options={
                'db_table': 'nhanvienbanhang',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nhanvienvanchuyen',
            fields=[
                ('manhanvien', models.OneToOneField(db_column='MaNhanVien', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='nhanvien.nhanvien')),
                ('banglaixe', models.CharField(blank=True, db_column='BangLaiXe', max_length=2, null=True)),
            ],
            options={
                'db_table': 'nhanvienvanchuyen',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Quanly',
            fields=[
                ('manhanvien', models.OneToOneField(db_column='MaNhanVien', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='nhanvien.nhanvien')),
                ('namkinhnghiem', models.IntegerField(blank=True, db_column='NamKinhNghiem', null=True)),
            ],
            options={
                'db_table': 'quanly',
                'managed': False,
            },
        ),
    ]