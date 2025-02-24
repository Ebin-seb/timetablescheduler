
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.cache import add_never_cache_headers
from django.middleware.csrf import rotate_token
from django.contrib.auth.hashers import make_password

from timetable_scheduler_app.models import *
from timetable_scheduler_app.form import *
from .models import *



class HomePage(View):
    def get(self, request):
        return render(request, "home.html")
    
class Logout(View):
    def get(self, request):
        logout(request)
        rotate_token(request)
        response = redirect('login')  # Redirect to login page after logout
        add_never_cache_headers(response)  # Prevent caching issues
        return response      
    
class LoginPage(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            obj=LoginTable.objects.get(username=username,password=password)
            request.session['user_id']=obj.id
            if obj.type=='admin':
                 return HttpResponse('''<script>alert('Login successfull');window.location='/adminprofile'</script>''')
            elif obj.type=='student':
                 return HttpResponse('''<script>alert('Login successfull');window.location='/studentprofile'</script>''')
            elif obj.type=='staff':
                 return HttpResponse('''<script>alert('Login successfull');window.location='/staffprofile'</script>''')
            else:
                 return HttpResponse('''<script>alert('user type  not recognized');window.location.href='/login';</script>''')
    
        except LoginTable.DoesNotExist:
            
    
            return HttpResponse('''<script>alert('invalid username and password');window.location.href='/login';</script>''')
        


class Add(View):
    def get(self,request):
        return render(request,"admin_add.html")
    
    
class RegPage(View):
    def get(self,request):
        return render(request,"staff_reg.html")
    
class VerifyStaff(View):
    def get(self,request):
        obj=StaffTable.objects.filter(login_id__type="pending")  
        return render(request,"admin_verifystaff.html",{'obj':obj})
    
class Accept_Staff(View):
    def get(self,request,staff_id):
        obj=LoginTable.objects.get(id=staff_id)
        obj.type="staff"
        obj.save()
        return HttpResponse('''<script>alert('verified');window.location.href='/verifystaff';</script>''')

class Reject_Staff(View):
    def get(self,request,staff_id):
        obj=LoginTable.objects.get(id=staff_id)
        obj.type="rejected"
        obj.save()
        return HttpResponse('''<script>alert('Rejected');window.location.href='/verifystaff';</script>''')


    
class ClassView(View):
    def get(self,request):
        return render(request,"admin_classview.html")
    
class ConflictView(View):
    def get(self,request):
        obj=ConflictTable.objects.all()
        return render(request,"admin_conflictview.html",{'obj':obj})
    
class ViewAlloc(View):
    def get(self, request):
        print("%%%%%%%%%%%%%%", request.session['user_id'])

        # Fetch subjects assigned to the logged-in staff
        obj = SubjectTable.objects.filter(staff__login_id=request.session['user_id']).prefetch_related('class1', 'class1__course_id')

        return render(request, "staff_viewalloc.html", {'obj': obj})

class StaffSubAdd(View):
    def  get(self,request):
        # form=StaffSubForm()
        return render(request,"staff_addsub.html")
    def post(self, request):
        form = StaffSubForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False) 
            user=StaffTable.objects.get(login__id=request.session.get('user_id') )
            subject.staff = user
            subject.save()
            return HttpResponse('''<script>alert('new subject added');window.location.href='/viewalloc';</script>''')

