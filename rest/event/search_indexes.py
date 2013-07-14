import datetime
from haystack import indexes
from haystack.fields import MultiValueField
from event.models import EventSchedule, Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    """
        Event schedule + partly event index
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    logo = indexes.CharField(model_attr="logo", null=True, index_fieldname="logo_s")
    descr = indexes.CharField(model_attr='descr')
    rating = indexes.FloatField(model_attr="rating")
    groups = MultiValueField(indexed=True)
    activities = MultiValueField()

    dateTimeFrom = indexes.DateTimeField(null=True)
    dateTimeTo = indexes.DateTimeField(null=True)

    actuality = indexes.FloatField(stored=False, default=0)  # how much time left till an event begins

    def get_model(self):
        return Event

    def prepare_activities(self, obj):
        return [activity.name for activity in obj.activities.all()]

    def prepare_groups(self, obj):
        return [activity.group.name for activity in obj.activities.all().select_related("group")]

    def prepare(self, obj):
        super(EventIndex, self).prepare(obj)
        today = datetime.datetime.now()
        theEarliestSchedule = obj.schedules.filter(dateFrom__gte=today).order_by("dateFrom")
        if len(theEarliestSchedule):
            theEarliestSchedule = theEarliestSchedule[0]
            diff = (datetime.datetime.combine(theEarliestSchedule.dateFrom, theEarliestSchedule.timeFrom) - today)
            self.prepared_data["actuality"] = diff.days + (float(diff.seconds) / 86400.0)
            self.prepared_data["dateTimeFrom"] = datetime.datetime.combine(theEarliestSchedule.dateFrom,
                                                                           theEarliestSchedule.timeFrom)
            if theEarliestSchedule.dateTo and theEarliestSchedule.timeTo:
                self.prepared_data["dateTimeTo"] = datetime.datetime.combine(theEarliestSchedule.dateTo,
                                                                             theEarliestSchedule.timeTo)
        return self.prepared_data

    def index_queryset(self, using=None):
        #TODO: update only if necessary
        """Used when the entire index for model is updated."""
        today = datetime.datetime.now()
        return self.get_model().objects.filter(schedules__dateFrom__gte=today).distinct()

    def load_all_queryset(self):
        return self.get_model().all()