from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from timetable_scheduler_app.models import *
from timetable_scheduler_app.form import *


class HomePage(View):
    def get(self, request):
        return render(request, "home.html")


class Logout(View):
    def get(self,request):
        return render(request,"login.html")
      
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
                 return HttpResponse('''<script>alert('Login successfull');window.location='/admindash'</script>''')
            elif obj.type=='staff':
                return render(request,'staff_dashboard.html')
            elif obj.type=='student':
                return render(request,'student_dashboard.html')
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
     def  get(self,request):
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
        print(request.POST['staff_id'])
        if form.is_valid():
            form.save()
            return redirect('viewsubject')
        
class ViewSub(View):
    def get(self,request):
        obj=SubjectTable.objects.all()
        return render(request,"college/view_subject.html",{'val':obj})
    
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
    def post(self,request,sub_id):
        obj = CourseTable.objects.get(id=sub_id)
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
    def get(self,request):
        return render(request,'adminbase.html')
    
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
        return render(request,"staff_dashboard.html")
    
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