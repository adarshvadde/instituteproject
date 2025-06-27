from django.db import models
import uuid
import random
from datetime import datetime
class AdminUser(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40)
    email=models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=100)

class StudentUser(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40)
    email=models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=100)
    
    
class AttendanceRecord(models.Model):
    unique_id = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='attendance_unique_id_records' ,null=True)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='student_attendance_records',null=True)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')],
        default='Absent'
    )
from django.db import transaction
class Application(models.Model):
    unique_id=models.ForeignKey(StudentUser,on_delete=models.CASCADE,null=True)

    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
    mobile = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    father_name = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=15)
    father_aadhar = models.CharField(max_length=20, blank=True, null=True)
    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=15, blank=True, null=True)
    mother_aadhar = models.CharField(max_length=20, blank=True, null=True)

    # Image uploads
    student_photo = models.ImageField(upload_to='photos/students/')
    father_photo = models.ImageField(upload_to='photos/fathers/')
    mother_photo = models.ImageField(upload_to='photos/mothers/')

    # Education Info
    qualification = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200)
    college_city = models.CharField(max_length=100)
    college_state = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=200, blank=True, null=True)
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    aggregate = models.CharField(max_length=10, blank=True, null=True)
    yop = models.CharField(max_length=4, blank=True,null=True)
    agg12 = models.CharField(max_length=10, blank=True, null=True)
    yop12 = models.CharField(max_length=4, blank=True, null=True)
    agg10 = models.CharField(max_length=10, blank=True, null=True)
    yop10 = models.CharField(max_length=4, blank=True, null=True)
    training = models.CharField(max_length=200, blank=True, null=True)
    current_backlogs = models.CharField(max_length=10, blank=True, null=True)
    history_backlogs = models.CharField(max_length=10, blank=True, null=True)
    gap_academics = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    referred_by = models.CharField(max_length=100, blank=True, null=True)
    studentid = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Office use only
    referred_by_office = models.CharField(max_length=100, blank=True, null=True)
    counsellor = models.CharField(max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=100, blank=True,null=True)
    cfs_code = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate studentid only if it's not already set
        if not self.studentid:
            current_datetime = datetime.now()
            year_part = self.yop if self.yop else "XXXX" # Use YOP or current year
            
            # Determine prefix based on model_name
            prefix_map = {
                'Ignite': 'IG',
                'Elite': 'ET',
                'Elite Premium': 'EP',
            }
            # Use .get() with a default for cases where model_name might be unexpected or None
            model_prefix = prefix_map.get(self.model_name, 'UN') # 'UN' for unknown model

            # Month abbreviation (e.g., Jan, Feb)
            month_abbr = current_datetime.strftime('%b')[:3].upper()

            # Construct the base ID prefix for querying
            base_id_pattern = f"SVR{year_part[3]}{month_abbr}{model_prefix}"

            # Atomically get the next sequence number to prevent race conditions
            # This is a common pattern for generating sequential IDs safely.
            with transaction.atomic():
                # Get the maximum existing sequence number for the current prefix
                last_application_with_prefix = Application.objects.filter(
                    studentid__startswith=base_id_pattern
                ).order_by('-studentid').first() # Get the latest entry

                sequence_num = 1
                if last_application_with_prefix and last_application_with_prefix.studentid:
                    try:
                        # Extract the numeric part from the end of the studentid
                        # Assuming the format is SVRYYMMMPREFIXNNNNN
                        current_sequence_str = last_application_with_prefix.studentid[len(base_id_pattern):]
                        sequence_num = int(current_sequence_str) + 1
                    except (ValueError, IndexError):
                        # Fallback if parsing fails, just start from 1
                        sequence_num = 1
                
                # Format the sequence number with leading zeros (e.g., 00001, 00010)
                # Adjust padding (e.g., 5 digits for up to 99999 applications per prefix per month/year)
                padded_sequence = f"{sequence_num:05d}" 

                self.studentid = f"{base_id_pattern}{padded_sequence}"
                print(f"Generated Student ID: {self.studentid}")

        super().save(*args, **kwargs)


    



    

class WeeklyWorkReport(models.Model):
    """
    Represents a weekly work report for a student.
    """
    # Header Information
    # ForeignKey to the User model, linking a report to a specific user.
    # null=True allows existing reports to be saved if unique_id is not immediately available,
    # though in practice, it should always be set for new reports.
    unique_id = models.ForeignKey(StudentUser, on_delete=models.CASCADE, null=True)

    student_name = models.CharField(
        max_length=255,
        verbose_name="Student Name" # Added verbose_name for better display in admin/forms
    )
    student_id = models.CharField(
        max_length=15,
        verbose_name="Student ID Number" # Added verbose_name
    )
    
    report_date_from = models.DateField(
        verbose_name="Report Start Date" # Added verbose_name
    )
    report_date_to = models.DateField(
        verbose_name="Report End Date" # Added verbose_name
    )

    # Summary Information
    # Changed back to CharField as per your last model definition
    total_hours_class = models.CharField(
        max_length=10,
        verbose_name="Total Hours Worked" # Added verbose_name
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the creation timestamp
    updated_at = models.DateTimeField(auto_now=True)     # Automatically updates the timestamp on each save

    def __str__(self):
        return f"Report for {self.student_name} ({self.report_date_from} to {self.report_date_to})"

    class Meta:
        # Optional: Define ordering, unique constraints, or database table name
        ordering = ['-report_date_from'] # Order reports by most recent first
        # verbose_name = "Weekly Work Report" # For single object display in admin
        # verbose_name_plural = "Weekly Work Reports" # For list display in admin


class DailyEntry(models.Model):
    """
    Represents a single day's work entry within a WeeklyWorkReport.
    """
    # ForeignKey to WeeklyWorkReport, linking this entry to its parent report.
    report = models.ForeignKey(
        WeeklyWorkReport,
        on_delete=models.CASCADE, # If the parent report is deleted, daily entries are also deleted
        related_name='daily_entries' # Allows accessing daily entries from report: report.daily_entries.all()
    )
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
        ],
        verbose_name="Day of Week" # Added verbose_name
    )
    entry_date = models.DateField(
        blank=True, # Allow field to be blank in forms
        null=True,  # Allow field to be NULL in the database
        verbose_name="Date" # Added verbose_name
    )
    
    task_accomplished = models.TextField(
        blank=True,
        null=True,
        verbose_name="Tasks Accomplished" # Added verbose_name
    )

    def __str__(self):
        return f"{self.report.student_name} - {self.day_of_week} ({self.entry_date})"

    class Meta:
        # Define ordering for daily entries within a report
        ordering = ['entry_date', 'day_of_week']
        # You might want to add unique_together if a student can only submit one entry per day per report
        # unique_together = ('report', 'entry_date',)
        # verbose_name = "Daily Entry"
        # verbose_name_plural = "Daily Entries"