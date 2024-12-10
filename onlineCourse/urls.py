from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views
from .views import UserView,UserDetail,CourseView,CourseDetail,Search,UserLogin,CourseEnrollment,EnrollmentManagement,EnrollmentFilter,UserEnrollmentView,UserEnrollmentEdit
#
router=SimpleRouter()
router.register('states',views.StateClass)
router.register('city',views.CityClass)
router.register('categories',views.CategoryClass)

urlpatterns = [
    path('', include(router.urls)),
    path('users/',UserView.as_view(),name='users'),
    path('users/<int:user_id>/',UserDetail.as_view(),name='user'),
    path('courses/',CourseView.as_view(),name='courses'),
    path('courses/<int:course_id>/',CourseDetail.as_view(),name='course'),
    path('search/',Search.as_view(),name='search'),
    path('login/',UserLogin.as_view(),name='login'),
    path('enroll/',CourseEnrollment.as_view(),name='enroll'),
    path('enrollManagement/',EnrollmentManagement.as_view(),name='enrollManagement'),
    path('courseFilter/<int:course_id>/',EnrollmentFilter.as_view(),name='courseFilter'),
    path('usercourseFilter/<int:user_id>/',UserEnrollmentView.as_view(),name='usercourseFilter'),
    path('editenroll/<int:id>/',UserEnrollmentEdit.as_view(),name='editenroll')
]