#simple converter (taken from Screen EventView) with show better 1.ShortDescription or 2.(Short)ExtendedDescription
#by mogli123

from Components.Converter.Converter import Converter
from Components.Element import cached

class EventDescription(Converter, object):
	EVENT_DESCRIPTION = 0
	EVENT_GENRE = 1
	
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "Description":
			self.type = self.EVENT_DESCRIPTION
		elif type == "Genre":
			self.type = self.EVENT_GENRE

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""
			
		if self.type == self.EVENT_DESCRIPTION:
		        name = event.getEventName()
                        short = event.getShortDescription()
  	                extended = event.getExtendedDescription()
                        empty = _("No description available.")                     
                        if short and short != name:         
                                 empty += ""     
                                 return short
                        elif extended:
                                 if len(extended) > 70:
                                         shortextended = extended[ 0 : 67 ]
                                         shortextended += "..."             
                                         return shortextended
                                 elif len(extended) < 70:
                                         shortextended = extended
                                         return shortextended
                        else:
     	                         return empty
                        
                elif self.type == self.EVENT_GENRE:
		        name = event.getEventName()
                        short = event.getShortDescription()
  	                extended = event.getExtendedDescription()
                        empty = _("No description available.")                     
                        if short and short == extended or short == name:              
                                 return empty
                        elif len(short) <= 0:              
                                 return empty
                        else:
     	                         return short 
                                      		
	text = property(getText)
