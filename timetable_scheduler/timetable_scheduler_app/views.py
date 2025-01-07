from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from timetable_scheduler_app.models import *
from timetable_scheduler_app.form import *
from .models import *


class HomePage(View):
    def get(self, request):
        return render(request, "home.html")
class Logout(View):
    def get(self,request):
        return redirect('login')
      
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
    def get(self,request):
        print("%%%%%%%%%%%%%%", request.session['user_id'])
        obj=SubjectTable.objects.filter(staff__login_id=request.session['user_id'])
        return render(request,"staff_viewalloc.html" ,{'obj':obj})

    
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
    def get(self,request):
        obj=SubjectTable.objects.all()

        return render(request,"student_viewsub.html",{'val':obj})

    
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
     def post(self,request):
        form=Semform(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.save()
            # Save ManyToManyField after saving the instance
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
        co=CourseTable.objects.all()
        return render(request, "college/edit_sem.html",{'c':c , 'sub':sub ,'co':co})
    def post(self,request,sem_id):
        c = SemesterTable.objects.get(id=sem_id)
        c.semester_name=request.POST.get('semester_name')
        c.save
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
            return redirect('student')

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
            return render(request, "staff_profile.html", {"username": name})
        
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
        return render(request,"student_reg.html")
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
            return render(request, "student_reg.html")
        


class RegPage(View):
    def get(self,request):
        return render(request , 'reg.html')
    
class HomeBase(View):
    def get(self,request):
        return render(request , 'home_base.html')

    

from django.http import HttpResponse
from django.db.models import Count
from .models import CourseTable, SubjectTable, TimetableEntry
import random
from random import shuffle
from django.views import View
def generate_timetable(request):
    #delete all timetable entries
    TimetableEntry.objects.all().delete()
    # Get all classes
    classes = SemesterTable.objects.all()
    
    # Define the days and periods
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day
    
    # Identify common subjects across all classes
    common_subject_ids = SubjectTable.objects.annotate(class_count=Count('class1')).filter(class_count__gt=1).values_list('id', flat=True)
    common_subjects = SubjectTable.objects.filter(id__in=common_subject_ids)
    uncommon_subjects = SubjectTable.objects.exclude(id__in=common_subject_ids)
    common_subject_slots = {}
    selected_slots=[]

    # Assign common subjects
    for subject in common_subjects:
        # Collect available slots across all classes where the subject is taught
        available_slots = []
        for cls in classes:
            class_subjects = cls.subjects.all()
            if subject in class_subjects:
                for day in days:
                    for period in periods:
                        available_slots.append({
                            'day': day,
                            'period': period,
                            'cls': cls
                        })

        # Assign slots for the subject
        
        hours_remaining = subject.contact_hours

        if available_slots:
            num_slots_to_select = min(len(available_slots), hours_remaining)
            selected_slots = random.sample(available_slots, num_slots_to_select)
        else:
            print(f"No available SubjectTableslots for subject {subject.subject_name}")
            selected_slots = []  # Ensure selected_slots is defined

        # Save selected slots for the subject
        common_subject_slots[subject.id] = selected_slots
        
    # Initialize timetable for each class
    for cls in classes:
        # Get subjects for the class
        class_subjects = cls.subjects.all()
        
        # Initialize timetable
        timetable = []
        for day in days:
            for period in periods:
                timetable.append({
                    'day': day,
                    'period': period,
                    'cls': cls,
                    'subject': None
                })
        
        # Assign common subjects
        for subject_id, slots in common_subject_slots.items():
            subject = SubjectTable.objects.get(id=subject_id)
            if subject in class_subjects:
                for slot in slots:
                    # Ensure that the slot is available
                    while True:
                        if not TimetableEntry.objects.filter(day=slot['day'], period=slot['period'], cls=cls, subject=subject).exists():
                            TimetableEntry.objects.create(
                                day=slot['day'],
                                period=slot['period'],
                                cls=cls,
                                subject=subject,
                                faculty=subject.staff
                            )
                            # print(f"Assigned {subject.name} to {cls.name} on {slot['day']} period {slot['period']}")
                            break  # Exit loop when assignment is successful
                        else:
                            # print(f"Slot already occupied: {slot['day']} period {slot['period']} for {subject.name} in {cls.name}")
                            # Remove the occupied slot and try another one
                            slots.remove(slot)
                            if slots:
                                slot = random.choice(slots)
                            else:
                                print(f"No more available slots for {subject.subject_name} in {cls.semester_name}")
                                break  # Exit loop if no slots are available
        
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
 
        # Create a dictionary to store subjects by the same faculty across all classes
    faculty_subjects = {}

    # Loop through all classes
    for cls in SemesterTable.objects.all():
        class_subjects = cls.subjects.all()  # Get all subjects for this class

        for subject in uncommon_subjects:
            faculty = subject.staff
            
            # Check if this faculty is already in the dictionary
            if faculty not in faculty_subjects:
                faculty_subjects[faculty] = set()  # Initialize an empty set for subjects
            
            # Add the full subject object to the faculty's set of subjects
            faculty_subjects[faculty].add(subject)

    # Filter only faculty who teach multiple subjects
    faculty_multiple_subjects = {faculty: subjects for faculty, subjects in faculty_subjects.items() if len(subjects) > 1}

    # Print final result (optional)
    # print(faculty_multiple_subjects)

    # First Pass: Assign subjects without checking if the faculty is already occupied
    for faculty, subjects in faculty_multiple_subjects.items():
        # Process each subject for the faculty
        for subject in subjects:
            # Only assign the subject if it belongs to the class for the current empty slot
            # print('Subject:', subject)

            # Loop through each class
            for cls in SemesterTable.objects.all():
                # print('Class:', cls.id)
                
                if subject in cls.subjects.all():  # Ensure subject is part of the current class
                    hours_remaining = subject.contact_hours
                    # print('Hours remaining:', hours_remaining)
                    # print('Contact hours:', subject.contact_hours)

                    # Collect available slots for this class
                    available_slots = [entry for entry in empty_slots if entry['cls'].id == cls.id]
                    # print('Available slots:', available_slots)
                    # Shuffle to get a random order
                    shuffle(available_slots)
                    
                    # Assign slots
                    for entry in available_slots:
                        if hours_remaining <= 0:
                            break
                        # Ensure the slot is available and not already occupied
                        if not TimetableEntry.objects.filter(day=entry['day'], period=entry['period'], cls=cls, subject=subject).exists():
                            # Initially, we skip the check for faculty conflict
                            TimetableEntry.objects.create(
                                day=entry['day'],
                                period=entry['period'],
                                cls=entry['cls'],
                                subject=subject,
                                faculty=faculty
                            )
                            hours_remaining -= 1
                            # print('Hours remaining after assignment:', hours_remaining)
                            empty_slots.remove(entry)
                            if hours_remaining == 0:
                                break  # Exit loop when all hours are assigned
                        else:
                            print(f"Slot already occupied for subject {subject.subject_name} in class {cls.name} on {entry['day']} period {entry['period']}")
                    
                    # If the subject is not assigned yet and there are no available slots left, print a message
                    if hours_remaining > 0:
                        print(f"No available slots for {subject.subject_name} in class {cls.semester_name}")
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
    
    
    # Second Pass: Check for faculty conflicts and reassign if necessary
    for faculty in faculty_multiple_subjects.keys():
        # Find all timetable entries for this faculty
        faculty_entries = TimetableEntry.objects.filter(faculty=faculty)
        
        # Dictionary to track periods and days where the faculty is already scheduled
        occupied_slots = {}
        
        # Loop through each entry for this faculty
        for entry in faculty_entries:
            slot_key = (entry.day, entry.period)
            
            if slot_key in occupied_slots:
                # Conflict found: faculty is already assigned in this slot
                conflicting_entry = occupied_slots[slot_key]
                # print(f"Conflict found: faculty {faculty} is scheduled for both {conflicting_entry.subject.name} and {entry.subject.name} on {entry.day}, period {entry.period}.")
                
                # Try to reassign one of the subjects (you can choose which one to reassign)
                reassign_entry = entry  # For example, reassign the current entry
                reassign_cls = reassign_entry.cls
                reassign_subject = reassign_entry.subject
                
                # Collect available slots for reassignment
                available_slots = [e for e in empty_slots if e['cls'] == reassign_cls]
                shuffle(available_slots)
                
                # Find a new slot for the conflicting subject
                for new_entry in available_slots:
                    if not TimetableEntry.objects.filter(day=new_entry['day'], period=new_entry['period'], faculty=faculty).exists():
                        # Reassign to a new slot
                        TimetableEntry.objects.filter(id=reassign_entry.id).update(
                            day=new_entry['day'],
                            period=new_entry['period']
                        )
                        # print(f"Reassigned subject {reassign_subject.name} to {new_entry['day']} period {new_entry['period']} for class {reassign_cls.name}.")
                        empty_slots.remove(new_entry)
                        break
            else:
                # No conflict, mark the slot as occupied by this faculty
                occupied_slots[slot_key] = entry

    # Flatten the list of subjects from faculty_multiple_subjects
    faculty_subject_ids = [subject.id for subjects in faculty_multiple_subjects.values() for subject in subjects]

    # Identify remaining subjects by excluding subjects from faculty_multiple_subjects
    remaining_subjects = uncommon_subjects.exclude(id__in=faculty_subject_ids)
    print('remaining_subjects',remaining_subjects)
    
    empty_slots = []
    # Calculate empty slots by filtering out occupied ones from the timetable
    for cls in classes:
        # Get all periods for this class
        timetable_entries = TimetableEntry.objects.filter(cls=cls)

        # Initialize a list of all possible slots for this class
        full_slots = []
        for day in days:
            for period in periods:
                full_slots.append({'day': day, 'period': period, 'cls': cls})

        # Filter out the slots already occupied in the timetable
        
        for slot in full_slots:
            if not timetable_entries.filter(
                day=slot['day'], 
                period=slot['period'],
                cls=slot['cls']
            ).exists():
                empty_slots.append(slot)
    print('emptyslots',empty_slots)
    

    for cls in SemesterTable.objects.all():
        class_subjects = cls.subjects.all()  # Get all subjects for this class

        for subject in remaining_subjects:
            if subject in class_subjects:  # Only assign if the subject is in the current class
                hours_remaining = subject.contact_hours

                # Collect available slots for this class
                available_slots = [entry for entry in empty_slots if entry['cls'].id == cls.id]
                shuffle(available_slots)  # Shuffle to ensure random assignment
                
                # Assign slots
                for entry in available_slots:
                    if hours_remaining <= 0:
                        break  # Stop if all hours are assigned
                    
                    # Ensure the slot is available and not already occupied
                    if not TimetableEntry.objects.filter(day=entry['day'], period=entry['period'], cls=cls, subject=subject).exists():
                        # Check if the faculty is available for this slot
                        if not TimetableEntry.objects.filter(day=entry['day'], period=entry['period'], faculty=subject.staff).exists():
                            # Create a new timetable entry
                            TimetableEntry.objects.create(
                                day=entry['day'],
                                period=entry['period'],
                                cls=entry['cls'],
                                subject=subject,
                                faculty=subject.staff
                            )
                            hours_remaining -= 1  # Decrease remaining contact hours
                            empty_slots.remove(entry)  # Remove the slot from available slots

                    # Exit loop when all hours for this subject are assigned
                    if hours_remaining == 0:
                        break
    return HttpResponse("Timetable generated successfully!")        

# from django.shortcuts import render
# from .models import TimetableEntry, CourseTable

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
        entries = TimetableEntry.objects.all()
        for entry in entries:
            if '-' in entry.subject.subject_name:
                entry.subject.subject_name = entry.subject.subject_name.split("-")[1]
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
        # Get all classes
        classes = SemesterTable.objects.all()
        faculties = StaffTable.objects.all()

        # Define the days and periods
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [1, 2, 3, 4, 5]  # Assuming 5 periods per day

        # Initialize a dictionary to hold timetable data
        timetable_data = {cls: {day: {period: None for period in periods} for day in days} for cls in classes}

        # Populate the timetable dictionary with entries
        entries = TimetableEntry.objects.select_related('cls', 'subject', 'faculty').all()
        for entry in entries:
            if '-' in entry.subject.subject_name:
                entry.subject.subject_name = entry.subject.subject_name.split("-")[1]
            timetable_data[entry.cls][entry.day][entry.period] = entry

        # Adjust the context for the frontend template
        context = {
            'timetable_data': timetable_data,
            'classes': classes,  # To populate the class filter dropdown
            'days': days,
            'periods': periods,
            'faculties': faculties,  # In case faculty filter is also needed
        }

        return render(request, self.template_name, context)
