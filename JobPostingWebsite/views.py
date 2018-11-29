"""class"""
from django.shortcuts import render, redirect, HttpResponse
from .DataForm import UserRegisterForm, CompanyRegisterForm, LoginForm, PostJobForm, SearchJobByKeywordForm, AdvancedSearchForm, UserUpdateForm, CompanyUpdateForm, PasswordUpdateForm, RetrievePasswordForm
from .models import User, Company, Jobs, JobApplication, Admin, JobType, JobCategory, Skill
from django.core.mail import send_mail, EmailMultiAlternatives
import datetime

# Create your views here.

SESSION_KEY_USERID="user_id"
SESSION_KEY_USERNAME = "username"
SESSION_KEY_USERTYPE = "user_type"
USERTYPE_NORMAL = "Normal"
USERTYPE_COMPANY = "Company"
USERTYPE_ADMIN = "Admin"
SERVER_IP="127.0.0.1"
SERVER_PORT=":8080"
SERVER_URL="http://"+SERVER_IP+SERVER_PORT
HOST_EMAIL = "tommy04081996@gmail.com"
LAST_EXPIRATION_CHECK_DATE = datetime.datetime.now()


def index(req):
    """ return index page """
    # check for jobs expiration
    check_expiration(LAST_EXPIRATION_CHECK_DATE)

    # make decision on which page to return
    companies = Company.objects.all()
    if SESSION_KEY_USERID not in req.session:
        return render(req, "index.html", {"companies":companies})
    else:
        if req.session[SESSION_KEY_USERTYPE] == USERTYPE_NORMAL:
            return render(req, "welcome.html", {"companies":companies, "jobs":get_relevant_job(req.session[SESSION_KEY_USERID])})
        elif req.session[SESSION_KEY_USERTYPE] == USERTYPE_ADMIN:
            return render(req, "welcome.html", {"jobs":Jobs.objects.filter(is_approved=False, is_declined=False)})
        elif req.session[SESSION_KEY_USERTYPE] == USERTYPE_COMPANY:
            return render(req, "welcome.html")
           
def redirect_index(req):
    """ redirect user back to index """
    return redirect(SERVER_URL)

def user_center(req):
    """ return userCenter.html """
    user = []
    if req.session[SESSION_KEY_USERTYPE] == USERTYPE_NORMAL:
        user = User.objects.get(id=req.session[SESSION_KEY_USERID])
        return render(req, "userCenter.html", {"user":user, "skills":Skill.objects.all()})
    elif req.session[SESSION_KEY_USERTYPE] == USERTYPE_COMPANY:
        user = Company.objects.get(id=req.session[SESSION_KEY_USERID])
        return render(req, "userCenter.html", {"user":user, "company_types":JobCategory.objects.all()})

def search_jobs(req):
    """ return searchJobs.html """
    if SESSION_KEY_USERID in req.session:
        return render(req, "searchJobs.html", {
        "jobs":get_relevant_job(req.session[SESSION_KEY_USERID]),
        "job_types":JobType.objects.all()
        })
    else:
        return render(req, "searchJobs.html", {
        "jobs":Jobs.objects.filter(is_approved=True, is_expired=False),
        "job_types":JobType.objects.all()
        })

def get_job(req, j_id):
    """ return specific job detail page based on job id (j_id) """
    job_is_applied = False
    job_application = []

    job = Jobs.objects.get(id=j_id)
    if SESSION_KEY_USERTYPE in req.session:
        if req.session[SESSION_KEY_USERTYPE] != USERTYPE_COMPANY:
            job.accessed_count = job.accessed_count + 1
            job.save()
    
    company = Company.objects.get(id=job.company.id)
    if SESSION_KEY_USERID in req.session:
        if req.session[SESSION_KEY_USERTYPE] == USERTYPE_NORMAL:
            job_application = JobApplication.objects.filter(
                user=User.objects.get(id=req.session[SESSION_KEY_USERID]))

    #check if this user have already applied this job
    for e in job_application:
        if job.id == e.job.id:
            job_is_applied = True

    return render(req, "jobDetail.html", {
        "company":company,
        "job":job,
        "job_is_applied":job_is_applied
    })

