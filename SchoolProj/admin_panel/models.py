from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
import random as rand, string 
import uuid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        # Set is_staff=True for regular users who can log in
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        
        extra_fields.setdefault('username', str(uuid.uuid4()))
        extra_fields.setdefault('first_name', "admin")
        extra_fields.setdefault('last_name', "admin")
        return self.create_user(email, password, **extra_fields)

class Students(AbstractUser):
    LEVEL = (
        ("ND-1", "ND-1"),
        ("ND-2", "ND-2"),
        ("ND-3", "ND-3")
    )
    
    STATUS = (
        ("EXCO", "EXCO"),
        ("Student", "Student")
    )
    
    DEPARTMENT = (
        ("Computer Science", "Computer Science"),
        ("Office Technology Management", "Office Technology Management"),
        ("Accounting", "Accounting"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Electrical Engineering", "Electrical Engineering"),
        ("Hospitality Management", "Hospitality Management"),
        ("Science and Laboratory Technology", "Science and Laboratory Technology")
    )
    
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    matric_number = models.CharField(max_length=20, null=True)
    department = models.CharField(choices=DEPARTMENT, max_length=33)
    level = models.CharField(choices=LEVEL, max_length=4)
    status = models.CharField(choices=STATUS, max_length=7)
    date_registered = models.DateField(auto_now_add=True)
    passport = models.FileField(upload_to="student_password/", null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    
    def __str__(self):
        return self.first_name
    
class ComplaintForm(models.Model):
    student = models.CharField(max_length=200)
    title = models.CharField(max_length=250)
    issue = models.TextField()
    
    def __str__(self):
            return self.title
        