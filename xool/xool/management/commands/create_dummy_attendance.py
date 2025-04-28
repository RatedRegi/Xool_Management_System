from django.core.management.base import BaseCommand
from xool.models import Enrollment, Attendance
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates dummy attendance records for enrolled students'

    def handle(self, *args, **kwargs):
        # Get all active enrollments
        enrollments = Enrollment.objects.filter(is_active=True)
        if not enrollments:
            self.stdout.write('No active enrollments found. Please create students and enrollments first.')
            return

        # Create attendance records for the last 30 days
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            
            # Skip weekends
            if date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
                continue
                
            for enrollment in enrollments:
                # 90% chance of being present
                is_present = random.random() < 0.9
                
                # Create attendance record
                Attendance.objects.get_or_create(
                    student=enrollment.student,
                    class_enrolled=enrollment.class_enrolled,
                    date=date,
                    defaults={
                        'is_present': is_present,
                        'time_in': timezone.now().replace(hour=8, minute=random.randint(0, 30)) if is_present else None,
                        'time_out': timezone.now().replace(hour=15, minute=random.randint(0, 30)) if is_present else None,
                        'remarks': '' if is_present else 'Absent'
                    }
                )

        self.stdout.write('Successfully created dummy attendance records') 