def search_company(req):
    """ return searchCompany.html """
    companies = Company.objects.all()
    return render(req, "searchCompany.html", {"companies":companies})

def searchjob_by_keyword(req):
    """ search job by keyword """
    search_form = SearchJobByKeywordForm(req.POST)
    if search_form.is_valid():
        searched_list = []
        search_keyword = search_form.cleaned_data["search_keyword"].lower()
        job_list = Jobs.objects.filter(is_approved=True, is_expired=False)
        for e in job_list:
            if e.job_type.name.lower().find(search_keyword) != -1 and e.is_approved == True and e.is_expired == False:
                searched_list.append(e)
            elif e.skill_required.lower().find(search_keyword) != -1 and e.is_approved == True and e.is_expired == False:
                searched_list.append(e)
            elif e.name.lower().find(search_keyword) != -1 and e.is_approved == True and e.is_expired == False:
                searched_list.append(e)
            elif e.desc.lower().find(search_keyword) != -1 and e.is_approved == True and e.is_expired == False:
                searched_list.append(e)
        return render(req, "searchJobs.html", {
            "jobs":searched_list,
            "searched_list": True,
            "job_types":JobType.objects.all()
            })
    else:
        return HttpResponse("Search Form invalid")

def advanced_search(req):
    """ search by more detail """
    search_form = AdvancedSearchForm(req.POST)
    if search_form.is_valid():
        searched_list = []
        tmp_list = []

        country = search_form.cleaned_data["country"]
        state = search_form.cleaned_data["state"]
        job_type = search_form.cleaned_data["job_type"]
        start_time = search_form.cleaned_data["start_time"]
        end_time = search_form.cleaned_data["end_time"]
        min_salary = search_form.cleaned_data["min_salary"]
        max_salary = search_form.cleaned_data["max_salary"]

        # get job by country and state
        if country != "":
            companies = []
            if state != "":
                companies = Company.objects.filter(state=state)
            else:
                companies = Company.objects.filter(country=country)

            for c in companies:
                for j in Jobs.objects.filter(company=c, is_approved=True, is_expired=False):
                    searched_list.append(j)
        else:
            searched_list = Jobs.objects.filter(is_approved=True, is_expired=False)
        
        # get job by start and end time
        if start_time is not None:
            tmp_list.clear()
            for e in searched_list:
                if e.start_time >= start_time:
                    tmp_list.append(e)
            searched_list = tmp_list.copy()

        if end_time is not None:
            tmp_list.clear()
            for e in searched_list:
                if e.end_time <= end_time:
                    tmp_list.append(e)
            searched_list = tmp_list.copy()

        # get job by job type
        if job_type is not None and job_type.name != "-":
            tmp_list.clear()
            for e in searched_list:
                if e.job_type == job_type:
                    tmp_list.append(e)
            searched_list = tmp_list.copy()

        # get job by salary
        if min_salary is not None:
            tmp_list.clear()
            for e in searched_list:
                if e.salary >= min_salary:
                    tmp_list.append(e)
            searched_list = tmp_list.copy()

        if max_salary is not None:
            tmp_list.clear()
            for e in searched_list:
                if e.salary <= max_salary:
                    tmp_list.append(e)
            searched_list = tmp_list.copy()
        
        return render(req, "searchJobs.html", {
            "jobs":searched_list,
            "searched_list": True,
            "job_types":JobType.objects.all()
            })
    else:
        return HttpResponse("invalid form")

def get_company(req, c_id):
    """ return specific company detail page based on company id (c_id) """
    company = Company.objects.get(id=c_id)
    jobs = Jobs.objects.filter(company=c_id)

    return render(req, "companyDetail.html", {
        "company":company,
        "jobs":jobs
    })

def login(req):
    """ return login.html """
    return render(req, "login.html")

