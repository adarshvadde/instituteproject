from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from svr.models import StudentUser, AttendanceRecord,Application,AdminUser,DailyEntry,WeeklyWorkReport
import calendar
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import uuid
import base64 # Import base64 module
from datetime import date as date_obj 
from django.db.models import Q
import uuid
import base64
from django.forms import inlineformset_factory
from django.shortcuts import render
from datetime import date, timedelta
from collections import defaultdict
from django.shortcuts import render, redirect
from .forms import AttendanceForm
from datetime import datetime

def encode_uuid_to_base64(uuid_input):
    """
    Encodes a UUID (either a uuid.UUID object or its string representation)
    into a URL-safe base64 string.
    """
    # Ensure uuid_input is a uuid.UUID object
    if isinstance(uuid_input, str):
        try:
            uuid_obj = uuid.UUID(uuid_input)
        except ValueError:
            raise ValueError(f"Invalid UUID string format: '{uuid_input}'")
    elif isinstance(uuid_input, uuid.UUID):
        uuid_obj = uuid_input
    else:
        raise TypeError(f"Input must be a uuid.UUID object or a UUID string, but got {type(uuid_input).__name__}.")

    # Convert UUID to bytes, then base64 encode, then strip padding and make URL-safe
    encoded_bytes = base64.urlsafe_b64encode(uuid_obj.bytes)
    return encoded_bytes.decode('utf-8').rstrip('=') # Remove trailing '==' or '=' padding
def decode_base64_to_uuid(b64_string):
    """
    Decodes a URL-safe base64 string back into a uuid.UUID object.
    """
    # Add padding back (base64 requires padding to be a multiple of 4)
    padded_b64_string = b64_string + '=' * (4 - len(b64_string) % 4)
    decoded_bytes = base64.urlsafe_b64decode(padded_b64_string)
    return uuid.UUID(bytes=decoded_bytes)
def student_home_view(request):
    gets=StudentUser.objects.all()
    
    for i in gets:
        
        print([i.username, i.phone_number, i.email, i.password,i.id])
    return render(request,'home.html')
def student_signup_view(request):
    gets=StudentUser.objects.all()
    for i in gets:
        print([i.username, i.phone_number, i.email, i.password])
    form1=forms.StudentUserForm()
    mydict={'form1':form1}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        print(request.POST)
        print(form1.is_valid())
        if form1.is_valid() :   
            user=form1.save()
            
            print([user.username,user.phone_number,user.email,user.password])

        return HttpResponseRedirect('/studentlogin')
    return render(request,'signup.html',context=mydict)
def student_login_view(request):
    form=forms.StudentUserLoginForm()
    mydict={'form':form}
    if request.method=='POST':
        form=forms.StudentUserLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            try:
                user=StudentUser.objects.get(email=email,password=password)
                uniqueid=encode_uuid_to_base64(user.unique_id)
                application=Application.objects.filter(unique_id=user)
                if application.exists():
                    try:
                        print("\nApplications found for this student:1")
                        return HttpResponseRedirect(f"/studenthome/{uniqueid}")

                    except:
                        print("No applications found for this student.1")
                else:
                    try:
                        print("\nApplications found for this student:1")
                        return HttpResponseRedirect(f"/studentapplicationform/{uniqueid}")

                    except:
                        print("No applications found for this student.1")

            except StudentUser.DoesNotExist:               
                admin=AdminUser.objects.get(email=email,password=password)
                uniqueid=encode_uuid_to_base64(admin.unique_id)
                try:
                    print("\nApplications found for this student:1")
                    return HttpResponseRedirect(f'/adminpage/{uniqueid}')

                except:
                    print("No applications found for this student.1")


            return render(request,'login.html',context=mydict)
    
            
    return render(request,'login.html',context=mydict)
@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        
        otp = str(random.randint(100000, 999999))

        # Save OTP in session
        request.session['otp'] = otp
        request.session['otp_email'] = email
        request.session.modified = True

        # Send email
        send_mail(
            subject='Your SVR OTP Code',
            message=f'Your OTP is {otp}',
            from_email='vaddeadarsh150@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'})
@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        print(request.POST)
        otp_input = request.POST.get('otp')
        otp_session = request.session.get('otp')
        print(f"Input OTP: {otp_input}, Session OTP: {otp_session}")

        if otp_input == otp_session:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})
@csrf_exempt
def forget_send_otp(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        
        if StudentUser.objects.filter(email=email).exists():
            otp = str(random.randint(100000, 999999))
            # Save OTP in session
            request.session['otp'] = otp
            request.session['otp_email'] = email
            request.session.modified = True

            # Send email
            send_mail(
                subject='Your SVR OTP Code',
                message=f'Your OTP is {otp}',
                from_email='vaddeadarsh150@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Email not registered'})
@csrf_exempt
def forget_verify_otp(request):
    if request.method == 'POST':
        print(request.POST)
        otp_input = request.POST.get('otp')
        otp_session = request.session.get('otp')
        print(f"Input OTP: {otp_input}, Session OTP: {otp_session}")

        if otp_input == otp_session:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})
