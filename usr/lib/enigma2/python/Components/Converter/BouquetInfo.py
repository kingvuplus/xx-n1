################################################################################
#                                                                              #
# BouquetInfo Converter show your current Bouquet: in InfoBar or SecondInfobar #
#                         by betonme and mogli123                              #
#                                                                              #
# Skin Example:                                                                #
#                                                                              #
#        <widget source="session.CurrentService" render="Label" .......>       #
#          <convert type="BouquetInfo">Bouquet</convert>                       #
#        </widget>                                                             #
#                                                                              #
################################################################################

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference, eEPGCache, eServiceCenter 
from Components.Element import cached
from ServiceReference import ServiceReference
from Screens.InfoBar import InfoBar

class BouquetInfo(Converter, object):                 
	BOUQUET = 0

	def __init__(self, type):
		Converter.__init__(self, type)
                if type == "Bouquet":
			self.type = self.BOUQUET
		else:
                        return "Bouquet not found"
                
	@cached
	def getText(self):
                if self.type == self.BOUQUET:
                         Servicelist = None
		         if InfoBar and InfoBar.instance:
			         Servicelist = InfoBar.instance.servicelist                                 		
                                 bouquets = Servicelist and Servicelist.getBouquetList()
			         actbouquet = bouquets and Servicelist.getRoot()
                                 if actbouquet:
			         	return ServiceReference(actbouquet).getServiceName()
                return "Bouquet not found"
                
	text = property(getText)
