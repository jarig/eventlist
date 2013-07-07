from haystack import indexes
from haystack.fields import MultiValueField
from event.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    descr = indexes.CharField(model_attr='descr')
    groups = MultiValueField()
    activities = MultiValueField()

    def get_model(self):
        return Event

    def prepare_activities(self, obj):
        return [activity.name for activity in obj.activities.all()]

    def prepare_groups(self, obj):
        return [activity.group.name for activity in obj.activities.all().select_related("group")]

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
