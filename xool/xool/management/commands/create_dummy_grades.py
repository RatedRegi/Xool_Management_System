from django.core.management.base import BaseCommand
from xool.models import Enrollment, Subject, Grade
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates dummy grades for enrolled students'

    def handle(self, *args, **kwargs):
        # Get all active enrollments
        enrollments = Enrollment.objects.filter(is_active=True)
        if not enrollments:
            self.stdout.write('No active enrollments found. Please create students and enrollments first.')
            return

        # Get all subjects
        subjects = Subject.objects.all()
        if not subjects:
            self.stdout.write('No subjects found. Please create subjects first.')
            return

        # Create grades for each student in their enrolled classes
        for enrollment in enrollments:
            class_obj = enrollment.class_enrolled
            student = enrollment.student
            
            # Get subjects for this class
            class_subjects = class_obj.subjects.all()
            
            for subject in class_subjects:
                # Create multiple grades for different assignments/tests
                for i in range(1, 4):  # Create 3 grades per subject
                    # Generate a random grade between 60 and 100
                    grade = random.randint(60, 100)
                    
                    # Create the grade record
                    Grade.objects.get_or_create(
                        student=student,
                        subject=subject,
                        class_enrolled=class_obj,
                        defaults={
                            'grade': grade,
                            'grade_type': random.choice(['assignment', 'quiz', 'test']),
                            'date': timezone.now().date() - timezone.timedelta(days=random.randint(1, 30)),
                            'remarks': f'Grade for {subject.name} {random.choice(["Assignment", "Quiz", "Test"])} {i}'
                        }
                    )

        self.stdout.write('Successfully created dummy grades') 