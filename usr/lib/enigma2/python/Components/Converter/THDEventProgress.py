from Converter import Converter
from Poll import Poll
from time import time
from Components.Element import cached, ElementError

class THDEventProgress(Poll, Converter, object):
	PROGRESSBACKROUND = 0

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "Background":
			self.type = self.PROGRESSBACKROUND
			self.poll_interval = 30*1000
			self.poll_enabled = True

	@cached
	def getValue(self):
		assert self.type == self.PROGRESSBACKROUND

		event = self.source.event
		if event is None:
			return None

                progress = int(time()) + event.getDuration()
		duration = event.getDuration()
		if duration > 0 and progress >= 0:
			if progress > duration:
				progress = duration
			return progress * 1000 / duration
		else:
			return None

	value = property(getValue)
	range = 1000

	def changed(self, what):
		Converter.changed(self, what)
		if self.type == self.PROGRESSBACKROUND and len(self.downstream_elements):
			if not self.source.event and self.downstream_elements[0].visible:
				self.downstream_elements[0].visible = False
			elif self.source.event and not self.downstream_elements[0].visible:
				self.downstream_elements[0].visible = True