def login_validation(req):
    """ validate user info and login user """
    email_found = False
    password_matched = False
    tmp_user = []
    login_form = LoginForm(req.POST)
    if login_form.is_valid():
        login_email = login_form.cleaned_data["login_email"]
        login_password = login_form.cleaned_data["login_password"]

        # check if email is in User list
        try:
            email_found = True
            tmp_user = User.objects.get(email=login_email)
            # check if password correct
            if login_password == tmp_user.password:
                password_matched = True
        except User.DoesNotExist:
            try:
                email_found = True
                tmp_user = Company.objects.get(email=login_email)
                # check if password correct
                if login_password == tmp_user.password:
                    password_matched = True
            except Company.DoesNotExist:
                try:
                    email_found = True
                    tmp_user = Admin.objects.get(email=login_email)
                    # check if password correct
                    if login_password == tmp_user.password:
                        password_matched = True
                except Admin.DoesNotExist:
                    email_found = False
        # prompt error message if email not found or password not matched
        if not email_found or not password_matched:
            return render(req, "login.html", {
                "email_found":email_found,
                "password_matched":password_matched
            })
        # store session and redirect user to index
        else:
            req.session[SESSION_KEY_USERID] = tmp_user.id
            req.session[SESSION_KEY_USERNAME] = tmp_user.username
            req.session[SESSION_KEY_USERTYPE] = tmp_user.user_type
            return redirect(SERVER_URL)
    else:
        # prompt error if form error
        return HttpResponse("Fail to login")

def logout(req):
    """ logout user """
    req.session.flush()
    return redirect(SERVER_URL)

def register_user(req):
    """ return registerUser.html """
    return render(req, "registerUser.html", {"skills":Skill.objects.all()})

def store_user(req):
    """ store user into database """
    email_crashed = False
    nric_crashed = False
    password_matched = True

    register_form = UserRegisterForm(req.POST)
    if register_form.is_valid():
        tmp_user = User(
            email=register_form.cleaned_data["email"],
            username=register_form.cleaned_data["username"],
            nric=register_form.cleaned_data["nric"],
            skills=register_form.cleaned_data["skills"],
            contact=register_form.cleaned_data["contact"],
            password=register_form.cleaned_data["password"]
        )

        # identify data availability
        if not User.objects.filter(email=tmp_user.email) and  not Company.objects.filter(email=tmp_user.email):
            email_crashed = False
            if not User.objects.filter(nric=tmp_user.nric):
                if tmp_user.password == register_form.cleaned_data["password2"]:
                    tmp_user.save()
                    del tmp_user
                    return render(req, "registerUserSuccess.html")
                else:
                    password_matched = False
            else:
                nric_crashed = True
        else:
            email_crashed = True
        
        return render(req, "registerUser.html", {
            "password_matched":password_matched,
            "nric_crashed":nric_crashed,
            "email_crashed":email_crashed
        })
    else:
        return HttpResponse("register user not success")

def register_company(req):
    """ return registerUser.html """
    return render(req, "registerCompany.html", {"company_types":JobCategory.objects.all()})

def store_company(req):
    """ store company in db """
    email_crashed = False
    reg_crashed = False
    password_matched = True

    register_form = CompanyRegisterForm(req.POST, req.FILES)
    if register_form.is_valid():
        tmp_user = Company(
            email=register_form.cleaned_data["email"],
            username=register_form.cleaned_data["username"],
            company_reg=register_form.cleaned_data["company_reg"],
            company_type=register_form.cleaned_data["company_type"],
            contact=register_form.cleaned_data["contact"],
            state=register_form.cleaned_data["state"],
            country=register_form.cleaned_data["country"],
            password=register_form.cleaned_data["password"],
            spoken_lang=register_form.cleaned_data["spoken_lang"],
            website=register_form.cleaned_data["website"],
            img=register_form.cleaned_data["img"]
        )

        # identify data availability
        if  not User.objects.filter(email=tmp_user.email) and not Company.objects.filter(email=tmp_user.email):
            email_crashed = False
            if not Company.objects.filter(company_reg=tmp_user.company_reg):
                if tmp_user.password == register_form.cleaned_data["password2"]:
                    tmp_user.save()
                    del tmp_user
                    return render(req, "registerCompanySuccess.html")
                else:
                    password_matched = False
            else:
                reg_crashed = True
        else:
            email_crashed = True
        
        return render(req, "registerCompany.html", {
            "password_matched":password_matched,
            "reg_crashed":reg_crashed,
            "email_crashed":email_crashed,
            "company_types":JobCategory.objects.all()
        })
    else:
        return HttpResponse("register user not success")

