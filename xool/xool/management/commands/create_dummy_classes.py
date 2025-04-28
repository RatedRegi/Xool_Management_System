from django.core.management.base import BaseCommand
from xool.models import Class, Teacher, Subject
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates dummy classes'

    def handle(self, *args, **kwargs):
        # Create or get the user first
        user, created = User.objects.get_or_create(
            username='dummy_teacher',
            defaults={
                'first_name': 'Dummy',
                'last_name': 'Teacher',
                'email': 'dummy@example.com',
                'password': 'dummy123'  # This is just for testing
            }
        )

        # Create or get the teacher
        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'years_of_experience': 5,  # Adding the required field
                'subject': 'Mathematics',  # Adding required field
                'qualification': 'B.Ed',  # Adding required field
                'phone': '1234567890',  # Adding required field
                'gender': 'M'  # Adding required field
            }
        )

        # Get all subjects
        subjects = Subject.objects.all()
        if not subjects:
            self.stdout.write('No subjects found. Please create subjects first.')
            return

        # Create some sample classes
        classes_data = [
            {
                'name': 'Mathematics 101',
                'grade_level': '9',
                'academic_year': '2023-2024',
                'room_number': '101',
                'section': 'A',
                'subjects': ['MATH101']
            },
            {
                'name': 'Science 101',
                'grade_level': '9',
                'academic_year': '2023-2024',
                'room_number': '102',
                'section': 'B',
                'subjects': ['SCI101']
            },
            {
                'name': 'English 101',
                'grade_level': '9',
                'academic_year': '2023-2024',
                'room_number': '103',
                'section': 'C',
                'subjects': ['ENG101']
            }
        ]

        for class_data in classes_data:
            # Extract subjects from the class data
            subject_codes = class_data.pop('subjects')
            
            # Create the class
            class_obj = Class.objects.create(
                teacher=teacher,
                **class_data
            )
            
            # Add subjects to the class
            for code in subject_codes:
                subject = Subject.objects.get(code=code)
                class_obj.subjects.add(subject)

        self.stdout.write('Successfully created dummy classes with subjects') 