from django.core.management.base import BaseCommand
from xool.models import Subject

class Command(BaseCommand):
    help = 'Creates dummy subjects'

    def handle(self, *args, **kwargs):
        # List of subjects to create
        subjects = [
            {
                'name': 'Mathematics',
                'description': 'Study of numbers, quantities, and shapes',
                'grade_level': '9',
                'code': 'MATH101',
                'is_elective': False,
                'credits': 4
            },
            {
                'name': 'Science',
                'description': 'Study of the natural world and its phenomena',
                'grade_level': '9',
                'code': 'SCI101',
                'is_elective': False,
                'credits': 4
            },
            {
                'name': 'English',
                'description': 'Study of language, literature, and composition',
                'grade_level': '9',
                'code': 'ENG101',
                'is_elective': False,
                'credits': 3
            },
            {
                'name': 'History',
                'description': 'Study of past events and their impact on society',
                'grade_level': '9',
                'code': 'HIS101',
                'is_elective': False,
                'credits': 3
            },
            {
                'name': 'Computer Science',
                'description': 'Study of computers and computational systems',
                'grade_level': '9',
                'code': 'CS101',
                'is_elective': True,
                'credits': 3
            },
            {
                'name': 'Art',
                'description': 'Study of visual arts and creative expression',
                'grade_level': '9',
                'code': 'ART101',
                'is_elective': True,
                'credits': 2
            }
        ]

        # Create subjects
        for subject_data in subjects:
            Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )

        self.stdout.write('Successfully created dummy subjects') 