def retrieve_password(req):
    """ return retrievePassword.html """
    return render(req, "retrievePassword.html")

def retrieval_success(req):
    """ send email to retrieve password """
    retrieve_form = RetrievePasswordForm(req.POST)
    if retrieve_form.is_valid():
        dest_email = retrieve_form.cleaned_data["email"]
        email_sub = "Password reset"
        html_content = """
        <h1>Password reset</h1>
        <p>You have request to reset your password, please kindly click the link below to reset your password</p>
        <a href="{}">Reset password</a>
        """.format("{}/changePassword/{}".format(SERVER_URL, dest_email))
        send_job_email(email_sub, html_content, dest_email, HOST_EMAIL, html_content)
        return render(req, "retrievalSuccess.html", {"email":dest_email})
    return HttpResponse("Fail")

def change_password(req, email):
    """ return changePassword.html """
    user = []
    user = User.objects.filter(email=email)
    company = Company.objects.filter(email=email)
    if user:
        return render(req, "changePassword.html", {"user":user[0]})
    elif company:
        return render(req, "changePassword.html", {"user":company[0]})
    
    return HttpResponse("cannot find email")

def update_password(req):
    """ update user password """
    update_form = PasswordUpdateForm(req.POST)
    if update_form.is_valid():
        user = []
        user_type = update_form.cleaned_data["user_type"]
        user_id = update_form.cleaned_data["user_id"]
        newPassword1 = update_form.cleaned_data["newPassword1"]
        newPassword2 = update_form.cleaned_data["newPassword2"]
        if user_type == USERTYPE_COMPANY:
            user = Company.objects.get(id=user_id)
        elif user_type == USERTYPE_NORMAL:
            user = User.objects.get(id=user_id)

        if newPassword1 == newPassword2:
            user.password = newPassword1
            user.save()
            return render(req, "updatePassword.html")
        else:
            return render(req, "updatePasswordFail.html")
    else:
        return HttpResponse("invalid")

def apply_job(req, j_id):
    """ apply the job by sending email to company """
    job_is_applied = False
    c_date = datetime.datetime.now()
    date_str = "{}, {} {} {}, {}:{} {}".format(
        c_date.strftime("%A"),
        c_date.day,
        c_date.strftime("%b"),
        c_date.year,
        c_date.strftime("%I"),
        c_date.strftime("%M"),
        c_date.strftime("%p")
        )
    job = Jobs.objects.get(id=j_id)
    user = User.objects.get(id=req.session[SESSION_KEY_USERID])
    job_application = JobApplication.objects.filter(user=user)

    #check if this user have already applied this job
    for e in job_application:
        if job.id == e.job.id:
            job_is_applied = True
    
    # if job is not applied
    if not job_is_applied:

        # email text
        email_subject = 'Job application for {} in {}'.format(job.name, job.company.username)
        text_msg_company  = """
            This is an auto generated email, please do not reply this email.
            Applied at """+date_str+""".
            You have a job application from """+user.username+""".
            <h3>Applicant's information</h3>
            Username: """+user.username+"""
            NRIC: """+user.nric+"""
            Skills: """+user.skills+"""
            Contact: """+user.contact+"""
            Email: """+user.email+"""

            Please kindly contact """+user.username+""" for further discussion.
            Sincerly,
            SideIncome
        """

        text_msg_user  = "123"
        html_msg_company = """
            This is an auto generated email, please do not reply this email.<br>
            Applied at """+date_str+""".<br>
            <h1>You have a job application from """+user.username+""".</h1><br><br>
            <h3>Applicant's information</h3>
            <p>Username: """+user.username+"""</p><br>
            <p>NRIC: """+user.nric+"""</p><br>
            <p>Skills: """+user.skills+"""</p><br>
            <p>Contact: """+user.contact+"""</p><br>
            <p>Email: """+user.email+"""</p><br>

            <p>Please kindly contact """+user.username+""" for further discussion.<br>
            Sincerly,<br>
            SideIncome<p><br><br>
        """
        html_msg_user = """
            This is an auto generated email, please do not reply this email.<br>
            Applied at {0}.<br>
            <h1>You have applied {1} offered by {2}.</h1><br><br>
            <h3>Job's information</h3>
            <p>Job: {1} </p><br>
            <p>Type: {3}</p><br>
            <p>Skills required: {4}</p><br>
            <p>Description: {5}</p><br>
            <p>Salary: RM {6}</p><br>
            <p>Company: {7}</p><br>
            <p>Company location: {11}, {12}, {13}</p><br>
            <p>Working hour: {8} - {9}</p><br>

            <p>Please kindly wait for the reply of {10}<br>
            Sincerly,<br>
            SideIncome<p><br><br>
        """.format(date_str, job.name, job.company.username, job.job_type, job.skill_required, job.desc, 
        job.salary, job.company.username, job.start_time, job.end_time, job.company.username, 
        job.company.town, job.company.state, job.company.country)

        # send email to company
        send_job_email(email_subject, text_msg_company, job.company.email, HOST_EMAIL, html_msg_company)

        # store this application to db as a history
        JobApplication(user=user, job=job).save()

        # send email to user
        send_job_email(email_subject, text_msg_user, user.email, HOST_EMAIL, html_msg_user)

        return render(req, "applySuccess.html", {"name":job.company.username})
    # if job is applied
    else:
        return render(req, "applyFail.html", {"name":job.company.username})
        
