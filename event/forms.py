
from django.forms.models import ModelForm, BaseModelFormSet, modelformset_factory
from django.forms.widgets import HiddenInput
from blogs.models import Blog
from common.forms import AddressForm
from common.models import Address
from common.utils import uploadLocalImage
from event.models import Event, EventSchedule
from django import forms
from organization.models import Organization

class EventForm(ModelForm):
    organizers = forms.ModelMultipleChoiceField(Organization.objects.none(),
                                                widget=forms.SelectMultiple(attrs={'placeholder':"Choose an organizers"}))
    logo = forms.CharField(widget=HiddenInput)

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['organizers'].queryset = Organization.objects.filter(members=user).all()

    class Meta:
        exclude = ('rating','created','participants','author')
        model = Event
        widgets = {
            'blogs': forms.SelectMultiple(attrs={'placeholder':'Select Event Place'})
        }
        
    def saveEvent(self, request, eventSchedules):
        #print "Saving event"
        newEvent = self.save(commit=False)
        newEvent.author = request.user
        newEvent.save()
        
        #for schedule in eventSchedules.forms:
        #    blogId = schedule.cleaned_data["blog"]
        #    if blogId is not None: newEvent.blogs.add(blogId)
        self.save_m2m() #save manyToMany rls

        eventSchedules.saveSchedules(newEvent)
        
        #save logo
        uploadLocalImage(self.cleaned_data["logo"],
                         str(newEvent.pk) + '_logo',
                         newEvent.logo.save)

        return newEvent



class EventScheduleForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                                                                attrs={
                                                                                    "class":"dateFrom"
                                                                                }))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                                                                attrs={
                                                                                    "class":"dateTo"
                                                                                }), required=False)
    #TODO get blog list dynamically
    blog = forms.ModelChoiceField(queryset=Blog.objects.all(), empty_label="Custom Address", required=False)
    address = forms.IntegerField(widget=HiddenInput(), required=False)

    def clean_address(self):
        data = self.cleaned_data['address']
        if data:
            data = Address.objects.get(pk=data)
        else: #if custom address
            data = None
        return data

    def __init__(self, *args, **kwargs):
        super(EventScheduleForm, self).__init__(*args, **kwargs)
        address = None
        data = None
        blog = None
        if len(self.data): data = self.data
        
        if self.instance:#TODO refactor
            try:
                if self.is_bound:
                    addressId = self.data["%s-address" % self.prefix]
                    if addressId != '': address = Address.objects.get(pk=addressId)
                else:
                    address = self.instance.address
            except Address.DoesNotExist: pass
            try:
                if self.is_bound:
                    blogId = self.data["%s-blog" % self.prefix]
                    if blogId != '': blog = Blog.objects.get(pk=blogId)
                else:
                    blog = self.instance.blog
            except Blog.DoesNotExist: pass
        # if it is a blog address pass Address object
        if blog:
            self.blogAddress = address
            address = None
            data = None

        
        self.customAddressForm = AddressForm(
                                       data=data,
                                       prefix='%s-address' % self.prefix,
                                       instance=address)

    def saveSchedule(self, event):
        schedule = self.save(commit=False)
        schedule.event = event
        schAddress = None
        if self.cleaned_data["blog"] is not None and self.cleaned_data["blog"] > 0:
            #get address id
            schAddress = self.cleaned_data["address"]
        else:
            #create/save address
            self.customAddressForm.save()
            schAddress = self.customAddressForm.instance

        print schAddress
        schedule.address = schAddress
        schedule.save()
        
        return schedule

    def is_valid(self):
        res = super(EventScheduleForm, self).is_valid()
        print self.cleaned_data["address"]
        if self.cleaned_data["address"] == "" or self.cleaned_data["address"] <= 0:#if custom form
            return res and self.customAddressForm.is_valid()
        return res
        

    class Meta:
        model = EventSchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M'),
            'blog': forms.Select(attrs={'placeholder':'Select Event Place'})
        }

class EventScheduleFormSet(BaseModelFormSet):
    
    def __init__(self, *args, **kwargs):
        super(EventScheduleFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(EventScheduleFormSet, self).add_fields(form, index)

    def is_valid(self):
        result = super(EventScheduleFormSet, self).is_valid()
        for form in self.forms:
            if not form.is_valid(): return False
        return result
    
    def saveSchedules(self, event):
        schedules = []
        for schForm in self.forms:
            schedules.append(schForm.saveSchedule(event))
                
        return schedules