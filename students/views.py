from typing import Any, Dict
from django import http
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, DetailView, ListView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import Certificate
from django.db.models import Q
import numpy as np
from django.shortcuts import render
from django.utils import timezone as tz
import json


# Create your views here.
class setUp(LoginRequiredMixin, View):
    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        self.student = Student.objects.get(user=request.user)
        self.current_sem = Semester.objects.get(student=self.student, category="C")
        self.sems = Semester.objects.filter(student=self.student)

        # setting up the grades and credits in Semester model
        for sem in self.sems:
            subs = StudentSubjects.objects.filter(semester_number=sem)
            credits = [sub.subjectID.credits for sub in subs]
            sem.gpa = 0
            sem.credits = sum(credits)
            if subs:
                grades = [
                    sub.grade_point if sub.grade_point is not None else 0
                    for sub in subs
                ]
                gpa = np.average(grades, weights=credits)
                sem.gpa = gpa
            sem.save()

        # setting up the attendance in Attendance model
        subs = StudentSubjects.objects.filter(studentID=self.student)
        for sub in subs:
            att = []
            classes = Sessions.objects.filter(subject=sub)
            if classes:
                att = [int(day.attendance) for day in classes]
            sub.agg_attendance = 0 or np.average(att) * 100
            sub.save()

        return super().setup(request, *args, **kwargs)


class AddressView(setUp, DetailView):
    template_name = "address.html"

    def get_object(self, *args, **kwargs):
        address = Address.objects.get(student_ID=self.student)
        return address


class AnnouncementPageView(setUp, ListView):
    model = Announcement
    template_name = "announcements.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Announcement.objects.filter(dept_ref=self.student.department)


