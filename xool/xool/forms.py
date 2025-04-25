from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Teacher, Student

class TeacherRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    subject = forms.CharField(max_length=100, required=True)
    school = forms.CharField(max_length=100, required=True)
    years_experience = forms.IntegerField(required=True)
    qualifications = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            teacher = Teacher.objects.create(
                user=user,
                subject=self.cleaned_data['subject'],
                years_of_experience=self.cleaned_data['years_experience'],
                qualification=self.cleaned_data['qualifications'],
                phone=self.cleaned_data['phone']
            )
        return user

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    grade_level = forms.CharField(max_length=10, required=True)
    parent_name = forms.CharField(max_length=100, required=True)
    parent_phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                grade_level=self.cleaned_data['grade_level'],
                parent_name=self.cleaned_data['parent_name'],
                parent_phone=self.cleaned_data['parent_phone'],
                address=self.cleaned_data['address']
            )
        return user

def SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'subject', 'school', 'years_experience', 'qualifications')
    
