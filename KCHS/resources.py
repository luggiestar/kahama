from import_export import resources, fields

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User
from import_export.widgets import ForeignKeyWidget

from .models import *


#
#
class FeeStructureResource(resources.ModelResource):
    fee = fields.Field(
        column_name='fee',
        attribute='fee',
        widget=ForeignKeyWidget(FeeItem, 'name')

    )
    semester = fields.Field(
        column_name='semester',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, 'name')

    )
    level = fields.Field(
        column_name='level',
        attribute='level',
        widget=ForeignKeyWidget(Level, 'name')

    )
    account = fields.Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(BankAccount, 'bank')

    )
    programme = fields.Field(
        column_name='programme',
        attribute='programme',
        widget=ForeignKeyWidget(Programme, 'name')

    )

    class Meta:
        model = FeeStructure
        fields = (
            'id', 'fee', 'semester', 'level', 'account', 'programme', 'amount')


class PaymentStructureResource(resources.ModelResource):

    semester = fields.Field(
        column_name='semester',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, 'name')

    )
    level = fields.Field(
        column_name='level',
        attribute='level',
        widget=ForeignKeyWidget(Level, 'name')

    )
    account = fields.Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(BankAccount, 'bank')

    )
    programme = fields.Field(
        column_name='programme',
        attribute='programme',
        widget=ForeignKeyWidget(Programme, 'name')

    )

    class Meta:
        model = PaymentStructure
        fields = (
            'id', 'semester', 'level', 'account', 'programme', 'amount','minimum')


class ProgrammeCourseStructureResource(resources.ModelResource):
    course = fields.Field(
        column_name='course',
        attribute='course',
        widget=ForeignKeyWidget(Course, 'code')

    )
    semester = fields.Field(
        column_name='semester',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, 'name')

    )
    level = fields.Field(
        column_name='level',
        attribute='level',
        widget=ForeignKeyWidget(Level, 'name')

    )
    group = fields.Field(
        column_name='group',
        attribute='group',
        widget=ForeignKeyWidget(CourseGroup, 'name')

    )
    programme = fields.Field(
        column_name='programme',
        attribute='programme',
        widget=ForeignKeyWidget(Programme, 'name')

    )

    class Meta:
        model = ProgrammeCourseStructure
        fields = (
            'id', 'programme', 'course', 'semester', 'level', 'group','credit')


#
class PaymentResource(resources.ModelResource):
    registration = fields.Field(
        column_name='registration',
        attribute='registration',
        widget=ForeignKeyWidget(Registration, 'student__user__username')

    )
    account = fields.Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(BankAccount, 'bank')

    )

    class Meta:
        model = Payment
        fields = ('id', 'registration', 'account', 'amount', 'due')


class WorkloadResource(resources.ModelResource):
    course = fields.Field(
        column_name='course',
        attribute='course',
        widget=ForeignKeyWidget(ProgrammeCourseStructure, 'course__code')

    )
    tutor = fields.Field(
        column_name='tutor',
        attribute='tutor',
        widget=ForeignKeyWidget(User, 'username')

    )

    class Meta:
        model = Workload
        fields = ('id', 'course', 'tutor')



from import_export import resources


# class StudentResource(resources.ModelResource):
#     registerer = fields.Field(
#         column_name='registerer',
#         attribute='registerer',
#         widget=ForeignKeyWidget(User, 'email')
#
#     )
#
#     class Meta:
#         model = Student
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'parent_phone', 'sex', 'registerer')
# #
#
# class OrganizationResource(resources.ModelResource):
#     class Meta:
#         model = Region
#         fields = ('id', 'name', 'email')
#
#
class LevelResource(resources.ModelResource):
    class Meta:
        model = Level
        fields = ('id', 'name', 'year',)


class FeeItemResource(resources.ModelResource):
    class Meta:
        model = FeeItem
        fields = ('id', 'name',)


#
#
class GroupAssessmentResource(resources.ModelResource):
    item = fields.Field(
        column_name='item',
        attribute='item',
        widget=ForeignKeyWidget(AssessmentItem, 'name')

    )

    group = fields.Field(
        column_name='group',
        attribute='group',
        widget=ForeignKeyWidget(CourseGroup, 'name')

    )

    class Meta:
        model = GroupAssessment
        fields = ('id', 'item', 'group', 'category', 'weight', 'passmark')


#
#
class RegionResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')

    )

    class Meta:
        model = Region
        fields = ('id', 'name', 'created_by')


class DistrictResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')

    )
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'name')

    )

    class Meta:
        model = District
        fields = ('id', 'name', 'created_by')
