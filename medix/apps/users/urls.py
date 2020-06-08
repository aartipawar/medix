from django.urls import path
from users import views
from .ajax import * 

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),

    #user dashboard
    path('edit/profile/<int:pk>',views.PracticeUpdateView.as_view(), name='edit-practice'),
    path('dashboard/institution/<int:pk>',views.InstitutionDashboardView.as_view(), name='institution-dashboard'),
    path('dashboard/emergency-service/<int:pk>',views.EmergencyServicesDashboard.as_view(), name='emergency-service-dashboard'),
    path('dashboard/health-insurance/<int:pk>',views.HealthInsuranceDashboard.as_view(), name='health-insurance-dashboard'),
    path('location/update/<int:pk>',views.LocationUpdateView.as_view(), name='location-update'),

    #admin dashboard
    path('admin/dashboard/',views.AdminDashboardView.as_view(), name='admin-dashboard'),

    path('logout/',views.LogoutView.as_view(), name='users-logout'),
    # path('user/login/',views.LoginView.as_view(), name='users-login'),


    #signup step first
    path('user-type/step1/',views.UserTypeStep1View.as_view(), name='registration-step1'),
   
    
    #signup step third
    path('practice/signup/step3/<int:pk>',views.PracticeSignupStep3View.as_view(), name='practice-signup'),
    path('emergency-service/signup/step3/<int:pk>',views.EmergencyServiceSignupStep3View.as_view(), name='emergency-service-signup'),
    path('institution/signup/step3/<int:pk>',views.InstitutionSignupStep3View.as_view(), name='institution-signup'),
    
    #signup step second
    path('emergency-services/step2/',views.EmergencyServiceStep2CreateView.as_view(), name='select-emergency-service'),
    path('patient/signup/step2/',views.PatientSignupStep2View.as_view(), name='patient-signup'),
    path('insurance/signup/step2/',views.InsuranceProviderSignupStep2View.as_view(), name='insurance-provider-signup'),
    path('practice/step2/',views.PracticeStep2CreateView.as_view(), name='select-specialisation'),
    path('institution/step2/',views.InstitutionStep2CreateView.as_view(), name='institution-step2'),


    # path('practice/step1/',views.PracticeStep1CreateView.as_view(), name='practice-step1'),
    path('form/submit/',views.UserFormSubmitView.as_view(), name='form-submit'),

    
    path('create/overview/<int:pk>',views.ProfessionalOverviewUpdate.as_view(), name='professional-overview'),

    path('profile/detail/<int:pk>',views.PracticeInfoDetailView.as_view(), name='profile-information'),
    path('professional/detail/<int:pk>',views.ProfessionalOverviewDetail.as_view(), name='professional-detail'),
    
    # path('create/product/<int:pk>',views.ProductCreateView.as_view(), name='create-product'),
    
    # path('price/detail/<int:pk>',views.PriceDetail.as_view(), name='price-detail'),

    path('create/education/',views.EducationCreateView.as_view(), name='create-education'),
    
    path('education/detail/<int:pk>',views.EducationDetailView.as_view(), name='education-detail'),

    path('dashboard/practice/<int:pk>',views.PracticeProfileDetailView.as_view(), name='profile-dashboard'),

    path('file/upload/<int:pk>',views.file_upload, name='file-upload'),
    #-------home-----about
    #---see all specilization
    path('specialization/',views.Specialisation.as_view(), name='all-specialization'),
    path('find-by-specialization/list/',views.SpecialisationListView.as_view(), name='find-by-specialization'),
    
    path('profile-detail/<int:pk>/',views.ProfileDetail.as_view(), name='book'),

    path('home/',views.Home.as_view(), name='home-1'),
    path('about/',views.About_us.as_view(), name='about-1'),
    path('blog/',views.Blog.as_view(), name='blog-1'),
    path('blog-post/',views.BlogPost.as_view(), name='blog-post'),
    path('faq/',views.Faq.as_view(), name='faq-1'),
    path('search-keyword/', search_keyword, name='search-keyword'),
    path('institution-detail/<int:pk>/', views.InstitutionDetailView.as_view(), name='search-institution'),
    path('add/location', views.add_location, name='add-location'),  
]

ajaxpatterns = [
    #practice add ,edit ,delete ajax
   
    path('edit/location', edit_location, name='edit-location'),
    path('delete/location', delete_location, name='delete-location'),
    path('edit/profile/', edit_profile, name='edit-profile'),
    path('add/statement', add_statement, name='add-statement'),
    path('add/education', add_education, name='add-education'),
    path('add/product', add_product, name='add-product'),
    path('edit/education', edit_education, name='edit-education'),
    path('edit/product', edit_product, name='edit-product'),
    path('add/keyword', add_keyword, name='add-keyword'),
    path('delete/education', delete_education, name='qualification-delete'),
    path('delete/product', delete_product, name='product-delete'),
     
    #Health Insurance add, edit, delete ajax
    path('edit/insurance-profile', edit_insurance_profile, name='edit-insurance-profile'),
    path('add/insurance-overview', add_insurance_overview , name='add-insurance-overview'),
    path('add/insurance-product', add_insurance_product , name='add-insurance-product'),
    path('delete/insurance-product', insurance_product_delete , name='insurance-product-delete'),
    path('edit/insurance-product', edit_insurance_product, name='insurance-product'),
    # path('add/insurance-keyword', add_insurance_keyword, name='add-insurance-keyword'),
    path('delete/keyword', delete_keyword ,name='delete-keyword'),
    path('delete/description', delete_description ,name='delete-description'),
    path('delete/experience', delete_experience,name='delete-experience'),

    
    path('add/ambulance-info', add_ambulance_info,name='add-ambulance-info'),
    path('delete/ambulance-info', ambulance_info_delete,name='ambulance-info-delete'),

    path('edit/ambulance-info', edit_ambulance_info, name='edit-ambulance-info'),
    
    #login urls
    
    path('prctice/login', practice_login, name='prctice-login'),
    path('institution/login/', institution_login, name='institution-login'),
    path('service/login/', service_login, name='service-login'),
    path('insurance/login/', insurance_login, name='insurance-login'),
    path('patient/login/', patient_login, name='patient-login'),
    
    path('edit/location/hour', edit_location_hour, name='edit-location-hour'),

    # search-keyword
    path('search-keyword/', search_keyword, name='search-keyword'),
    path('institution/list/', service_request, name='service-request'),
    path('requested/user/', requested_user, name='requested-user'),
    path('send/email/', price_request_mail, name='send-email'),
    path('send/sms/', send_url_sms, name='send_sms'),
    path('upload/image/', views.upload_user_image, name='upload-user-image')
    
   
]    

urlpatterns = urlpatterns + ajaxpatterns