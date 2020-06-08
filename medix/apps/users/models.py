from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from users.select_choices import *
from datetime import datetime
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+|\-?(0|9)\d{9,14}$', message="Use 0-9 digit or + or - symbol for phone number")

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Created At'))
    modified_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_('Modified At'))

    class Meta:
        abstract = True

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank = True, null = True)

    custom_role = models.IntegerField(verbose_name=_('User Role'), choices=ROLE_TYPE_CHOICES, default=0)
    practice = models.IntegerField(verbose_name=_('Practice Specialisation'), choices=SPECIALISATION_TYPE_CHOICES, blank = True, null = True)
    institution = models.IntegerField(verbose_name=_('Institution Type'), choices=INSTITUTION_TYPE_CHOICES, blank = True, null = True)
    emergency_services = models.IntegerField(verbose_name=_('Service Type'), choices=SERVICES_TYPE_CHOICES, blank = True, null = True)
    gender = models.IntegerField(verbose_name=_('Gender'), choices=GENDER_CHOICES, blank = True, null = True)

    phone = models.CharField(_("Phone Number"), max_length=254, blank = True, null = True, validators=[phone_regex])
    national_identification_number = models.CharField(_("National Identification Number"), max_length=100, blank = True, null = True)
    trading_name = models.CharField(_("Trading Name"), max_length=254, blank = True, null = True)
    address_of_institution = models.TextField(_("Address Of Institution"), blank = True, null = True)
    contact_person = models.CharField(_("Contact Person"), max_length=254, blank = True, null = True)
    description = models.TextField(_("Descrption"), blank = True, null = True)
    image = models.ImageField(_("Image"),blank = True, null=True)
    experience = models.CharField(_("Experience"), max_length=5, blank = True, null = True)

    status = models.IntegerField(verbose_name=_('Profile Status'), choices=PROFILE_STATUS_CHOICES, default=0,null=True,blank=True)
    
    class Meta:
        ordering = ['id']

    # def __str__(self):
    #     return self.user.email

    @property
    def full_name(self):
        if self.user.first_name != '' or self.user.last_name != '' :
           return "%s %s" % (self.user.first_name, self.user.last_name)
        else:
           return self.trading_name

    def get_location(self):
       return self.user.location_users.filter(user=self.user)
    

class Education(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education', blank = True, null = True)
    qualification = models.CharField(_("Doctor qualification"), max_length=254, blank = True, null = True)
    specialisation = models.CharField(_("Doctor specialisation"), max_length=254, blank = True, null = True)
    
    class Meta:
        ordering = ['id']

class Location(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location', blank = True, null = True)
    location = models.TextField(_("Clinic location"), blank = True, null = True)
    mobility = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']

class OperatingHours(BaseModel):

    open_time = models.IntegerField(verbose_name=_('Doctor Opening Time'), choices=OPEN_TIME_CHOICES, default=0,null=True,blank=True)
    close_time = models.IntegerField(verbose_name=_('Doctor Closing Time'), choices=CLOSE_TIME_CHOICES, default=0,null=True,blank=True)
    day = models.CharField(_("Day"), max_length=50, blank = True, null = True)
    status = models.BooleanField(default=False)
 
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_hour', blank = True, null = True)
    
    class Meta:
        ordering = ['id']
    
class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Product', blank = True, null = True)
    price = models.FloatField(_("Product Pricing"), blank = True, null = True)
    item = models.CharField(_("Product Item"), max_length=254, blank = True, null = True)
    on_request = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

class AmbulanceService(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Ambulance', blank = True, null = True)
    location = models.TextField(_("Ambulance location"), blank = True, null = True)
    contact = models.CharField(_("Contact Number"), max_length=15, blank = True, null = True)

class Keywords(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Keyword', blank = True, null = True)
    keyword = models.CharField(_("Keyword"), max_length=50, blank = True, null = True)
    
    class Meta:
        ordering = ['id']

class Attachment(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Attachment', blank = True, null = True)
    document = models.FileField(blank=True)
    
    class Meta:
        ordering = ['id']

class ServiceRequest(BaseModel):
    service_provider = models.ForeignKey(User, related_name='Service_Provider',on_delete=models.CASCADE, blank = True, null = True)
    service_member = models.ForeignKey(User, related_name='Service_Member',on_delete=models.CASCADE, blank = True, null = True)
    is_accept = models.IntegerField(verbose_name=_('Doctor Status'), choices=PROFILE_STATUS_CHOICES, default=0,null=True,blank=True)
    
    class Meta:
        ordering = ['id']