from event.models import EventSchedule

__author__ = 'jarik'



def getFeaturedEvents(dateFrom, dateTo):
    #get event schedules within some date range
    eventSchedules = EventSchedule.objects.select_related('event','blog').filter(dateFrom__gt=dateFrom, dateTo__le=dateTo)
    #
    pass