
from django.contrib import admin
from django.urls import path

from timetable_scheduler_app import views
from timetable_scheduler_app.views import *

urlpatterns = [
    path('regpage',RegPage.as_view(),name="regpage"),
    path('',HomeBase.as_view(),name="homebase"),
    path('homedash', HomePage.as_view(), name="home"),
    path('login',LoginPage.as_view(), name="login"),
    path('logout',Logout.as_view(),name="logout"),
    path('reg',RegPage.as_view(),name="reg"),
    path('forgot-password/', forgot_password, name='forgot_password'),

    path('admindash',AdminDash.as_view(),name="admindash"),
    path('adminprofile',Profile.as_view(),name='adminprofile'),
    path('verifystaff',VerifyStaff.as_view(),name="verifystaff"),
    path('classview',ClassView.as_view(),name="addclass"),
    path('conflictview',ConflictView.as_view(),name="conflictview"),
    path('viewfeedback',ViewFeedback.as_view(),name="viewfeedback"),
    path('addcollege',AddCollege.as_view(),name="add_college"),
    path('viewcollege',ViewCollege.as_view(),name="view_college"),
    path('editcollege/<int:id>',EditCollege.as_view(),name="edit_college"),  
    path('deletecollege/<int:id>', DeleteCollege.as_view(), name='delete_college') ,
    path('adddep', AddDep.as_view(), name='add_dep') ,
    path('viewdep', ViewDep.as_view(), name='view_dep') ,
    path('deletedep/<int:dep_id>', DeleteDep.as_view(), name='delete_dep'),
    path('editdep/<int:dep_id>',EditDep.as_view(),name="edit_dep"),  
    path('addsubject', AddSub.as_view(), name='addsubject') ,  
    path('viewsubject', ViewSub.as_view(), name='viewsubject') ,
    path('deletesubject/<int:sub_id>', DeleteSub.as_view(), name='deletesubject'),
    path('editsubject/<int:sub_id>',EditSub.as_view(),name="editsubject"),  
    path('addcourse', AddCourse.as_view(), name='addcourse') ,  
    path('viewcourse', ViewCourse.as_view(), name='viewcourse') ,
    path('deletecourse/<int:course_id>', DeleteCourse.as_view(), name='deletecourse'),
    path('editcourse/<int:course_id>',EditCourse.as_view(),name="editcourse"),  
    path('addsem', AddSem.as_view(), name='addSem') ,  
    path('viewsem', ViewSem.as_view(), name='viewsem') ,
    path('add',Add.as_view(),name="add"),
    path('deletesem/<int:sem_id>', DeleteSem.as_view(), name='deletesem'),
    path('accept_staff/<int:staff_id>',Accept_Staff.as_view(),name="accept_staff"),
    path('timetable',TimetableView.as_view(),name='timetable'),
    path('edit_timetable/', edit_timetable, name='edit_timetable'),
    path('save_timetable/', save_timetable, name='save_timetable'),
    path('reject_staff/<int:staff_id>',Reject_Staff.as_view(),name="reject_staff"),
    path('editsem/<int:sem_id>',EditSem.as_view(),name='editsem'),
    path('admindeleteconflict/<int:conflict_id>',AdminDeleteConflict.as_view(),name='deleteconflict'),
    path('createtimetable',TimetablePage.as_view(),name='createtimetable'),
    path('generatetimetable',generate_timetable,name='generatetimetable'),
    path('deleteall/deleteall/',DeleteAll,name='deleteall'),


    path('staffconflict',StaffConflict.as_view(),name="staffconflict"),
    path('staffreg',StaffReg.as_view(),name="staffreg"),
    path('staffdeletesub/<int:sub_id>', StaffDeleteSub.as_view(), name='staffdeletesub'),
    path('staffdash',StaffDash.as_view(),name='staffdash'),
    path('viewalloc',ViewAlloc.as_view(),name="viewalloc"),
    path('deleteconflict/<int:conflict_id>',DeleteConflict.as_view(),name='deleteconflict'),
    path('timetable3',StaffTimetable.as_view(),name='timetable3'),   
    path('staffprofile',StaffProfile.as_view(),name='staffprofile'),
    path('staffeditprofile/<int:prof_id>',StaffEditProfile.as_view(),name="staffeditprofile"),
    path('staffaddsub',StaffSubAdd.as_view(),name="staffaddsub"),
    path('staffeditsub/<int:sub_id>',StaffSubEdit.as_view(),name="staffeditsub"),
    path('individual',StaffIndividual.as_view(),name="individual"),

    path('studentdash',StudentDash.as_view(),name="student"),
    path('studreg',StudentReg.as_view(),name="studreg"),
    path('studentfeedback',StudentFeedback.as_view(),name="studentfeedback"),
    path('studviewsubject', StudSub.as_view(), name='studviewsubject') ,
    path('timetable2',StudentTimetable.as_view(),name='timetable2'),
    path('studentprofile',StudentProfile.as_view(),name='studentprofile'),
    path('studenteditprofile/<int:prof_id>',StudentEditProfile.as_view(),name="studenteditprofile"),
 
]






