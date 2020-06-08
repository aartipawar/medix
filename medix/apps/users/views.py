from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView,  UpdateView, DeleteView, View, TemplateView
from users.models import Profile, Education, Product, OperatingHours, Location, AmbulanceService, Keywords, Attachment, ServiceRequest
from django.contrib.auth.models import User
from .forms import UserTypeForm, PracticeSignupForm, UserForm, PatientSignupForm, InstitutionSignupForm, InsuranceProviderSignupForm, EmergencyServiceSignupForm, EmergencyServiceForm,PracticeSpecialisationForm, InstitutionForm, PracticeUserForm, ProfessionalOverviewForm, ProfileInfoForm, ProfileUserForm,  EducationForm, TradingHourForm, AmbulanceForm, DocumentForm, ImageUpload, UserEditMultiForm
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from users.utils import specialization_value
from django.contrib.auth import get_user_model

location = get_user_model()

class LocationUpdateView(UpdateView):
    model = OperatingHours
    template_name = 'dashboard/update_location.html'
    
    form_class = TradingHourForm
    success_url = '/dashboard/practice/'
    
    # def get_form_kwargs(self):
    #     kwargs = super(LocationUpdateView, self).get_form_kwargs()
    #     kwargs.update(instance={
    #         'location': self.object.location,
    #         'hour': self.object.operatingHours,
    #     })
    #     return kwargs

    def form_valid(self, form, **kwargs):
        # import pdb; pdb.set_trace()
        hour = form.save(commit=False)
        hour.save()
        return redirect(self.success_url+str(request.user.profile.id))

def add_location(request):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=request.user.profile.id)
        user = profile.user
        day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        open_list = request.POST.getlist('open_time')
        close_list = request.POST.getlist('close_time')
        toggle_list = []
        try:
            toggle_list.append(request.POST.get('monTog').title()) if request.POST.get('monTog') else toggle_list.append('None')
            toggle_list.append(request.POST.get('tueTog').title()) if request.POST.get('tueTog') else toggle_list.append('None')
            toggle_list.append(request.POST.get('wedTog').title()) if request.POST.get('wedTog') else toggle_list.append('None') 
            toggle_list.append(request.POST.get('thuTog').title()) if request.POST.get('thuTog') else toggle_list.append('None') 
            toggle_list.append(request.POST.get('friTog').title()) if request.POST.get('friTog') else toggle_list.append('None')
            toggle_list.append(request.POST.get('satTog').title()) if request.POST.get('satTog') else toggle_list.append('None')
            toggle_list.append(request.POST.get('sunTog').title()) if request.POST.get('sunTog') else toggle_list.append('None')
            if request.POST.get("location")!=None and request.POST.get("location")!= '' and not Location.objects.filter(user=user,location=request.POST.get("location")).exists():       
                if request.POST.get('mobility')!=None: 
                    location_obj = Location.objects.create(user=user,location=request.POST.get("location"),mobility = True)
                else:
                    location_obj = Location.objects.create(user=user,location=request.POST.get("location"),mobility = False)
            
                for day, openl, closel, toggle in zip(day_list,open_list,close_list,toggle_list):
                    if openl=='' and closel =='':
                        OperatingHours.objects.create(location = location_obj,day = day,status = False)
                    elif openl != '' and closel=='':
                        OperatingHours.objects.create(
                            open_time = openl,
                            day = day,
                            location = location_obj,
                            status = True
                        )
                    else: 
                        OperatingHours.objects.create(
                            open_time = openl,
                            close_time = closel,
                            day = day,
                            location = location_obj,
                            status = True
                        )         
        except Exception as e:
            print("Uh oh, Error : ", str(e))
      
    if request.POST.get('practLoc') == 'practice':
        if request.POST.get("location")==None or request.POST.get("location")=='':
            messages.error(request, 'Please Fill Location')
        else:
            messages.error(request, 'Location already exists')
        return redirect('/dashboard/practice/'+str(request.user.profile.id))
    if request.POST.get('instLoc') == 'institution':
        if request.POST.get("location")==None or request.POST.get("location")=='' :
            messages.error(request, 'Please Fill Location')
        else:
            messages.error(request, 'Location already exists')
        return redirect('/dashboard/institution/'+str(request.user.profile.id))
    if request.POST.get('emergLoc') == 'emergency':
        if request.POST.get("location")==None or request.POST.get("location")=='':
            messages.error(request, 'Please Fill Location')
        else:
            messages.error(request, 'Location already exists')
        return redirect('/dashboard/emergency-service/'+str(request.user.profile.id))
    if request.POST.get('healthLoc') == 'insurance':
        if request.POST.get("location")==None or request.POST.get("location")=='':
            messages.error(request, 'Please Fill Location')
        else:
            messages.error(request, 'Location Already Exists')
        return redirect('/dashboard/health-insurance/'+str(request.user.profile.id))


