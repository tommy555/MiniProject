"""MiniProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from JobPostingWebsite import views

urlpatterns = [
    path('', views.index),
    path('index/', views.redirect_index),
    path('searchJobs/', views.search_jobs),
    path('searchJobByKeyword/', views.searchjob_by_keyword),
    path('advancedSearch/', views.advanced_search),
    path('getJob/<int:j_id>/', views.get_job),
    path('searchCompany/', views.search_company),
    path('getCompany/<int:c_id>/', views.get_company),
    path('login/', views.login),
    path('loginValidation/', views.login_validation),
    path('registerUser/', views.register_user),
    path('storeUser/', views.store_user),
    path('registerCompany/', views.register_company),
    path('storeCompany/', views.store_company),
    path('retrievePassword/', views.retrieve_password),
    path('retrievalSuccess/', views.retrieval_success),
    path('changePassword/<str:email>', views.change_password),
    path('updatePassword/', views.update_password),
    path('userCenter/', views.user_center),
    path('postJobs/', views.post_job),
    path('addJob/', views.add_job),
    path('editJobPost/<int:j_id>/', views.edit_job_post),
    path('editJob/<int:j_id>/', views.edit_job_detail),
    path('applyJob/<int:j_id>/', views.apply_job),
    path('approveJob/<int:j_id>/', views.approve_job),
    path('declineJob/<int:j_id>/', views.decline_job),
    path('deleteJob/<int:j_id>/', views.delete_job),
    path('viewDeclinedJob/', views.view_declined_job),
    path('viewExpiredJob/', views.view_expired_job),
    path('viewPostedJobs/', views.view_posted_jobs),
    path('makePayment/<int:j_id>/', views.make_payment),
    path('extendJob/<int:j_id>/', views.extend_job),
    path('updateUserInfo/', views.update_user_info),
    path('updateCompanyInfo/', views.update_company_info),
    path('logout/', views.logout),
    path('admin/', admin.site.urls),
    path('contactus/', views.contact_us),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)