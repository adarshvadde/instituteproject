# Generated by Django 3.0.6 on 2025-06-22 16:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyWorkReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=255, verbose_name='Student Name')),
                ('student_id', models.CharField(max_length=15, verbose_name='Student ID Number')),
                ('report_date_from', models.DateField(verbose_name='Report Start Date')),
                ('report_date_to', models.DateField(verbose_name='Report End Date')),
                ('total_hours_class', models.CharField(max_length=10, verbose_name='Total Hours Worked')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unique_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='svr.StudentUser')),
            ],
            options={
                'ordering': ['-report_date_from'],
            },
        ),
        migrations.CreateModel(
            name='DailyEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=10, verbose_name='Day of Week')),
                ('entry_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('task_accomplished', models.TextField(blank=True, null=True, verbose_name='Tasks Accomplished')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_entries', to='svr.WeeklyWorkReport')),
            ],
            options={
                'ordering': ['entry_date', 'day_of_week'],
            },
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent', max_length=10)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance_records', to='svr.StudentUser')),
                ('unique_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_unique_id_records', to='svr.StudentUser')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('mobile', models.CharField(max_length=15)),
                ('whatsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('father_name', models.CharField(max_length=100)),
                ('father_mobile', models.CharField(max_length=15)),
                ('father_aadhar', models.CharField(blank=True, max_length=20, null=True)),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('mother_aadhar', models.CharField(blank=True, max_length=20, null=True)),
                ('student_photo', models.ImageField(upload_to='photos/students/')),
                ('father_photo', models.ImageField(upload_to='photos/fathers/')),
                ('mother_photo', models.ImageField(upload_to='photos/mothers/')),
                ('qualification', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=100)),
                ('college_name', models.CharField(max_length=200)),
                ('college_city', models.CharField(max_length=100)),
                ('college_state', models.CharField(blank=True, max_length=100, null=True)),
                ('university', models.CharField(blank=True, max_length=200, null=True)),
                ('roll_no', models.CharField(blank=True, max_length=50, null=True)),
                ('aggregate', models.CharField(blank=True, max_length=10, null=True)),
                ('yop', models.CharField(blank=True, max_length=4, null=True)),
                ('agg12', models.CharField(blank=True, max_length=10, null=True)),
                ('yop12', models.CharField(blank=True, max_length=4, null=True)),
                ('agg10', models.CharField(blank=True, max_length=10, null=True)),
                ('yop10', models.CharField(blank=True, max_length=4, null=True)),
                ('training', models.CharField(blank=True, max_length=200, null=True)),
                ('current_backlogs', models.CharField(blank=True, max_length=10, null=True)),
                ('history_backlogs', models.CharField(blank=True, max_length=10, null=True)),
                ('gap_academics', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('referred_by', models.CharField(blank=True, max_length=100, null=True)),
                ('studentid', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('referred_by_office', models.CharField(blank=True, max_length=100, null=True)),
                ('counsellor', models.CharField(blank=True, max_length=100, null=True)),
                ('model_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cfs_code', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('unique_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='svr.StudentUser')),
            ],
        ),
    ]
