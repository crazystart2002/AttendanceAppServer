from django.urls import path
from django.urls import include
from . import views



urlpatterns = [
    # path('register', views.UserRegistrationView.as_view(), name='Register'),
    # path('login', views.UserLoginView.as_view(), name='Login'),
    # path('userInfo', views.UserProfileView.as_view(), name='Profile'),
    path('create', views.create_new_session, name='created'),
    path('course', views.create_new_course, name="course"),
    path('student', views.new_student, name="student"),
    path('attendance', views.mark_attendance, name="attendance"),
    path('course_details_teacher',
         views.course_session_details_teacher, name="session_teacher"),
    path('session_attendance_details',
         views.session_attendance_list, name="attendance_list"),
    #session_attendance_stats

    path('course_details_student',
         views.course_session_details_student, name="session_student"),
    # path('register_image', views.Register_Image_Cls.as_view(), name='Register_image'),

    path('course_registration', views.course_registration,name="registerCourse_Student"),
    path('show_created',views.show_created,name="CreatedCourse_Display")





]
