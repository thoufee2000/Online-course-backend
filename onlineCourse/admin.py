from django.contrib import admin
from .models import Userdetails,State,City,Course_category,Course,EnrollmentList

admin.site.register(Userdetails)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Course)
admin.site.register(Course_category)
admin.site.register(EnrollmentList)
