# vim: set fileencoding=utf-8
"""
Model Representative

Depends on popit
"""
__docformat__ = 'epytext en'

import datetime
from cms.models.pluginmodel import CMSPlugin
from django.db import models
try:
    # SIGH! this is Django 1.4 which spits out warnings otherwise
    # Django 1.4. was necessary to fix an issue with PostGIS
    # an issue that occurred with the introduction of unit tests.
    from django.utils.timezone import utc
except ImportError:
    utc = None
from django.utils.translation import ugettext as _
from sorl.thumbnail.fields import ImageWithThumbnailsField

import glt
from popit.models import Person, Organisation


#: minimum length of (representative's) name
NAME_MINLEN = 4



class Party (Organisation):
    """A political party in a unit, as used in the template representative/unit.html"""
    #: acronym of this party
    acronym = models.CharField(max_length=16, blank=False, null=False,
        help_text=_('Acronym of this Party'))
    #: url of this representative
    url = models.TextField(blank=True, null=True,
        help_text=_('URL of this Party'))



class Unit (models.Model):
    """A unit/house, like Parliament or Tbilisi City Hall."""
    #: name of the unit
    name = models.CharField(max_length=255, blank=False, null=False,
        help_text=_('Name of the Unit.'))
    #: short name of the unit, as used in css, etc.
    short = models.CharField(max_length=32, blank=False, null=False,
        help_text=_('Short Name of the Unit, as used in e.g. CSS'))
    #: parties of this unit
    parties = models.ManyToManyField(Party, related_name='unit',
        help_text=_('Parties in this unit'))


    def __unicode__ (self):
        return u'%s' % self.name



class Representative (Person):
    """A representative derived from popit.Person."""
    #: personal photo
    photo = ImageWithThumbnailsField(upload_to='representatives',
        thumbnail={'size': (50, 50), 'options': ('crop',)},
        blank=True, null=True, help_text=_('Personal Photo'))
    #: party membership
    party = models.ForeignKey(Party, related_name='representatives', null=True,
        help_text=_('Party Membership'))
    #: unit membership
    unit = models.ForeignKey(Unit, related_name='representatives', null=True,
        help_text=_('Unit Membership'))
    #: committee membership
    committee = models.TextField(blank=True, null=True,
        help_text=_('Committee Membership'))
    #: faction membership
    faction = models.TextField(blank=True, null=True,
        help_text=_('Faction Membership'))
    #: is majoritarian?
    is_majoritarian = models.BooleanField(blank=True, default=False,
        help_text=_('Is Majoritarian?'))
    #: electoral district
    electoral_district = models.TextField(blank=True, null=True,
        help_text=_('Electoral District (if Majoritarian)'))
    #: date elected
    elected = models.TextField(blank=True, null=True,
        help_text=_('Date Elected'))
    #: place of birth
    pob = models.TextField(blank=True, null=True,
        help_text=_('Place of Birth'))
    #: family status
    family_status = models.TextField(blank=True, null=True,
        help_text=_('Family Status'))
    #: education
    education = models.TextField(blank=True, null=True,
        help_text=_('Education'))
    #: contact, address and phone number
    contact_address_phone = models.TextField(blank=True, null=True,
        help_text=_('Contact Address / Phone Number'))
    #: url of this representative
    url = models.TextField(blank=True, null=True,
        help_text=_('URL of this Representative'))
    #: attendance record
    attendance_record = models.TextField(blank=True, null=True,
        help_text=_('Attendance Record'))
    #: salary
    salary = models.FloatField(default=0, null=True,
        help_text=_('== Wages'))
    #: other income
    other_income = models.FloatField(default=0, null=True,
        help_text=_('== Entrepreneurial Income'))
    #: expenses
    expenses = models.TextField(blank=True, null=True,
        help_text=_('Expenses'))
    #: property & assets
    property_assets = models.TextField(blank=True, null=True,
        help_text=_('Property & Assets'))
    #: percentage of questions answered on shenmartav.ge
    answered = models.FloatField(default=0, null=True,
        help_text=_('Percentage of Answered Questions on shenmartav.ge'))


    @classmethod
    def find (cls, name):
        """Find a representative with given name.

        @param name: name of the representative
        @type name: str
        @return: representative matching the name
        @rtype: representative.Representative
        """
        if len(name) < NAME_MINLEN: return None
        name = glt.to_georgian(name)

        representative = cls.objects.filter(names__name__icontains=name)
        if representative: return representative[0]

        firstname_first = glt.firstname_first(name)
        representative = cls.objects.filter(
            names__name__icontains=firstname_first)
        if representative: return representative[0]

        lastname_first = glt.lastname_first(name)
        representative = cls.objects.filter(
            names__name__icontains=lastname_first)
        if representative: return representative[0]

        splitname = name.split()
        if len(splitname[0]) > NAME_MINLEN:
            representative = cls.objects.filter(
                names__name__icontains=splitname[0][:NAME_MINLEN])
            if representative: return representative[0]

        try:
            if len(splitname[-1]) > NAME_MINLEN:
                representative = cls.objects.filter(
                    names__name__icontains=splitname[-1][:NAME_MINLEN])
                if representative: return representative[0]
        except IndexError:
            pass

        return None


    @property
    def averaged_income (self):
        """Get averaged income of this representative.

        @return: averaged income
        @rtype: str
        """
        try: # remove the richest representative -> 4 million GEL
            richest = Representative.objects.all().order_by('-salary')[0]
            qs = Representative.objects.exclude(pk=richest)
        except IndexError:
            qs = Representative.objects.all()
        avg_salary = qs.aggregate(models.Avg('salary'))['salary__avg']

        try: # remove the richest representative -> 4 million GEL
            richest = Representative.objects.all().order_by('-other_income')[0]
            qs = Representative.objects.exclude(pk=richest)
        except IndexError:
            qs = Representative.objects.all()
        avg_other = qs.aggregate(models.Avg('other_income'))['other_income__avg']

        avg = avg_salary + avg_other
        income = self.salary + self.other_income
        try:
            percentage = income * 100. / avg
            return '%.1f' % percentage
        except ZeroDivisionError:
            return ''


    @property
    def total_income (self):
        return int(self.salary + self.other_income)


    @property
    def attendance (self):
        """Reorganise attendance data structure

        @return: reorganised attendance record
        @rtype: {\
            'percentage': float,\
            'attended': { 'relative': float, 'absolute': int },\
            'absent': { 'relative': float, 'absolute': int }\
        }
        """
        attendance = self.attendance_record.split(' ')
        attended, total = attendance[0].split('/')
        attended = int(attended)

        total = float(total)
        if total == 0:
            return {
                'percentage': 0,
                'attended': { 'relative': 0, 'absolute': 0, },
                'absent': { 'relative': 0, 'absolute': 0, }
            }


        absent = int(total) - attended
        return {
            'percentage': attendance[1][1:].split('%')[0],
            'attended': {
                'relative': '%.1f' % (attended / total * 100),
                'absolute': attended,
            },
            'absent': {
                'relative': '%.1f' % (absent / total * 100),
                'absolute': absent,
            }
        }


    def save (self, *args, **kwargs):
        from representative.piechart import PieChart
        PieChart().save(str(self.pk), [self.salary, self.other_income])
        super(Representative, self).save(*args, **kwargs)



