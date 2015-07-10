# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BaseFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FeeTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receipt_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LectureBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('duration', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('gender', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('gender', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StaffRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch', models.ForeignKey(to='portal.Branch')),
                ('role', models.ForeignKey(to='portal.Role')),
                ('staff', models.ForeignKey(to='portal.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('gender', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StudentBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch', models.ForeignKey(to='portal.Batch')),
                ('student', models.ForeignKey(to='portal.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentParent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent', models.ForeignKey(to='portal.Parent')),
                ('student', models.ForeignKey(to='portal.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('standard', models.ForeignKey(to='portal.Standard')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='academicyear',
            name='is_current',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subjectyear',
            name='academic_year',
            field=models.ForeignKey(to='portal.AcademicYear'),
        ),
        migrations.AddField(
            model_name='subjectyear',
            name='subject',
            field=models.ForeignKey(to='portal.Subject'),
        ),
        migrations.AddField(
            model_name='studentbatch',
            name='subject_years',
            field=models.ManyToManyField(to='portal.SubjectYear'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subject_year',
            field=models.ForeignKey(to='portal.SubjectYear'),
        ),
        migrations.AddField(
            model_name='feetransaction',
            name='fee_type',
            field=models.ForeignKey(to='portal.FeeType'),
        ),
        migrations.AddField(
            model_name='feetransaction',
            name='student_batch',
            field=models.ForeignKey(to='portal.StudentBatch'),
        ),
        migrations.AddField(
            model_name='basefee',
            name='subject_years',
            field=models.ManyToManyField(to='portal.SubjectYear'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='lecture_batch',
            field=models.ForeignKey(to='portal.LectureBatch'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student_batch',
            field=models.ForeignKey(to='portal.StudentBatch'),
        ),
    ]
