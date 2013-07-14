import logging
import tempfile
import datetime
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
from _ext import httplib2
from _ext.bs3.BeautifulSoup import BeautifulSoup
from account.models import Account
from blog.models import Blog
from event.models import Event, EventActivity, event_logo_name, EventSchedule
import urllib

logger = logging.getLogger(__name__)

class EventSource(object):

    def __init__(self, baseURL):
        logger.info("Initializing %s" % baseURL)
        self.baseURL = baseURL
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)


    def importEvents(self, dateFrom=None, dateTo=None):
        pass


class SuperKinodSource(EventSource):
    def __init__(self):
        super(SuperKinodSource, self).__init__('https://www.forumcinemas.ee')
        #eng/Websales/SelectShow/?dt=17.02.2013
        self.movieListURL = self.baseURL+ "/eng/Movies/NowInTheatres/"
        try:
            self.account = Account.objects.get(username="SuperKinod")
        except Account.DoesNotExist:
            self.account = Account.objects.create(username="SuperKinod", password="reserved", email="import@rest.ee")

        try:
            self.parentCinemaActivity = EventActivity.objects.get(name="cinema", parent=None)
        except EventActivity.DoesNotExist:
            #create it
            self.parentCinemaActivity = EventActivity()
            self.parentCinemaActivity.name = "cinema"
            self.parentCinemaActivity.save()
            pass
        logger.info("Initialized")
    pass

    def importEvents(self, dateFrom=None, dateTo=None):
        """
        @rtype: list
        @return: list of events and attached event schedules
        """
        if dateFrom is None:
            dateFrom = datetime.date.today()
        response, content = self.http.request(self.movieListURL+"?dt=%s" % dateFrom.strftime("%d.%m.%Y"), "GET")
        soup = BeautifulSoup(content, fromEncoding="utf-8")
        #
        movieList = soup.findAll("div", attrs={ "class" : "result" } )
        events = []
        for movie in movieList:
            eventName = movie.find("span", attrs={"class":"result_h"}).contents[0].strip()
            logger.info("Event name: %s" % eventName)
            #try to get such event from SOLR DB
            querySet = SearchQuerySet().models(EventSchedule).filter(name=Raw("%s~0.9" % eventName))
            if len(querySet):
                event = querySet[0].object.event
                logger.info("Found existing event: %s" % event.name)
            else:
                logger.info("New event")
                event = Event()
                event.name = eventName
                event.descr = movie.table.tr.findAll("td")[1].findAll("div")[1].string.strip()
                event.author = self.account
                #

                #download thumb to temp dir and assign thumbnail to event
                logoUrl = movie.table.tr.td.find("div", attrs={"class":"eventImageDiv"}).find("img")["src"]
                tmpFile = tempfile.gettempdir()+"/logo.jpg"
                urllib.urlretrieve(logoUrl, tmpFile)
                logger.info("Saving logo: %s" % event.logo)
                event.logo.save(event_logo_name(None,None)+".jpg",open(tmpFile))

                #save event
                event.save()

                #get genres, save them under cinema category
                tdContents = movie.table.tr.findAll("td")[1].contents
                for content in tdContents:
                    if "Genres" in content:
                        for genre in content.replace("Genres:","").split(","):
                            genre = genre.strip().lower()
                            try:
                                activity = EventActivity.objects.get(name=genre)
                            except EventActivity.DoesNotExist:
                                activity = EventActivity()
                                activity.name = genre
                                activity.parent = self.parentCinemaActivity
                                activity.save()
                            event.activities.add(activity)
                #event creation end

            releaseDateAndLength = movie.table.tr.findAll("td")[1].findAll("div")[3].findAll("b")
            movieLength = None
            releaseDate = None
            if len(releaseDateAndLength) >= 2:
                releaseDate = datetime.datetime.strptime(releaseDateAndLength[0].string.strip(), "%d.%m.%Y")
                movieLength = datetime.datetime.strptime(releaseDateAndLength[1].string.strip(),"%Hh\n %M\n min")
                movieLength = datetime.timedelta(hours=movieLength.hour,minutes=movieLength.minute)

            #get schedules
            scheduleDiv = movie.table.findAll("tr")[1].findAll("td")[1].div
            if scheduleDiv is not None and scheduleDiv.h2 is not None:
                pageName  = scheduleDiv.h2.string.strip()
                logger.info("Page name: %s" % pageName)
                #TODO: try to find blog/page with such name
                try:
                    blog = Blog.objects.get(name=pageName)
                    logger.info("Found blog with name: %s" % blog)
                except Blog.DoesNotExist:
                    logger.info("Couldn't find blog with name: %s" % pageName)
                    pass
                tableTchedules = scheduleDiv.div.findAll("table")
                for sch in tableTchedules:
                    startDate = sch.tr.th.b.string.strip()
                    scheduleLanguage = ""
                    if len(sch.tr.th.contents) > 0:
                        scheduleLanguage = sch.tr.th.contents[1].strip()
                    logger.info("Start date: %s" % startDate)
                    times = sch.findAll("tr")[1].findAll("td")
                    for time in times:
                        if time.a is None: continue
                        time = time.a.string.strip()
                        eventSchedule = EventSchedule()
                        eventSchedule.shortDescription = "%(lang)s " % { 'lang': scheduleLanguage }
                        dateFrom = datetime.datetime.strptime(startDate+ " "+time, "%d.%m.%Y %H:%M")
                        eventSchedule.dateFrom = dateFrom
                        eventSchedule.timeFrom = datetime.time(hour=dateFrom.hour, minute=dateFrom.minute)
                        #derive session end
                        if movieLength is not None:
                            dateTo = dateFrom + movieLength
                            eventSchedule.dateTo = dateTo
                            eventSchedule.timeTo = datetime.time(hour=dateTo.hour, minute=dateTo.minute)
                            logger.info("Session start: %s" % dateFrom)
                            logger.info("Session end: %s" % dateTo)
                        eventSchedule.event = event
                        eventSchedule.save()
                    pass
                pass
            events.append(event)
        logger.info("Total imported events: %d" % len(events))
        return events