class ApplicationPageView(setUp, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["not_valid"] = False
        context["duplicate"] = False

        current_sem = Semester.objects.filter(student=self.student, semester_number=2)
        duplicate = Applications.objects.filter(
            student=self.student, name="Branch Change"
        )
        if current_sem.exists() and current_sem[0].category == "C":
            if duplicate.exists():
                context["duplicate"] = True
            else:
                context["department"] = Department.objects.exclude(
                    department_name=self.student.department
                )
        else:
            context["not_valid"] = True

        return render(request, "application.html", context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST["branch_name"]

        application = {}

        application["submitted_at"] = str(tz.now())  # not JSON serializable
        application["current_branch_name"] = str(self.student.department)
        application["requested_branch_name"] = data
        json_app = json.dumps(application, indent=3)

        app = Applications(
            student=self.student,
            date=tz.now(),
            name="Branch Change",
            status="R",
            file=json_app,
        )
        app.save()
        context = {}
        toast = {
            "title": "Your Application is submitted",
            "line_one": "The status of your application can be viewed in the Application Status.",
            "time": "0 mins ago",
        }
        context["object_list"] = Events.objects.all()
        context["toast"] = toast

        return render(request, "home.html", context)


class ApplicationStatusView(setUp, ListView):
    model = Applications
    template_name = "status.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["applications"] = Applications.objects.filter(student=self.student)
        return context


class AttendanceDetails(setUp, TemplateView):
    template_name = "attendance.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["semesters"] = self.sems

        sem_input = self.request.GET.get("semester") or ""

        if sem_input:
            sem = Semester.objects.get(
                Q(student=self.student), Q(semester_number=sem_input)
            )
            subs = StudentSubjects.objects.filter(semester_number=sem)
            context["subjects"] = subs
        context["input"] = sem_input
        return context


class CertView(setUp, FormView):
    form_class = Certificate
    template_name = "certs.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # student = Student.objects.get(user=self.request.user)
        context["phone"] = self.student.phone_number
        context["email"] = self.student.email
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        student = Student.objects.get(user=self.request.user)
        json_app = json.dumps(form.cleaned_data, indent=3)
        app = Applications(
            student=student,
            date=tz.now(),
            name="Application for Certificate",
            status="R",
            file=json_app,
        )
        app.save()
        context = {}
        toast = {
            "title": "Your Application for Certificate is complete",
            "line_one": "Stay posted for the updates regarding this application through Application Status.",
            "time": "0 mins ago",
        }
        context["object_list"] = Events.objects.all()
        context["toast"] = toast
        # return super().form_valid(form)
        return render(self.request, "home.html", context)


class CourseDetails(setUp, TemplateView):
    template_name = "course_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["semesters"] = self.sems

        sem_input = self.request.GET.get("semester") or ""

        if sem_input:
            sem = Semester.objects.get(
                Q(student=self.student), Q(semester_number=sem_input)
            )
            context["course"] = StudentSubjects.objects.filter(semester_number=sem)
        context["input"] = sem_input
        return context


class EnrolmentDetails(setUp, TemplateView):
    template_name = "academics.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(EnrolmentDetails, self).get_context_data(**kwargs)
        context[
            "name"
        ] = f"{self.student.user.first_name} {self.student.user.last_name}"
        context["regiration_number"] = self.student.registration_number
        context["enrolment_number"] = self.student.enrolment_number
        context["year_of_joining"] = self.student.year_of_joining
        context["year_of_graduation"] = self.student.year_of_graduation
        context["current_year"] = self.student.current_year
        context["current_semester"] = self.current_sem.semester_number
        context["department_name"] = self.student.department.department_name

        return context


class FeePaymentView(setUp, TemplateView):
    template_name = "pay_fees.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["not_valid"] = False
        # student = Student.objects.get(user=self.request.user)
        # semesters = Semester.objects.filter(student=student)
        flag = 0
        for fee in self.sems:
            if not fee.fees_paid:
                flag = 1
        if flag:
            context["not_valid"] = False
            sem = Semester.objects.get(Q(student=self.student), Q(category="C"))
            context["sem"] = sem.semester_number
        else:
            context["not_valid"] = True
        return context


class FinanceView(setUp, ListView):
    model = Semester
    template_name = "finances.html"
    context_object_name = "finances"

    def get_queryset(self) -> QuerySet[Any]:
        student = Semester.objects.filter(student=self.student)
        return student


class GradesheetDetails(setUp, ListView):
    model = StudentSubjects
    template_name = "gradesheet.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # student = Student.objects.get(user=self.request.user)
        # sems = Semester.objects.filter(student=student)
        context["semesters"] = self.sems
        context["nonee"] = False
        sem_input = self.request.GET.get("semester") or ""
        gpas = [sem.gpa for sem in self.sems]
        credits = [sem.credits for sem in self.sems]
        context["cgpa"] = round(np.average(gpas, weights=credits), 2)
        if sem_input:
            sem = Semester.objects.get(
                Q(student=self.student), Q(semester_number=sem_input)
            )
            subs = StudentSubjects.objects.filter(semester_number=sem)
            context["nonee"] = False
            if subs:
                context["grades"] = subs
                context["gpa"] = sem.gpa
            else:
                context["nonee"] = True
        context["input"] = sem_input
        return context


class HomePageView(LoginRequiredMixin, ListView):
    model = Events
    template_name = "home.html"


class InternalDetails(setUp, TemplateView):
    template_name = "marks.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # student = Student.objects.get(user=self.request.user)
        # sems = Semester.objects.filter(student=self.student)
        context["semesters"] = self.sems
        sem_input = self.request.GET.get("semester") or ""

        if sem_input:
            sem = Semester.objects.get(
                Q(student=self.student), Q(semester_number=sem_input)
            )
            subs = StudentSubjects.objects.filter(semester_number=sem)
            # context["subjects"] = subs
            exams = {}
            for sub in subs:
                name = f"{sub.subjectID.department_ID.department_name}{sub.subjectID.subjectID} {sub.subjectID.name}"
                exams[name] = Exams.objects.filter(subject=sub).values()
            context["exams"] = exams
        context["input"] = sem_input
        return context


class ParentView(setUp, DetailView):
    model = ParentDetails
    template_name = "parents.html"

    def get_object(self, *args, **kwargs):
        parents = ParentDetails.objects.get(ward_ID=self.student)
        return parents


class ProfileView(setUp, DetailView):
    model = Student
    template_name = "admission_profile.html"

    def get_object(self, *args, **kwargs):
        return self.student


class RedoExamView(setUp, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["not_valid"] = False
        context["duplicate"] = False
        # student = Student.objects.get(user=self.request.user)
        # current_sem = Semester.objects.get(student=student, category="C")
        current_subs = StudentSubjects.objects.filter(semester_number=self.current_sem)
        failed_subs = [
            sub.subjectID.name for sub in current_subs if sub.grade_point == 0
        ]
        duplicate = Applications.objects.filter(
            student=self.student, name="Re-registration of Exam"
        )
        details = {}
        flag = 0
        if duplicate.exists():
            for sub in duplicate:
                details = json.loads(sub.file)
            if set(details["subject_of_reexam"]) == set(failed_subs):
                flag = 1

        if len(failed_subs):
            if flag:
                context["duplicate"] = True
            else:
                context["subjects"] = failed_subs
        else:
            context["not_valid"] = True

        return render(request, "redo_exam.html", context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.getlist("redo_exam")

        application = {}
        # student = Student.objects.get(user=self.request.user)
        application["submitted_at"] = str(tz.now())  # not JSON serializable
        # sem = Semester.objects.get(student=student, category="C")
        application["semester"] = self.current_sem.semester_number
        application["subject_of_reexam"] = data
        json_app = json.dumps(application, indent=3)

        app = Applications(
            student=self.student,
            date=tz.now(),
            name="Re-registration of Exam",
            status="R",
            file=json_app,
        )
        app.save()
        context = {}
        toast = {
            "title": "Your Registraion is complete",
            "line_one": "Stay posted for the updates regarding this registration through Application Status.",
            "time": "0 mins ago",
        }
        context["object_list"] = Events.objects.all()
        context["toast"] = toast

        return render(request, "home.html", context)


class RedoSubjectView(setUp, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["not_valid"] = False
        context["duplicate"] = False

        # failed subjects before the current semester
        current_subs = StudentSubjects.objects.exclude(semester_number=self.current_sem)
        failed_subs = [
            sub.subjectID.name
            for sub in current_subs
            if (sub.grade_point == 0)
            or (sub.agg_attendance == None)
            or (sub.agg_attendance < 75)
        ]
        duplicate = Applications.objects.filter(
            student=self.student, name="Re-registration of Subject"
        )
        details = {}
        flag = 0
        if duplicate.exists():
            for sub in duplicate:
                details = json.loads(sub.file)

            if set(details["subject_of_reapply"]) == set(failed_subs):
                flag = 1

        if len(failed_subs):
            if flag:
                context["duplicate"] = True
            else:
                context["subjects"] = failed_subs
        else:
            context["not_valid"] = True

        return render(request, "redo_sub.html", context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.getlist("redo_sub")
        # sem = Semester.objects.get(student=student, category="C")
        # for name in data:
        #     sub = Subject.objects.get(name = name)
        #     applied_sub = StudentSubjects.objects.get(studentID=student, subjectID = sub)
        #     applied_sub['category'] = 'R'
        application = {}
        application["submitted_at"] = str(tz.now())  # not JSON serializable
        # application["semester"] = sem.semester_number
        application["subject_of_reapply"] = data
        json_app = json.dumps(application, indent=3)

        #################################
        app = Applications(
            student=self.student,
            date=tz.now(),
            name="Re-registration of Subject",
            status="R",
            file=json_app,
        )
        app.save()
        ################################
        context = {}
        toast = {
            "title": "Your Registraion is complete",
            "line_one": "Stay posted for the updates regarding this registration through Application Status.",
            "time": "0 mins ago",
        }
        context["object_list"] = Events.objects.all()
        context["toast"] = toast

        return render(request, "home.html", context)