def post_job(req):
    """ allow company to post a job """
    return render(req, "postJob.html", {"job_types":JobType.objects.all(), "skills":Skill.objects.all()})

def add_job(req):
    """ add job to datatabase """
    # get company data
    c = Company.objects.get(id=req.session[SESSION_KEY_USERID])
    # get form data
    job_form = PostJobForm(req.POST)
    # if form is valid
    if job_form.is_valid():
        # create jobs object
        job = Jobs(
            name=job_form.cleaned_data["name"],
            job_type=job_form.cleaned_data["job_type"],
            skill_required=job_form.cleaned_data["skill_required"],
            desc=job_form.cleaned_data["desc"],
            salary=job_form.cleaned_data["salary"],
            company=c,
            start_time=job_form.cleaned_data["start_time"],
            end_time=job_form.cleaned_data["end_time"],
            expired_date=get_expired_date(),
            is_approved=False
        )
        job.save()
        del job
        return render(req, "jobPostSuccess.html")
    # if form is not valid
    else:
        return HttpResponse("form fail")

def edit_job_post(req, j_id):
    """ return edit job page """
    return render(req, "editJob.html", {
        "job":Jobs.objects.get(id=j_id),
        "job_types":JobType.objects.all(),
        "skills":Skill.objects.all()
        })

def edit_job_detail(req, j_id):
    """ allow company to edit the job """
    job_form = PostJobForm(req.POST)
    if job_form.is_valid():
        # update field
        job = Jobs.objects.get(id=j_id)
        job.name = job_form.cleaned_data["name"]
        job.job_type = job_form.cleaned_data["job_type"]
        job.skill_required = job_form.cleaned_data["skill_required"]
        job.desc = job_form.cleaned_data["desc"]
        job.salary = job_form.cleaned_data["salary"]
        job.start_time = job_form.cleaned_data["start_time"]
        job.end_time = job_form.cleaned_data["end_time"]
        job.is_approved = False
        job.save()
        del job
    return render(req, "jobEditSuccess.html")
        

def approve_job(req, j_id):
    """ Approve a job in db """
    admin = Admin.objects.get(id=req.session[SESSION_KEY_USERID])
    job = Jobs.objects.get(id=j_id)
    job.is_approved = True
    job.is_declined = False
    job.save()

    sub = "Your job: {} has been approved!".format(job.name)
    html = """
    <h1>Your job: {0} has been approved by admin {7}</h1>
    <h3>Approved job's information</h3>
    <p>Job: {0} </p>
    <p>Type: {1}</p>
    <p>Skills required: {2}</p>
    <p>Description: {3}</p>
    <p>Salary: RM {4}</p>
    <p>Working hour: {5} - {6}</p>

    <h3>Admin's info</h3>
    <p>Name: {7}</p>
    <p>Email: {8}</p>

    <p>If you have any inquiries, please kindly contact our admin for support</p>
    <p>Sincerely,</p>
    <p>SideIncome</p>
    """.format(
        job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
        admin.username, admin.email)
    text = """
    Your job: {0} has been approved by admin {7}
    Approved job's information
    Job: {0} <br>
    Type: {1}<br>
    Skills required: {2}
    Description: {3}
    Salary: RM {4}
    Working hour: {5} - {6}

    Admin's info
    Name: {7}
    Email: {8}

    If you have any inquiries, please kindly contact our admin for support
    Sincerely,
    SideIncome
    """.format(
        job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
        admin.username, admin.email)
    send_job_email(sub, text, job.company.email, admin.email, html)

    return redirect(SERVER_URL)