def upload_user_image(request):
   
    if request.method == 'POST':
        profile = Profile.objects.get(pk=request.user.profile.id) 
        if request.POST.get('practice') == 'practice':
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
                profile.save()
            else:
                messages.error(request, 'Please select image')
            return redirect('/dashboard/practice/'+str(request.user.profile.id))
        if request.POST.get('institution') == 'institution':
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
                profile.save()
            else:
                messages.error(request, 'Please select image')
            return redirect('/dashboard/institution/'+str(request.user.profile.id))
        if request.POST.get('emergency') == 'emergency':
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
                profile.save()
            else:
                messages.error(request, 'Please select image')
            return redirect('/dashboard/emergency-service/'+str(request.user.profile.id))
        if request.POST.get('health') == 'health':
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
                profile.save()
            else:
                messages.error(request, 'Please select image')
            return redirect('/dashboard/health-insurance/'+str(request.user.profile.id))
    

def file_upload(request,pk):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=pk)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            fileForm=form.save(commit=False)
            fileForm.profile = profile
            fileForm.save()
            messages.success(request, 'Successfully uploaded')
            return redirect('/file/upload/'+str(pk))
        else:
            messages.error(request, 'Invalid')
            return redirect('/file/upload/'+str(pk))
    else:
        form = DocumentForm()
        
    return render(request, 'users/file_upload.html', {
        'form': form
    })

def index(request):
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        return redirect('home/')

class UserFormSubmitView(View):
    def get(self,request):
        messages.success(self.request, 'Successfully registered')
        return render(request,"users/form_submit.html")

class PracticeProfileDetailView(View):
    def get(self,request,pk):
        loc_list = []
        hour_list = []
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            profileInfo = Profile.objects.get(user=user)
            education = Education.objects.filter(user=user)
            product = Product.objects.filter(user=user)
            location_obj = Location.objects.filter(user=user)
            keyword = Keywords.objects.filter(user=user)
            instList = Profile.objects.filter(custom_role=2)
            serviceMember = ServiceRequest.objects.filter(service_member=user)
            for loc in location_obj:
                loc_list.append(loc)
            for val in loc_list:    
                opratHour = OperatingHours.objects.filter(location=val)
                for vals in opratHour:  
                    hour_list.append(vals)   
            
            tradHour = TradingHourForm 
            proInfo = ProfileInfoForm

            context = {'first_name':user.first_name,'last_name':user.last_name,'phone':profileInfo.phone,'description':profileInfo.description,'experience':profileInfo.experience,'educations':education,'products':product,'email':user.email,'gender':profileInfo.get_gender_display(),'keyword':keyword, 'specialisation':profileInfo.get_practice_display(), 'pk':pk, 'tradHour':tradHour, 'proInfo':proInfo,'opratHour':hour_list,'instList' : instList, 'serviceMember':serviceMember, 'image': profileInfo}
            return render(request,"users/dashboard.html", context)
        return redirect('user-type/step1/')


class UserTypeStep1View(TemplateView):
    template_name = 'users/user_type_form.html'


class PracticeStep2CreateView(CreateView):
    model = Profile
    form_class = PracticeSpecialisationForm
    template_name = 'registration/select_specialisation.html'
    success_url = '/practice/signup/step3/'
    
    def form_valid(self, form, **kwargs):
        spec_type = form.save(commit=False)
        spec_type.custom_role = 1
        spec_type.practice = self.request.POST.get('practice')
        spec_type.save()
        return redirect(self.success_url+str(spec_type.id))

class InstitutionStep2CreateView(CreateView):
    model = Profile
    form_class = InstitutionForm
    template_name = 'registration/select_institution.html'
    success_url = '/institution/signup/step3/'
    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.custom_role = 2
        form.institution = self.request.POST.get('institution')
        form.save()
        return redirect(self.success_url+str(form.id))

class EmergencyServiceStep2CreateView(CreateView):
    model = Profile
    form_class = EmergencyServiceForm
    template_name = 'registration/select_emergency_service.html'
    success_url = '/emergency-service/signup/step3/'
    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.custom_role = 3
        form.emergency_services = self.request.POST.get('emergency_services')
        form.save()
        return redirect(self.success_url+str(form.id))