class AdditionalInformation (models.Model):
    #: representative this info belongs to
    representative = models.ForeignKey(Representative,
        related_name='additional_information', null=True,
        help_text=_('Representative'))
    #: value of this info
    value = models.TextField(null=True, help_text=_('Additional Information'))




class RandomRepresentative (models.Model):
    """Defines the randomly selected representative of the day."""
    #: date when the current random representative was set
    date_set = models.DateTimeField(help_text=_('When random representative was set'))
    #: random representative
    representative = models.ForeignKey(Representative,
        null=True, help_text=_('Random Representative'))


    @classmethod
    def get(cls):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        date_set = datetime.datetime(
            now.year, now.month, now.day, 0, 0).replace(tzinfo=utc)

        try:
            rr = RandomRepresentative.objects.all()[0]
            if (now - rr.date_set).days >= 1:
                rr.date_set = date_set
                rr.representative = Representative.objects.all().order_by('?')[0]
                rr.save()
        except IndexError:
            try:
                representative = Representative.objects.all().order_by('?')[0]
            except IndexError:
                representative = None

            rr = RandomRepresentative(date_set=date_set,
                representative=representative)
            rr.save()


        return rr.representative


    def __unicode__ (self):
        if self.representative:
            return u'%s' % self.representative.name
        else:
            return _('Unknown')



# There must be a bug in CMS plugin models. Without exception handler, on
# running an admin command, the class definition would yield:
#  File "/votingrecord/models.py", line 70, in <module>
#      class VotingRecordPluginConf (CMSPlugin):
#        File "/usr/local/lib/python2.7/dist-packages/cms/models/pluginmodel.py", line 56, in __new__
#            table_name = 'cmsplugin_%s' % splitted[1]
#            IndexError: list index out of range
class RepresentativePluginConf (CMSPlugin):
    """Configuration for Representative plugin."""
    #: title of the plugin
    title = models.CharField(max_length=32, default=_('Representative'))