def forget_password_view(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        user= StudentUser.objects.filter(email=email).first()
        user.password = request.POST.get('password')
        user.save()
        data={'status':'success', 'message': 'Password updated successfully'}
        return JsonResponse(data)

    return render(request,'forget.html')
def application_view(request, studentid):
    try:
        decoded_uuid = decode_base64_to_uuid(studentid)
    except ValueError:
        pass
        
    student = get_object_or_404(StudentUser, unique_id=str(decoded_uuid))
    application = Application.objects.filter(unique_id=student).first()

    if request.method == 'POST':
        submitted_fields = [k for k in request.POST.keys() if k != 'csrfmiddlewaretoken']
        
        if len(submitted_fields) == 1:
            field_name_to_update = submitted_fields[0]
            
            # Create a temporary form instance to get its default fields for validation
            # This is safer than _meta.fields directly if exclude is used.
            temp_form_for_field_check = forms.ApplicationForm() 

            if field_name_to_update not in temp_form_for_field_check.fields.keys():
                return JsonResponse({'success': False, 'errors': {field_name_to_update: ['Invalid or unauthorized field for update.']}}, status=400)

            if application:
                form = forms.ApplicationForm(request.POST, request.FILES, instance=application, fields=[field_name_to_update])
            else:
                return JsonResponse({'success': False, 'errors': 'No application to update.'}, status=400)
            
            if form.is_valid():
                form.save() 
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        else: # Full form submission
            if application:
                form = forms.ApplicationForm(request.POST, request.FILES, instance=application)
            else:
                form = forms.ApplicationForm(request.POST, request.FILES)

            if form.is_valid():
                formdata = form.save(commit=False)
                if not application:
                    formdata.unique_id = student
                formdata.save()
                return redirect('applicationform', studentid=studentid)
    else: # GET request
        form = forms.ApplicationForm(instance=application)
        
    context = {
        'application': application,
        'student_id_encoded': studentid,
        'form': form,
        'links': studentid # 'links' is still redundant if 'student_id_encoded' is used
    }
    return render(request, 'applicationform.html', context)
def application_view_data(request,value):
    data = Application.objects.filter(id=value)
    return render(request, 'applicationformdata.html', {'applications': data})
def application_list_view(request):
    applications = Application.objects.all()
    return render(request, 'application_list.html', {'applications': applications})
def emailsender(request):
    applications = Application.objects.all()
    student_list = []  # Renamed 'lists' to 'student_list' for better clarity
    for app in applications:
        student_list.append({
            'id': app.studentid,
            'name': f"{app.first_name} {app.last_name}",
            'email': app.email
        })
    # Pass the student_list to the template context
    return render(request, 'sendemails.html', {'students': student_list})
def sendemails(request):
    if request.method=='POST':
        print(request.POST.get('email_recipients'))
        send_mail(
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
                from_email='vaddeadarsh150@gmail.com',
                recipient_list=request.POST.get('email_recipients').split(',')  ,
                fail_silently=False,
            )
    return JsonResponse({'data':'success'})
#https://chatgpt.com/share/684aab84-e014-800b-a05d-58436d85a6cb
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            students = StudentUser.objects.all()

            for student in students:
                status = form.cleaned_data.get(f'student_{student.id}', 'Absent')
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'status': status}
                )
            return redirect('attendance_transposed')  # Or any success page
    else:
        form = AttendanceForm()
    
    return render(request, 'markatt.html', {'form': form})
def attendance_transposed(request):
    # Define date range for June
    start_date = date(2025, 6, 1)
    end_date = date(2025, 6, 30)
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Fetch all students
    students = list(StudentUser.objects.all())

    # Fetch all attendance records in one query
    records = AttendanceRecord.objects.filter(date__range=(start_date, end_date)).select_related('student')

    # Create a lookup dictionary: {(student_id, date): status}
    record_map = {(record.student.id, record.date): record.status for record in records}

    # Prepare transposed data: each row is a date with student statuses
    transposed_data = []
    dicts=dict()
    for current_date in date_range:
        row = {'date': current_date.strftime('%d %b')}
        record_id = str(random.randint(100000, 999999))
        c=0
        for student in students:
            status = record_map.get((student.id, current_date), 'Absent')  # Default to 'Absent' if no record found
            row['record_id'] = record_id
            row[row['record_id']+str(c)] = student.username
            row['status'+str(record_id)+str(c)] = status
            c+=1
        transposed_data.append(row)

    # Render template
    print(len(transposed_data))
    
    attendance_by_student = defaultdict(dict)
    all_dates = []

    for record in transposed_data:
        datee = record['date']
        all_dates.append(datee)
        for key, value in record.items():
            if key not in ['date', 'record_id'] and not key.startswith('status'):
                student = value
                status_key = f'status{key}'
                status = record.get(status_key, 'N/A')
                attendance_by_student[student][datee] = status

    context = {
        'dates': sorted(set(all_dates), key=lambda x: int(x.split()[0])),  # sorted by day
        'attendance_by_student': dict(attendance_by_student),
    }
    return render(request, 'attend.html', context)
def adminpage(request,adminid):
    try: 
        applications = Application.objects.all()
        uniqueid=decode_base64_to_uuid(adminid)
        admin=AdminUser.objects.get(unique_id=str(uniqueid))
        uniqueid=encode_uuid_to_base64(admin.unique_id)
        return render(request,'adminpage.html',{'applications': applications,'adminlinks':f'{adminid}'})
    except:
        return HttpResponseRedirect('studentlogin')
def adminpagestudentlist(request,adminid):
    try: 
        applications = Application.objects.all()
        uniqueid=decode_base64_to_uuid(adminid)
        admin=AdminUser.objects.get(unique_id=str(uniqueid))
        uniqueid=encode_uuid_to_base64(admin.unique_id)
        return render(request,'adminpagestudentlist.html',{'applications': applications,'adminlinks':f'{adminid}'})
    except:
        return HttpResponseRedirect('studentlogin')
def adminstudentprofile(request,adminid,studentid):
    try: 
        uniqueid=decode_base64_to_uuid(adminid)
        admin=AdminUser.objects.get(unique_id=str(uniqueid))
        studentid=decode_base64_to_uuid(studentid)
        student=StudentUser.objects.get(unique_id=str(studentid))
        applications = Application.objects.filter(unique_id=student)
        return render(request,'adminstudentprofile.html',{'applications': applications,'adminlinks':f'{adminid}'})
    except:
        return HttpResponseRedirect('studentlogin')
