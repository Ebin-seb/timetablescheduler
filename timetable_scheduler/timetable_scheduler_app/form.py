from django.forms import ModelForm

from timetable_scheduler_app.models import *

class LoginForm(ModelForm):
    class Meta:
        model = LoginTable
        fields = ['username', 'password']

class CollegeForm(ModelForm):
    class Meta:
        model = CollegeTable
        fields = ['college']

class DepForm(ModelForm):
    class Meta:
        model = DepartmentTable
        fields = ['dep_name']

class SubForm(ModelForm):
    class Meta:
        model = SubjectTable
        fields = ['subject_name','contact_hours','staff']

class CourseForm(ModelForm):
    class Meta:
        model = CourseTable
        fields = ['course_name','dep_id']

class Semform(ModelForm):
    class Meta:
        model=SemesterTable
        fields=['semester_name','course_id','subjects']

class FeedbackForm(ModelForm):
    class Meta:
        model=FeedbackTable
        fields=['feedback_text']

class StaffForm(ModelForm):
    class Meta:
        model=StaffTable
        fields=['name','college_id','email','department_id','qualification']

class StudentForm(ModelForm):
    class Meta:
        model=StudentTable
        fields=['name','email']

class ConflictForm(ModelForm):
    class Meta:
        model=ConflictTable
        fields=['conflict_text']


