from django.db import models


class State(models.Model):
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.state


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city

class Userdetails(models.Model):
    fullName=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phoneNumber=models.CharField(max_length=10)
    password=models.CharField(max_length=50)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    gender=models.CharField(max_length=50)
    dateOfBirth=models.DateField(null=True,blank=True)
    profilePicture=models.ImageField(upload_to='profile')
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.fullName

class Course_category(models.Model):
    category=models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Course(models.Model):
    courseTitle=models.CharField(max_length=80)
    courseDesc=models.TextField()
    category=models.ForeignKey(Course_category,on_delete=models.CASCADE)
    courseThumb=models.ImageField(upload_to='course')

    def __str__(self):
        return self.courseTitle

class EnrollmentList(models.Model):
    user=models.ForeignKey(Userdetails,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    enrollmentDate=models.DateField()
    status = models.CharField(max_length=5,default='true',null=True,blank=True)

    def __str__(self):
        return self.user.fullName