from optparse import make_option
import os
from subprocess import Popen
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run Solr'

    option_list = BaseCommand.option_list + (
        make_option('--killExisting',
                    action='store_true',
                    dest='kill',
                    default=False,
                    help='Kill Solr instance if found'),
    )

    def handle(self, *args, **options):
        # check if Solr is already running
        pidFilePath = os.path.join(settings.SOLR_DISTRIB, "running.pid")
        if os.path.exists(pidFilePath):
            # at least pid file exist, let's check pid file itself
            pid = int(open(pidFilePath).read())
            if self.check_pid(pid):
                if options["kill"]:
                    # kill instance
                    os.kill(pid, 9)
                    pass
                else:
                    raise Exception("New solr instance cannot be started as one is already running, pid: %s" % pid)
                pass
        callArgs = ["java", '-jar', '%s/start.jar' % settings.SOLR_DISTRIB, "-Dsolr.solr.home=%s" % settings.SOLR_HOME]
        pObj = Popen(callArgs, cwd=settings.SOLR_DISTRIB)
        open(pidFilePath, "w").write(str(pObj.pid))
        pObj.wait()
        pass

    def check_pid(self, pid):
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True