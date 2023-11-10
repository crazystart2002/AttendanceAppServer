from rest_framework import serializers
from .models import person_table, course_table, session_record_table, attendance_record_table

class Person_Table_Serializers(serializers.ModelSerializer):
    class Meta:
        model = person_table
        fields = ("__all__")


class Course_Table_Serializers(serializers.ModelSerializer):
    class Meta:
        model = course_table
        fields = ("__all__")


class Session_Record_Table_Serializers(serializers.ModelSerializer):
    class Meta:
        model = session_record_table
        fields = ("__all__")


class Attendance_Record_Table_Serializers(serializers.ModelSerializer):
    class Meta:
        model = attendance_record_table
        fields = ("__all__")

class Regisatration_Image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = attendance_record_table
        fields= ["student_Id", "image"]
