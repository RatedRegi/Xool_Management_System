from django.core.management.base import BaseCommand
from xool.models import Class, CourseMaterial
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates dummy course materials'

    def handle(self, *args, **kwargs):
        classes = Class.objects.all()
        if not classes:
            self.stdout.write('No classes found')
            return

        for class_obj in classes:
            CourseMaterial.objects.create(
                class_enrolled=class_obj,
                title=f"Introduction to {class_obj.name}",
                description="Basic concepts and overview",
                material_type='lecture',
                is_visible=True
            )
            CourseMaterial.objects.create(
                class_enrolled=class_obj,
                title=f"{class_obj.name} Assignment 1",
                description="First assignment covering basic topics",
                material_type='assignment',
                is_visible=True
            )
            CourseMaterial.objects.create(
                class_enrolled=class_obj,
                title=f"{class_obj.name} Quiz 1",
                description="First quiz to test understanding",
                material_type='quiz',
                is_visible=True
            )

        self.stdout.write('Successfully created dummy materials') 