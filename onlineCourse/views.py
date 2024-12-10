from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Userdetails,State,City,Course,Course_category,EnrollmentList
from .serializer import Stateview,Cityview,CategoryView,SearchView


class StateClass(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = Stateview

class CityClass(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = Cityview

class CategoryClass(viewsets.ModelViewSet):
    queryset = Course_category.objects.all()
    serializer_class = CategoryView

class UserView(APIView):
    def get(self, request):
        # Retrieve all users
        users = Userdetails.objects.all()

        # List to store all user details
        user_list = []

        # Iterate through each user
        for user in users:
            # Prepare user details dictionary
            user_details = {

                    'id': user.id,
                    'fullName': user.fullName,
                    'email': user.email,
                    'phoneNumber':user.phoneNumber,
                    'state':user.state.id,
                    'city':user.city.id,
                    'dateOfBirth': str(user.dateOfBirth) if user.dateOfBirth else None,
                    'gender': user.gender,
            }
            if user.profilePicture:
                user_details['profilePicture'] = user.profilePicture.url
            else:
                user_details['profilePicture'] = None  # Or a default placeholder URL

            user_list.append(user_details)
        # Return the list of all users
        return Response(user_list, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # DRF will handle parsing
        print(data)

        try:
            # Personal Details
            fullName = data.get('fullName')
            email = data.get('email')
            phoneNumber = data.get('phoneNumber')
            password = data.get('password')
            state = data.get('state')
            city = data.get('city')
            gender = data.get('gender')
            dateOfBirth = data.get('dateOfBirth')
            profilePicture = request.FILES.get('profilePicture')




            try:
                state_obj = State.objects.get(id=state)
            except State.DoesNotExist:
                return Response({'error': 'Invalid state ID'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                city_obj = City.objects.get(id=city)
            except City.DoesNotExist:
                return Response({'error': 'Invalid city ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = Userdetails.objects.create(
                fullName=fullName,
                email=email,
                phoneNumber=phoneNumber,
                password=password,
                state=state_obj,
                city=city_obj,
                gender=gender,
                profilePicture=profilePicture
            )
            print(user)

            if data.get('dateOfBirth')!='null':
                user.dateOfBirth=dateOfBirth

            # Return the created user's details
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {e}")
            return Response({'message': 'Email Already registered'})


class UserDetail(APIView):
    def get(self, request, user_id):
        # Retrieve specific user by ID
        user = get_object_or_404(Userdetails, id=user_id)

        # Prepare user details dictionary
        user_details = {
            'id': user.id,
            'fullName': user.fullName,
            'email': user.email,
            'phoneNumber':user.phoneNumber,
            'state':user.state.state,
            'city':user.city.city,
            'dateOfBirth': str(user.dateOfBirth) if user.dateOfBirth else None,
            'gender': user.gender,
            }
        if user.profilePicture:
            user_details['profilePicture'] = user.profilePicture.url
        else:
            user_details['profilePicture'] = None  # Or a default placeholder URL

        print(user_details)

        # Return the user details
        return Response(user_details, status=status.HTTP_200_OK)

    # def put(self, request, user_id):
    #     # Retrieve the user
    #     user = get_object_or_404(User_details, id=user_id)
    #     personal_data = request.data['PersonalDetails']
    #     # Personal Details Update
    #     user.firstName = personal_data.get('firstName', user.firstName)
    #     user.lastName = personal_data.get('lastName', user.lastName)
    #     user.dateOfBirth = personal_data.get('dateOfBirth', user.dateOfBirth)
    #     user.email = personal_data.get('email', user.email)
    #     user.gender = personal_data.get('gender', user.gender)
    #     user.save()
    #
    #     # Languages Update
    #     if 'languages' in request.data:
    #         user.language.clear()
    #         for lang_id in request.data['languages']:
    #             language = Languages.objects.get(id=lang_id)
    #             user.language.add(language)
    #
    #     # Address Update
    #     if 'address' in request.data:
    #         address_data = request.data['address']
    #         address, created = Address_details.objects.get_or_create(user=user)
    #         address.houseNumber = address_data.get('houseNumber', address.houseNumber)
    #         address.street = address_data.get('street', address.street)
    #         address.city = address_data.get('city', address.city)
    #         address.state = address_data.get('state', address.state)
    #         address.pincode = address_data.get('pin', address.pincode)
    #         address.save()
    #
    #     # Experiences Update
    #     if 'experience' in request.data:
    #         # Remove existing experiences
    #         Experience_details.objects.filter(user=user).delete()
    #
    #         # Add new experiences
    #         for exp_data in request.data['experience']:
    #             Experience_details.objects.create(
    #                 user=user,
    #                 cName=exp_data['cName'],
    #                 position=exp_data['position'],
    #                 joiningDate=exp_data['exp_date'].get('joiningDate'),
    #                 resignDate=exp_data['exp_date'].get('resignDate')
    #             )
    #
    #         # Retrieve updated user details
    #         user_details = {
    #             'PersonalDetails': {
    #                 'id': user.id,
    #                 'firstName': user.firstName,
    #                 'lastName': user.lastName,
    #                 'dateOfBirth': str(user.dateOfBirth) if user.dateOfBirth else None,
    #                 'email': user.email,
    #                 'gender': user.gender
    #             },
    #             'languages': [lang.id for lang in user.language.all()],
    #             'address': None,
    #             'experience': []
    #         }
    #
    #         # Fetch address
    #         address = Address_details.objects.get(user=user)
    #         user_details['address'] = {
    #             'houseNumber': address.houseNumber,
    #             'street': address.street,
    #             'city': address.city,
    #             'state': address.state,
    #             'pincode': address.pincode
    #         }
    #
    #         # Fetch experiences
    #         experiences = Experience_details.objects.filter(user=user)
    #         user_details['experience'] = [
    #             {
    #                 'cName': exp.cName,
    #                 'position': exp.position,
    #                 'exp_date': {
    #                     'joiningDate': str(exp.joiningDate) if exp.joiningDate else None,
    #                     'resignDate': str(exp.resignDate) if exp.resignDate else None
    #                 }
    #             } for exp in experiences
    #         ]
    #         return Response(user_details, status=status.HTTP_200_OK)

    # def delete(self, request, user_id):
    #
    #     # Retrieve the user
    #     user = get_object_or_404(User_details, id=user_id)
    #
    #     # Delete associated experiences
    #     Experience_details.objects.filter(user=user).delete()
    #
    #     # Delete associated address
    #     Address_details.objects.filter(user=user).delete()
    #
    #     # Delete the user
    #     user.delete()

class CourseView(APIView):
    def get(self, request):
        # Retrieve all users
        courses = Course.objects.all()

        # List to store all user details
        course_list = []

        # Iterate through each user
        for course in courses:
            # Prepare user details dictionary
            course_details = {
                    'id': course.id,
                    'courseTitle': course.courseTitle,
                    'courseDesc': course.courseDesc,
                    'category': course.category.category,
                    'courseThumb': course.courseThumb.url,
            }

            course_list.append(course_details)
        # Return the list of all users
        return Response(course_list, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        try:
            # Validate required fields
            courseTitle = data.get('courseTitle')
            courseDesc = data.get('courseDesc')
            category_id = data.get('category')
            courseThumb = request.FILES.get('courseThumb')

            if not all([courseTitle, courseDesc, category_id, courseThumb]):
                return Response({
                    'error': 'Missing required fields'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve category object
            category_obj = Course_category.objects.get(id=category_id)

            # Create course
            course = Course.objects.create(
                courseTitle=courseTitle,
                courseDesc=courseDesc,
                category=category_obj,
                courseThumb=courseThumb
            )

            return Response({
                'message': 'Course added successfully',
                'course_id': course.id
            }, status=status.HTTP_201_CREATED)

        except Course_category.DoesNotExist:
            return Response({
                'error': 'Invalid category'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseDetail(APIView):
    def get(self, request, course_id):
        # Retrieve specific course by ID
        course = get_object_or_404(Course, id=course_id)

        # Prepare course details dictionary
        course_details = {
            'id': course.id,
            'courseTitle': course.courseTitle,
            'courseDesc': course.courseDesc,
            'category': course.category.id,
            'courseThumb': course.courseThumb.url,
        }


        print(course_details)

        # Return the user details
        return Response(course_details, status=status.HTTP_200_OK)

    def put(self, request, course_id):
        try:
            # Retrieve the course
            course = get_object_or_404(Course, id=course_id)

            # Update course details
            course.courseTitle = request.data.get('courseTitle', course.courseTitle)
            course.courseDesc = request.data.get('courseDesc', course.courseDesc)

            # Handle category update
            category_id = request.data.get('category')
            if category_id:
                try:
                    category = Course_category.objects.get(id=category_id)
                    course.category = category
                except Course_category.DoesNotExist:
                    return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

            # Handle file upload
            if 'courseThumb' in request.FILES:
                course.courseThumb = request.FILES['courseThumb']

            # Save the updated course
            course.save()

            # Construct response data
            response_data = {
                "id": course.id,
                "courseTitle": course.courseTitle,
                "courseDesc": course.courseDesc,
                "category": course.category.id if course.category else None,
                "courseThumb": request.build_absolute_uri(course.courseThumb.url) if course.courseThumb else None,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        try:
            # Retrieve the course
            course = get_object_or_404(Course, id=course_id)

            # Delete the course
            course.delete()

            # Return a successful response
            return Response({
                'status': 'success',
                'message': 'Course deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class Search(APIView):
    def get(self, request):
        print(request.query_params)
        query = request.query_params.get('search', '')  # Correct way to get query parameters in DRF

        if query:
            # Filter courses containing the query string (case-insensitive)
            courses = Course.objects.filter(courseTitle__icontains=query)
            if courses.exists():
                course_serializer = SearchView(courses, many=True)
                return Response(course_serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "No courses found for the given query."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Search query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self,request):
        try:
            data=request.data
            print(data)
            email=data.get('email')
            password=data.get('password')

            user=Userdetails.objects.get(email=email)
            if user.password == password:

                if user.is_admin == True:
                    return Response({'message': 'Login successful', 'userId': user.id, 'user': 1})
                else:
                    return Response({'message': 'Login successful', 'userId': user.id, 'user': 2})

            else:
                return Response({'error': 'Invalid password'}, status=400)
        except Userdetails.DoesNotExist:
                return Response({'error': 'Invalid email'}, status=400)

        return Response({'error': 'Invalid request method'}, status=405)


class CourseEnrollment(APIView):
    def post(self, request):
        try:
            # Validate input data
            data = request.data
            user_id = data.get('userId')
            course_id = data.get('Id')

            # Check if required parameters are present
            if not user_id or not course_id:
                return Response({
                    'message': 'Invalid user or course information'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch user and course objects
            try:
                user_obj = Userdetails.objects.get(id=user_id)
                course_obj = Course.objects.get(id=course_id)
            except Userdetails.DoesNotExist:
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except Course.DoesNotExist:
                return Response({
                    'message': 'Course not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check for existing enrollment
            existing_enrollment = EnrollmentList.objects.filter(
                user=user_obj,
                course=course_obj
            ).exists()

            if existing_enrollment:
                return Response({
                    'message': 'You have already enrolled in this course'
                })

            # Create new enrollment
            enrollment = EnrollmentList.objects.create(
                user=user_obj,
                course=course_obj,
                enrollmentDate=timezone.now().date()
            )

            return Response({
                'message': 'Enrolled successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Catch any unexpected errors
            return Response({
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnrollmentManagement(APIView):
    def get(self,request):
        enrollment = EnrollmentList.objects.all()
        # print(enrollment)

        enrollment_list = []
        today = timezone.now().date()

        for enroll in enrollment:
            # Check if enrollment is older than 30 days
            if (today - enroll.enrollmentDate).days > 30:
                enroll.status = 'false'
                enroll.save()  # Optionally save the status change

            enroll_details = {
                'id': enroll.id,
                'user': enroll.user.fullName,
                'course': enroll.course.courseTitle,
                'enrollmentDate':enroll.enrollmentDate,
                'status':enroll.status
            }

            enrollment_list.append(enroll_details)
            # print(enrollment_list)

        return Response(enrollment_list, status=status.HTTP_200_OK)

class EnrollmentFilter(APIView):
    def get(self, request, course_id):
        try:
            # Retrieve enrollments for the specific course
            enrollments = EnrollmentList.objects.filter(course=course_id)

            if not enrollments:
                return Response({
                    'status': 'error',
                    'message': 'No Data Found'
                })

            enroll_list = []
            today = timezone.now().date()

            for enr in enrollments:
                # Check if enrollment is older than 30 days
                if (today - enr.enrollmentDate).days > 30:
                    enr.status = 'false'
                    enr.save()  # Optionally save the status change

                enr_details = {
                    'id': enr.id,
                    'user': enr.user.fullName,
                    'courseTitle': enr.course.courseTitle,
                    'user_id': enr.user.id,
                    'enrollmentDate': enr.enrollmentDate,
                    'status': enr.status
                }

                enroll_list.append(enr_details)

            return Response(enroll_list, status=status.HTTP_200_OK)

        except EnrollmentList.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not found'
            })

        except Exception as e:
            # Log the error for debugging
            print(f"Unexpected error: {e}")
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, course_id):
        try:
            # Retrieve the course
            enrollment = get_object_or_404(EnrollmentList, id=course_id)

            # Delete the course
            enrollment.delete()

            # Return a successful response
            return Response({
                'status': 'success',
                'message': 'Course deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UserEnrollmentView(APIView):
    def get(self, request, user_id):
        try:
            # Retrieve enrollments for the specific course
            enrollments = EnrollmentList.objects.filter(user=user_id)

            if not enrollments:
                return Response({
                    'status': 'error',
                    'message': 'No Data Found'
                })

            enroll_list = []
            today = timezone.now().date()

            for enr in enrollments:
                # Check if enrollment is older than 30 days
                if (today - enr.enrollmentDate).days > 30:
                    enr.status = 'false'
                    enr.save()  # Optionally save the status change

                enr_details = {
                    'id': enr.id,
                    'courseTitle': enr.course.courseTitle,
                    'enrollmentDate': enr.enrollmentDate,
                    'status': enr.status
                }

                enroll_list.append(enr_details)

            return Response(enroll_list, status=status.HTTP_200_OK)

        except EnrollmentList.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not found'
            })

        except Exception as e:
            # Log the error for debugging
            print(f"Unexpected error: {e}")
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserEnrollmentEdit(APIView):
    def get(self, request, id):
        try:
            # Retrieve enrollments for the specific course
            enr = EnrollmentList.objects.get(id=id)

            if not enr:
                return Response({
                    'status': 'error',
                    'message': 'No Data Found'
                })

            enroll_list = []
            today = timezone.now().date()

            # Check if enrollment is older than 30 days
            if (today - enr.enrollmentDate).days > 30:
                enr.status = 'false'
                enr.save()  # Optionally save the status change

            enr_details = {
                'id': enr.id,
                'name':enr.user.fullName,
                'courseTitle': enr.course.courseTitle,
                'enrollmentDate': enr.enrollmentDate,
                'status': enr.status
            }
            print(enr_details)
            enroll_list.append(enr_details)

            return Response(enroll_list, status=status.HTTP_200_OK)

        except EnrollmentList.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not found'
            })

        except Exception as e:
            # Log the error for debugging
            print(f"Unexpected error: {e}")
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            # Retrieve the course
            enroll = get_object_or_404(EnrollmentList, id=id)
            data=request.data
            print(data)
            # Update course details
            enroll.course.courseTitle = request.data.get('course', enroll.course.courseTitle)
            enroll.user.fullName = request.data.get('name', enroll.user.fullName)
            enroll.enrollmentDate = request.data.get('enrollDate', enroll.enrollmentDate)
            enroll.status = request.data.get('status', enroll.status)

            print(enroll.course.courseTitle)


            enroll.save()

            # Construct response data
            response_data = {
                "id": enroll.id,
                "courseTitle": enroll.course.courseTitle,
                "enrollDate": enroll.enrollmentDate,
                "name":enroll.user.fullName,
                "status":enroll.status

            }
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