class PracticeSignupStep3View(View):
    def get(self,request,pk):
        form = PracticeSignupForm
        userform = UserForm
        return render(self.request,'registration/practice.html',
            {'form':form,'userform':userform,'pk':pk})

    def post(self,request,pk):
        user_form = UserForm(request.POST)
        profile = Profile.objects.get(pk=pk)
        practice_form = PracticeSignupForm(request.POST,instance=profile)
        if user_form.is_valid() and practice_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.username = request.POST.get('username')
                user.is_active = False
                user.save()
                profile.status = 0
                profile.save()
                practice_obj = practice_form.save(commit=False)
                practice_obj.user = user
                practice_obj.gender = request.POST.get('gender')
                practice_obj.save()
                frm = settings.DEFAULT_FROM_EMAIL
                ctx = {'root_url':settings.ROOT_URL,'pk':pk}
                html_content = render_to_string('users/email.html',ctx)
                email = EmailMessage("Attach Id and Registered certificate", html_content,frm,to=[user.email])
                email.content_subtype = "html" 
                email.send()
            except Exception as e:
                messages.error(self.request, 'Email not sent')
                return HttpResponseRedirect('/practice/signup/step3/'+str(pk))
        else:
            # messages.error(self.request, 'Invalid form')
            return render(self.request,'registration/practice.html',
                {'form':practice_form,'userform':user_form,'pk':pk})
        # messages.success(self.request, 'Successfully registered.Please check your authorised email')
        return HttpResponseRedirect('/form/submit/')

class PatientSignupStep2View(View):
    def get(self,request):
        patient_form = PatientSignupForm
        user_form = UserForm
        return render(self.request,'registration/patient.html',{'patient_form':patient_form,'user_form':user_form,})

class InstitutionSignupStep3View(View):
    def get(self, request, pk):
        institution_form = InstitutionSignupForm
        user_form = UserForm
        return render(self.request,'registration/institution.html',{'institution_form':institution_form,'user_form':user_form,'pk':pk})

    def post(self, request, pk):
        user_form = UserForm(request.POST)
        profile = Profile.objects.get(pk=pk)
        institution_form = InstitutionSignupForm(request.POST, instance=profile)
        if user_form.is_valid() and institution_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.username = request.POST.get('username')
                user.is_active = False
                user.save()
                profile.status = 0
                profile.save()
                institution_obj = institution_form.save(commit=False)
                institution_obj.user = user
                institution_obj.save()
                frm = settings.DEFAULT_FROM_EMAIL
                ctx = {'root_url':settings.ROOT_URL,'pk':pk}
                html_content = render_to_string('users/email.html',ctx)
                email = EmailMessage("Attach Id and Registered certificate", html_content,frm,to=[user.email])
                email.content_subtype = "html" 
                email.send()
            except Exception as e:
                messages.error(self.request, 'Email not sent')
                return HttpResponseRedirect('/institution/signup/step3/'+str(pk))
        else:
            return render(self.request,'registration/institution.html',
                {'user_form':user_form,'institution_form':institution_form})
        # messages.success(self.request, 'Successfully registered.Please check your authorised email')
        # return HttpResponseRedirect('/institution/signup/step3/'+str(pk))
        return HttpResponseRedirect('/form/submit/')

