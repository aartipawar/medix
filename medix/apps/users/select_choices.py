from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    (0, _("Male")),
    (1, _("Female")),
    (2, _("Other"))
)

ROLE_TYPE_CHOICES = (
    (0, _("Patient")),
    (1, _("Practice")),
    (2, _("Institution")),
    (3, _("Emergency Services")),
    (4, _("Health Insurance Providers"))
)

SPECIALISATION_TYPE_CHOICES = (
    (0, _("Ayurvedic Medicine")),
    (1, _("Anaesthesiologist")),
    (2, _("Cardiologist")),
    (3, _("Chiropractor")),
    (4, _("Cosmetic Surgeon")),
    (5, _("Dentist")),
    (6, _("Dermatologist")),
    (7, _("Ear-Nose-Throat(otolaryngologists)")),
    (8, _("Endocrinologist")),
    (9, _("Gastroenterologist")),
    (10, _("Gynaecologist Obstetrician")),
    (11, _("General Practitioner")),
    (12, _("General Surgeon")),
    (13, _("Nephrologist")),
    (14, _("Neurologist & Neuro Surgeon")),
    (15, _("Oncologist")),
    (16, _("Ophthalmologist")),
    (17, _("Optometrics")),
    (18, _("Orthopaedist")),
    (19, _("Paediatric")),
    (20, _("Pathologist")),
    (21, _("Pulmonologist")),
    (22, _("Physiotherapist")),
    (23, _("Podiatrist")),
    (24, _("Psychologist & Psychiatrist")),
    (25, _("Radiologist")),
    (26, _("Rheumatologists")),
    (27, _("Sports Medicine Specialist")),
    (28, _("Urologist")),
)

INSTITUTION_TYPE_CHOICES = (
    (0, _("Private Hospital")),
    (1, _("Public Hospital")),
    (2, _("Clinic")),
    (3, _("Area Health Center")),
    (4, _("Pharmacy")),
    (5, _("Medical Laboratories")),
)

SERVICES_TYPE_CHOICES = (
    (1, _("Private Ambulance")),
)

OPEN_TIME_CHOICES = (
(0, _('24 Hours')),
(1, _('12:00 AM')),
(2, _('00:30 AM')),
(3, _('02:00 AM')),
(4, _('03:30 AM')),
(5, _('05:00 AM')),
(6, _('06:30 AM')),
(7, _('07:00 AM')),
(8, _('07:30 AM')),
(9, _('08:00 AM')),
(10, _('09:00 AM')),
(11, _('09:30 AM')),
(12, _('10:00 AM')),
(13, _('10:30 AM')),
(14, _('11:00 AM')),
(15, _('11:30 AM')),
(16, _('12:00 PM')),
(17, _('12:30 PM')),
(18, _('01:30 PM')),
(19, _('02:00 PM')),
(20, _('02:30 PM')),
(21, _('03:00 PM')),
(22, _('03:30 PM')),
(23, _('04:00 PM')),
(24, _('04:30 PM')),
(25, _('05:00 PM')),
(26, _('05:30 PM')),
(27, _('06:00 PM')),
(28, _('06:30 PM')),
(29, _('07:00 PM')),
(30, _('07:30 PM')),
(31, _('08:00 PM')),
(32, _('08:30 PM')),
(33, _('09:00 PM')),
(34, _('09:30 PM')),
(35, _('10:00 PM')),
(36, _('10:30 PM')),
(37, _('11:00 PM')),
(38, _('11:30 PM')),
)


CLOSE_TIME_CHOICES = (
(0, _('00:00 AM')),
(1, _('00:30 AM')),
(2, _('01:00 AM')),
(3, _('01:30 AM')),
(4, _('02:00 AM')),
(5, _('02:30 AM')),
(6, _('03:00 AM')),
(7, _('03:30 AM')),
(8, _('04:00 AM')),
(9, _('04:30 AM')),
(10, _('05:00 AM')),
(11, _('05:30 AM')),
(12, _('06:00 AM')),
(13, _('06:30 AM')),
(14, _('07:00 AM')),
(15, _('07:30 AM')),
(16, _('08:00 AM')),
(17, _('08:30 AM')),
(18, _('09:00 AM')),
(19, _('09:30 AM')),
(20, _('10:00 AM')),
(21, _('10:30 AM')),
(22, _('11:00 AM')),
(23, _('11:30 AM')),
(24, _('12:00 PM')),
(25, _('12:30 PM')),
(26, _('01:00 PM')),
(27, _('01:30 PM')),
(28, _('02:00 PM')),
(29, _('02:30 PM')),
(30, _('03:00 PM')),
(31, _('03:30 PM')),
(32, _('04:00 PM')),
(33, _('04:30 PM')),
(34, _('05:00 PM')),
(35, _('10:00 PM')),
(36, _('10:30 PM')),
(37, _('11:00 PM')),
(38, _('11:30 PM')),
(39, _('12:00 AM')),
)

STATUS_CHOICES=(
    (0, _("Open")),
    (1, _("Close")),
)

PROFILE_STATUS_CHOICES=(
    (0, _("Pending")),
    (1, _("Active")),
    (2, _("Deactive"))
)