#taken from "ServicePosition" Converter 
#edited by mogli123 @ xtrend-alliance.com
from Components.Converter.Converter import Converter
from Poll import Poll
from enigma import iPlayableService, iPlayableServicePtr, iServiceInformation, eTimer, eLabel
from Components.Element import cached, ElementError
from time import localtime, strftime, time, gmtime, asctime


class THDServiceStartTime(Poll, Converter, object):
	TYPE_STARTTIME = 0

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)

		if type == "StartTime":
			self.type = self.TYPE_STARTTIME

		self.poll_enabled = True
  
        def getSeek(self):
		s = self.source.service
		return s and s.seek()

		
        @cached
	def getText(self):
                seek = self.getSeek()
		if seek is None:
			return ""
		else:
			if self.type == self.TYPE_STARTTIME:
                                return strftime("%H:%M", localtime(time()))  
	                        
	text = property(getText)

	def changed(self, what):
                time_refresh = what[0] == self.CHANGED_SPECIFIC and what[1] in (iPlayableService.evStart,iPlayableService.evStopped,iPlayableService.evEnd,iPlayableService.evCuesheetChanged,)

                if time_refresh:
			self.downstream_elements.changed(what)

                        