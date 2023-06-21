from django import forms
from django.core import validators, exceptions
from django.utils.translation import gettext_lazy


def num_validator(value):
    if len(str(value)) != 10:
        raise exceptions.ValidationError(
            gettext_lazy(
                "Mobile Number must be a 10 digit number. Please enter a valid mobile number!"
            ),
            params={"value": value},
        )


class Certificate(forms.Form):
    categories = [
        ("Bonafide Certificate", "Bonafide Certificate"),
        ("Course Completion Certificate", "Course Completion Certificate"),
        ("Custody Certificate", "Custody Certificate"),
        ("Duplicate Degree Certificate", "Duplicate Degree Certificate"),
        ("Duplicate Grade Sheet", "Duplicate Grade Sheet"),
        ("Duplicate Identity Card", "Duplicate Identity Card"),
        ("Migration Certificate", "Migration Certificate"),
        ("No Objection Certificate", "No Objection Certificate"),
        ("Official Transcript", "Official Transcript"),
        ("Provisional Pass Certificate", "Provisional Pass Certificate"),
        ("Rank Certificate", "Rank Certificate"),
    ]
    purposes = [
        ("Applying for Passport", "Applying for Passport"),
        ("Applying for Higher Studies", "Applying for Higher Studies"),
        ("Applying for Internship", "Applying for Internship"),
        ("Applying for VISA", "Applying for VISA"),
        ("Applying for Conference", "Applying for Conference"),
    ]
    application_category = forms.ChoiceField(
        label="Application Category",
        choices=categories,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    purpose = forms.ChoiceField(
        choices=purposes, widget=forms.Select(attrs={"class": "form-select"})
    )
    mode_of_delivery = forms.ChoiceField(
        label="Mode of Delivery",
        choices=[("In Person", "In Person"), ("Courier", "Courier")],
        widget=forms.Select(attrs={"class": "form-select", "onchange": "amountSet()"}),
    )

    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "readonly": "readonly",
                "disabled": "disabled",
            }
        )
    )

    mobile_check = forms.BooleanField(
        label="Same as the registered number?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "onclick": "mobileSet()"}
        ),
    )
    mobile = forms.IntegerField(
        validators=[num_validator],
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    email_check = forms.BooleanField(
        label="Same as the registered email?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "onclick": "emailSet()"}
        ),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
