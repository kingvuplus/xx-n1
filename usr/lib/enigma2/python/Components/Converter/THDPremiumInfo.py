from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Components.Language import language
from Poll import Poll

# not_widescreen = 4:3
NOT_WIDESCREEN = [1, 2, 5, 6, 9, 0xA, 0xD, 0xE]
# widescreen 16:9
WIDESCREEN = [3, 4, 7, 8, 0xB, 0xC, 0xF, 0x10]

class THDPremiumInfo(Poll, Converter, object):
	AUDIO_LANGUAGE = 0
	SUBTITLES_AVAILABLE = 2
	AUDIO_DESCRIPTION = 3
	AUDIO_STEREO = 4
	IS_NOT_WIDESCREEN = 5                                                                     
	IS_WIDESCREEN = 6
        IS_720I = 7
	IS_720P = 8
	IS_1080I = 9
	IS_1080P = 10
	

	def __init__(self, type):
	        Poll.__init__(self)
		Converter.__init__(self, type)
		self.type, self.interesting_events = {
				"AudioLanguage": (self.AUDIO_LANGUAGE, (iPlayableService.evUpdatedInfo,)),
				"SubtitlesAvailable": (self.SUBTITLES_AVAILABLE, (iPlayableService.evUpdatedInfo,)),
				"AudioDescription": (self.AUDIO_DESCRIPTION, (iPlayableService.evUpdatedInfo,)),
				"AudioStereo": (self.AUDIO_STEREO, (iPlayableService.evUpdatedInfo,)),
				"NotWidescreen": (self.IS_NOT_WIDESCREEN, (iPlayableService.evVideoSizeChanged,iPlayableService.evUpdatedInfo,)),
				"IsWidescreen": (self.IS_WIDESCREEN, (iPlayableService.evVideoSizeChanged,iPlayableService.evUpdatedInfo,)),
				"HD720i": (self.IS_720I, (iPlayableService.evVideoSizeChanged,iPlayableService.evVideoProgressiveChanged,iPlayableService.evUpdatedInfo,)),
				"HD720p": (self.IS_720P, (iPlayableService.evVideoSizeChanged,iPlayableService.evVideoProgressiveChanged,iPlayableService.evUpdatedInfo,)),
				"HD1080i": (self.IS_1080I, (iPlayableService.evVideoSizeChanged,iPlayableService.evVideoProgressiveChanged,iPlayableService.evUpdatedInfo,)),
				"HD1080p": (self.IS_1080P, (iPlayableService.evVideoSizeChanged,iPlayableService.evVideoProgressiveChanged,iPlayableService.evUpdatedInfo,))
			}[type]
		self.poll_enabled = True

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		
		if self.type == self.AUDIO_LANGUAGE:
			audio = service.audioTracks()
                        if audio:
				n = audio.getNumberOfTracks()
                                idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
                                        languages = i.getLanguage()
                                        description = i.getDescription()
					lange = language.getLanguage()
                                        if lange == 'de_DE':
                                                if "Englisch" in languages or "English" in languages or "Spanish" in languages or "Turkish" in languages or "Kommentar" in languages or "Stadion" in languages or "stereo englisch" in languages or "franz" in languages or "Franz\xc3\xb6sisch" in languages or "franz\xc3\xb6sisch" in languages or "Italian" in languages or "Russian" in languages or "French" in languages or "Italienisch" in languages or "Tonopt. 2" in languages:
						        return True
                                                elif "DTS audio" in description or "AC-3 audio" in description:
                                                        if n > 1:
                                                                return True
                                                        return False
                                                idx += 1
                                        elif lange == 'en_EN':
                                                if "Deutsch" in languages or "German" in languages:
						        return True
                                                elif "DTS audio" in description or "AC-3 audio" in description:
                                                        if n > 1:
                                                                return True
                                                        return False
					        idx += 1
					elif lange == 'it_IT':
                                                if "Englisch" in languages or "English" in languages:
						        return True
                                                elif "DTS audio" in description or "AC-3 audio" in description:
                                                        if n > 1:
                                                                return True
                                                        return False
                                                idx += 1       
					else:
					        return False
			return False

		elif self.type == self.SUBTITLES_AVAILABLE:
			subtitle = service and service.subtitle()
			subtitlelist = subtitle and subtitle.getSubtitleList()
			if subtitlelist:
			       	return len(subtitlelist) > 0
			return False
			
		elif self.type == self.AUDIO_DESCRIPTION:
			audio = service.audioTracks()
                        if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
                                        languages = i.getLanguage().split('/')
                                        description = i.getDescription() 
                                        if "H\xc3\xb6rfilm" in languages or "Zweikanal" in languages or "mit Audiodeskription" in languages:
						return True
					idx += 1
			return False
		
	        elif self.type == self.AUDIO_STEREO:
                        audio = service.audioTracks()
                        if audio:
                                n = audio.getNumberOfTracks()
                                idx = 0
                                while idx < n:
                                        i = audio.getTrackInfo(idx)
                                        description = i.getDescription()
                                        if "AC3" in description or "AC-3" in description or "DTS" in description:
                                                return False
                                        idx += 1
                                if n <= 0:
                                	return False
                        return True
         
                elif self.type == self.IS_NOT_WIDESCREEN:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
                        if width >= 1279:
                                return False
                        else:        
                                return info.getInfo(iServiceInformation.sAspect) in NOT_WIDESCREEN
                
                elif self.type == self.IS_WIDESCREEN:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
                        if width < 1280:
                                return info.getInfo(iServiceInformation.sAspect) in WIDESCREEN
                        return False
                
                elif self.type == self.IS_720I:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
		        progressive = info.getInfo(iServiceInformation.sProgressive)      
                        prog = progressive == 0 and "i" 
                        if width == 1280 and prog == "i": 
                                return True
                        else:
                                return False
                        return False
                
                elif self.type == self.IS_720P:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
		        progressive = info.getInfo(iServiceInformation.sProgressive)      
                        prog = progressive == 1 and "p" 
                        if width == 1280 and prog == "p": 
                                return True
                        else:
                                return False
                        return False
                
                elif self.type == self.IS_1080I:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
		        progressive = info.getInfo(iServiceInformation.sProgressive)      
                        prog = progressive == 0 and "i" 
                        if width == 1920 and prog == "i": 
                                return True
                        else:
                                return False
                        return False
                
                elif self.type == self.IS_1080P:
                        width = info.getInfo(iServiceInformation.sVideoWidth)
                        progressive = info.getInfo(iServiceInformation.sProgressive)
                        prog = progressive == 1 and "p"                        
                        if width == 1920 and prog == "p": 
                                return True
                        else:
                                return False
                        return False
                                         
	boolean = property(getBoolean)
	
                
	def changed(self, what):
		if what[0] == self.CHANGED_POLL or what[0] == self.CHANGED_SPECIFIC and what[1] in self.interesting_events:
			Converter.changed(self, what)