def decline_job(req, j_id):
    """ Decline a job in db """
    admin = Admin.objects.get(id=req.session[SESSION_KEY_USERID])
    job = Jobs.objects.get(id=j_id)
    job.is_declined = True
    job.save()

    sub = "Your job: {} has been declined".format(job.name)
    html = """
    <h1>Your job: {0} has been declined by admin {7}</h1>
    <h3>Declined job's information</h3>
    <p>Job: {0} </p>
    <p>Type: {1}</p>
    <p>Skills required: {2}</p>
    <p>Description: {3}</p>
    <p>Salary: RM {4}</p>
    <p>Working hour: {5} - {6}</p>

    <h3>Admin's info</h3>
    <p>Name: {7}</p>
    <p>Email: {8}</p>

    <p>If you have any inquiries, please kindly contact our admin for support</p>
    <p>Sincerely,</p>
    <p>SideIncome</p>
    """.format(
        job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
        admin.username, admin.email)
    text = """
    Your job: {0} has been declined by admin {7}
    Declined job's information
    Job: {0} <br>
    Type: {1}<br>
    Skills required: {2}
    Description: {3}
    Salary: RM {4}
    Working hour: {5} - {6}

    Admin's info
    Name: {7}
    Email: {8}

    If you have any inquiries, please kindly contact our admin for support
    Sincerely,
    SideIncome
    """.format(
        job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
        admin.username, admin.email)
    send_job_email(sub, text, job.company.email, admin.email, html)

    return redirect(SERVER_URL)

def delete_job(req, j_id):
    """ Delete a job in db """
    if req.session[SESSION_KEY_USERTYPE] == USERTYPE_ADMIN:
        admin = Admin.objects.get(id=req.session[SESSION_KEY_USERID])
    elif req.session[SESSION_KEY_USERTYPE] == USERTYPE_COMPANY:
        admin = Company.objects.get(id=req.session[SESSION_KEY_USERID])

    job = Jobs.objects.get(id=j_id)

    if req.session[SESSION_KEY_USERTYPE] == USERTYPE_ADMIN:
        sub = "Your job: {} has been deleted".format(job.name)
        html = """
        <h1>Your job: {0} has been deleted by admin {7}</h1>
        <h3>deleted job's information</h3>
        <p>Job: {0} </p>
        <p>Type: {1}</p>
        <p>Skills required: {2}</p>
        <p>Description: {3}</p>
        <p>Salary: RM {4}</p>
        <p>Working hour: {5} - {6}</p>

        <h3>Admin's info</h3>
        <p>Name: {7}</p>
        <p>Email: {8}</p>

        <p>If you have any inquiries, please kindly contact our admin for support</p>
        <p>Sincerely,</p>
        <p>SideIncome</p>
        """.format(
            job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
            admin.username, admin.email)
        text = """
        Your job: {0} has been deleted by admin {7}
        deleted job's information
        Job: {0} <br>
        Type: {1}<br>
        Skills required: {2}
        Description: {3}
        Salary: RM {4}
        Working hour: {5} - {6}

        Admin's info
        Name: {7}
        Email: {8}

        If you have any inquiries, please kindly contact our admin for support
        Sincerely,
        SideIncome
        """.format(
            job.name, job.job_type, job.skill_required, job.desc, job.salary, job.start_time, job.end_time, 
            admin.username, admin.email)
        send_job_email(sub, text, job.company.email, admin.email, html)
    
    job.delete()
    if req.session[SESSION_KEY_USERTYPE] == USERTYPE_ADMIN:
        return redirect("{}/viewExpiredJob/".format(SERVER_URL))
    elif req.session[SESSION_KEY_USERTYPE] == USERTYPE_COMPANY:
        return redirect("{}/viewPostedJobs/".format(SERVER_URL))