def adminstudentdailyatendance(request,adminid):
    # 1. Authenticate and retrieve AdminUser
    admin_unique_id = decode_base64_to_uuid(adminid)
    admin = get_object_or_404(AdminUser, unique_id=str(admin_unique_id))

    # 2. Handle the date range form for filtering
    if request.method == "POST":
        form = forms.DateRangeForm(request.POST)
    else:
        # For GET requests, initialize with default initial values from the form
        form = forms.DateRangeForm() 

    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

    # If dates are not provided or invalid from form, set robust defaults
    if not start_date:
        start_date = date.today() - timedelta(days=30) # Default to 30 days ago
    if not end_date:
        end_date = date.today() # Default to today
    
    # Ensure end_date is not before start_date (form validation should primarily handle this)
    if end_date < start_date:
        end_date = start_date 

    # 3. Fetch all students
    all_students = StudentUser.objects.all()

    # 4. Fetch all relevant attendance records in one efficient query
    # Use select_related to get student details along with attendance records
    all_attendance_records = AttendanceRecord.objects.filter(
        date__range=(start_date, end_date),
        student__in=all_students # Ensure we only get records for existing students
    ).select_related('student') # Optimizes fetching related StudentUser objects

    # 5. Prepare the data for the transposed table
    # This will be the main data structure for the template
    # Format: {student_id: {date: status, 'total_days': X, 'attended_days': Y, 'percentage': Z}}
    student_attendance_map = defaultdict(lambda: {'records': {}, 'total_days': 0, 'attended_days': 0})

    # Populate the map with fetched records
    for record in all_attendance_records:
        student_id = record.student.id
        student_attendance_map[student_id]['records'][record.date] = record.status
        
        # Calculate summary for each student on the fly
        if record.status == 'Present':
            student_attendance_map[student_id]['attended_days'] += 1
        # Only count days where a status (Present/Absent) was explicitly recorded
        student_attendance_map[student_id]['total_days'] += 1 


    # Create a list of all dates in the range for table headers
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Final list to pass to template, associating student object with their attendance data
    # Ensure all students are included, even those with no records in the range
    transposed_attendance_data = []
    for student in all_students:
        student_data = student_attendance_map[student.id]
        applications=Application.objects.filter(unique_id=student).values('studentid', 'first_name', 'last_name', 'email','model_name').order_by('studentid')
        if applications.exists():

        
            # Calculate percentage
            total_days_in_period = len(date_range) # Total possible attendance days in selected range
            attended_days_calculated = 0

            # Recalculate attended and total based on the *full date range* for accuracy
            # This handles cases where a student has no records for the entire period
            current_student_daily_records = {}
            for d in date_range:
                status = student_data['records'].get(d, 'Absent') # Default to Absent if no record
                current_student_daily_records[d] = status
                if status == 'Present':
                    attended_days_calculated += 1

            # Use total_days_in_period for denominator for consistent percentage calculation
            percentage = (attended_days_calculated / total_days_in_period * 100) if total_days_in_period > 0 else 0.0

            transposed_attendance_data.append({
                'student': applications,
                'daily_records': current_student_daily_records, # date: status for all days in range
                'attended_days': attended_days_calculated,
                'total_days_in_range': total_days_in_period, # Total number of days in the selected range
                'attendance_percentage': f"{percentage:.2f}%"
            })
        else:
            pass
    
    # 6. Prepare context for the template
    context = {
        'admin': admin,
        'all_students': all_students, # Not strictly needed if using transposed_attendance_data
        'date_range': [d.strftime('%d %b') for d in date_range], # Formatted dates for table header
        'transposed_attendance_data': transposed_attendance_data[::-1], # The main data for the table body
        'form': form, # The date range form for filtering
        'start_date_value': start_date.strftime('%Y-%m-%d'), # For setting initial form input values
        'end_date_value': end_date.strftime('%Y-%m-%d'),
        'adminlinks': adminid, # Pass admin ID for navigation
    }

    return render(request, 'adminstudentdailyatendance.html', context)
def adminapplicationformslist(request, adminid):
    uniqueid = decode_base64_to_uuid(adminid)
    admin = get_object_or_404(AdminUser, unique_id=uniqueid)

    all_applications = Application.objects.select_related('unique_id').all()

    student_applications_list = []
    for app in all_applications:
        student_applications_list.append({
            'application': app
        })
    return render(request, 'adminapplicationformslist.html', {
        'applications': student_applications_list,
        'adminlinks': adminid
    })
def adminapplicationformsstudent(request,adminid,studentuniqueid):
    try:
        uniqueid=decode_base64_to_uuid(adminid)
        admin=AdminUser.objects.get(unique_id=str(uniqueid))
        studentid=decode_base64_to_uuid(studentuniqueid)
        student=StudentUser.objects.get(unique_id=str(studentid))
        applications = Application.objects.filter(unique_id=student)
        return render(request,'adminapplicationformsstudent.html',{'applications': applications,'adminlinks':f'{adminid}'})
    except:
        return HttpResponseRedirect('studentlogin')
