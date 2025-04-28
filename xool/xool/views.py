from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TeacherRegistrationForm, StudentRegistrationForm
from .models import Teacher, Student, Class, Attendance, Enrollment
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                logger.info(f"Created new student user: {user.username}")
                login(request, user)
                messages.success(request, 'Student registration successful!')
                return redirect('student_dashboard')
            except Exception as e:
                logger.error(f"Error creating student user: {str(e)}")
                messages.error(request, 'Error during registration. Please try again.')
        else:
            logger.error(f"Student registration form errors: {form.errors}")
    else:
        form = StudentRegistrationForm()
    return render(request, 'register_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                logger.info(f"Created new teacher user: {user.username}")
                login(request, user)
                messages.success(request, 'Teacher registration successful!')
                return redirect('teacher_dashboard')
            except Exception as e:
                logger.error(f"Error creating teacher user: {str(e)}")
                messages.error(request, 'Error during registration. Please try again.')
        else:
            logger.error(f"Teacher registration form errors: {form.errors}")
    else:
        form = TeacherRegistrationForm()
    return render(request, 'register_teacher.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        classes = Class.objects.filter(teacher=teacher)
        recent_attendance = Attendance.objects.filter(class_enrolled__teacher=teacher).order_by('-date')[:10]
        
        context = {
            'teacher': teacher,
            'classes': classes,
            'recent_attendance': recent_attendance,
        }
        return render(request, 'teacher_dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'You are not registered as a teacher.')
        return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        enrollments = student.enrollments.filter(is_active=True)
        recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
        
        context = {
            'student': student,
            'enrollments': enrollments,
            'recent_attendance': recent_attendance,
        }
        return render(request, 'student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'You are not registered as a student.')
        return redirect('teacher_dashboard')

def custom_login_redirect(request):
    # Check if user is a teacher
    try:
        Teacher.objects.get(user=request.user)
        return redirect('teacher_dashboard')
    except Teacher.DoesNotExist:
        pass
    
    # Check if user is a student
    try:
        Student.objects.get(user=request.user)
        return redirect('student_dashboard')
    except Student.DoesNotExist:
        messages.error(request, 'You are not registered as either a student or teacher.')
        return redirect('home')

@login_required
def view_course(request, course_id):
    try:
        # Get the course
        course = get_object_or_404(Class, id=course_id)
        logger.info(f"Attempting to view course: {course.name} (ID: {course_id})")
        
        # Get the student profile
        try:
            student = request.user.student
            logger.info(f"Student found: {student.user.get_full_name()}")
        except Student.DoesNotExist:
            logger.error(f"User {request.user.username} is not registered as a student")
            messages.error(request, 'You are not registered as a student.')
            return redirect('home')
        
        # Check enrollment
        try:
            enrollment = student.enrollments.get(class_enrolled=course, is_active=True)
            logger.info(f"Enrollment found for student {student.user.get_full_name()} in course {course.name}")
        except Enrollment.DoesNotExist:
            logger.error(f"Student {student.user.get_full_name()} is not enrolled in course {course.name}")
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('student_dashboard')
            
        # Get course materials
        materials = course.materials.filter(is_visible=True)
        logger.info(f"Found {materials.count()} materials for course {course.name}")
        
        context = {
            'course': course,
            'student': student,
            'progress': enrollment.progress,
            'materials': materials
        }
        return render(request, 'course_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error viewing course: {str(e)}")
        logger.error(f"User: {request.user.username}")
        logger.error(f"Course ID: {course_id}")
        messages.error(request, 'An error occurred while accessing the course. Please try again later.')
        return redirect('student_dashboard') 