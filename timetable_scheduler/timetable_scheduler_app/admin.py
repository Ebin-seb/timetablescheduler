from django.contrib import admin

from timetable_scheduler_app.models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(StudentTable)
admin.site.register(CollegeTable)
admin.site.register(DepartmentTable)
admin.site.register(SubjectTable)
admin.site.register(StaffTable)
admin.site.register(CourseTable)
admin.site.register(SemesterTable)
admin.site.register(FeedbackTable)
admin.site.register(ConflictTable)
admin.site.register(TimetableEntry)