import csv

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# from .resources import AcademicRegistrationResource
from .resources import *

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'phone', 'sex', 'title', 'is_active',
                    'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('personal', {'fields': ('first_name', 'middle_name', 'last_name', 'sex', 'phone', 'title'),
                      }),

        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups',
                                    'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)


class AcademicSemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'academic_year', 'start', 'end', 'is_active', 'created_by')
    search_field = ['semester', 'academic_year']
    list_filter = ['academic_year', 'academic_year']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(AcademicSemester, AcademicSemesterAdmin)


class AcademicYearAdmin(ImportExportModelAdmin):
    list_display = ('financial_year', 'created_by', 'is_active')
    search_fields = ['financial_year', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(AcademicYear, AcademicYearAdmin)


class BankAccountAdmin(ImportExportModelAdmin):
    list_display = ('bank', 'number', 'name', 'created_by')
    search_fields = ['bank', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(BankAccount, BankAccountAdmin)


class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource
    list_display = ('name', 'region', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(District, DistrictAdmin)


class LevelAdmin(ImportExportModelAdmin):
    resource_class = LevelResource
    list_display = ('name', 'year', 'created_by')
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Level, LevelAdmin)


class AssessmentItemAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name',)
    search_fields = ['name', ]

    # list_filter = ['is_core']


admin.site.register(AssessmentItem, AssessmentItemAdmin)


class CourseGroupAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'description',)
    search_fields = ['name', ]

    # list_filter = ['is_core']


admin.site.register(CourseGroup, CourseGroupAdmin)


class GroupAssessmentAdmin(ImportExportModelAdmin):
    resource_class = GroupAssessmentResource
    list_display = ('item', 'group', 'category', 'weight', 'passmark')
    search_fields = ['item', ]

    list_filter = ['item', 'group', 'category']


admin.site.register(GroupAssessment, GroupAssessmentAdmin)


class CourseAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('code', 'name')
    search_fields = ['code', ]

    # list_filter = ['item', 'group', 'category']


admin.site.register(Course, CourseAdmin)


class FeeItemAdmin(ImportExportModelAdmin):
    resource_class = FeeItemResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    # list_filter = ['is_core']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(FeeItem, FeeItemAdmin)


class FeeStructureAdmin(ImportExportModelAdmin):
    # resource_class = FeeStructureResource
    list_display = ('fee', 'semester', 'level', 'account', 'programme', 'amount')
    search_fields = ['level', ]

    list_filter = ['semester', 'level', 'programme']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(FeeStructure, FeeStructureAdmin)


class ProgrammeCourseStructureAdmin(ImportExportModelAdmin):
    resource_class = ProgrammeCourseStructureResource
    list_display = ('course', 'programme', 'level', 'semester', 'group','credit')
    search_fields = ['course', ]
    autocomplete_fields = ('course','level','programme')


    list_filter = ['semester', 'level', 'programme']


admin.site.register(ProgrammeCourseStructure, ProgrammeCourseStructureAdmin)


class PaymentStructureAdmin(ImportExportModelAdmin):
    resource_class = PaymentStructureResource
    list_display = ('semester', 'level', 'programme', 'amount', 'minimum')
    search_fields = ['programme', ]

    list_filter = ['semester', 'level', 'programme']


admin.site.register(PaymentStructure, PaymentStructureAdmin)


class SemesterAssessmentAdmin(ImportExportModelAdmin):
     # resource_class =
    list_display = ('registration','academic_semester', 'programme_course', 'assessment_group', 'marks', 'weight')
    search_fields = ['registration__student__user__username', ]

    list_filter = ['academic_semester', 'programme_course', 'assessment_group']


admin.site.register(SemesterAssessment, SemesterAssessmentAdmin)

class SemesterResultAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('registration','academic_semester', 'programme_course', 'ca', 'es', 'total','grade','remark')
    search_fields = ['registration__student__user__username', ]

    list_filter = ['academic_semester', 'programme_course']


admin.site.register(SemesterResult, SemesterResultAdmin)
class IntakeAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Intake, IntakeAdmin)


class PaymentAdmin(ImportExportModelAdmin):
    resource_class = PaymentResource
    list_display = ('registration', 'account', 'amount', 'due', 'date', 'created_by')
    search_fields = ['registration', ]

    list_filter = ['registration', 'account']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Payment, PaymentAdmin)


class ProgrammeAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name',)
    search_fields = ['name', ]

    list_filter = ['name']

    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     obj.save()


admin.site.register(Programme, ProgrammeAdmin)


class WorkloadAdmin(ImportExportModelAdmin):
    resource_class = WorkloadResource
    list_display = ('course', 'tutor')
    search_fields = ['tutor', ]

    list_filter = ['tutor']

    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     obj.save()


admin.site.register(Workload, WorkloadAdmin)


class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Region, RegionAdmin)


class SemesterAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'number', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Semester, SemesterAdmin)


class StatusAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('code', 'created_by')
    search_fields = ['code', ]

    list_filter = ['code']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Status, StatusAdmin)


class StudentAdmin(ImportExportModelAdmin):
    # resource_class = LocationResource
    list_display = (
        'user', 'programme', 'dob', 'parent_phone', 'residency',)
    search_fields = ['user', ]
    autocomplete_fields = ('user','residency','programme')

    list_filter = ['programme']
    # autocomplete_fields = ['district']

    def save_model(self, request, obj, form, change):
        obj.registerer = request.user
        obj.save()


admin.site.register(Student, StudentAdmin)


class RegistrationAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('student', 'intake', 'semester', 'level', 'status', 'is_active', 'is_registered', 'registerer')
    search_fields = ['student', ]

    list_filter = ['semester', 'level', 'is_active']
    #
    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     obj.save()


admin.site.register(Registration, RegistrationAdmin)

admin.site.register(CollegeSettings)