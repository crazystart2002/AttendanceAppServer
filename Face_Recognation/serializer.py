from rest_framework import serializers
from .models import Face_Recognation2
from drf_extra_fields.fields import Base64ImageField


class Register_Image_Serializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Face_Recognation2
        fields = ('student_Id', 'image')

    def create(self, validated_data):
        image = validated_data.pop('image')
        student_Id = validated_data.pop('student_Id')
        return Face_Recognation2.objects.create(student_Id=student_Id, image=image)
