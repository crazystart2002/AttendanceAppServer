from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class person_table(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rollNumber = models.CharField(max_length=255)
    courses_list = models.TextField(default='[]')
    course_list_created = models.TextField(default='[]')


class course_table(models.Model):
    name = models.CharField(max_length=50)
    verification_code = models.TextField()
    teacher = models.TextField()
    students_list = models.TextField(null=True)
    sessions_list = models.TextField(null=True)


class session_record_table(models.Model):
    course_name = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.TextField()


class attendance_record_table(models.Model):
    student_Id = models.IntegerField()
    course_name = models.CharField(max_length=50)
    session = models.TextField()  # stores session id