class StaffSubEdit(View):
    def get(self, request,sub_id):
        s =SubjectTable.objects.get(id=sub_id)
        return render(request, "staff_editsub.html",{'s':s })
    def post(self,request,sub_id):
        obj = SubjectTable.objects.get(id=sub_id)
        form=StaffSubForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('subject updated');window.location.href='/viewalloc';</script>''')
    
class StaffConflict(View):
    def  get(self,request):
        obj=ConflictTable.objects.filter(staff_id__login_id=request.session['user_id'])
        return render(request,"staff_conflict.html" ,{'obj':obj})
    def post(self,request):
        form=ConflictForm(request.POST)
        if form.is_valid():
            conflict = form.save(commit=False)
            user=StaffTable.objects.get(login_id=request.session.get('user_id') )   
            conflict.staff_id = user
            conflict.save()
            return HttpResponse('''<script>alert('submitted');window.location.href='/staffconflict';</script>''')


class DeleteConflict(View):
    def get(self,request,conflict_id):
        d=ConflictTable.objects.get(id=conflict_id)
        d.delete()
        return redirect('staffconflict')
    
class AdminDeleteConflict(View):
    def get(self,request,conflict_id):
        d=ConflictTable.objects.get(id=conflict_id)
        d.delete()
        return redirect('conflictview')
        
class AdminDash(View):
    def get(self, request):
        return render(request,"adminbase.html")
         
     
     
     
class AddCollege(View):
    def get(self, request):
        return render(request, "college/add_college.html")
    def post(self,request):
        form=CollegeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_college')
        

class ViewCollege(View):
    def get(self,request):
        obj=CollegeTable.objects.all()
        return render(request,"college/view_college.html",{'val':obj})
    
class DeleteCollege(View):
    def get(self, request,id):
        c = CollegeTable.objects.get(id=id)
        c.delete()
        return redirect('view_college')
    
  
class EditCollege(View):
    def get(self, request, id):
        c = CollegeTable.objects.get(id=id)
        return render(request, "college/edit_college.html",{'c':c})
    def post(self,request, id):
        obj = CollegeTable.objects.get(id=id)
        form=CollegeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('view_college')
        
class AddDep(View):
    def get(self, request):
        return render(request, "college/add_dep.html")
    def post(self,request):
        form=DepForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_dep')
        
class ViewDep(View):
    def get(self,request):
        obj=DepartmentTable.objects.all()
        return render(request,"college/view_dep.html",{'val':obj})


class DeleteDep(View):
    def get(self, request,dep_id):
        d = DepartmentTable.objects.get(id=dep_id)
        d.delete()
        return redirect('view_dep')
    
class EditDep (View):
    def get(self, request,dep_id):
        c = DepartmentTable.objects.get(id=dep_id)
        return render(request, "college/edit_dep.html",{'c':c})
    def post(self,request,dep_id):
        obj = DepartmentTable.objects.get(id=dep_id)
        form=DepForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('view_dep')

class AddSub(View):
     def  get(self,request):
        c = StaffTable.objects.all()
        return render(request,"college/add_subject.html",{'v':c})
     def post(self,request):
        form=SubForm(request.POST)
        # print(request.POST['staff_id'])
        if form.is_valid():
            form.save()
            return redirect('addsubject')
        
class ViewSub(View):
    def get(self,request):
        obj=SubjectTable.objects.all()

        return render(request,"college/view_subject.html",{'val':obj})

class StudSub(View):
    def get(self, request):
        userid = request.session.get('user_id')

        if not userid:
            return redirect('login')

        try:
            # Get the logged-in student
            student = StudentTable.objects.get(login_id__id=userid)
        except StudentTable.DoesNotExist:
            return redirect('login')  

        # Get the student's course
        student_course = student.course_id  

        # Get all semesters related to the student's course
        semesters = SemesterTable.objects.filter(course_id=student_course).prefetch_related('subjects')

        # Get the selected semester (if any)
        semester_id = request.GET.get('semester_id')

        if semester_id:
            # If a semester is selected, filter subjects for that semester only
            selected_semester = semesters.filter(id=semester_id).first()
            subjects = selected_semester.subjects.all() if selected_semester else []
        else:
            # If no semester is selected, get all subjects from all semesters of the course
            subjects = SubjectTable.objects.filter(semesters__in=semesters).distinct().select_related('staff')

        return render(request, "student_viewsub.html", {
            'semesters': semesters,
            'subjects': subjects,
            'student_course': student_course,
            'selected_semester': semester_id
        })
    
class DeleteSub(View):
    def get(self, request,sub_id):
        d = SubjectTable.objects.get(id=sub_id)
        d.delete()
        return redirect('viewsubject')

class EditSub (View):
    def get(self, request,sub_id):
        c =SubjectTable.objects.get(id=sub_id)
        staff = StaffTable.objects.all()
        return render(request, "college/edit_subject.html",{'c':c , 'staff':staff})
    def post(self,request,sub_id):
        obj = SubjectTable.objects.get(id=sub_id)
        form=SubForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('viewsubject')
     
class AddCourse(View):
     def  get(self,request):
        c = DepartmentTable.objects.all()
        return render(request,"college/add_course.html",{'v':c})
     def post(self,request):
        form=CourseForm(request.POST)
        print(request.POST['dep_id'])
        if form.is_valid():
            form.save()
            return redirect('viewcourse')
        
class ViewCourse(View):
    def get(self,request):
        obj=CourseTable.objects.all()
        return render(request,"college/view_course.html",{'val':obj})

class DeleteCourse(View):
    def get(self, request,course_id):
        d = CourseTable.objects.get(id=course_id)
        d.delete()
        return redirect('viewcourse')
    
class EditCourse (View):
    def get(self, request,course_id):
        c =CourseTable.objects.get(id=course_id)
        dep = DepartmentTable.objects.all()
        return render(request, "college/edit_course.html",{'c':c , 'dep':dep})
    def post(self,request,course_id):
        obj = CourseTable.objects.get(id=course_id)
        form=CourseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('viewcourse')


class AddSem(View):
    def  get(self,request):
        c = CourseTable.objects.all()
        d = SubjectTable.objects.all()
        return render(request,"college/add_sem.html",{'v':c,'k':d})
    def post(self, request):
        form = Semform(request.POST)

        if form.is_valid():
            semester = form.save(commit=False)
             # Handling the 'is_odd' field manually from the radio buttons
            is_odd = request.POST.get('is_odd') == 'True'  # Convert 'True'/'False' to boolean
            semester.is_odd = is_odd  # Set the 'is_odd' field based on the selected radio button
            semester.save()  # Save the semester instance
            form.save_m2m()

            return redirect('viewsem') 


class ViewSem(View):
    def get(self,request):
        obj=SemesterTable.objects.prefetch_related('subjects').all()
        return render(request,"college/view_sem.html",{'val':obj})
    
class EditSem (View):
    def get(self, request,sem_id):
        c =SemesterTable.objects.get(id=sem_id)
        sub = SubjectTable.objects.all()
        selected_sub=c.subjects.all()
        co=CourseTable.objects.all()
        return render(request, "college/edit_sem.html",{'c':c , 'sub':sub ,'co':co , 'selected_sub':selected_sub})
    def post(self,request,sem_id):
        c = SemesterTable.objects.get(id=sem_id)
        c.semester_name=request.POST.get('semester_name')
        c.save()
        selected_subjects = request.POST.getlist('subjects')
        c.subjects.set(selected_subjects)
        return redirect('viewsem')
    
class Profile(View):
    def get(self, request):
        # Assume the username is stored in the session after login
        userid = request.session.get('user_id')
        print(userid)
        
        if userid:
            # Query the LoginTable to fetch the user's details
            try:
                user = CollegeTable.objects.get(login__id=userid)
                print(user)
            except LoginTable.DoesNotExist:
                return redirect('login')  # Redirect to login if user not found
            
            # Pass the username to the template
            return render(request, "adminbase.html", {"username": user})
        
        return redirect('login') 
    
class StaffEditProfile(View):
    def get(self,request,prof_id):
        obj=StaffTable.objects.get(id=prof_id)
        dep=DepartmentTable.objects.all()
        return render(request,"staff_editprofile.html",{'obj':obj,'dep':dep})
    def post(self, request, prof_id):
        obj = StaffTable.objects.get(id=prof_id)
        dep = DepartmentTable.objects.all()
        obj.name = request.POST.get('name')
        obj.email = request.POST.get('email')
        obj.qualification = request.POST.get('qualification')
        department_id = request.POST.get('department_id')
        new_password = request.POST.get('password')
        if new_password:  # Only update if a new password is provided
            obj.login.password = new_password
            obj.login.save() 
        usrname=request.POST.get('username')
        if usrname:
            obj.login.username=usrname
            obj.login.save()
        try:
            department = DepartmentTable.objects.get(id=department_id)
            obj.department_id = department
        except DepartmentTable.DoesNotExist:
            return render(request, "staff_editprofile.html", {
                'obj': obj,
                'dep': dep,
                'error': 'Invalid department selected'
            })
        obj.save()
        return render(request, "staff_editprofile.html", {
            'obj': obj,
            'dep': dep,
            'success': 'Profile updated successfully!'
        })

class StaffDeleteSub(View):
    def get(self, request,sub_id):
        d = SubjectTable.objects.get(id=sub_id)
        d.delete()
        return redirect('viewalloc')
    
class StudentEditProfile(View):
    def get(self,request,prof_id):
        obj=StudentTable.objects.get(id=prof_id)
        c=CourseTable.objects.all()
        return render(request,"student_editprofile.html",{'obj':obj,'c':c})
    def post(self, request, prof_id):
        obj = StudentTable.objects.get(id=prof_id)
        c  = CourseTable.objects.all()
        obj.name = request.POST.get('name')
        obj.email = request.POST.get('email')
        course_id = request.POST.get('course_id')
        new_password = request.POST.get('password')
        if new_password:  # Only update if a new password is provided
            obj.login_id.password = new_password
            obj.login_id.save() 
        usrname=request.POST.get('username')
        if usrname:
            obj.login_id.username=usrname
            obj.login_id.save()
        try:
            course = CourseTable.objects.get(id=course_id)
            obj.course_id = course
        except CourseTable.DoesNotExist:
            return render(request, "student_editprofile.html", {
                'obj': obj,
                'c': c,
                'error': 'Invalid department selected'
            })
        obj.save()
        return render(request, "student_editprofile.html", {
            'obj': obj,
            'c': c,
            'success': 'Profile updated successfully!'
        })

         
class DeleteSem(View):
    def get(self, request,sem_id):
        d = SemesterTable.objects.get(id=sem_id)
        d.delete()
        return redirect('viewsem')
    

class ViewFeedback(View):
    def get(self,request):
            feedbacks = FeedbackTable.objects.all()  
            return render(request, 'admin_viewfeedback.html', {'feedbacks': feedbacks})

class StudentDash(View):
     def  get(self,request):
        return render(request,"student_dashboard.html")
  
class StudentFeedback(View):
    def get(self,request):
        return render(request,'student_feedback.html')
    def post(self,request):
        form=FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # Assuming `student_id` is linked to the logged-in user
            user=LoginTable.objects.get(id=request.session.get('user_id') )
            feedback.student_id = user
            feedback.save()
            return redirect('studentprofile')

class StaffDash(View):
     def  get(self,request):
        return render(request,"staff_profile.html")
     
class StaffProfile(View):
    def get(self, request):
        # Assume the username is stored in the session after login
        userid = request.session.get('user_id')
        print(userid)
        if userid:
            # Query the LoginTable to fetch the user's details
            try:
                name = StaffTable.objects.get(login__id=userid)
                
                # email=StaffTable.objects.get()
                # print(user)
            except LoginTable.DoesNotExist:
                return redirect('login')  # Redirect to login if user not found
            
            # Pass the username to the template
            return render(request, "staff_profile.html", {"username": name })
        
        return redirect('login') 

class StudentProfile(View):
    def get(self, request):
        # Assume the user is logged in and their ID is available in session
        userid = request.session.get('user_id')
        
        if userid:
            # Query the StudentTable to fetch the student's details using the login_id (foreign key)
            try:
                student = StudentTable.objects.get(login_id__id=userid)
            except StudentTable.DoesNotExist:
                return redirect('login')  # Redirect to login if student not found
            
            # Pass the student's data to the template
            return render(request, "student_profile.html", {"student": student})
        
        # Redirect to login if the user is not authenticated or no session exists
        return redirect('login')

    
class StaffReg(View):
    def get(self,request):
        c=CollegeTable.objects.all()
        d=DepartmentTable.objects.all()
        return render(request,"staff_reg.html",{'c':c ,'d':d })
    def post(self, request):
        s = StaffForm(request.POST)
        if s.is_valid():
            # Create a LoginTable entry for the staff
            login_obj = LoginTable.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                type='pending'
            )
            
            # Save the StaffTable instance without committing to the database
            staff_instance = s.save(commit=False)
            
            # Assign the foreign key `login` to the `login_obj`
            staff_instance.login = login_obj
            
            # Save the `StaffTable` instance
            staff_instance.save()
            
            return redirect('login')
        else:
            # If the form is not valid, reload the registration page with errors
            c = CollegeTable.objects.all()
            d = DepartmentTable.objects.all()
            return render(request, "staff_reg.html", {'c': c, 'd': d, 'errors': s.errors})
        
class StudentReg(View):
    def get(self,request):
        c=CourseTable.objects.all()
        return render(request,"student_reg.html",{'c':c})
    def post(self, request):
        s = StudentForm(request.POST)
        if s.is_valid():
            
            login_obj = LoginTable.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                type='student'
            )
            
            student_instance = s.save(commit=False)
            
            # Assign the foreign key `login` to the `login_obj`
            student_instance.login_id = login_obj
            
            # Save the `StaffTable` instance
            student_instance.save()
            
            return redirect('login')
        else:
            # If the form is not valid, reload the registration page with errors
            c=CourseTable.objects.all()
            return render(request, "student_reg.html",{'c':c})
        


class RegPage(View):
    def get(self,request):
        return render(request , 'reg.html')
    
class HomeBase(View):
    def get(self,request):
        return render(request , 'home_base.html')

    

from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import redirect
from .models import CourseTable, SubjectTable, TimetableEntry, SemesterTable
import random
from random import shuffle

def generate_timetable(request):
    # Delete all existing timetable entries
    TimetableEntry.objects.all().delete()
    
    # Get all semesters (classes)
    classes = SemesterTable.objects.all()
    
    # Define days and periods
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day
    
    # Identify common and uncommon subjects
    common_subject_ids = SubjectTable.objects.annotate(class_count=Count('class1')).filter(class_count__gt=1).values_list('id', flat=True)
    common_subjects = SubjectTable.objects.filter(id__in=common_subject_ids)
    lab_subjects = SubjectTable.objects.filter(subject_name__icontains='-lab')
    uncommon_subjects = SubjectTable.objects.exclude(id__in=common_subject_ids).exclude(id__in=lab_subjects)
    
    common_subject_slots = {}
    
    # Allocate lab subjects first
    for cls in classes:
        class_labs = lab_subjects.filter(class1=cls)
        
        for lab in class_labs:
            hours_remaining = lab.contact_hours
            allocated = False  # Track if we successfully allocated the lab
            
            # Generate available slots for the class
            available_slots = {
                day: [period for period in periods if not TimetableEntry.objects.filter(day=day, period=period, cls=cls).exists()]
                for day in days
            }

            shuffle(days)  # Randomize day selection to distribute labs across the week

            # Try to find continuous slots based on contact hours
            for day in days:
                if allocated:
                    break  # Stop if lab is fully assigned
                
                available_periods = available_slots[day]
                available_periods.sort()  # Ensure periods are in order
                
                # Check for continuous blocks of lab.contact_hours
                for i in range(len(available_periods) - (hours_remaining - 1)):
                    if all(available_periods[j] == available_periods[i] + j for j in range(hours_remaining)):
                        # Found a continuous block
                        for j in range(hours_remaining):
                            TimetableEntry.objects.create(
                                day=day,
                                period=available_periods[i] + j,
                                cls=cls,
                                subject=lab,
                                faculty=lab.staff
                            )

                        allocated = True  # Lab has been scheduled
                        break  # Stop checking this day

    # Assign slots for common subjects
    for subject in common_subjects:
        available_slots = [
            {'day': day, 'period': period, 'cls': cls}
            for cls in classes if subject in cls.subjects.all()
            for day in days for period in periods
            if not TimetableEntry.objects.filter(day=day, period=period, cls=cls, subject__in=lab_subjects).exists()  # Exclude lab slots
        ]
        
        selected_slots = random.sample(available_slots, min(len(available_slots), subject.contact_hours)) if available_slots else []
        common_subject_slots[subject.id] = selected_slots
    # Initialize timetable entries
    for cls in classes:
        class_subjects = cls.subjects.all()
        
        for subject_id, slots in common_subject_slots.items():
            subject = SubjectTable.objects.get(id=subject_id)
            if subject in class_subjects:
                # Get how many periods have already been assigned for this subject
                assigned_hours = TimetableEntry.objects.filter(cls=cls, subject=subject).count()
                remaining_hours = subject.contact_hours - assigned_hours  # How many more we need to assign
                
                # Assign only up to the required contact hours
                for slot in slots[:remaining_hours]:  
                    if not TimetableEntry.objects.filter(day=slot['day'], period=slot['period'], cls=cls).exists():
                        TimetableEntry.objects.create(
                            day=slot['day'],
                            period=slot['period'],
                            cls=cls,
                            subject=subject,
                            faculty=subject.staff
                        )
    
    # Find empty slots
    empty_slots = [
        {'day': day, 'period': period, 'cls': cls}
        for cls in classes for day in days for period in periods
        if not TimetableEntry.objects.filter(day=day, period=period, cls=cls).exists()
    ]
    
    # Group subjects by faculty
    faculty_subjects = {}
    for subject in uncommon_subjects:
        faculty_subjects.setdefault(subject.staff, set()).add(subject)
    
    # Assign uncommon subjects
    for faculty, subjects in faculty_subjects.items():
        for subject in subjects:
            for cls in classes:
                if subject in cls.subjects.all():
                    available_slots = [entry for entry in empty_slots if entry['cls'].id == cls.id]
                    shuffle(available_slots)
                    
                    for entry in available_slots:
                        if subject.contact_hours <= 0:
                            break
                        if not TimetableEntry.objects.filter(day=entry['day'], period=entry['period'], faculty=faculty).exists():
                            TimetableEntry.objects.create(
                                day=entry['day'],
                                period=entry['period'],
                                cls=cls,
                                subject=subject,
                                faculty=faculty
                            )
                            empty_slots.remove(entry)
                            subject.contact_hours -= 1
    
    # Conflict resolution: Check for faculty scheduling conflicts and reassign
    for faculty in faculty_subjects.keys():
        faculty_entries = TimetableEntry.objects.filter(faculty=faculty)
        occupied_slots = {}
        
        for entry in faculty_entries:
            slot_key = (entry.day, entry.period)
            if slot_key in occupied_slots:
                conflicting_entry = occupied_slots[slot_key]
                available_slots = [e for e in empty_slots if e['cls'] == entry.cls]
                shuffle(available_slots)
                
                for new_entry in available_slots:
                    if not TimetableEntry.objects.filter(day=new_entry['day'], period=new_entry['period'], faculty=faculty).exists():
                        TimetableEntry.objects.filter(id=entry.id).update(
                            day=new_entry['day'],
                            period=new_entry['period']
                        )
                        empty_slots.remove(new_entry)
                        break
            else:
                occupied_slots[slot_key] = entry

    subject_hours_tracker = {sub.id: sub.contact_hours for sub in uncommon_subjects}

    for entry in empty_slots:
        # Get only uncommon subjects for the specific class
        available_subjects = uncommon_subjects.filter(class1=entry['cls'])

        # Exclude subjects already scheduled for this period in the class
        available_subjects = available_subjects.exclude(
            id__in=TimetableEntry.objects.filter(
                day=entry['day'], period=entry['period'], cls=entry['cls']
            ).values_list('subject', flat=True)
        )

        # Exclude subjects whose faculty is already teaching in the same period
        available_subjects = available_subjects.exclude(
            staff__in=TimetableEntry.objects.filter(
                day=entry['day'], period=entry['period']
            ).values_list('faculty', flat=True)
        )

        # Ensure subject has remaining contact hours
        available_subjects = [sub for sub in available_subjects if subject_hours_tracker[sub.id] > 0]

        if available_subjects:
            # Pick a random subject from the available ones
            subject = random.choice(available_subjects)

            # Assign the subject to the timetable
            TimetableEntry.objects.create(
                day=entry['day'],
                period=entry['period'],
                cls=entry['cls'],
                subject=subject,
                faculty=subject.staff
            )

            # Decrease the remaining contact hours for this subject
            subject_hours_tracker[subject.id] -= 1

    
    return redirect('timetable')



def timetable_view(request):
    # Get all classes
    classes = CourseTable.objects.all()
    
    # Define the days and periods
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

    # Initialize a dictionary to hold timetable data
    timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

    # Populate the timetable dictionary with entries
    entries = TimetableEntry.objects.all()
    for entry in entries:
        timetable_data[entry.cls][entry.day][entry.period] = entry

    # Create a context dictionary for the template
    context = {
        'timetable_data': timetable_data,
        'days': days,
        'periods': periods,
    }
    
    return render(request, 'view_timetable.html', context)



class TimetableView(View):
    template_name = 'timetable1.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get all classes
        


        classes = SemesterTable.objects.all()
    
        faculties= StaffTable.objects.all()
        
        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry.objects.filter(cls__in=classes)    
        for entry in entries:
            if '-' in entry.subject.subject_name:
                entry.subject.subject_name = entry.subject.subject_name.partition("-")[2]
            timetable_data[entry.cls][entry.day][entry.period] = entry
        print(entries)
        # Create a context dictionary for the template
        context = {
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'faculties':faculties
        }
        
        return render(request, self.template_name, context)
    

class StudentTimetable(View):
    template_name = 'timetable2.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get the logged-in student
        userid = request.session.get('user_id')
        print(userid)
        
        if userid:
            # Query the LoginTable to fetch the user's details
            try:
                student = StudentTable.objects.get(login_id__id=userid)
                print(student)
            except LoginTable.DoesNotExist:
                return redirect('login')  

        # Get the course the student is pursuing
        student_course = student.course_id # Assuming StudentTable has a ForeignKey to CourseTable

        # Get all semesters for that course
        semesters = SemesterTable.objects.filter(course_id=student_course)

        # Get faculties (for potential filtering)
        faculties = StaffTable.objects.all()

        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {
            semester: {day: {period: None for period in periods} for day in days} 
            for semester in semesters
        }

        # Populate the timetable dictionary with entries filtered for the student's course and semesters
        entries = TimetableEntry.objects.filter(cls__in=semesters).select_related('cls', 'subject', 'faculty')

        for entry in entries:
            if '-' in entry.subject.subject_name:
                entry.subject.subject_name = entry.subject.subject_name.partition("-")[2]
            timetable_data[entry.cls][entry.day][entry.period] = entry

        # Adjust the context for the frontend template
        context = {
            'timetable_data': timetable_data,
            'semesters': semesters,  # To populate the semester filter dropdown
            'days': days,
            'periods': periods,
            'faculties': faculties,  # In case faculty filter is also needed
        }

        return render(request, self.template_name, context)

class StaffTimetable(View):
    template_name = 'timetable3.html'  # Specify your template name here

    def get(self, request, *args, **kwargs):
        # Get all classes
        


        classes = SemesterTable.objects.all()
    
        faculties= StaffTable.objects.all()
        
        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry.objects.filter(cls__in=classes)    
        for entry in entries:
            if '-' in entry.subject.subject_name:
                entry.subject.subject_name = entry.subject.subject_name.partition("-")[2]
            timetable_data[entry.cls][entry.day][entry.period] = entry
        print(entries)
        # Create a context dictionary for the template
        context = {
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'faculties':faculties
        }
        
        return render(request, self.template_name, context)
    

class TimetablePage(View):
    def get(self,request):
        return render(request , "createtimetable.html")
   
    
def DeleteAll(request):
    if request.method == "POST":
        # Delete all objects from the model
        FeedbackTable.objects.all().delete()
      
    return redirect('viewfeedback')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TimetableEntry, SemesterTable, StaffTable, SubjectTable

def get_timetable_data():
    classes = SemesterTable.objects.all()
    faculties = StaffTable.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [1, 2, 3, 4, 5]  

    timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

    entries = TimetableEntry.objects.filter(cls__in=classes)
    for entry in entries:
        timetable_data[entry.cls][entry.day][entry.period] = entry

    return {
        'timetable_data': timetable_data,
        'days': days,
        'periods': periods,
        'classes': classes,
        'faculties': faculties
    }

def edit_timetable(request):
    context = get_timetable_data()
    return render(request, 'edit_timetable.html', context)

from django.http import JsonResponse
from .models import TimetableEntry, SemesterTable, StaffTable, SubjectTable
import json

def save_timetable(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            updated_timetable = data.get("timetable", {})
            force_update = data.get("force_update", False)

            conflicts = []
            existing_entries = TimetableEntry.objects.all()

            for key, value in updated_timetable.items():
                parts = key.split("_")
                if len(parts) == 4:
                    _, cls_id, day, period = parts
                    subject_id = updated_timetable.get(f"subject_{cls_id}_{day}_{period}")
                    faculty_id = updated_timetable.get(f"faculty_{cls_id}_{day}_{period}")

                    if subject_id and faculty_id:
                        subject = SubjectTable.objects.get(id=int(subject_id))
                        faculty = StaffTable.objects.get(id=int(faculty_id))

                        # Check for existing entry
                        entry = TimetableEntry.objects.filter(cls_id=int(cls_id), day=day, period=int(period)).first()

                        if entry:
                            # Conflict check (only if not force updating)
                            if not force_update:
                                conflict_entry = TimetableEntry.objects.filter(day=day, period=int(period), faculty=faculty).exclude(cls_id=int(cls_id)).first()
                                if conflict_entry:
                                    conflicts.append({
                                        "class_id": cls_id,
                                        "day": day,
                                        "period": period
                                    })
                                    continue  # Skip saving to prevent overwrite

                            # Update existing entry
                            entry.subject = subject
                            entry.faculty = faculty
                            entry.save()
                        else:
                            # Create new entry if none exists
                            TimetableEntry.objects.create(
                                day=day,
                                period=int(period),
                                cls_id=int(cls_id),
                                subject=subject,
                                faculty=faculty
                            )

            if conflicts and not force_update:
                return JsonResponse({"status": "conflict", "conflicts": conflicts}, status=400)

            return JsonResponse({"status": "success", "conflicts": []})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import LoginTable, StudentTable, StaffTable
import random
import string

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Case-insensitive email check
        staff = StaffTable.objects.filter(email__iexact=email).first()
        student = StudentTable.objects.filter(email__iexact=email).first()

        # If no user is found, show an error message
        if not staff and not student:
            messages.error(request, "No user found with this email.")
            return redirect("forgot_password")

        # Determine which user type it is and get the login instance
        login = None
        if staff and staff.login:
            login = staff.login
        elif student and student.login_id:
            login = student.login_id
        else:
            messages.error(request, "No user found with this email.")
            return redirect("forgot_password")

        # Generate a temporary password
        usr=login.username
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Update the password (Consider hashing for security)
        login.password = temp_password
        login.save()

        # Send email with the new password
        subject = "Your Temporary Password"
        message = f"Here is your temporary password: {temp_password} for the username {usr}\n\nPlease log in and change it immediately."
        send_mail(subject, message, "your-email@gmail.com", [email])

        messages.success(request, "A temporary password has been sent to your email.")
        HttpResponse("a temperory password is send to your email")
        return redirect("login")

    return render(request, "forgot_password.html")