def view_declined_job(req):
    """ view declined job list """
    return render(req, "declinedJobsList.html", {"jobs":Jobs.objects.filter(is_declined=True)})

def view_expired_job(req):
    """ view expired job list """
    return render(req, "expiredJobList.html", {"jobs":Jobs.objects.filter(is_expired=True)})

def view_posted_jobs(req):
    """ view company posted jobs """
    company = Company.objects.get(id=req.session[SESSION_KEY_USERID])
    return render(req, "postedJobs.html", {"jobs":Jobs.objects.filter(company=company)})

def make_payment(req, j_id):
    """ make payment to extends job """
    return render(req, "confirmPayment.html", {"job":Jobs.objects.get(id=j_id)})

def extend_job(req, j_id):
    """ extend job expiration date """
    job = Jobs.objects.get(id=j_id)
    job.expire_date = get_expired_date()
    job.is_expired = False
    job.save()

    return render(req, "extendExpireSuccess.html", {"job":Jobs.objects.get(id=j_id)})

def update_user_info(req):
    """ update user information in db """
    update_form = UserUpdateForm(req.POST)
    if update_form.is_valid():
        user = User.objects.get(id=req.session[SESSION_KEY_USERID])
        user.username = update_form.cleaned_data["username"]
        user.skills = update_form.cleaned_data["skills"]
        user.contact = update_form.cleaned_data["contact"]
        user.bio = update_form.cleaned_data["bio"]
        user.save()

        return render(req, "updateInfoSuccess.html")
    else:
        return HttpResponse("form is not valid")
    pass

def update_company_info(req):
    """ update company information in db """
    update_form = CompanyUpdateForm(req.POST, req.FILES)
    if update_form.is_valid():
        user = Company.objects.get(id=req.session[SESSION_KEY_USERID])
        user.username = update_form.cleaned_data["username"]
        user.company_type = update_form.cleaned_data["company_type"]
        user.contact = update_form.cleaned_data["contact"]
        if update_form.cleaned_data["state"] != "":
            user.state = update_form.cleaned_data["state"]
        else:
            user.state = None
        user.country = update_form.cleaned_data["country"]
        user.spoken_lang = update_form.cleaned_data["spoken_lang"]
        user.website = update_form.cleaned_data["website"]
        user.desc = update_form.cleaned_data["desc"]
        if update_form.cleaned_data["img"] is not None:
            user.img = update_form.cleaned_data["img"]
        user.save()

        return render(req, "updateInfoSuccess.html")
    else:
        return HttpResponse("form is not valid")
    
"""
    extra useful fucntion
"""
def send_job_email(email_sub, email_content, dest, host, html_content):
    """ send email function """
    msg = EmailMultiAlternatives(email_sub, email_content, host, [dest])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def check_expiration(last_date):
    """ check expiration of a job """
    c_date = datetime.datetime.now()
    c_date = datetime.date(int(c_date.strftime("%Y")), int(c_date.strftime("%m")), int(c_date.strftime("%d")))
    if last_date == "":
        last_date = c_date
    if last_date != c_date:
        print("CHECKING FOR EXPIRATION DATE NOW. CURRENT DATE: {}, LAST DATE: {}".format(c_date, last_date))
        jobs = Jobs.objects.all()
        for e in jobs:
            if c_date > e.expired_date:
                e.is_expired = True
                e.save()
        last_date = c_date

def get_expired_date():
    # get expire date
    c_date = datetime.datetime.now()
    expire_date = c_date + datetime.timedelta(days=+60)

    return expire_date

def get_relevant_job(user_id):
    """ find relevant job for user """
    # find relevant job
    result = []
    user = User.objects.get(id=user_id)
    skills = user.skills.replace(" ", "")
    skills = skills.split(',')

    # search job by skill required
    for job in Jobs.objects.filter(is_approved=True, is_expired=False):
        for skill in skills:
            if job.skill_required.find(skill) != -1 and job not in result:
                result.append(job)
    return result

def contact_us(req):
    """ return contact us page """
    return render(req, "contactUs.html", {"admins":Admin.objects.all()})