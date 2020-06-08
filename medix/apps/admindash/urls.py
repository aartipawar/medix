from admindash.views import *
from django.urls import path, include


urlpatterns = [
    # Staff Login
    path('stafflogin/', stafflogin, name='stafflogin'),
    path('logout/', stafflogout, name='stafflogout'),

    # Staff Dashboard
    path('dashboard/', MyAdminDashboard.as_view(), name='my-admin-dashboard'),
    path('account_listing/', AccountManagementView.as_view(), name='my-admin-management'),

    # Dashboard Catogories
    path('patient_listing/', PatientListingView.as_view(), name='patients-listing'),
    path('practice_listing/', PracticeListingView.as_view(), name='practice-listing'),
    path('institution_listing/', InstitutionListingView.as_view(), name='institution-listing'),
    path('emergency_listing/', EmergencyListingView.as_view(), name='emergency-listing'),
    path('insurance_provider_listing/', InsuranceProvidersListingView.as_view(), name='insurance-listing'),
    
    # Statistics Catogories
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('active_status_listing/', ActiveAccountStatusView.as_view(), name='active-status'),
    path('deactive_status_listing/', DeactiveAccountStatusView.as_view(), name='deactive-status'),
    path('pending_listing/', PendingStatusView.as_view(), name='pending'),

    # Ajax Calls
    path('activate_user/', activate_user_ajax, name='activate-user'),

    # Profile View
    path('profile/detail/<int:pk>/', ProfileDetail.as_view(), name='book'),
]