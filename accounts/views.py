from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache


from accounts.models import Student


# Create your views here.
@login_required
@never_cache
def dashboard_view(request):
    return render(request,'dashboard.html')

def signup_page(request):
    if request.method == 'POST':
        username=request.POST.get('txtname')
        email=request.POST.get('email')
        password=request.POST.get('pwd')
        conforim_password=request.POST.get('cpwd')

        if password != conforim_password:
            messages.error(request,"password & conforim_password not matching")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User is already exists")
            return redirect('signup')

        user=User.objects.create_user(username=username,
                                   email=email,
                                   password=password)
        user.save()
        messages.success(request,"successfully created")
    return render(request,'signup.html')

@login_required
def mystudents_view(request):
    if request.user.is_superuser:
        my_students = Student.objects.all().values()
    else:
        my_students= Student.objects.filter(user_id=request.user.id).values()
    return render(request,'Display.html',{"student_data":my_students})

@login_required
def addstudents_view(request):
    if request.method == 'POST':
        student_name=request.POST.get("student_name")
        student_email=request.POST.get("student_email")
        student_education=request.POST.get("education")
        student_course=request.POST.get("course")
        student_paid_fee=float(request.POST.get("fee_paid"))
        student_total_fee=float(request.POST.get("total_fee"))

        if Student.objects.filter(email=student_email).exists():
            messages.error(request,"email is already exists")
            return render(request,'add_students.html')
        student = Student.objects.create(user=request.user,
                                     name=student_name,
                                     email=student_email,
                                     education=student_education,
                                     course=student_course,
                                     paid_fee=student_paid_fee,
                                     total_fee=student_total_fee)
        pending_fee=student_total_fee-student_paid_fee
        subject = "Admission Confirmation"
        message = f"""
              Hello {student_name},


              You have successfully joined the course: {student_course}.
              Total Fee: ₹{student_total_fee}
              Fee Paid: ₹{student_paid_fee}
              Pending Fee: ₹{pending_fee}


              Please pay the remaining fee on time.


              Regards,
              Palle Institute
                      """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return redirect('mystudents')
    return render(request,'add_students.html',{'action':'Add'})

@login_required
def deletestudent_view(request,id):
        if request.user.is_superuser:
            student = get_object_or_404(Student, id=id)
        else:
            student = get_object_or_404(Student, id=id, user=request.user)

        student.delete()
        return redirect('mystudents')

@login_required
def updatestudent_view(request,id):
    student = get_object_or_404(Student, id=id, user=request.user)
    if request.method == 'POST':
        student.name=request.POST.get("student_name")
        student.email=request.POST.get("student_email")
        student.education=request.POST.get("education")
        student.course=request.POST.get("course")
        student.paid_fee=float(request.POST.get("fee_paid"))
        student.total_fee=float(request.POST.get("total_fee"))
        student.save()
        return redirect('mystudents')

    return render(request,'Add_students.html',{'action':'update',"student":student})

@login_required
def myemployee_view(request):
        my_employees = User.objects.all().values()
        return render(request, 'emp_Display.html', {"employee_data": my_employees})



@login_required
def addemployees_view(request):
    if request.method == 'POST':
        employee_name = request.POST.get("username")
        employee_email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        role = request.POST.get("role")
        if password != cpassword:
            messages.error(request, "password and confirm password is not matching")
            return redirect('addemployee')

        if User.objects.filter(email=employee_email).exists():
            messages.error(request, "email already exists")
            return redirect('addemployee')
        if role == 'admin':
            employee = User.objects.create_superuser(username=employee_name,
                                                         email=employee_email,
                                                         password=password)
        else:
            employee = User.objects.create_user(username=employee_name,
                                                    email=employee_email,
                                                    password=password)
            employee.is_active = True
            employee.is_staff = False
            employee.save()
        messages.success(request, "sucessfully added")
        return redirect('myemployees')
    return render(request, "add_employee.html", {"action": "Add"})

@login_required
def delete_employee_view(request, id):
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect('myemployees')

@login_required
def updateemployee_view(request, id):
    employee = get_object_or_404(User, id=id)
    if request.method == 'POST':
        employee.username = request.POST.get("username")
        employee.email = request.POST.get("email")
        # employee.role = request.POST.get("role")
        employee.save()
        messages.success(request, "Employee updated successfully!")
        return redirect('myemployees')

    return render(request, 'add_employee.html', {'action': 'update', "employee": employee})