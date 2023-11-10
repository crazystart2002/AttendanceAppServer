import random

import simplejson as json

from rest_framework.decorators import api_view, action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .serializers import Session_Record_Table_Serializers, Course_Table_Serializers, Person_Table_Serializers, \
    Attendance_Record_Table_Serializers, Regisatration_Image_Serializer
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import person_table, course_table, session_record_table, attendance_record_table




@api_view(['POST'])
def create_new_course(request):
    code = ""
    for i in range(0, 10):
        code = code + chr(random.randint(50, 100))

    request.data['verification_code'] = code
    print(request.data)
    serializer = Course_Table_Serializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        person = person_table.objects.get(rollNumber=request.data["teacher"])
        course = course_table.objects.filter(verification_code=code)
        courseId = course.values('id')[0]['id']

        jsonDec = json.decoder.JSONDecoder()
        course_records = jsonDec.decode(person.course_list_created)
        course_records.append(courseId)
        print(course_records)
        person.course_list_created = json.dumps(course_records)
        person.save()

        person_serializer = Person_Table_Serializers(person)  # Serialize the person object

        course_data = course_table.objects.filter(id__in=course_records)  # Get course data
        course_serializer = Course_Table_Serializers(course_data, many=True)  # Serialize the course data

        return Response({
            "message": f"Created New Course {request.data['name']}",
            "Code": f"{code}",
            "person": person_serializer.data,
            "course_data": course_serializer.data  # Include serialized course data in the response
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_new_session(request):
    serializer = Session_Record_Table_Serializers(data=request.data)

    if serializer.is_valid(raise_exception=False):
        session = serializer.save()
        course_name = request.data.get('course_name', None)
        date = request.data.get('date', None)
        start_time = request.data.get('start_time', None)
        end_time = request.data.get('end_time', None)
        location = request.data.get('location', None)

        session_id = session_record_table.objects.filter(
            course_name=course_name, date=date, start_time=start_time, end_time=end_time, location=location).values(
            "id")[0]["id"]

        print(session_id)

        course = course_table.objects.get(name=course_name)
        if not (course):
            return Response(status=status.HTTP_404_NOT_FOUND)
        jsonDec = json.decoder.JSONDecoder()
        session_records = jsonDec.decode(course.sessions_list)
        session_records.append(session_id)

        course.sessions_list = json.dumps(session_records)
        course.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def new_student(request):
    serializer = Person_Table_Serializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def mark_attendance(request):
    serializer = Attendance_Record_Table_Serializers(data=request.data)
    if serializer.is_valid():
        student_id = serializer.validated_data['student_id']
        course_name = serializer.validated_data['course_name']

        try:
            course = course_table.objects.get(name=course_name)
            print(course.sessions_list)
            course_sessions_list = json.loads(course.sessions_list)
            print(course_sessions_list)
            session_id = course_sessions_list[-1]
            print(session_id)
            ins = attendance_record_table(student_id=student_id, course_name=course_name, session=session_id)
            ins.save()
            return Response({'msg': 'Attendance marked successfully.'}, status=status.HTTP_201_CREATED)
        except course_table.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid sessions_list format in course.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def course_session_details_teacher(request):
    if 'course_name' not in request.data:
        return Response({'error': 'course_name field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    course_name = request.data['course_name']
    try:
        course = course_table.objects.get(name=course_name)
        course_sessions_list = json.loads(course.sessions_list)
        print(course_sessions_list)
        sessions_list = session_record_table.objects.filter(id__in=course_sessions_list)
        print(sessions_list)

        serialized_sessions = []
        for session in sessions_list:
            serialized_session = {
                'id': session.id,
                'course_name': session.course_name,
                'date': session.date,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'location': session.location,
            }

            serialized_sessions.append(serialized_session)

        return Response(serialized_sessions, status=status.HTTP_200_OK)

    except course_table.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid sessions_list format in course.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def session_attendance_list(request):
    if 'course_name' not in request.data or 'date' not in request.data or 'start_time' not in request.data or 'end_time' not in request.data:
        return Response({'error': 'course_name, date, start_time, and end_time fields are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    course_name = request.data['course_name']
    date = request.data['date']
    start_time = request.data['start_time']
    end_time = request.data['end_time']

    try:
        session = session_record_table.objects.get(
            course_name=course_name, date=date, start_time=start_time, end_time=end_time)

        students_marked = list(attendance_record_table.objects.filter(course_name=course_name, session=session))

        serialized_students = []
        for student in students_marked:
            serialized_student = {
                'student_id': student.student_id,
                'course_name': student.course_name,
                'session': student.session.id,
                # Add other fields if needed
            }
            serialized_students.append(serialized_student)

        return Response(serialized_students, status=status.HTTP_200_OK)

    except session_record_table.DoesNotExist:
        return Response({'error': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)

    except attendance_record_table.DoesNotExist:
        return Response({'error': 'Attendance records not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def session_attendance_stats(request):
    if 'course_name' not in request.data or 'date' not in request.data or 'start_time' not in request.data or 'end_time' not in request.data:
        return Response({'error': 'course_name, date, start_time, and end_time fields are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    course_name = request.data['course_name']
    date = request.data['date']
    start_time = request.data['start_time']
    end_time = request.data['end_time']

    try:
        session = session_record_table.objects.get(
            course_name=course_name, date=date, start_time=start_time, end_time=end_time)

        session_id = session.id

        # getting number of students present
        students_marked = len(list(attendance_record_table.objects.filter(
            course_name=course_name, session=session_id)))

        # getting total number of students in the course
        course = course_table.objects.get(name=course_name)
        total_students = len(json.loads(course.students_list))

        return Response({'students_marked': students_marked, 'total_students': total_students},
                        status=status.HTTP_200_OK)

    except session_record_table.DoesNotExist:
        return Response({'error': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)

    except attendance_record_table.DoesNotExist:
        return Response({'error': 'Attendance records not found.'}, status=status.HTTP_404_NOT_FOUND)

    except course_table.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError:
        return Response({'error': 'Invalid students_list format in course.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def course_session_details_student(request):
    if 'course_name' not in request.data or 'student_id' not in request.data:
        return Response({'error': 'course_name and student_id fields are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    course_name = request.data['course_name']
    student_id = request.data['student_id']

    try:
        # Get the list of sessions the student is marked present for
        present_sessions_data = list(
            attendance_record_table.objects.filter(course_name=course_name, student_id=student_id))
        present_sessions = [session_record_table.objects.get(id=i.session) for i in present_sessions_data]

        # Get the list of all sessions for the specified course
        course_sessions_list = json.loads(course_table.objects.get(name=course_name).sessions_list)
        sessions_list = session_record_table.objects.filter(id__in=course_sessions_list)

        serialized_present_sessions = []
        for session in present_sessions:
            serialized_session = {
                'id': session.id,
                'course_name': session.course_name,
                'date': session.date,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'location': session.location,
            }
            serialized_present_sessions.append(serialized_session)

        serialized_all_sessions = []
        for session in sessions_list:
            serialized_session = {
                'id': session.id,
                'course_name': session.course_name,
                'date': session.date,
                'start_time': session.start_time,
                'end_time': session.end_time,
                'location': session.location,
            }
            serialized_all_sessions.append(serialized_session)

        return Response({'present': serialized_present_sessions, 'total': serialized_all_sessions},
                        status=status.HTTP_200_OK)

    except attendance_record_table.DoesNotExist:
        return Response({'error': 'Attendance records not found.'}, status=status.HTTP_404_NOT_FOUND)

    except course_table.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError:
        return Response({'error': 'Invalid sessions_list format in course.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def course_registration(request):
    if 'student_id' not in request.data or 'verification_code_entered' not in request.data:
        return Response({'error': 'student_id and verification_code_entered fields are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    student_id = request.data['student_id']
    verification_code_entered = request.data['verification_code_entered']
    # print(student_id,verification_code_entered)

    try:
        # Check the validity of the verification code
        course = course_table.objects.get(verification_code=verification_code_entered)
        student = person_table.objects.get(rollNumber=student_id)
        # print(course,student)

        # Adding the course to student profile
        jsonDec = json.decoder.JSONDecoder()
        course_records = jsonDec.decode(student.courses_list)
        # print("H?RLLO")
        course_records.append(course.id)
        student.courses_list = json.dumps(course_records)

        student.save()

        # Adding the student to course profile
        print("hello")
        print(course.students_list)
        if(course.students_list==None):
            students_records = jsonDec.decode("[]")
        else:
            students_records = jsonDec.decode(course.students_list)

        students_records.append(student.id)
        course.students_list = json.dumps(students_records)
        course.save()

        return Response({'msg': 'Course registration successful.'}, status=status.HTTP_200_OK)

    except course_table.DoesNotExist:
        return Response({'error': 'Invalid Verification Code'}, status=status.HTTP_400_BAD_REQUEST)

    except person_table.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError:
        return Response({'error': 'Invalid courses_list format in student.'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def show_created(request):
    course=course_table.objects.filter(teacher=request.data["teacher"])
    courseId = course.values('id')[0]['id']

    jsonDec = json.decoder.JSONDecoder()

    person=person_table.objects.filter(rollNumber=request.data["teacher"])
    person_serialised=Person_Table_Serializers(person, many=True)
    # print(person_serialised)
    if(len(person)==0):
        return Response(status=status.HTTP_404_NOT_FOUND)
    # print(person)
    course_records = jsonDec.decode(person[0].course_list_created)
    # print(course_records)
    course_records.append(courseId)
    course_data = course_table.objects.filter(id__in=course_records)  # Get course data
    course_serializer = Course_Table_Serializers(course_data, many=True)  # Serialize the course data
    # print(course_serializer)
    a={"info":person_serialised.data}
    a.update({"course_data": course_serializer.data})
    return Response(a, status=status.HTTP_200_OK)




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = (request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)