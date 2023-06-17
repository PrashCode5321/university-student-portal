from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("announcements/", AnnouncementPageView.as_view(), name="announcements"),
    path("application/", ApplicationPageView.as_view(), name="application"),
    path("application/pay_fees", FeePaymentView.as_view(), name="pay_fees"),
    path("application/redo_exam", RedoExamView.as_view(), name="redo_exam"),
    path("application/redo_sub", RedoSubjectView.as_view(), name="redo_sub"),
    path("application/certs", CertView.as_view(), name="certs"),
    path("status/", ApplicationStatusView.as_view(), name="status"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/parents", ParentView.as_view(), name="parents"),
    path("profile/address", AddressView.as_view(), name="address"),
    path("academics/", EnrolmentDetails.as_view(), name="enrolment"),
    path("academics/course-details/", CourseDetails.as_view(), name="course-details"),
    path("academics/gradesheet/", GradesheetDetails.as_view(), name="gradesheet"),
    path("academics/attendance/", AttendanceDetails.as_view(), name="attendance"),
    path("academics/internals/", InternalDetails.as_view(), name="internals"),
    path("finances", FinanceView.as_view(), name="finances"),
]
