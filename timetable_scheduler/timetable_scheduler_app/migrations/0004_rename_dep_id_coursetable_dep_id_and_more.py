# Generated by Django 5.1.3 on 2024-12-12 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_scheduler_app', '0003_rename_college_name_collegetable_college'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursetable',
            old_name='DEP_ID',
            new_name='dep_id',
        ),
        migrations.RenameField(
            model_name='semestertable',
            old_name='LOGIN_ID',
            new_name='login_id',
        ),
        migrations.RenameField(
            model_name='stafftable',
            old_name='department',
            new_name='department_id',
        ),
        migrations.RenameField(
            model_name='stafftable',
            old_name='lOGIN_ID',
            new_name='login_id',
        ),
        migrations.RenameField(
            model_name='studenttable',
            old_name='LOGIN_ID',
            new_name='login_id',
        ),
        migrations.RenameField(
            model_name='studenttable',
            old_name='SEMESTER_ID',
            new_name='semester_id',
        ),
        migrations.RemoveField(
            model_name='stafftable',
            name='COLLEGE_ID',
        ),
        migrations.AddField(
            model_name='stafftable',
            name='college_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable_scheduler_app.collegetable'),
        ),
    ]
