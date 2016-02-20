#
# Converter NextEvents
# by m0rphU & LN
# thanks to Shaderman & Dr.Best
#
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache, eServiceReference
from time import localtime, strftime, mktime, time
from datetime import datetime


class THDNextEvents(Converter, object):
	Event1 = 0
	Event2 = 1
	Event3 = 2
	Event4 = 3
	Event5 = 4
	Event6 = 5
	Event7 = 6
	Event8 = 7
	Event9 = 8
	Event10 = 9
	Event11 = 10
	PrimeTime = 11
	noDuration = 12
	onlyDuration = 13
	withDuration = 14
	showDuration = 15

	def __init__(self, type):
		Converter.__init__(self, type)
		self.epgcache = eEPGCache.getInstance()

		args = type.split(',')
		if len(args) != 2: 
			raise ElementError("type must contain exactly 2 arguments")
	
		type = args.pop(0)
		showDuration = args.pop(0)
				
		if type == "Event2":
			self.type = self.Event2
		elif type == "Event3":
			self.type = self.Event3
		elif type == "Event4":
			self.type = self.Event4
		elif type == "Event5":
			self.type = self.Event5
		elif type == "Event6":
			self.type = self.Event6
		elif type == "Event7":
			self.type = self.Event7
		elif type == "Event8":
			self.type = self.Event8
		elif type == "Event9":
			self.type = self.Event9
		elif type == "Event10":
			self.type = self.Event10
		elif type == "Event11":
			self.type = self.Event11
		elif type == "PrimeTime":
			self.type = self.PrimeTime
		else:
			self.type = self.Event1
			
		if showDuration == "noDuration":
			self.showDuration = self.noDuration
		elif showDuration == "onlyDuration":
			self.showDuration = self.onlyDuration
		else:
			self.showDuration = self.withDuration
	
	@cached
	def getText(self):
		ref = self.source.service
		info = ref and self.source.info
		if info is None:
			return ""
		textvalue = ""
		if self.type < self.PrimeTime:
			curEvent = self.source.getCurrentEvent()
			if curEvent:
				self.epgcache.startTimeQuery(eServiceReference(ref.toString()))#, curEvent.getBeginTime() + curEvent.getDuration())
				nextEvents = []
				for i in range(self.type): # Hole x-1 Eintraege aus dem EPG
					self.epgcache.getNextTimeEntry()
				#nextEvent.getEventId(), sRef, nextEvent.getBeginTime(), nextEvent.getDuration(), nextEvent.getEventName(), nextEvent.getShortDescription(), nextEvent.getExtendedDescription()
				next = self.epgcache.getNextTimeEntry()
				if next:
					textvalue = self.formatEvent(next)
		
		elif self.type == self.PrimeTime:
			curEvent = self.source.getCurrentEvent()
			if curEvent:
				now = localtime(time())
				dt = datetime(now.tm_year, now.tm_mon, now.tm_mday, 20, 15)
				primeTime = int(mktime(dt.timetuple()))
				self.epgcache.startTimeQuery(eServiceReference(ref.toString()), primeTime)
				next = self.epgcache.getNextTimeEntry()
				if next and (next.getBeginTime() <= int(mktime(dt.timetuple()))):
					textvalue = self.formatEvent(next)
		return textvalue

	text = property(getText)
	
	def formatEvent(self, event):
		begin = strftime("%H:%M", localtime(event.getBeginTime()))
		end = strftime("%H:%M", localtime(event.getBeginTime() + event.getDuration()))
		title = event.getEventName()#[:self.titleWidth]
		duration = "%d min" % (event.getDuration() / 60)
		if self.showDuration == self.withDuration:
			f = "{begin} - {end:7}{title:<} -  {duration}"
			return f.format(begin = begin, end = end, title = title, duration = duration)
		elif self.showDuration == self.onlyDuration:
			return duration
		elif self.showDuration == self.noDuration:
		#	f = "{begin} - {end:10}{title:<}"
			f = "{begin} - {end:7}{title:<}"
			return f.format(begin = begin, end = end, title = title)
		else:
			return ""