def adminpagetakeingattendance(request, adminid):
    admin_unique_id = decode_base64_to_uuid(adminid)
    admin = get_object_or_404(AdminUser, unique_id=str(admin_unique_id))

    all_applications = Application.objects.all().order_by('studentid')
    
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST, all_applications=all_applications)
        print("Form data on POST:", request.POST) # Good for debugging
        print("Is form valid?", form.is_valid())
        print("Form errors:", form.errors) # Crucial for debugging invalid forms

        if form.is_valid():
            selected_date = form.cleaned_data['date']
            
            for application_obj in all_applications:
                # IMPORTANT: Use the unique_id of the StudentUser linked to the application
                # This should be a UUID value if StudentUser.unique_id is a UUIDField
                student_user_unique_id_value = application_obj.unique_id.unique_id 
                status_field_name = f'student_{student_user_unique_id_value}'
                
                status = form.cleaned_data.get(status_field_name, 'Absent')
                
                # student_to_record is the StudentUser object linked by application.unique_id
                student_to_record = application_obj.unique_id 
                print(f"Processing Student: {student_to_record} (Status: {status})")
                
                try:
                    AttendanceRecord.objects.update_or_create(
                        # The 'unique_id' here if it's the primary key/unique identifier of AttendanceRecord
                        # and you also have a ForeignKey 'student'
                        # If 'unique_id' is *also* a FK to StudentUser, it might be redundant.
                        # Assuming 'student' is the ForeignKey to StudentUser as discussed earlier:
                        student=student_to_record, # Pass the StudentUser object
                        date=selected_date,
                        defaults={'status': status}
                    )
                except Exception as e:
                    print(f"Error updating/creating attendance for {student_to_record}: {e}")
                    pass
            
            return redirect(f'/adminpagetakeingattendance/{adminid}')
    else: # GET request
        all_applications = Application.objects.all().order_by('studentid')
        
        initial_data = {'date': date.today()}

        # Get all StudentUser objects that have applications
        # This implicitly filters StudentUser objects that are linked by at least one Application
        all_student_users_with_applications = StudentUser.objects.filter(application__in=all_applications).distinct()
        
        existing_records = AttendanceRecord.objects.filter(
            date=date.today(),
            student__in=all_student_users_with_applications # This expects StudentUser objects
        )
        for record in existing_records:
            try:
                # Here, record.student is a StudentUser object.
                # We need its unique_id to form the initial_data key.
                # Assuming StudentUser has a 'unique_id' field (UUIDField or similar primary key)
                student_user_id_for_key = record.student.unique_id 
                
                # The key in initial_data must match the field names expected by the form
                initial_data[f'student_{student_user_id_for_key}'] = record.status
            except AttributeError as e:
                print(f"Error accessing unique_id for student record {record.student}: {e}")
                pass
            except Exception as e:
                print(f"An unexpected error occurred for record {record}: {e}")
                pass
                
        form = forms.AttendanceForm(initial=initial_data, all_applications=all_applications)
    
    return render(request, 'adminpagetakeingattendance.html', {
        'form': form,
        'all_students': all_applications, # Pass applications to the template for their data (name, batch, etc.)
        'adminlinks': f'{adminid}',
        'admin': admin,
    })
def adminemailsender(request,adminid):
    applications = Application.objects.all()
    student_list = []  # Renamed 'lists' to 'student_list' for better clarity
    for app in applications:
        student_list.append({
            'id': app.studentid,
            'name': f"{app.first_name} {app.last_name}",
            'email': app.email
        })
    return render(request, 'adminemailsender.html', {'students': student_list,'adminlinks':adminid})
def search_suggestions_api(request):
    """
    API endpoint to provide student search suggestions based on query.
    Returns a JSON list of student IDs and names for the live search box.
    """
    query = request.GET.get('q', '').strip()
    suggestions = []

    if query:
        # Query your StudentUser model (or the primary model where student names/IDs are stored)
        # Adjust 'unique_id', 'first_name', 'last_name' to your actual fields in StudentUser model
        # The error indicates that 'first_name' and 'last_name' do not exist directly on StudentUser.
        # It seems you only have 'username' and 'unique_id' as name-like fields.
        students = Application.objects.filter(
            Q(studentid__icontains=query)  # Use 'username' instead of 'first_name'/'last_name'
        ).values('unique_id_id','studentid', 'first_name','last_name')# Limit suggestions for performance

        for student in students:
            suggestions.append({
                'id': student['studentid'], # This will be used for the direct link
                'name': student['first_name']+" "+student['last_name'] # Use 'username' as the display name
            })  

    return JsonResponse(suggestions, safe=False)
def application_detail(request,adminid,student_id):
    """
    Displays the details of a single application based on its unique student ID.
    """
    try:
        uniqueid=decode_base64_to_uuid(adminid)
        admin=AdminUser.objects.get(unique_id=str(uniqueid))
        applications = Application.objects.filter(studentid=student_id)
        context = {
        'applications': applications,
        'adminlinks':adminid
        }
        return render(request, 'adminstudentprofile.html', context)
    except Application.DoesNotExist:
        # If the student ID doesn't exist, return a 404 Not Found response
        pass  
def studentemailconform(request,studentid):
    query = request.GET.get('q', '').strip()
    uniqueid=decode_base64_to_uuid(studentid)
    students=[]
    if query:
        student = StudentUser.objects.filter(unique_id=uniqueid).values('email')
        for i in student:
            students.append({'email':i['email']})
    print(students)
    return JsonResponse(students,safe=False)
def studenthome(request, studentuniqueid):
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)

    try:
        
        target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))

        applications = Application.objects.filter(unique_id=target_student_user)
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)

        
        if applications.exists():
            print("\nApplications found for this student:")
            for app in applications:
                print(f"- Application ID: {app.pk}, Student Ref ID: {app.unique_id.id}, Name: {app.first_name} {app.last_name}")
        else:
           
            return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

                    

    except StudentUser.DoesNotExist:
        print(f"Error: No StudentUser found with unique_id '{str(decoded_uuid_obj)}'.")
        applications = Application.objects.none() 
    except Exception as e:
        print(f"An unexpected error occurred in studentprofile: {e}")
        applications = Application.objects.none() # Return an empty queryset
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)

    return render(request, 'studenthome.html', {'applications': applications,'links':uniqueid})
def studentprofile(request,studentuniqueid):
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)

    try:
        
        target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))

        applications = Application.objects.filter(unique_id=target_student_user)
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)


        
        if applications.exists():
            print("\nApplications found for this student:")
            for app in applications:
                print(f"- Application ID: {app.pk}, Student Ref ID: {app.unique_id.id}, Name: {app.first_name} {app.last_name}")
        else:
            return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

    except StudentUser.DoesNotExist:
        print(f"Error: No StudentUser found with unique_id '{str(decoded_uuid_obj)}'.")
        applications = Application.objects.none() 
    except Exception as e:
        print(f"An unexpected error occurred in studentprofile: {e}")
        applications = Application.objects.none() # Return an empty queryset
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)

    return render(request, 'studentprofile.html', {'applications': applications,'links':uniqueid})
