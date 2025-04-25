from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Teacher, Subject, Class, Enrollment, Attendance

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student'

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline, TeacherInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'enrollment_date', 'parent_name', 'parent_phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'grade_level')
    list_filter = ('grade_level', 'enrollment_date', 'gender')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'years_of_experience', 'qualification', 'joining_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'subject')
    list_filter = ('subject', 'years_of_experience', 'qualification', 'is_class_teacher')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'grade_level', 'is_elective', 'credits')
    search_fields = ('name', 'code', 'grade_level')
    list_filter = ('grade_level', 'is_elective')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'section', 'teacher', 'academic_year', 'room_number')
    search_fields = ('name', 'grade_level', 'teacher__user__first_name', 'teacher__user__last_name')
    list_filter = ('grade_level', 'academic_year', 'section')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_enrolled', 'roll_number', 'enrollment_date', 'is_active')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_enrolled__name')
    list_filter = ('is_active', 'enrollment_date', 'academic_year')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_enrolled', 'date', 'is_present', 'time_in', 'time_out')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'class_enrolled__name')
    list_filter = ('is_present', 'date', 'class_enrolled') 
