# Generated by Django 5.1.3 on 2024-12-09 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoginTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(blank=True, max_length=50, null=True)),
                ('LOGIN_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.logintable')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField(blank=True, null=True)),
                ('DEP_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.departmenttable')),
            ],
        ),
        migrations.CreateModel(
            name='classTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('DEP_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.departmenttable')),
                ('LOGIN_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.logintable')),
                ('SEM_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.semestertable')),
            ],
        ),
        migrations.CreateModel(
            name='StaffTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('qualification', models.CharField(blank=True, max_length=50, null=True)),
                ('COLLEGE_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.collegetable')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.departmenttable')),
                ('lOGIN_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.logintable')),
            ],
        ),
        migrations.CreateModel(
            name='StudentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('COLLEGE_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.collegetable')),
                ('DEP_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.departmenttable')),
                ('LOGIN_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.logintable')),
            ],
        ),
    ]