def studentapplications(request,studentuniqueid):
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)

    try:
        
        target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))

        applications = Application.objects.filter(unique_id=target_student_user)
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)


        
        if applications.exists():
            print("\nApplications found for this student:")
            for app in applications:
                print(f"- Application ID: {app.pk}, Student Ref ID: {app.unique_id.id}, Name: {app.first_name} {app.last_name}")
        else:
            return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

    except StudentUser.DoesNotExist:
        print(f"Error: No StudentUser found with unique_id '{str(decoded_uuid_obj)}'.")
        applications = Application.objects.none() 
    except Exception as e:
        print(f"An unexpected error occurred in studentprofile: {e}")
        applications = Application.objects.none() # Return an empty queryset
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)
    

    return render(request, 'studentapplicationdetails.html', {'applications': applications,'links':uniqueid,})
def studentapplicationform(request,studentuniqueid):
    try:
        decoded_uuid = decode_base64_to_uuid(studentuniqueid)
    except ValueError:
        pass
        
    student = get_object_or_404(StudentUser, unique_id=str(decoded_uuid))
    application = Application.objects.filter(unique_id=student).first()

    if request.method == 'POST':
        submitted_fields = [k for k in request.POST.keys() if k != 'csrfmiddlewaretoken']
        
        if len(submitted_fields) == 1:
            field_name_to_update = submitted_fields[0]
            
            # Create a temporary form instance to get its default fields for validation
            # This is safer than _meta.fields directly if exclude is used.
            temp_form_for_field_check = forms.ApplicationForm() 

            if field_name_to_update not in temp_form_for_field_check.fields.keys():
                return JsonResponse({'success': False, 'errors': {field_name_to_update: ['Invalid or unauthorized field for update.']}}, status=400)

            if application:
                form = forms.ApplicationForm(request.POST, request.FILES, instance=application, fields=[field_name_to_update])
            else:
                return JsonResponse({'success': False, 'errors': 'No application to update.'}, status=400)
            
            if form.is_valid():
                form.save() 
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        else: # Full form submission
            if application:
                form = forms.ApplicationForm(request.POST, request.FILES, instance=application)
            else:
                form = forms.ApplicationForm(request.POST, request.FILES)

            if form.is_valid():
                formdata = form.save(commit=False)
                if not application:
                    formdata.unique_id = student
                formdata.save()
                return redirect('applicationform', studentid=studentuniqueid)
    else: # GET request
        form = forms.ApplicationForm(instance=application)
        
    context = {
        'applications': application,
        'student_id_encoded': studentuniqueid,
        'form': form,
        'links': studentuniqueid # 'links' is still redundant if 'student_id_encoded' is used

    }
    return render(request, 'studentapplicationform.html',context)
def studentattendances(request,studentuniqueid):
    if request.method=="POST":
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass # Handle invalid date format if necessary
            
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass # Handle invalid date format if necessary
        decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)
        try:
            target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))
            applications = AttendanceRecord.objects.filter(unique_id=target_student_user)
            uniqueid=encode_uuid_to_base64(target_student_user.unique_id)
            if applications.exists():
                print("\nApplications found for this student:")
                for app in applications:
                    print(f"- Application ID: {app.pk}, Student Ref ID: {app.unique_id.id}, Name: {app.first_name} {app.last_name}")
            else:
                return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

        except StudentUser.DoesNotExist:
            print(f"Error: No StudentUser found with unique_id '{str(decoded_uuid_obj)}'.")
            applications = Application.objects.none() 
        except Exception as e:
            print(f"An unexpected error occurred in studentprofile: {e}")
            applications = Application.objects.none() # Return an empty queryset
            uniqueid=encode_uuid_to_base64(target_student_user.unique_id)
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        # Fetch all students
        students = list(StudentUser.objects.all())
        # Fetch all attendance records in one query
        records = AttendanceRecord.objects.filter(date__range=(start_date, end_date)).select_related('student')
        # Create a lookup dictionary: {(student_id, date): status}
        record_map = {(record.student.id, record.date): record.status for record in records}
        # Prepare transposed data: each row is a date with student statuses
        transposed_data = []
        for current_date in date_range:
            row = {'date': current_date.strftime('%d %b')}
            record_id = str(random.randint(100000, 999999))
            c=0
            for student in students:
                status = record_map.get((student.id, current_date), 'Absent')  # Default to 'Absent' if no record found
                row['record_id'] = record_id
                row[row['record_id']+str(c)] = student.username
                row['status'+str(record_id)+str(c)] = status
                c+=1
            transposed_data.append(row)
        # Render template
        print(transposed_data)
        attendance_by_student = defaultdict(dict)
        all_dates = []
        for record in transposed_data:
            datee = record['date']
            all_dates.append(datee)
            for key, value in record.items():
                if key not in ['date', 'record_id'] and not key.startswith('status'):
                    student = value
                    status_key = f'status{key}'
                    status = record.get(status_key, 'N/A')
                    attendance_by_student[student][datee] = status
        context = {
            'dates': all_dates,  # sorted by day
            'attendance_by_student': dict(attendance_by_student),
            'links':uniqueid,
            'applications':applications,
        }
        return render(request, 'studentattendancetable.html',context )
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)
    target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))
    a=AttendanceRecord.objects.filter(unique_id=target_student_user)
    print(a)
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)
    try:
        target_student_user = StudentUser.objects.get(unique_id=str(decoded_uuid_obj))
        applications = AttendanceRecord.objects.filter(unique_id=target_student_user)
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)
        print(applications)
        if applications.exists():
            print("\nApplications found for this student:")
            for app in applications:
                print(f"- Application ID: {app.pk}, Student Ref ID: {app.unique_id.id}, Name: {app.first_name} {app.last_name}")
        else:
            return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

    except StudentUser.DoesNotExist:
        print(f"Error: No StudentUser found with unique_id '{str(decoded_uuid_obj)}'.")
        applications = Application.objects.none() 
    except Exception as e:
        print(f"An unexpected error occurred in studentprofile: {e}")
        applications = Application.objects.none() # Return an empty queryset
        uniqueid=encode_uuid_to_base64(target_student_user.unique_id)
    start_date = date(2025, 6, 1)
    end_date = date(2025, 6, 30)
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    # Fetch all students
    datass=StudentUser.objects.get(unique_id=str(decoded_uuid_obj))
    students = list(StudentUser.objects.filter(unique_id=str(decoded_uuid_obj)))
    # Fetch all attendance records in one query
    records = AttendanceRecord.objects.filter(date__range=(start_date, end_date),unique_id=datass).select_related('student')
    print(records)
    # Create a lookup dictionary: {(student_id, date): status}
    record_map = {(record.student.id, record.date): record.status for record in records}
    # Prepare transposed data: each row is a date with student statuses
    transposed_data = []
    dicts=dict()
    for current_date in date_range:
        row = {'date': current_date.strftime('%d %b')}
        record_id = str(random.randint(100000, 999999))
        c=0
        for student in students:
            status = record_map.get((student.id, current_date), 'Absent')  # Default to 'Absent' if no record found
            row['record_id'] = record_id
            row[row['record_id']+str(c)] = student.username
            row['status'+str(record_id)+str(c)] = status
            c+=1
        transposed_data.append(row)
    # Render template
    attendance_by_student = defaultdict(dict)
    all_dates = []
    for record in transposed_data:
        datee = record['date']
        all_dates.append(datee)
        for key, value in record.items():
            if key not in ['date', 'record_id'] and not key.startswith('status'):
                student = value
                status_key = f'status{key}'
                status = record.get(status_key, 'N/A')
                attendance_by_student[student][datee] = status
    context = {
        'dates': sorted(set(all_dates), key=lambda x: int(x.split()[0])),  # sorted by day
        'attendance_by_student': dict(attendance_by_student),
        'links':uniqueid,
        'applications':applications,
    }
    

    return render(request, 'studentattendancetable.html',context )
