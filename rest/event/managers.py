from django.db import models
from common.models import Address
import event


class EventManager(models.Manager):

    def latest_schedules(self, limit=None):
        if limit is not None: limit = " LIMIT %d " % limit
        else: limit = ""
        sch = event.models.EventSchedule.objects.raw("""select EE.*,
                                                        SCH.*
                                                    FROM  %s EE,
                                                    (SELECT * FROM %s SC GROUP BY %s) as SCH
                                                    WHERE EE.id=SCH.%s ORDER BY SCH.dateFrom DESC, SCH.timeFrom DESC %s""" % (
            event.models.Event._meta.db_table,
            event.models.EventSchedule._meta.db_table,
            event.models.EventSchedule.event.field.column,
            event.models.EventSchedule.event.field.column,
            limit))

        return  sch
