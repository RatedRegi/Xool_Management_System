from django.core.management.base import BaseCommand
from xool.models import Student, Class, Enrollment
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates dummy students and enrolls them in classes'

    def handle(self, *args, **kwargs):
        # Get all available classes
        classes = Class.objects.all()
        if not classes:
            self.stdout.write('No classes found. Please create classes first.')
            return

        # Create 10 dummy students
        for i in range(1, 11):
            # Create user
            user, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'first_name': f'Student',
                    'last_name': f'{i}',
                    'email': f'student{i}@example.com',
                    'password': 'dummy123'  # This is just for testing
                }
            )

            # Create student profile
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'grade_level': '9',
                    'parent_name': f'Parent {i}',
                    'parent_phone': f'123456789{i}',
                    'address': f'Address {i}',
                    'gender': random.choice(['M', 'F']),
                    'date_of_birth': timezone.now().date().replace(year=2005)
                }
            )

            # Enroll student in random classes
            selected_classes = random.sample(list(classes), random.randint(1, 3))
            for class_obj in selected_classes:
                # Get the next available roll number for this class
                last_roll = Enrollment.objects.filter(class_enrolled=class_obj).order_by('-roll_number').first()
                next_roll = 1 if last_roll is None else last_roll.roll_number + 1
                
                Enrollment.objects.get_or_create(
                    student=student,
                    class_enrolled=class_obj,
                    defaults={
                        'roll_number': next_roll,
                        'academic_year': '2023-2024',
                        'is_active': True
                    }
                )

        self.stdout.write('Successfully created dummy students and enrollments') 