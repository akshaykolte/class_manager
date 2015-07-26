# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year_start', models.IntegerField()),
                ('year_end', models.IntegerField()),
                ('is_current', models.BooleanField()),
            ],
        ),
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
                ('academic_year', models.ForeignKey(to='portal.AcademicYear')),
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
                ('batch', models.ForeignKey(to='portal.Batch')),
                ('lecture', models.ForeignKey(to='portal.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
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
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
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
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
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
                ('academic_year', models.ForeignKey(to='portal.AcademicYear')),
                ('subject', models.ForeignKey(to='portal.Subject')),
            ],
        ),
        migrations.AddField(
            model_name='studentbatch',
            name='subject_years',
            field=models.ManyToManyField(to='portal.SubjectYear'),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set([('email',), ('phone_number',), ('username',)]),
        ),
        migrations.AlterUniqueTogether(
            name='standard',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='staff',
            unique_together=set([('email',), ('phone_number',), ('username',)]),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='parent',
            unique_together=set([('email',), ('phone_number',), ('username',)]),
        ),
        migrations.AddField(
            model_name='lecturebatch',
            name='staff_role',
            field=models.ForeignKey(to='portal.StaffRole'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subject_year',
            field=models.ForeignKey(to='portal.SubjectYear'),
        ),
        migrations.AlterUniqueTogether(
            name='feetype',
            unique_together=set([('name',)]),
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
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='batch',
            name='branch',
            field=models.ForeignKey(to='portal.Branch'),
        ),
        migrations.AddField(
            model_name='batch',
            name='standard',
            field=models.ForeignKey(to='portal.Standard'),
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
        migrations.AlterUniqueTogether(
            name='academicyear',
            unique_together=set([('year_start', 'year_end')]),
        ),
        migrations.AlterUniqueTogether(
            name='subjectyear',
            unique_together=set([('subject', 'academic_year')]),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('name', 'standard')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentparent',
            unique_together=set([('student', 'parent')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentbatch',
            unique_together=set([('student', 'batch')]),
        ),
        migrations.AlterUniqueTogether(
            name='staffrole',
            unique_together=set([('role', 'staff', 'branch')]),
        ),
        migrations.AlterUniqueTogether(
            name='lecturebatch',
            unique_together=set([('lecture', 'batch')]),
        ),
        migrations.AlterUniqueTogether(
            name='lecture',
            unique_together=set([('name', 'subject_year')]),
        ),
        migrations.AlterUniqueTogether(
            name='feetransaction',
            unique_together=set([('receipt_number',)]),
        ),
        migrations.AlterUniqueTogether(
            name='batch',
            unique_together=set([('name', 'academic_year', 'branch', 'standard')]),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('lecture_batch', 'student_batch')]),
        ),
    ]
