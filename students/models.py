from django.db import models
from django.core import exceptions, validators
from django.utils.translation import gettext_lazy
from uuid import uuid4
from django.conf import settings
import os


# Create your validators here.
def pincode_validator(value):
    if len(str(value)) != 6:
        raise exceptions.ValidationError(
            gettext_lazy(
                "Pin code must be a six digit number. Please enter a valid pin code!"
            ),
            params={"value": value},
        )


def phone_number_validator(value):
    if len(str(value)) != 10:
        raise exceptions.ValidationError(
            gettext_lazy(
                "Phone number must be a ten digit number. Please enter a valid phone number!"
            ),
            params={"value": value},
        )


def year_validator(value):
    if len(str(value)) != 4:
        raise exceptions.ValidationError(
            gettext_lazy(
                "Year must be a four digit number. Please enter a valid year!"
            ),
            params={"value": value},
        )


def number_validator(value):
    if len(str(value)) != 9:
        raise exceptions.ValidationError(
            gettext_lazy(
                "This number must be a nine digit number. Please enter a valid number!"
            ),
            params={"value": value},
        )


def path_and_rename(instance, filename):
    upload_to = "students"
    extension = filename.split(".")[-1]
    filename = f"{instance.registration_number}.{extension}"
    return os.path.join(upload_to, filename)


# Create your models here.
class Department(models.Model):
    departments = [
        ("MTE", "Mechatronics"),
        ("ECE", "Electronics and Communication"),
        ("CSE", "Computer Science"),
        ("MEC", "Mechanical"),
        ("MAT", "Mathematics"),
        ("EEE", "Electrical and Electronics"),
        ("IUC", "Inter University Course"),
        ("PHY", "Physics"),
        ("CHM", "Chemistry"),
        ("HUM", "Humanities"),
        ("CRA", "Coursera"),
        ("AER", "Aeronautical"),
    ]
    categories = [
        ("ENG", "Engineering"),
        ("COM", "Commerce"),
        ("ARC", "Architecture"),
        ("PHR", "Pharmacy"),
    ]
    department_ID = models.IntegerField(primary_key=True, auto_created=True)
    department_name = models.CharField(max_length=3, choices=departments)
    category = models.CharField(max_length=3, choices=categories)

    def __str__(self) -> str:
        return self.department_name


class Semester(models.Model):
    semester_number = models.IntegerField()
    gpa = models.FloatField(
        null=True,
        blank=True,
        validators=[validators.MaxValueValidator(10), validators.MinValueValidator(0)],
    )
    credits = models.IntegerField(
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(0)],
    )
    fees = models.IntegerField()
    fees_paid = models.BooleanField()
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        default="a524bd15-8983-4ae6-ba5e-624cefc45522",
    )
    category = models.CharField(
        default="C",
        max_length=1,
        choices=[("C", "Current"), ("R", "Re-Registered"), ("D", "Completed")],
    )

    def __str__(self) -> str:
        return f"{self.student.user.first_name} {self.student.registration_number} : {self.semester_number}"


class Subject(models.Model):
    subjectID = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=30)
    credits = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
    )
    department_ID = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.department_ID.department_name} : {self.name}"


class StudentSubjects(models.Model):
    studentID = models.ForeignKey("Student", on_delete=models.CASCADE)
    subjectID = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade_point = models.IntegerField(
        null=True,
        blank=True,
        validators=[validators.MaxValueValidator(10), validators.MinValueValidator(0)],
    )
    agg_attendance = models.FloatField(
        null=True,
        blank=True,
        validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)],
    )
    semester_number = models.ForeignKey(Semester, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=1,
        choices=[("C", "Current"), ("R", "Re-Registered"), ("D", "Completed")],
    )

    def __str__(self) -> str:
        return f"{self.studentID.registration_number} - {self.subjectID.name} in {self.semester_number.semester_number}"