class InsuranceProviderSignupStep2View(View):
    def get(self, request):
        insurance_form = InsuranceProviderSignupForm
        user_form = UserForm
        return render(self.request,'registration/insurance_provider.html',{'insurance_form':insurance_form,'user_form':user_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        insurance_form = InsuranceProviderSignupForm(request.POST)
        if user_form.is_valid() and insurance_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.username = request.POST.get('username')
                user.is_active = False
                user.save()
                insurance_obj = insurance_form.save(commit=False)
                insurance_obj.custom_role = 4
                insurance_obj.user = user
                insurance_obj.save()
                profile = Profile.objects.get(user=user)
                profile.status = 0
                profile.save()
                frm = settings.DEFAULT_FROM_EMAIL
                ctx = {'root_url':settings.ROOT_URL,'pk':profile.id}
                html_content = render_to_string('users/email.html',ctx)
                email = EmailMessage("Attach Id and Registered certificate", html_content,frm,to=[user.email])
                email.content_subtype = "html" 
                email.send()
            except Exception as e:
                messages.error(self.request, 'Email not sent')
                return HttpResponseRedirect('/insurance/signup/step2/')
        else:
            return render(self.request,'registration/insurance_provider.html',
                {'user_form':user_form,'insurance_form':insurance_form})
        # messages.success(self.request, 'Successfully registered.Please check your authorised email')
        # return HttpResponseRedirect('/insurance/signup/step2/')
        return HttpResponseRedirect('/form/submit/')

class EmergencyServiceSignupStep3View(View):
    def get(self,request,pk):
        service_form = EmergencyServiceSignupForm
        user_form = UserForm
        return render(self.request,'registration/emergency_service.html',{'service_form':service_form,'user_form':user_form,'pk':pk})

    def post(self,request,pk):
        user_form = UserForm(request.POST)
        profile = Profile.objects.get(pk=pk)
        service_form = EmergencyServiceSignupForm(request.POST,instance=profile)
        if user_form.is_valid() and service_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.username = request.POST.get('username')
                user.is_active = False
                user.save()
                profile.status = 0
                profile.save()
                service_obj = service_form.save(commit=False)
                service_obj.user = user
                service_obj.save()
                frm = settings.DEFAULT_FROM_EMAIL
                ctx = {'root_url':settings.ROOT_URL,'pk':pk}
                html_content = render_to_string('users/email.html',ctx)
                email = EmailMessage("Attach Id and Registered certificate", html_content,frm,to=[user.email])
                email.content_subtype = "html" 
                email.send()
            except Exception as e:
                messages.error(self.request, 'Email not sent')
                return HttpResponseRedirect('/emergency-service/signup/step3/'+str(pk))
        else:
            return render(self.request,'registration/emergency_service.html',
                {'user_form':user_form,'service_form':service_form})
        # messages.success(self.request, 'Successfully registered.Please check your authorised email')
        # return HttpResponseRedirect('/emergency-service/signup/step3/'+str(pk))
        return HttpResponseRedirect('/form/submit/')


class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')

class PracticeUpdateView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            profile_info = ProfileInfoForm
            user_info= ProfileUserForm
            return render(request, 'dashboard/practice.html',{'profile_info':profile_info,'user_info':user_info,'pk':pk})

    def post(self, request, pk):
        user_info = ProfileUserForm(request.POST,instance=User.objects.get(pk=request.user.id))
        profile = Profile.objects.get(pk=pk)
        profile_info = ProfileInfoForm(request.POST,request.FILES,instance=profile)
        if user_info.is_valid() and profile_info.is_valid():
            user = user_info.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            profile_obj= profile_info.save(commit=False)
            profile_obj.user = user
            profile_obj.image  = request.FILES.get('image')
            profile_obj.gender = request.POST.get('gender')
            profile_obj.phone = request.POST.get('phone')
            profile_obj.save()
        else:
            messages.error(request, 'Invalid')
            return HttpResponseRedirect('/edit/profile/'+str(pk))
        return HttpResponseRedirect('/edit/profile/'+str(pk))

class PracticeInfoDetailView(DetailView):
    model = Profile
    template_name = 'practice/profile_detail.html'

class ProfessionalOverviewUpdate(UpdateView): 
    model = Profile
    form_class = ProfessionalOverviewForm 
    template_name = 'dashboard/overview.html'
    success_url = '/create/overview/'
    def form_valid(self, form, **kwargs):
        overview = form.save(commit=False)
        overview.description = self.request.POST.get('description')
        overview.experience = self.request.POST.get('experience')
        overview.save()
        return redirect(self.success_url+str(self.request.user.profile.id))

class ProfessionalOverviewDetail(DetailView):
    model = Profile
    template_name = 'practice/overview_detail.html'


class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'practice/education.html'
    success_url = '/create/education/'
    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.id)
        form.user = user
        form.qualification = self.request.POST.get('qualification')
        form.specialisation = self.request.POST.get('specialisation')
        form.save()
        return redirect(self.success_url)

class EducationDetailView(DetailView):
    model = Education
    template_name = 'practice/education_detail.html'

class InstitutionDashboardView(View):
    def get(self, request, pk):
        loc_list=[]
        hour_list=[]
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            profileInfo = Profile.objects.get(user=user)
            product = Product.objects.filter(user=user)
            ambulanceInfo = AmbulanceService.objects.filter(user=user)
            keyword = Keywords.objects.filter(user=user)
            doctorList = ServiceRequest.objects.filter(service_provider=user)
            tradHour = TradingHourForm  
            ambulance = AmbulanceForm
            location_obj = Location.objects.filter(user=user)
            for loc in location_obj:
                loc_list.append(loc)
            for val in loc_list:    
                opratHour = OperatingHours.objects.filter(location=val)
                for vals in opratHour:  
                    hour_list.append(vals)
            context = {'trading_name':profileInfo.trading_name,'phone':profileInfo.phone,'address_of_institution':profileInfo.address_of_institution,'contact_person':profileInfo.contact_person,'email':user.email,'keyword':keyword,'description':profileInfo.description,'experience':profileInfo.experience,'institution':profileInfo.get_institution_display(),'products':product,'pk':pk, 'tradHour':tradHour, 'ambulance':ambulance, 'ambulanceInfo':ambulanceInfo,'opratHour':hour_list , "doctorList":doctorList, 'image': profileInfo}
            return render(request, 'dashboard/institution.html', context)
        return redirect('user-type/step1/')
        
class EmergencyServicesDashboard(View):
    def get(self, request, pk):
        loc_list = []
        hour_list = []
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            profileInfo = Profile.objects.get(user=user)
            product = Product.objects.filter(user=user)
            location_obj = Location.objects.filter(user=user)
            keyword = Keywords.objects.filter(user=user)
            for loc in location_obj:
                loc_list.append(loc)
            for val in loc_list:    
                opratHour = OperatingHours.objects.filter(location=val)
                for vals in opratHour:  
                    hour_list.append(vals)
            tradHour = TradingHourForm 
            context = {'trading_name':profileInfo.trading_name,'phone':profileInfo.phone,'address_of_institution':profileInfo.address_of_institution,'contact_person':profileInfo.contact_person,'email':user.email,'keyword':keyword,'description':profileInfo.description,'experience':profileInfo.experience,'products':product,'services':profileInfo.get_emergency_services_display(),'pk':pk, 'opratHour':hour_list,'image': profileInfo ,'tradHour':tradHour}
            return render(request, 'dashboard/emergency-services.html',context)
        return redirect('user-type/step1/')

class HealthInsuranceDashboard(View):
    def get(self, request, pk):
        loc_list = []
        hour_list = []
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            profileInfo = Profile.objects.get(user=user)
            product = Product.objects.filter(user=user)
            location_obj = Location.objects.filter(user=user)
            keyword = Keywords.objects.filter(user=user)
            for loc in location_obj:
                loc_list.append(loc)
            for val in loc_list:    
                opratHour = OperatingHours.objects.filter(location=val)
                for vals in opratHour:  
                    hour_list.append(vals)
            tradHour = TradingHourForm 
            context = {'trading_name':profileInfo.trading_name,'phone':profileInfo.phone,'address_of_institution':profileInfo.address_of_institution,'contact_person':profileInfo.contact_person,'email':user.email,'keyword':keyword,'description':profileInfo.description,'experience':profileInfo.experience,'products':product,'pk':pk, 'opratHour':hour_list,'image': profileInfo ,'tradHour':tradHour}
            return render(request, 'dashboard/health_insurance.html', context)
        return redirect('user-type/step1/')

class LogoutView(View):
    def get(self,request):
        if request.user.username:
            logout(request)
        return HttpResponseRedirect('/home/')

class Home(View):
   def get(self,request):
       return render(request,'home/home.html')

class About_us(TemplateView):
       template_name = 'home/about.html'

class Blog(TemplateView):
    template_name = 'home/blog.html'


class BlogPost(TemplateView):
    template_name = 'home/blog-post.html'

class Faq(TemplateView):
    template_name = 'home/faq.html'

class Specialisation(TemplateView):
    template_name = 'home/all-specialization.html'

class SpecialisationListView(ListView):
    model = Profile
    queryset = Profile.objects.all()
    template_name = 'home/list.html'  
    def get_context_data(self, **kwargs):
        context = super(SpecialisationListView, self).get_context_data(**kwargs)
        specialization = self.request.GET['specialization']
        context['specialization'] = self.queryset.filter(status=1, practice=specialization_value(specialization))
        return context

class ProfileDetail(DetailView):
    model = Profile  
    template_name = 'home/detail-page.html'
    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['education'] = Education.objects.filter(user_id=self.object.user)
        context['product'] = Product.objects.filter(user_id=self.object.user)
        context['keywords'] = Keywords.objects.filter(user=self.object.user)
        context['opratHour'] = OperatingHours.objects.filter(location__user=self.object.user)
        context['serviceMember'] = ServiceRequest.objects.filter(service_member=self.object.user)
        return context 

class InstitutionDetailView(DetailView):
    model = Profile
    template_name = 'home/institution-detail.html'
    def get_context_data(self, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(**kwargs)
        context['product'] = Product.objects.filter(user_id=self.object.user)
        context['ambulanceInfo'] = AmbulanceService.objects.filter(user_id=self.object.user)
        context['keywords'] = Keywords.objects.filter(user=self.object.user)
        context['opratHour'] = OperatingHours.objects.filter(location__user=self.object.user)
        context['doctorList'] = ServiceRequest.objects.filter(service_provider=self.object.user)
        return context



