import os

from dal import autocomplete
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from .models import *

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username',)


class UploadForm(forms.Form):

    def validate_file_extension(value):
        from django.core.exceptions import ValidationError

        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.csv']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Invalid file extension ')

    excel_file = forms.FileField(label='Excel File (.csv)', required=False, validators=[validate_file_extension])


# class EntryForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = ('admission', 'first_name', 'middle_name', 'last_name', 'sex', 'entry_rank')
#

# class SchoolForm(ModelForm):
#     class Meta:
#         model = School
#         fields = ('name', 'district')
#         widgets = {
#             'district': autocomplete.ModelSelect2(url='KCHS:district_autocomplete')
#         }


# class WorkLoadForm(ModelForm):
#     class Meta:
#         model = WorkLoad
#         fields = ('staff', 'subject', 'rank')


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(ModelForm):
    class Meta:
        model = Student
        fields = ('dob', 'parent_phone','residency')
        widgets = {
            'dob': DateInput(),
        }


# class CoordinatorForm(ModelForm):
#     class Meta:
#         model = Coordinator
#         fields = ('staff', 'rank')



# class AcademicEventForm(ModelForm):
#     class Meta:
#         model = AcademicEvent
#         fields = ('year', 'event', 'rank', 'deadline')
#         widgets = {
#             'deadline': DateInput(),
#
#         }


# class CombinationSubjectForm(ModelForm):
#     class Meta:
#         model = CombinationSubject
#         fields = ('combination', 'subject')


# class SubjectForm(ModelForm):
#     class Meta:
#         model = Subject
#         fields = ('name', 'is_core')