def studentattendance(request, studentuniqueid):
    # Get the target student user
    decoded_uuid_obj = decode_base64_to_uuid(studentuniqueid)
    target_student_user = get_object_or_404(StudentUser, unique_id=str(decoded_uuid_obj))
    target_student_userid=Application.objects.filter(unique_id=target_student_user)
    if not target_student_userid.exists():
        return HttpResponseRedirect(f"/studentapplicationform/{studentuniqueid}")

    
    # Handle the date range form
    if request.method == "POST":
        form = forms.DateRangeForm(request.POST)
    else:
        form =forms.DateRangeForm() # For GET requests, initialize with default initial values

    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

    # If dates are not provided via form (e.g., initial GET or invalid form), set robust defaults
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Ensure end_date is not before start_date, or Django form validation already handles it.
    # If the form itself handles this with a ValidationError, this check may be redundant after form.is_valid()
    # but acts as a fallback for initial defaults.
    if end_date < start_date:
        end_date = start_date 

    # Fetch attendance records for the TARGET student within the selected date range
    # Filter by the correct ForeignKey 'student'
    attendance_records_queryset = AttendanceRecord.objects.filter(
        student=target_student_user, 
        date__range=(start_date, end_date)
    ).order_by('date') # Order by date for chronological display

    # Prepare data for the template: a list of dictionaries with date and status
    attendance_data_for_template = []
    
    # Create a map for quick status lookup for the fetched records
    status_map = {record.date: record.status for record in attendance_records_queryset}

    # Generate the full date range to ensure all days are displayed, even if no record exists
    delta = end_date - start_date
    for i in range(delta.days + 1):
        current_date = start_date + timedelta(days=i)
        # Get status from map, default to 'Absent' if no record for that day
        status = status_map.get(current_date, 'Absent') 
        
        attendance_data_for_template.append({
            'date': current_date, # Raw date object
            'formatted_date': current_date.strftime('%d %b %Y'), # Formatted for display
            'status': status
        })

    # Prepare context for the template
    context = {
        'applications': target_student_userid, # The specific student object
        'attendance_by_student': attendance_data_for_template, # The prepared attendance list
        'links': studentuniqueid, # The encoded unique ID for navigation
        'form': form, # The date range form for filtering
        'start_date': start_date.strftime('%Y-%m-%d'), # Pass selected dates back to template for input values
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
   

    return render(request, 'studentattendancetable.html', context)
def applicatinsform(request,studentid):
    decode=decode_base64_to_uuid(studentid)
    student=StudentUser.objects.get(unique_id=str(decode))
    if request.method == 'POST':
            form = forms.ApplicationForm(request.POST, request.FILES)
            applications=Application.objects.filter(unique_id=student).first()
            if form.is_valid():
                if applications: 
                    form = forms.ApplicationForm(request.POST, request.FILES,instance=applications)
                    formdata=form.save()
                else:
                    formdata=form.save(commit=False)
                    formdata.unique_id=student
                    formdata.save()
                return redirect(f'/studenthome/{studentid}')
    else:
        form = forms.ApplicationForm()
    return render(request,'applicationform.html',{'form':form,'links':studentid})
DailyEntryFormSet = inlineformset_factory(
    WeeklyWorkReport,
    DailyEntry,
    form=forms.DailyEntryForm,
    extra=6,  # 6 days: Monday to Saturday
    can_delete=False, # Set to True if you want to allow deleting daily entries
    # Fields must match those in DailyEntryForm.Meta.fields
    fields=('day_of_week', 'entry_date', 'task_accomplished') 
)
def studentweeklyreport(request, studentid):
    """
    View to create a new weekly work report or edit an existing one for a specific student.
    
    Args:
        request: HttpRequest object.
        studentid: A base64 encoded UUID string representing the StudentUser.
        pk: Optional primary key of an existing WeeklyWorkReport to edit.
    """
    report_instance = None # Initialize report_instance; will be set if editing an existing report
    extra_value=6
    
    # Decode the studentid from the URL to find the associated StudentUser
    decoded_student_uuid = decode_base64_to_uuid(studentid)
    
    if not decoded_student_uuid:
        # If decoding fails, return an error page or redirect.
        # In a production environment, consider a more robust error handling mechanism.
        return render(request, 'error_page.html', {'message': 'Invalid student ID provided in URL.'})

    # Retrieve the StudentUser object based on the decoded UUID.
    # Assuming 'unique_id' in your StudentUser model stores the UUID as a CharField.
    student_user = get_object_or_404(StudentUser, unique_id=str(decoded_student_uuid))

    # --- Fetch associated Application data ---
    application = None
    try:
        # Assuming Application model has a ForeignKey or OneToOneField to StudentUser
        # named 'unique_id' that links it. Adjust this query as per your specific model relationship.
        application = Application.objects.get(unique_id=student_user) 
    except Application.DoesNotExist:
        print(f"No application found for student {student_user.username} ({student_user.unique_id}).")
    except Application.MultipleObjectsReturned:
        print(f"Multiple applications found for student {student_user.username}. Picking the first one.")
        application = Application.objects.filter(unique_id=student_user).first()
    # --- End Fetch associated Application data ---
    
    
    if request.method == 'POST':
        # If the request method is POST, process the submitted form data
        # Initialize the main report form with POST data and the instance (if editing)
        report_form = forms.WeeklyWorkReportForm(request.POST, instance=report_instance)
        # Initialize the formset with POST data and the instance (if editing), using a prefix
        formset = DailyEntryFormSet(request.POST, instance=report_instance, prefix='daily_entries')

        # For debugging purposes: print submitted data and form validation status
        print("POST Data:", request.POST)
        print(f"Report Form Valid: {report_form.is_valid()}, Formset Valid: {formset.is_valid()}")

        if report_form.is_valid() and formset.is_valid():
            # If both forms are valid, save the main WeeklyWorkReport first
            new_report = report_form.save(commit=False) # commit=False prevents immediate save
            
            # If it's a new report (no primary key yet), set the unique_id (foreign key to StudentUser)
            if not new_report.pk: 
                new_report.unique_id = student_user # Link the report to the identified student
            new_report.save() # Save the new or updated report to the database

            # Associate the formset instances with the newly saved or retrieved report
            formset.instance = new_report 
            formset.save() # Save all daily entries related to this report

            # Redirect to the detail view of the saved report, passing both studentid and the new report's pk
            return redirect(f'/studentweeklyreports/{studentid}') 

    else:
        # If the request method is GET, display the empty or pre-filled forms
        initial_report_data = {}
            # Preload student_name and student_id from the student_user instance
        initial_report_data['student_name'] = application.first_name+" "+application.last_name # Assuming username is the student's name
            # IMPORTANT: Ensure 'student_id' below matches the actual field name for student ID on your StudentUser model
            # For example, if your StudentUser has a field `student_id_number`, use `student_user.student_id_number`
        initial_report_data['student_id'] =application.studentid 

        report_form = forms.WeeklyWorkReportForm(instance=report_instance, initial=initial_report_data)

        # Handle initial data for the daily entries formset
        CurrentDailyEntryFormSet = inlineformset_factory(
            WeeklyWorkReport, 
            DailyEntry,       
            form=forms.DailyEntryForm, 
            extra=6, # Set extra to 0 for existing, 6 for new
            can_delete=False, 
            fields=('day_of_week', 'entry_date', 'task_accomplished') 
        )

        # Handle initial data for the daily entries formset
        if report_instance:
            # If editing, the formset will automatically populate with existing DailyEntry objects
            # No initial data is needed here as instance handles population.
            formset = CurrentDailyEntryFormSet(instance=report_instance, prefix='daily_entries')
        else:
            # If creating a new report, provide initial data for each day of the week
            initial_daily_entries = [
                {'day_of_week': 'Monday'},
                {'day_of_week': 'Tuesday'},
                {'day_of_week': 'Wednesday'},
                {'day_of_week': 'Thursday'},
                {'day_of_week': 'Friday'},
                {'day_of_week': 'Saturday'},
            ]
            # When creating new reports, use initial data for day_of_week
            formset = CurrentDailyEntryFormSet(instance=None, initial=initial_daily_entries, prefix='daily_entries')

    # Render the HTML template with the initialized forms
    return render(request, 'studentweekly_report_form.html', {
        'report_form': report_form,
        'daily_entry_forms': formset, # The formset for daily entries
        'student_user': student_user, # Pass the student_user object to the template (optional, but useful for context)
        'links':studentid,
        'applications':application

    })
def studentaddweeklyreport(request, studentid, fromto):
    report_instance = None
    extra_value = 6

    decoded_student_uuid = decode_base64_to_uuid(studentid)

    if not decoded_student_uuid:
        return render(request, 'error_page.html', {'message': 'Invalid student ID provided in URL.'})

    student_user = get_object_or_404(StudentUser, unique_id=str(decoded_student_uuid))

    report_date_from = None
    report_date_to = None
    try:
        parts = fromto.split('-')
        # Expecting YYYY-Mon-DD-YYYY-Mon-DD, so 6 parts
        if len(parts) == 6:
            start_year_str, start_month_abbr, start_day_str = parts[0], parts[1], parts[2]
            end_year_str, end_month_abbr, end_day_str = parts[3], parts[4], parts[5]

            # Map month abbreviations to numbers
            month_name_to_num = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            
            start_month_num = month_name_to_num.get(start_month_abbr)
            end_month_num = month_name_to_num.get(end_month_abbr)

            if start_month_num is None or end_month_num is None:
                raise ValueError("Invalid month abbreviation in fromto parameter.")

            report_date_from = datetime(int(start_year_str), start_month_num, int(start_day_str)).date()
            report_date_to = datetime(int(end_year_str), end_month_num, int(end_day_str)).date()

        else:
            raise ValueError("Incorrect date format in 'fromto' parameter.")
    except (ValueError, IndexError) as e:
        print(f"Error parsing fromto: {e}")
        return render(request, 'error_page.html', {'message': f'Invalid date range format in URL. Expected YYYY-Mon-DD-YYYY-Mon-DD. Error: {e}'})

    application = None
    try:
        application = Application.objects.get(unique_id=student_user)
    except Application.DoesNotExist:
        print(f"No application found for student {student_user.username} ({student_user.unique_id}).")
    except Application.MultipleObjectsReturned:
        print(f"Multiple applications found for student {student_user.username}. Picking the first one.")
        application = Application.objects.filter(unique_id=student_user).first()

    try:
        report_instance = WeeklyWorkReport.objects.get(
            unique_id=student_user,
            report_date_from=report_date_from,
            report_date_to=report_date_to
        )
        extra_value = 0
        print(f"Found existing report for student {student_user.username} from {report_date_from} to {report_date_to}.")
    except WeeklyWorkReport.DoesNotExist:
        print(f"No existing report found for student {student_user.username} from {report_date_from} to {report_date_to}. Creating new.")
    except WeeklyWorkReport.MultipleObjectsReturned:
        print(f"Multiple reports found for student {student_user.username} for the same period. Picking the first one.")
        report_instance = WeeklyWorkReport.objects.filter(
            unique_id=student_user,
            report_date_from=report_date_from,
            report_date_to=report_date_to
        ).first()
        extra_value = 0

    if request.method == 'POST':
        report_form = forms.WeeklyWorkReportForm(request.POST, instance=report_instance)
        formset = DailyEntryFormSet(request.POST, instance=report_instance, prefix='daily_entries')

        print("POST Data:", request.POST)
        print(f"Report Form Valid: {report_form.is_valid()}, Formset Valid: {formset.is_valid()}")
        print("Report Form Errors:", report_form.errors)
        print("Formset Errors:", formset.errors)
        for f in formset:
            if f.errors:
                print(f"Daily Entry Form Errors for {f.prefix}:", f.errors)

        if report_form.is_valid() and formset.is_valid():
            new_report = report_form.save(commit=False)

            if not new_report.pk:
                new_report.unique_id = student_user
                new_report.report_date_from = report_date_from
                new_report.report_date_to = report_date_to
            new_report.save()

            formset.instance = new_report
            formset.save()

            return redirect(f'/studentweeklyreports/{studentid}')

    else:
        initial_report_data = {}
        if application:
            initial_report_data['student_name'] = f"{application.first_name} {application.last_name}"
            initial_report_data['student_id'] = application.studentid
        
        initial_report_data['report_date_from'] = report_date_from
        initial_report_data['report_date_to'] = report_date_to

        report_form = forms.WeeklyWorkReportForm(instance=report_instance, initial=initial_report_data)

        CurrentDailyEntryFormSet = inlineformset_factory(
            WeeklyWorkReport,
            DailyEntry,
            form=forms.DailyEntryForm,
            extra=extra_value,
            can_delete=False,
            fields=('day_of_week', 'entry_date', 'task_accomplished')
        )

        if report_instance:
            formset = CurrentDailyEntryFormSet(instance=report_instance, prefix='daily_entries')
        else:
            initial_daily_entries = []
            # Calculate actual dates for the days of the week based on report_date_from
            # Assuming Mon-Sat week (6 days)
            for i in range(6):
                current_day_date = report_date_from + timedelta(days=i)
                day_name = calendar.day_name[current_day_date.weekday()] # Get full day name (e.g., 'Monday')
                initial_daily_entries.append({
                    'day_of_week': day_name,
                    'entry_date': current_day_date
                })
            formset = CurrentDailyEntryFormSet(instance=None, initial=initial_daily_entries, prefix='daily_entries')

    return render(request, 'studentweekly_report_form.html', {
        'report_form': report_form,
        'daily_entry_forms': formset,
        'student_user': student_user,
        'from_date': report_date_from,
        'to_date': report_date_to,
        'links':studentid,
        'applications':application
    })
def studentweeklyreports(request, studentid):
    decoded_student_uuid = decode_base64_to_uuid(studentid)

    if not decoded_student_uuid:
        return render(request, 'error_page.html', {'message': 'Invalid student ID provided in URL.'})

    student_user = get_object_or_404(StudentUser, unique_id=str(decoded_student_uuid))

    application = None
    try:
        application = Application.objects.get(unique_id=student_user)
    except Application.DoesNotExist:
        print(f"No application found for student {student_user.username} ({student_user.unique_id}).")
    except Application.MultipleObjectsReturned:
        print(f"Multiple applications found for student {student_user.username}. Picking the first one.")
        application = Application.objects.filter(unique_id=student_user).first()

    weekly_reports = WeeklyWorkReport.objects.filter(unique_id=student_user).order_by('-report_date_from')

    return render(request, 'studentreport_details.html', {
        'student_user': student_user,
        'application': application,
        'weekly_reports': weekly_reports,
        'links':studentid,
        'applications':application

    })


def extendshtml2(request):
    return render(request,'extend2.html')

def extendshtml3(request):
    return render(request,'extend3.html')