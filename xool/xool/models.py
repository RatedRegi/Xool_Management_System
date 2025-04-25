from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    grade_level = models.CharField(max_length=10)
    enrollment_date = models.DateField(auto_now_add=True)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    blood_group = models.CharField(max_length=5, blank=True)
    medical_conditions = models.TextField(blank=True)

    class Meta:
        ordering = ('user__first_name', 'user__last_name')
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.get_full_name()} - Grade {self.grade_level}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    subject = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    qualification = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    blood_group = models.CharField(max_length=5, blank=True)
    medical_conditions = models.TextField(blank=True)
    is_class_teacher = models.BooleanField(default=False)

    class Meta:
        ordering = ('user__first_name', 'user__last_name')
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grade_level = models.CharField(max_length=10)
    code = models.CharField(max_length=10, unique=True)
    is_elective = models.BooleanField(default=False)
    credits = models.IntegerField(default=1)
    syllabus = models.FileField(upload_to='syllabus/', blank=True)

    class Meta:
        ordering = ('name', 'grade_level')
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.name} - Grade {self.grade_level}"

class Class(models.Model):
    name = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes')
    subjects = models.ManyToManyField(Subject)
    academic_year = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10, blank=True)
    capacity = models.IntegerField(default=30)
    section = models.CharField(max_length=1, default='A')

    class Meta:
        ordering = ('grade_level', 'section')
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.name} - Grade {self.grade_level}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    roll_number = models.IntegerField()
    academic_year = models.CharField(max_length=20)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ('class_enrolled', 'roll_number')
        unique_together = ('class_enrolled', 'roll_number')
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.student} enrolled in {self.class_enrolled}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ('-date', 'student__user__first_name')
        unique_together = ('student', 'class_enrolled', 'date')
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.is_present else 'Absent'}"

# Signal to create Student/Teacher profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # You can set default values or handle this differently based on your needs
        pass 