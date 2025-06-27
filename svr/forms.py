from django import forms
from django.contrib.auth.models import User
from . import models



#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = models.StudentUser
        fields = ['username', 'phone_number', 'email', 'password']

class StudentUserLoginForm(forms.Form):
     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


from django import forms
from . import models
from datetime import date

class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today())

    def __init__(self, *args, **kwargs):
        # Pass students_data or something similar to build dynamic fields
        all_applications = kwargs.pop('all_applications', []) 
        super().__init__(*args, **kwargs)

        for application_obj in all_applications:
            # Ensure application_obj.unique_id exists and has a unique_id attribute
            if application_obj.unique_id and hasattr(application_obj.unique_id, 'unique_id'):
                student_user_uuid = str(application_obj.unique_id.unique_id) # Convert UUID to string for field name
                field_name = f'student_{student_user_uuid}'
                
                # Define choices for attendance status
                ATTENDANCE_CHOICES = [
                    ('Present', 'Present'),
                    ('Absent', 'Absent'),
                    
                ]

                # Make sure the field is not required if it's acceptable for it to be unchecked
                # If radio buttons are used, one *must* be selected for the field to have a value.
                # If you want to allow no selection (which usually means Absent), you might make it not required
                # and handle the default in your view.
                self.fields[field_name] = forms.ChoiceField(
                    choices=ATTENDANCE_CHOICES,
                    widget=forms.RadioSelect, # Or forms.Select if you want a dropdown
                    required=False, # <--- THIS IS OFTEN THE CULPRIT!
                    label=f"{application_obj.first_name} {application_obj.last_name}"
                )
            else:
                print(f"Skipping application {application_obj.id} due to missing StudentUser unique_id.")
            
from datetime import date, timedelta

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, # Make it optional, will set defaults in view
        label="Start Date",
        initial=date.today() - timedelta(days=30) # Default to 30 days ago
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False, # Make it optional
        label="End Date",
        initial=date.today() # Default to today
    )




class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        exclude =['unique_id']
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class WeeklyWorkReportForm(forms.ModelForm):
    """
    Form for creating and updating WeeklyWorkReport instances.
    """
    class Meta:
        model = models.WeeklyWorkReport
        # Include 'unique_id' in fields because the HTML template now renders an input for it.
        # If 'unique_id' is intended to be automatically set by the view (e.g., to request.user),
        # consider making it a HiddenInput in widgets or removing it from fields and setting it in the view.
        exclude=['unique_id']
        fields = [
            'unique_id', # Included as requested
            'student_name',
            'student_id',
            'report_date_from',
            'report_date_to',
            'total_hours_class', # Matches the updated model field name
        ]
        widgets = {
            # unique_id could be a forms.HiddenInput() if you want to set it programmatically in the view
            # and not allow users to change it, or a forms.Select() if it's for selection.
            # For now, it will render as a default Select input if a ForeignKey.
            'report_date_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'report_date_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # For total_hours_class, using TextInput with a placeholder for consistency with CharField
            'total_hours_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 40'}), 
        }
        labels = {
            'unique_id': 'User ID', # Label for the unique_id field
            'student_name': 'Student Name',
            'student_id': 'Student ID Number',
            'report_date_from': 'Report Start Date',
            'report_date_to': 'Report End Date',
            'total_hours_class': 'Total Hours Worked', 
        }
    
    # You can add custom validation or modify form behavior here if needed
    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Example: ensure report_date_to is after report_date_from
    #     from_date = cleaned_data.get('report_date_from')
    #     to_date = cleaned_data.get('report_date_to')
    #     if from_date and to_date and from_date > to_date:
    #         self.add_error('report_date_to', "End date cannot be before start date.")
    #     return cleaned_data


class DailyEntryForm(forms.ModelForm):
    """
    Form for creating and updating DailyEntry instances.
    """
    class Meta:
        model = models.DailyEntry
        fields = [
            'day_of_week', # Hidden input in widget to ensure value is submitted, but not editable
            'entry_date',
            'task_accomplished',
            # 'approximate_hours' is removed as per your latest model definition
        ]
        widgets = {
            # Use HiddenInput for day_of_week so its value is passed, but not displayed as editable input.
            # The value will be pre-filled from initial data in the view.
            'day_of_week':forms.Select(attrs={'class': 'form-control'}),
            'entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'task_accomplished': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'day_of_week': 'Day', # Label is still useful for error messages or internal reference
            'entry_date': 'Date',
            'task_accomplished': 'Task Accomplished',
        }


    




    
    



