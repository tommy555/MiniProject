"""
    data form
"""
from django import forms
from .models import JobType, JobCategory


# Create your forms here.

class CompanyRegisterForm(forms.Form):
    """ Company data forms """
    email = forms.CharField()
    username = forms.CharField()
    company_reg = forms.CharField()
    company_type = forms.ModelChoiceField(queryset=JobCategory.objects.all(), empty_label=None)
    contact = forms.CharField()
    state = forms.CharField(required=False)
    country = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()
    spoken_lang = forms.CharField(required=False)
    website = forms.CharField(required=False)
    img = forms.ImageField(required=False)

class UserRegisterForm(forms.Form):
    """ User data forms """
    email = forms.CharField()
    username = forms.CharField()
    nric = forms.CharField()
    skills = forms.CharField()
    contact = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

class CompanyUpdateForm(forms.Form):
    """ Company data forms """
    username = forms.CharField()
    company_type = forms.ModelChoiceField(queryset=JobCategory.objects.all(), empty_label=None)
    contact = forms.CharField()
    state = forms.CharField(required=False)
    country = forms.CharField()
    spoken_lang = forms.CharField(required=False)
    website = forms.CharField(required=False)
    desc = forms.CharField(required=False)
    img = forms.ImageField(required=False)

class UserUpdateForm(forms.Form):
    """ User data forms """
    username = forms.CharField()
    skills = forms.CharField()
    contact = forms.CharField()
    bio = forms.CharField(required=False)

class LoginForm(forms.Form):
    """ login data form """
    login_email = forms.CharField()
    login_password = forms.CharField()

class PostJobForm(forms.Form):
    """ post job data form """
    name = forms.CharField()
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), empty_label=None)
    skill_required = forms.CharField(required=False)
    desc = forms.CharField(required=False)
    salary = forms.FloatField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()

class SearchJobByKeywordForm(forms.Form):
    """ search job by keyword data form """
    search_keyword = forms.CharField(required=False)

class AdvancedSearchForm(forms.Form):
    """ advanced search data form """
    country = forms.CharField(required=False)
    state = forms.CharField(required=False)
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), empty_label=None)
    start_time = forms.TimeField(required=False)
    end_time = forms.TimeField(required=False)
    min_salary = forms.FloatField(required=False)
    max_salary = forms.FloatField(required=False)

class PasswordUpdateForm(forms.Form):
    """ update passwor data form """
    user_type = forms.CharField(required=False)
    user_id = forms.CharField(required=False)
    newPassword1 = forms.CharField()
    newPassword2 = forms.CharField()

class RetrievePasswordForm(forms.Form):
    """ retrieve password data form """
    email = forms.CharField()
    