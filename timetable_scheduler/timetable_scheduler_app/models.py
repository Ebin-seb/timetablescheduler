from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.
class LoginTable(models.Model):
    username=models.CharField(max_length=50,blank=True,null=True)
    password=models.CharField(max_length=50,blank=True,null=True)
    type=models.CharField(max_length=50,blank=True,null=True)

class CollegeTable(models.Model):
    college=models.CharField(max_length=50,blank=True,null=True)
    
class DepartmentTable(models.Model):
    college_id=models.ForeignKey(CollegeTable,on_delete=models.CASCADE,blank=True,null=True)
    dep_name=models.CharField(max_length=50,blank=True,null=True)

class CourseTable(models.Model):
    dep_id=models.ForeignKey(DepartmentTable,on_delete=models.CASCADE,blank=True,null=True)
    course_name=models.CharField(max_length=50,blank=True,null=True)

class StaffTable(models.Model):
    login=models.ForeignKey(LoginTable,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50,blank=True,null=True)
    college_id=models.ForeignKey(CollegeTable,on_delete=models.CASCADE,blank=True,null=True)
    email=models.CharField(max_length=50,blank=True,null=True)
    department_id=models.ForeignKey(DepartmentTable,on_delete=models.CASCADE,blank=True,null=True)
    qualification=models.CharField(max_length=50,blank=True,null=True)



class SubjectTable(models.Model):
    subject_name=models.CharField(max_length=50,blank=True,null=True)
    contact_hours=models.IntegerField(blank=True,null=True)
    staff=models.ForeignKey(StaffTable,on_delete=models.CASCADE,null=True,blank=True)

class SemesterTable(models.Model):
    login_id=models.ForeignKey(LoginTable,on_delete=models.CASCADE,blank=True,null=True)
    course_id=models.ForeignKey(CourseTable,on_delete=models.CASCADE,null=True,blank=True)
    semester_name=models.CharField(max_length=50,blank=True,null=True)
    subjects=models.ManyToManyField(SubjectTable,related_name='class1')

@receiver(post_delete, sender=SubjectTable)
def delete_Classes_with_subject(sender, instance, **kwargs):
    for class_instance in SemesterTable.objects.filter(subjects=instance):
            class_instance.delete()

class TimetableEntry(models.Model):
    day=models.CharField(max_length=10)
    period=models.IntegerField()
    cls=models.ForeignKey(SemesterTable,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(SubjectTable,on_delete=models.CASCADE,blank=True,null=True)
    faculty=models.ForeignKey(StaffTable,on_delete=models.CASCADE,blank=True,null=True)

class StudentTable(models.Model):
    login_id=models.ForeignKey(LoginTable,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=50,blank=True,null=True)
    semester_id=models.ForeignKey(SemesterTable,on_delete=models.CASCADE,blank=True,null=True)
    email=models.CharField(max_length=50,blank=True,null=True)

    
class ConflictTable(models.Model):
    staff_id = models.ForeignKey(StaffTable, on_delete=models.CASCADE) 
    conflict_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  

class FeedbackTable(models.Model):
    student_id=models.ForeignKey(LoginTable, on_delete=models.CASCADE) 
    feedback_text = models.TextField() 
    submitted_at = models.DateTimeField(auto_now_add=True)

