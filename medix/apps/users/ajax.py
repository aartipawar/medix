from django.http import  JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import Profile, Education, Product, Location, OperatingHours, AmbulanceService, Keywords, ServiceRequest
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import twilio
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def send_url_sms(request):
    accountSid = 'ACb56f8ce5605c39b516633fc3058d8550'
    authToken = '26b82a1a98a34e8acd3d30ac5a6bc480'
    twilioClient = Client(accountSid, authToken)
    myTwilioNumber = '+12052878954'
    sendTo = request.POST.get('sendTo')
    drUrl = request.POST.get('drUrl')
    myMessage = twilioClient.messages.create(body = settings.ROOT_URL+drUrl, from_=myTwilioNumber, to=sendTo)
    return JsonResponse({'status':200,'message':'Message Sent Successfully'})

def price_request_mail(request):
    profile = Profile.objects.get(id=request.POST.get("profile_id"))
    user = User.objects.get(id=profile.user.id)
    price = Product.objects.filter(user=user)
    frm = settings.EMAIL_HOST_USER
    ctx = {'products':price}
    html_content = render_to_string('users/product_list.html',ctx)
    email = EmailMessage("List of Item & Price", html_content,frm,to=[request.POST.get("email")])
    email.content_subtype = "html" 
    email.send()
    return JsonResponse({'status':200,'message' : "Price list successfully submited on your email"}) 

def requested_user(request):
    service_id = request.POST.get("service_id")
    service    = ServiceRequest.objects.get(pk=service_id)
    action_is  = request.POST.get("action_is") #activate/pending
    if action_is == "acccept":
        if service.is_accept == 1:
            #Doctor is already Active. Raise Exception
            raise Exception("This Doctor is already Accepted!!!")
        else:
            service.is_accept = 1
            service.save()
            res = {'status'  : 200,'message' : "Successfully Accepted"}
    else:
        if service.is_accept == 2:
            #Doctor is already Active. Raise Exception
            raise Exception("This Doctor is already Rejected!!!")
        else:
            service.is_accept = 2
            service.save()
            res = {'status'  : 200,'message' : "Successfully Rejected!!!"}
    return JsonResponse(res)
            
def service_request(request):
    trad_name = request.POST.get("trading_name")
    s_member = User.objects.get(pk=request.POST.get("user_id"))
    profile = Profile.objects.filter(trading_name=trad_name).values('user')
    s_provider = User.objects.get(pk=profile[0]['user'])
    if ServiceRequest.objects.filter(service_member=s_member,service_provider=s_provider).exists():
        return JsonResponse({'status':400,'message':'Already sent request'})
    service = ServiceRequest.objects.create(service_member=s_member,service_provider=s_provider,is_accept=False)
    return JsonResponse({'status':200,'message':'Successfully submited request'}) 
       

def edit_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        user = User.objects.get(id=profile.user.id)
        profile.phone = request.POST.get("phone")
        # profile.gender = request.POST.get("gender")
        profile.save()
        user.first_name = request.POST.get("firstName")
        user.last_name = request.POST.get("lastName")
        user.email = request.POST.get("email")
        user.save()
        return JsonResponse({'status':200}) 

def add_statement(request):  
    if request.method == 'POST':
        if request.POST.get("description") and request.POST.get("experience"): 
            profile = Profile.objects.get(id=request.POST.get("profile_id"))
            profile.description = request.POST.get("description")
            profile.experience = request.POST.get("experience")
            profile.save()
            return JsonResponse({'status':200})
        return JsonResponse({'status':400,'message':'Please Fill Fields'})  

