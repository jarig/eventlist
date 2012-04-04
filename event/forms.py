
from django.forms.models import ModelForm, BaseModelFormSet
from django.forms.widgets import HiddenInput
from blog.models import Blog
from common.forms import AddressForm
from common.models import Address
from event.models import Event, EventSchedule
from django import forms
from organization.models import Organization

class EventForm(ModelForm):
    organizers = forms.ModelMultipleChoiceField(Organization.objects.none(),
                                                cache_choices=True,
                                                widget=forms.SelectMultiple(attrs={'placeholder':"Choose an organizers"}))
    _cached_orgs = None
    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self._cached_orgs is None:
            self._cached_orgs = Organization.objects.filter(members=user).all()
        self.fields['organizers'].queryset = self._cached_orgs

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

        return newEvent


class EventScheduleForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'), required=False)
    #TODO get blog list dynamically
    blog = forms.ModelChoiceField(queryset=Blog.objects.all(), cache_choices=True,
                                    empty_label="Custom Address", required=False)
    address = forms.IntegerField(widget=HiddenInput(), required=False)


    def clean_address(self):
        data = self.cleaned_data['address']
        if data:
            data = Address.objects.select_related().get(pk=data)
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
                    if addressId != '': address = Address.objects.select_related().get(pk=addressId)
                else:
                    address = self.instance.address
            except Address.DoesNotExist: pass
            try:
                if self.is_bound:
                    blogId = self.data["%s-blog" % self.prefix]
                    if blogId != '': blog = Blog.objects.select_related().get(pk=blogId)
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
        if not super(EventScheduleForm, self).is_valid(): return False
        print self.cleaned_data["address"]
        if self.cleaned_data["address"] == "" or self.cleaned_data["address"] <= 0:#if custom form
            return self.customAddressForm.is_valid()
        return True
        

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

    #def is_valid(self):
    #    result = super(EventScheduleFormSet, self).is_valid()
    #    for form in self.forms:
    #        if not form.is_valid(): return False
    #    return result
    
    def saveSchedules(self, event):
        schedules = []
        for schForm in self.forms:
            schedules.append(schForm.saveSchedule(event))
                
        return schedules