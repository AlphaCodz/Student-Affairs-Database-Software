from django.shortcuts import render, redirect, reverse
from .models import Students, ComplaintForm
from django.db.models import Count, Q
from django.views import View
from django.contrib import messages
import re

# Create your views here.
class HomePage(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        students = Students.objects.all().exclude(department='')
        complaints = ComplaintForm.objects.all()
        

        counts = students.aggregate(
            total_count=Count('pk'),
            final_year_students=Count('pk', filter=Q(level="ND-3")),
            year_two_students=Count('pk', filter=Q(level="ND-2")),
            freshers_count=Count('pk', filter=Q(level="ND-1")),
        )

        context = {
            "student": students,
            "count": counts['total_count'],
            "final_year_students": counts['final_year_students'],
            "year_two_students": counts['year_two_students'],
            "freshers": counts['freshers_count'],
            "complaint": complaints,
        }
        return render(request, self.template_name, context)
    
from django.http import HttpResponseRedirect  # Add this import

class StudentForms(View):
    def get(self, request, *args, **kwargs):
        print("IN GET ")
        return render(request, "forms.html")
    
    def check_is_digit(self, request, matric_number):
        return matric_number.isdigit()
    
    def check_matric_number(self, request, matric_number):
        pattern = r'^[a-zA-Z\d/]+$'
        if re.match(pattern, matric_number):
            return True
        else:
            # messages.error(request, "Invalid Matric Number")
            return False  # Return False for invalid matric number
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        passport = request.FILES.get("passport")
        email = request.POST.get("email")
        matric_number = request.POST.get("matric_number")
        department = request.POST.get("department")
        level = request.POST.get("level")
        status = request.POST.get("status")
        
        if len(matric_number) < 15:
            messages.error(request, "Invalid Matric Number")
            return HttpResponseRedirect(reverse("admin_panel:form"))
        
        if not self.check_matric_number(request, matric_number):
            messages.error(request, "Invalid Matric Number")
            return HttpResponseRedirect(reverse("admin_panel:form"))
        if self.check_is_digit(request, matric_number):
            messages.error(request, "Invalid Matric Number")
            return HttpResponseRedirect(reverse("admin_panel:form"))
        
        student = Students.objects.create(first_name=first_name, 
                                          last_name=last_name, 
                                          email=email,
                                          passport=passport,
                                          matric_number=matric_number, 
                                          department=department, 
                                          level=level,
                                          status=status, 
                                          username=username)
        messages.success(request, "Student Created Successfully")
        return HttpResponseRedirect(reverse("admin_panel:form"))

def forms_page(request):
    students = Students.objects.all()
    departments = Students.objects.values_list('department', flat=True).distinct()
    context = {
        "students": students,
        "departments": departments
    }
    return render(request, "forms.html", context=context)


class StudentComplaintForm(View):
    template_name = "biodata.html"
    
    def get(self, request):
        students = Students.objects.all().values(
           "id", "first_name", "last_name", "email", "matric_number"
        )
        
        context = {
            "students": students
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        student = request.POST.get("student")
        title = request.POST.get("title")
        issue = request.POST.get("issue")
        

        complaintform = ComplaintForm.objects.create(
            student=student,  # Use the student instance directly
            title=title,
            issue=issue
        )
        messages.success(request, f"{complaintform.title} has been submitted. Student Affairs will send a feedback soon!")
        return HttpResponseRedirect(reverse("admin_panel:homepage"))