def add_education(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        user = User.objects.get(id=profile.user.id)
        try:
            education = Education.objects.get(user=user)
            if request.POST.get("qualification"):
                Education.objects.create(user=user,qualification=request.POST.get("qualification"))
        except Exception as e:
            print(e)
            if request.POST.get("qualification"):
                Education.objects.create(user=user,qualification=request.POST.get("qualification"))
                return JsonResponse({'status':200}) 
            return JsonResponse({'status':400,'message':'Please fill qualification'})  
        return JsonResponse({'status':200}) 

def add_product(request):
    profile = Profile.objects.get(id=request.POST.get("profile_id"))
    user = User.objects.get(id=profile.user.id)
    try:
        if Product.objects.filter(user=user,item=request.POST.get("item")).exists(): 
            return JsonResponse({'status':400,'message':'Already exists'}) 
        Product.objects.create(user=user,item=request.POST.get("item"),price=request.POST.get("price"),on_request=request.POST.get("onRequest").title())

    except Exception as e: 
        print(e)
    return JsonResponse({'status':200}) 


def edit_education(request):
    if request.method == 'POST':
        if request.POST.get("qualification"):
            edu = Education.objects.get(id=request.POST.get("edu_id"))
            user = User.objects.get(id=edu.user.id)
            edu.qualification = request.POST.get("qualification")
            edu.user = user
            edu.save()
            return JsonResponse({'status':200})
        else:

            return JsonResponse({'status':400,'message':'Please fill qualification'})

def edit_product(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get("product_id"))
        product.item = request.POST.get("item")
        product.price = request.POST.get("price")
        product.on_request = request.POST.get("onRequest").title()
        product.save()
        return JsonResponse({'status':200})

def add_keyword(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        if not request.POST.get("keyword"):
            return JsonResponse({'status':400,'message':'Please Add Services'})
        Keywords.objects.create(user=profile.user,keyword=request.POST.get("keyword"))
        return JsonResponse({'status':200})

def delete_education(request):
    education = Education.objects.get(pk=request.GET.get('education_id'))
    education.delete()
    return JsonResponse({'status':200})

def delete_product(request):
    product = Product.objects.get(pk=request.GET.get('product_id'))
    product.delete()
    return JsonResponse({'status':200})

def edit_insurance_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.POST.get("profile_id"))
        user = User.objects.get(id=profile.user.id)
        user.email = request.POST.get('email')
        user.save()
        profile.phone = request.POST.get("phone")
        profile.contact_person = request.POST.get("contactp")
        profile.address_of_institution = request.POST.get("address")
        profile.trading_name = request.POST.get("trad_name")
        profile.save()
        return JsonResponse({'status':200})

def add_ambulance_info(request):
    profile = Profile.objects.get(id=request.POST.get("profile_id"))
    user = User.objects.get(id=profile.user.id)
    try:
        AmbulanceService.objects.create(user=user,location=request.POST.get("location"),contact=request.POST.get("contact"))
    except Exception as e:
        AmbulanceService.objects.create(user=user,location=request.POST.get("location"),contact=request.POST.get("contact"))
    return JsonResponse({'status':200})

def edit_ambulance_info(request):
    if request.method == 'POST':
        ambulance = AmbulanceService.objects.get(id=request.POST.get("ambulance_id"))
        ambulance.location = request.POST.get("locationInfo")
        ambulance.contact = request.POST.get("contact")
        ambulance.save()
        return JsonResponse({'status':200})

def ambulance_info_delete(request):
    ambulance = AmbulanceService.objects.get(pk=request.GET.get('ambulance_id'))
    ambulance.delete()
    return JsonResponse({'status':200})

def add_insurance_overview(request):
    add_statement(request)
    return JsonResponse({'status':200})

def add_insurance_product(request):
    add_product(request) 
    return JsonResponse({'status':200}) 

def insurance_product_delete(request):
    delete_product(request)
    return JsonResponse({'status':200})

def edit_insurance_product(request):
    edit_product(request)
    return JsonResponse({'status':200})

# def add_insurance_keyword(request):
#     add_keyword(request)
#     return JsonResponse({'status':200})

def delete_keyword(request):
    keyword = Keywords.objects.get(id=request.GET.get("keyword_id"))
    keyword.delete()
    return JsonResponse({'status':200})

def delete_description(request):
    profile = Profile.objects.filter(id=request.GET.get("profile_id")).update(description=None)
    return JsonResponse({'status':200})

def delete_experience(request):
    profile = Profile.objects.filter(id=request.GET.get("profile_id")).update(experience=None)
    return JsonResponse({'status':200})

#ajax for login page
def login_form(request):
    email = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    exist = User.objects.filter(username=email)
    if exist:
        if user == None and exist[0].is_active==True:
            return None 
    if user is not None:
        role = Profile.objects.filter(user_id=user.id)
        return role,user
    return False

def practice_login(request):
    if login_form(request) == None:
        return JsonResponse({'status':500}) 
    if login_form(request) != False:
        role,user = login_form(request)
        if role[0].custom_role==1 and user.is_active and user.is_staff==False:
            login(request, user)
            return JsonResponse({'status':200,'user_id':request.user.profile.id})
    return JsonResponse({'status':400})

def institution_login(request):
    if login_form(request) != False:
        role,user = login_form(request)
        if role[0].custom_role==2 and user.is_active and user.is_staff==False:
            login(request, user)
            return JsonResponse({'status':200,'user_id':request.user.profile.id})
    return JsonResponse({'status':400})

def service_login(request):
    if login_form(request) != False:
        role,user = login_form(request)
        if role[0].custom_role==3 and user.is_active and user.is_staff==False:
            login(request, user)
            return JsonResponse({'status':200,'user_id':request.user.profile.id})
    return JsonResponse({'status':400})

def insurance_login(request):
    if login_form(request) != False:
        role,user = login_form(request)
        if role[0].custom_role==4 and user.is_active and user.is_staff==False:
            login(request, user)
            return JsonResponse({'status':200,'user_id':request.user.profile.id})
    return JsonResponse({'status':400})

def patient_login(request):
    if login_form(request) != False:
        role,user = login_form(request)
        if role[0].custom_role==0 and user.is_active and user.is_staff==False:
            login(request, user)
            return JsonResponse({'status':200,'user_id':request.user.profile.id})
    return JsonResponse({'status':400})

def delete_location(request):
    try:
        location = Location.objects.get(pk=request.GET.get('location_id'))
        location.delete()
        return JsonResponse({'status':200})
    except Exception as e:
            print("Uh oh, Error : ", str(e))
            return JsonResponse({'status':400})


def edit_location(request):
    loc_hour_list=[]
    if request.method == 'POST':
        location_obj = Location.objects.get(id=request.POST.get("location_id"))
        tradHour_obj = OperatingHours.objects.filter(location=location_obj)
        loc_hour_list = [{
            'pk'        : hour.pk,
            'open_time' : hour.open_time,
            'close_time': hour.close_time,
            'day'       : hour.day,
            'status'    : hour.status,
            'location'  : hour.location.location,
            'mobility'  : hour.location.mobility
        } for hour in tradHour_obj]
        return JsonResponse({'status':200,'loc_hour_list':loc_hour_list}) 
    return JsonResponse({'status':400}) 

def edit_location_hour(request):
    day_list = []
    open_list = []
    close_list = []
    if request.method == 'POST':
        day_list.append(request.POST.get('mondy'))
        day_list.append(request.POST.get('tuedy'))
        day_list.append(request.POST.get('wedy'))
        day_list.append(request.POST.get('thusdy'))
        day_list.append(request.POST.get('frdy'))
        day_list.append(request.POST.get('satdy'))

        open_list.append(request.POST.get('monOpn'))
        open_list.append(request.POST.get('tueOpn'))
        open_list.append(request.POST.get('wedOpn'))
        open_list.append(request.POST.get('thuOpn'))
        open_list.append(request.POST.get('friOpn'))
        open_list.append(request.POST.get('satOpn'))
      
        close_list.append(request.POST.get('monCls'))
        close_list.append(request.POST.get('tueCls'))
        close_list.append(request.POST.get('wedCls'))
        close_list.append(request.POST.get('thuCls'))
        close_list.append(request.POST.get('friCls'))
        close_list.append(request.POST.get('satCls'))

        toggle_list = []
        toggle_list.append(request.POST.get('monTog').title())
        toggle_list.append(request.POST.get('tueTog').title())
        toggle_list.append(request.POST.get('wedTog').title())
        toggle_list.append(request.POST.get('thuTog').title())
        toggle_list.append(request.POST.get('friTog').title())
        toggle_list.append(request.POST.get('satTog').title())
          
        hom = request.POST.get('homVist').title()
        location_obj = Location.objects.get(id=request.POST.get("location_id"))
        Location.objects.filter(id=request.POST.get("location_id")).update(location = request.POST.get('loc_add'),mobility=request.POST.get('homVist').title())
        try:
            for dayl, openl, closel, toggle in zip(day_list,open_list,close_list,toggle_list):
                if openl != '' or closel != '':
                    operating_obj = OperatingHours.objects.filter(location=location_obj,day=dayl).update(open_time=openl,close_time=closel, status=toggle)
                # if operating_obj == 0:
                #     OperatingHours.objects.create(
                #         open_time = openl,
                #         close_time = closel,
                #         day = dayl,
                #         location = location_obj, 
                #         status=toggle  
                #     )
            return JsonResponse({'status':200})
        except Exception as e:
            print(e)
            return JsonResponse({'status':200})
    return JsonResponse({'status':400}) 


def search_keyword(request):
    suggestion = request.POST.get('suggestion')
    searchtype = request.POST.get('searchtype')
    json_res = []
    json_obj = {}
    if searchtype == 'all':
        suggestion_list = Profile.objects.filter(Q(user__first_name__istartswith=suggestion) | Q(trading_name__istartswith=suggestion), status=1)
        for record in suggestion_list:
            if record.trading_name:
                json_obj = dict(
                        searchtype = 'all',
                        is_institution = "yes",
                        user_id = record.id,
                        name =  record.trading_name,
                        specialization  = record.get_institution_display()                   
                        )
                if record.custom_role == 3:
                    is_emergency = "yes"
                    json_obj = dict(
                        is_emergency = is_emergency,
                        searchtype = 'all',
                        is_institution = "yes",
                        user_id = record.id,
                        name =  record.trading_name,
                                           
                        )
                elif record.custom_role == 4:
                    is_health = "yes"
                    json_obj = dict(
                        is_health = is_health,
                        searchtype = 'all',
                        is_institution = "yes",
                        user_id = record.id,
                        name =  record.trading_name,
                                      
                        )
            else:
                json_obj = dict(
                    user_id = record.id,
                    name      = record.user.first_name,
                    specialization  = record.get_practice_display(),
                    )
            json_res.append(json_obj)
        suggestion_list = Keywords.objects.filter(keyword__istartswith=suggestion)
        for record in suggestion_list:

            json_obj = dict(
                    name      = record.keyword,
                    searchtype = 'all',
                    )
            json_res.append(json_obj)
        return JsonResponse({'status':200,'suggestion':json_res})

    elif searchtype == 'doctors':
        suggestion_list = Profile.objects.filter(custom_role = 1, user__first_name__istartswith=suggestion, status=1)
        for record in suggestion_list:
            json_obj = dict(              
                user_id = record.id,
                name = record.user.first_name,
                specialization  = record.get_practice_display()
                )
            json_res.append(json_obj)

        return JsonResponse({'status':200,'suggestion':json_res})

    elif searchtype == 'pharmacy':
        suggestion_list = Profile.objects.filter(trading_name__istartswith=suggestion,institution = 4, status=1)
        for record in suggestion_list:
            json_obj = dict(
                is_institution = "yes",
                user_id = record.id,
                name =  record.trading_name,
                specialization  = record.get_institution_display()
                )
            json_res.append(json_obj)

        return JsonResponse({'status':200,'suggestion':json_res})

    elif searchtype == 'clinic':
        # suggestion_list = Profile.objects.filter(Q(institution = 2)| Q(trading_name__istartswith=suggestion), status=1)
        suggestion_list = Profile.objects.filter(trading_name__istartswith=suggestion,institution=2,status=1)
        for record in suggestion_list:
            json_obj = dict(
                institution = 2,
                is_institution = "yes",
                user_id = record.id,
                name =  record.trading_name,
                specialization  = record.get_institution_display()
                )
            json_res.append(json_obj)

        return JsonResponse({'status':200,'suggestion':json_res})

    elif searchtype == 'health-insurance':
        suggestion_list = Profile.objects.filter(custom_role = 4 , trading_name__istartswith=suggestion, status=1)
        for record in suggestion_list:
            json_obj = dict(
                custom_role = 4,
                is_institution = "yes",
                user_id = record.id,
                name =  record.trading_name,
                specialization  = record.get_institution_display()
                )
            json_res.append(json_obj)
        return JsonResponse({'status':200,'suggestion':json_res})
    return JsonResponse({'status':200}) 


    