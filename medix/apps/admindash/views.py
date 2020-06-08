from django.views import View
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, ListView, DetailView
from users.models import Profile, Education, Product, OperatingHours, Location, AmbulanceService, Keywords, Attachment, ServiceRequest
#from users.models import Profile
from .forms import CustomAuthForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


def stafflogin(request):
    if request.method == 'POST':
        form = CustomAuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('/myadmin/dashboard/')
            else:
                messages.error(request, 'You are not authorized!')
    else:
        form = CustomAuthForm()
    return render(request, 'admin/staff_login.html', {'form': form})


def stafflogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged out!')
    form = CustomAuthForm()
    return redirect("/myadmin/stafflogin/", {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class MyAdminDashboard(View):
    def get(self, request, *args, **kwargs):
        pateint     = Profile.objects.filter(custom_role__contains=0).count()
        practice    = Profile.objects.filter(custom_role__contains=1).count()
        institution = Profile.objects.filter(custom_role__contains=2).count()
        e_services  = Profile.objects.filter(custom_role__contains=3).count()
        h_providers = Profile.objects.filter(custom_role__contains=4).count()
        data = {
            "pateint"    : pateint,
            "practice"   : practice,
            "institution": institution,
            "e_services" : e_services,
            "h_providers": h_providers
        }
        return render(request, 'admin/staff_dashboard.html', data)


@method_decorator(staff_member_required, name='dispatch')
class AccountManagementView(View):
    def get(self, request, *args, **kwargs):
        account = Profile.objects.all().order_by('-modified_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(account, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/account_management.html',data)


@method_decorator(staff_member_required, name='dispatch')
class PatientListingView(View):
    def get(self, request, *args, **kwargs):
        institution    = Profile.objects.filter(custom_role__contains=0).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(institution, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/patient_listing.html',data)


@method_decorator(staff_member_required, name='dispatch')
class PracticeListingView(View):
    def get(self, request, *args, **kwargs):

        practice    = Profile.objects.filter(custom_role__contains=1).order_by('-modified_at')
        
        page = request.GET.get('page', 1)
        paginator = Paginator(practice, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/practice_listing.html',data)


@method_decorator(staff_member_required, name='dispatch')
class InstitutionListingView(View):
    def get(self, request, *args, **kwargs):
        institution    = Profile.objects.filter(custom_role__contains=2).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(institution, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/institution_listing.html',data)


@method_decorator(staff_member_required, name='dispatch')
class EmergencyListingView(View):
    def get(self, request, *args, **kwargs):
        emergency    = Profile.objects.filter(custom_role__contains=3).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(emergency, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/emergency_listing.html',data)


@method_decorator(staff_member_required, name='dispatch')
class InsuranceProvidersListingView(View):
    def get(self, request, *args, **kwargs):
        insurance = Profile.objects.filter(custom_role__contains=4).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(insurance, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/insurance_listing.html',data)


def activate_user_ajax(request):
    try:
        profile_id = request.POST.get("profile_id")
        profile    = Profile.objects.get(pk=profile_id)
        user       = profile.user
        action_is  = request.POST.get("action_is") #activate/deactivate/pending

        if action_is == "activate":
            if profile.status == 1:
                #User is already Active. Raise Exception
                raise Exception("This Profile is already ACTIVE!!!")
            else:
                profile.status = 1
                profile.save()
                user.is_active = True
                user.save()
            res = {'status'  : 200,'message' : "Successfully Activated"}
        elif action_is == "pending":
            # For action_is = pending
            if profile.status == 0:
                #User is already in Pending Status. Raise Exception
                raise Exception("This Profile is already in PENDING!!!")
            else:
                profile.status = 0
                profile.save()
                user.is_active = False
                user.save()
                res = {'status'  : 200,'message' : "Changed to Pending!!"}
        else:
            # For action_is = deactivate
            if profile.status == 2:
                #User is already Deactive. Raise Exception
                raise Exception("This Profile is already DEACTIVATE!!!")
            else:
                profile.status = 2
                profile.save()
                user.is_active = False
                user.save()
                res = {'status'  : 200,'message' : "Successfully Deactivated!!!"}
        return JsonResponse(res)
    except Exception as e:
        res = {'status'  : 400,'message' : str(e)}
        return JsonResponse(res)
        

@method_decorator(staff_member_required, name='dispatch')
class StatisticsView(View):
    def get(self, request, *args, **kwargs):
        profiles     = Profile.objects.all()
        active_users    = profiles.filter(status=1).count()
        pending_users   = profiles.filter(status=0).count()
        deactive_users  = profiles.filter(status=2).count()
        data = {
            "active_users"   : active_users,
            "deactive_users" : deactive_users,
            "pending_users"  : pending_users
        }
        return render(request,'admin/statistics.html', data)


@method_decorator(staff_member_required, name='dispatch')
class ActiveAccountStatusView(View):
    def get(self, request, *args, **kwargs):
        user    = Profile.objects.filter(status=1).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(user, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/active_status_listing.html',data)


@method_decorator(staff_member_required, name='dispatch')
class PendingStatusView(View):
    def get(self, request, *args, **kwargs):
        user    = Profile.objects.filter(status=0).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(user, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/pending_status.html',data)


@method_decorator(staff_member_required, name='dispatch')
class DeactiveAccountStatusView(View):
    def get(self, request, *args, **kwargs):
        user    = Profile.objects.filter(status=2).order_by('-modified_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(user, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        data = {
            'users' : users
        }
        return render(request,'admin/deactive_status_listing.html',data)


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'admin/detail-page.html'
    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['education'] = Education.objects.filter(user_id=self.object.user)
        context['product'] = Product.objects.filter(user_id=self.object.user)
        context['keywords'] = Keywords.objects.filter(user=self.object.user)
        context['opratHour'] = OperatingHours.objects.filter(location__user=self.object.user)
        return context 