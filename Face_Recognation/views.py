import http
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.views import APIView

from rest_framework.response import Response

from Face_Recognation.serializer import Register_Image_Serializer
import face_recognition, os, base64
import numpy as np


@api_view(['POST'])
def Register_Image(request):
    serializer = Register_Image_Serializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        _, image_data = request.data['image'].split(',')
        image_filename = f"{request.data['student_Id']}.png"  # You can set your desired filename
        image_path = os.path.join("/Users/admin/PycharmProjects/AttendanceSysytemServer/Face_Recognation/media_image",
                                  image_filename)

        # Decode and save the image
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        # Load the image using face_recognition library
        image = face_recognition.load_image_file(image_path)

        face_locations = face_recognition.face_locations(image)
        print(face_locations)

        print(face_locations)
        if len(face_locations) != 1:
            # Handle the case when no face or multiple faces are detected
            return Response({"error": "Invalid number of faces detected."}, status=status.HTTP_400_BAD_REQUEST)

        face_encoding = face_recognition.face_encodings(image, face_locations)[0]
        print(face_encoding)
        save_folder = "/Users/admin/PycharmProjects/AttendanceSysytemServer/Face_Recognation/encoding_folder"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        encoding_filename = f"{request.data['student_Id']}.npy"
        encoding_path = os.path.join(save_folder, encoding_filename)

        # Save the facial encoding to a file using numpy
        np.save(encoding_path, face_encoding)

        serializer.save()
        return Response({"success"}, status=status.HTTP_201_CREATED)


    return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
