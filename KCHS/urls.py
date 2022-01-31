from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# from .views import DistrictAutocomplete

app_name = 'KCHS'

urlpatterns = [
    path('', views.home, name="home"),

    path('login', views.user_login, name="login"),
    path('admission-letter', views.admission_letter, name="admission_letter"),
    path('user-home', views.user_home, name="user_home"),
    path('user-profile', views.user_profile, name="user_profile"),
    path('programme-list/', views.programme_list, name="programme_list"),
    path('programme-payment-structure/<programme_name>/<level_name>/', views.programme_payment_structure,
         name="programme_payment_structure"),
    path('financial-year-incomplete-payment/', views.financial_year_debt, name="financial_year_debt"),
    path('Semester-full-payment-list/', views.semester_complete_payment_list, name="semester_complete_payment_list"),
    path('fee-payment-item-list/', views.fee_payment_item, name="fee_payment_item"),

    # VIEWS FOR STUDENT
    path('student-semester-courses', views.student_semester_course, name="student_semester_course"),
    path('student-semester-payment-history', views.student_semester_payment, name="student_semester_payment"),
    path('student-semester-exam-result', views.student_semester_result, name="student_semester_result"),
    path('student-payment-structure', views.student_programme_payment_structure, name="student_programme_payment_structure"),

    # Views for Registration
    path('student-entry/', views.student_entry_list, name="student_entry_list"),
    path('upload-student-entry/', views.upload_student_entry, name="upload_student_entry"),
    path('-student-entry-template/', views.student_entry_template, name="student_entry_template"),
    path('registration-home-page/', views.start_registration, name="registration_home"),
    path('registration-phase-one/<username>', views.register_phase_one, name="register_phase_one"),
    path('registration-phase-one-save-payments/', views.save_student_payments, name="save_student_payments"),
    path('registration-phase-two/', views.registration_phase_two, name="registration_phase_two"),
    path('save-student-registration/<student>', views.complete_student_registration, name="complete_registration"),
    # VIEWS FOR ACADEMIC

    path('teaching-Workload-list/', views.workload_setting, name="workload_setting"),
    path('course-assessment-group/', views.course_assessment_group, name="course_assessment_group"),
    path('course-assessment-structure/', views.course_list, name="course_list"),
    path('department-tutors-list/', views.department_tutor_list, name="department_tutor_list"),
    path('department-semester-registered-student/', views.department_semester_student_list,
         name="department_semester_student_list"),

    path('programme-available/', views.programme_available, name="programme_available"),
    path('programme-course-structure/<programme_name>/<level_name>/', views.programme_course_structure,
         name="programme_course_structure"),
    # VIEWS FOR ASSESSMENT
    path('tutor-course-assessment/', views.tutor_course, name="tutor_course"),
    path('tutor-course-assessment-group-list/<assessment>', views.tutor_course_assessment,
         name="tutor_course_assessment"),
    path('tutor-course-assessment-group-result/<assessment>/<course>', views.course_assessment_result,
         name="course_assessment_result"),
    path('download-course-semester-assessment/<assessment>/<course>', views.download_course_assessment_excel,
         name="download_course_assessment_excel"),
    path('download-course-semester-result/<course>', views.download_course_result_excel,
         name="download_course_result_excel"),
    path('student-course-assessment-template/<assessment>/<course>', views.student_course_assessment_template,
         name="student_course_assessment_template"),
    path('delete-student-course-assessment-result/<assessment>/<course>', views.delete_course_assessment_result_data,
         name="delete_course_assessment_result_data"),
    path('upload-student-course-assessment-result/<assessment>/<course>', views.upload_course_assessment,
         name="upload_course_assessment"),
    path('pie-chart/', views.pie_chart, name="pie_chart"),
    # path('subject-list/', views.subject_list, name="subject"),
    # path('student-academic-year/', views.student_academic_year, name="student_academic_year"),
    # path('Combination-Subjects-list/', views.combination_subject_list, name="combination_subject_list"),
    #
    # path('classes-combination-coordinator_results/<rank>', views.coordinator_classes_combination_results,
    #      name="coordinator_classes_combination_results"),
    #
    # path('academic-event/', views.academic_events, name="academic_event"),
    # path('academic-year_result/<rank>/<combination>', views.event_result, name="event_result"),
    #
    # path('send-academic-year_result/<rank>/<combination>', views.send_event_result, name="send_event_result"),
    # path('send-Form3-4-academic-year_result/<rank>/<combination>', views.send_event_result_f3_f4,
    #      name="send_event_result_f3_f4"),
    # path('download-template/<subject>/<rank>/', views.download_csv_data, name="download_csv_data"),
    #
    #
    # path('coordinator-classes_results/', views.coordinator_classes_results, name="coordinator_classes_results"),
    #
    # path('class-results-pdf/<rank>/<combination>', views.download_result, name="download_result"),
    # path('parent-download-results-pdf/<rank>/<combination>', views.parent_download_result,
    #      name="parent_download_result"),
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # # URL FOR REGISTRATION PROCESS
    # path('fee-payment-structure/', views.payment_structure_list, name="payment_structure_list"),
    # path('school-payment-items/', views.payment_items_list, name="payment_items_list"),
    # path('financial-year-income/', views.financial_year_income, name="financial_year_income"),
    # path('financial-year-incomplete-payment/', views.financial_year_debt, name="financial_year_debt"),
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # path('teacher-Subject-list/', views.subject_teacher, name="subject_teacher"),
    # path('class-coordinator-list/', views.class_coordinator_list, name="class_coordinator_list"),
    # path('subject-result-lists/<rank>/<subject_name>', views.subject_results_list, name="subject_results_list"),
    #
    #
    #
    #
    #
    #
    #
    # path('available-Schools-list/', views.available_school, name="available_school"),
    # path('teaching-Workload-list/', views.workload_setting, name="workload_setting"),
    #
    #
    #
    # path('download-selected-student-list/', views.download_admitted_student, name="download_admitted_student"),
    # path('registration-home-page/', views.start_registration, name="registration_home"),
    # path('registration-phase-one/<entry>', views.register_phase_one, name="start_registration"),
    # path('registration-phase-one-save-payments/', views.save_student_payments, name="save_student_payments"),
    # path('registration-phase-two/<student>', views.complete_student_registration, name="complete_registration"),
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # path('rank-event-results/', views.rank_event_results, name="rank_event_results"),
    # path('student-registration-Template/', views.download_csv_template, name="download_csv_template"),
    # path('combination-subject-assessment/<rank>/<combination>', views.combination_subjects,
    #      name="combination_subjects"),
    # path('Academic-event-subject-upload/<get__subject>/<rank>', views.subject_result_upload,
    #      name="subject_result_upload"),
    #
    # path('event-subject-result/<rank>/<subject>/<combination>', views.subject_result, name="subject_results"),
    #
    # path('download-subject-result-data/<subject>/<rank>/', views.download_subject_result_data,
    #      name="download_subject_result_data"),
    # path('delete-subject-result-data/<subject>/<rank>/', views.delete_subject_result_data,
    #      name="delete_subject_result_data"),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # autocomplete views
    # path('district-auto-complete/', DistrictAutocomplete.as_view(), name='district_autocomplete'),
    path('password_reset/', auth_views.PasswordResetView.
         as_view(template_name='password/password_reset.html'), name='password_reset'),

]

'''
    Password view For reseting password
------------------------------------------
1 - PasswordResetView submit email from user
2 - PasswordResetDoneView email sent successfull
3 - link to password Rest form in email
4 - Password successfully changed
'''