class Sessions(models.Model):
    sessions = [("L", "Lecture"), ("T", "Tutorial"), ("P", "Practical")]
    subject = models.ForeignKey(StudentSubjects, on_delete=models.CASCADE)
    attendance = models.BooleanField()
    date = models.DateField()
    session_ID = models.IntegerField(primary_key=True)
    session_type = models.CharField(max_length=1, choices=sessions)

    def __str__(self) -> str:
        return f"{self.subject.studentID.registration_number} : {self.subject.subjectID.name}"


class Exams(models.Model):
    exams = [
        ("INT-1", "In-Semester Examination 1"),
        ("INT-2", "In-Semester Examination 2"),
        ("FISAC", "FISAC"),
        ("MISAC", "MISAC"),
        ("END", "End-Semester Examination"),
    ]
    subject = models.ForeignKey(
        StudentSubjects,
        on_delete=models.CASCADE,
        default=1,
    )
    date = models.DateField()
    max_score = models.IntegerField()
    score = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
    )
    name = models.CharField(max_length=5, choices=exams)


class Student(models.Model):
    student_ID = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student"
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=path_and_rename,
    )
    # user = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.IntegerField(
        validators=[phone_number_validator], null=True, blank=True
    )
    sex_choices = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    sex = models.CharField(choices=sex_choices, max_length=1, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrolment_number = models.IntegerField(
        validators=[number_validator], null=True, blank=True
    )
    registration_number = models.IntegerField(
        validators=[number_validator], null=True, blank=True
    )
    year_of_joining = models.IntegerField(
        validators=[year_validator], null=True, blank=True
    )
    year_of_graduation = models.IntegerField(
        validators=[year_validator], null=True, blank=True
    )
    current_year = models.IntegerField(
        validators=[year_validator], null=True, blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        id = (
            f"{self.registration_number} : {self.user.first_name} {self.user.last_name}"
        )
        return id


class ParentDetails(models.Model):
    ward_ID = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    father_name = models.CharField(max_length=50)
    father_occupation = models.CharField(max_length=50)
    father_email = models.EmailField(max_length=50)
    father_contact_no = models.IntegerField(validators=[phone_number_validator])
    mother_name = models.CharField(max_length=50)
    mother_occupation = models.CharField(max_length=50)
    mother_email = models.EmailField(max_length=50)
    mother_contact_no = models.IntegerField(validators=[phone_number_validator])

    def __str__(self) -> str:
        return f"Parents of {self.ward_ID.registration_number} : {self.ward_ID.user.first_name}"


class Address(models.Model):
    student_ID = models.OneToOneField(
        Student, on_delete=models.CASCADE, primary_key=True
    )
    permanent_address1 = models.TextField(max_length=200)
    permanent_address2 = models.TextField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    pin_code = models.IntegerField(validators=[pincode_validator])

    def __str__(self) -> str:
        return f"Address of {self.student_ID.registration_number} : {self.student_ID.user.first_name}"


class Announcement(models.Model):
    ann_ID = models.IntegerField(primary_key=True, auto_created=True)
    dept_ref = models.ForeignKey(Department, on_delete=models.CASCADE)
    ann_title = models.CharField(max_length=50)
    ann_info = models.TextField(max_length=200)


class Events(models.Model):
    event_name = models.CharField(max_length=50)
    event_details = models.CharField(max_length=200)
    event_time = models.DateTimeField()
    event_venue = models.CharField(max_length=30)


class Applications(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=[("C", "Completed"), ("P", "Processing"), ("R", "Registered")],
    )
    file = models.JSONField()

    def __str__(self) -> str:
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.student.registration_number}"


"""d = Department.objects.get(department_ID="MTE")
listt = [
    ("Hydraulics and Pneumatics", 3),
    ("Theory of Machines", 4),
    ("Drives, Controls Lab", 2),
    ("Robotics Lab 2", 2),
]
i = 25
for name in listt:
    s = Subject(subjectID=i, name=name[0], credits=name[1], department_ID=d)
    s.save()
    i = i + 1"""
