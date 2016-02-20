from Components.config import ConfigSubsection, config
import os
config.plugins = ConfigSubsection()

class PluginDescriptor:
    WHERE_EXTENSIONSMENU = 0
    WHERE_MAINMENU = 1
    WHERE_PLUGINMENU = 2
    WHERE_MOVIELIST = 3
    WHERE_MENU = 4
    WHERE_AUTOSTART = 5
    WHERE_WIZARD = 6
    WHERE_SESSIONSTART = 7
    WHERE_TELETEXT = 8
    WHERE_FILESCAN = 9
    WHERE_NETWORKSETUP = 10
    WHERE_EVENTINFO = 11
    WHERE_NETWORKCONFIG_READ = 12
    WHERE_AUDIOMENU = 13
    WHERE_SOFTWAREMANAGER = 14
    WHERE_CHANNEL_CONTEXT_MENU = 15
    WHERE_NETWORKMOUNTS = 16

    def __init__(self, name = 'Plugin', where = [], description = '', icon = None, fnc = None, wakeupfnc = None, needsRestart = None, internal = False, weight = 0):
        self.name = name
        self.internal = internal
        self.needsRestart = needsRestart
        self.path = None
        if isinstance(where, list):
            self.where = where
        else:
            self.where = [where]
        self.description = description
        if icon is None or isinstance(icon, str):
            self.iconstr = icon
            self._icon = None
        else:
            self.iconstr = None
            self._icon = icon
        self.weight = weight
        self.wakeupfnc = wakeupfnc
        self.__call__ = fnc

    def updateIcon(self, path):
        self.path = path

    def getWakeupTime(self):
        return self.wakeupfnc and self.wakeupfnc() or -1

    @property
    def icon(self):
        if self.iconstr:
            from Tools.LoadPixmap import LoadPixmap
            return LoadPixmap(os.path.join(self.path, self.iconstr))
        else:
            return self._icon

    def __eq__(self, other):
        return self.__call__ == other.__call__

    def __ne__(self, other):
        return self.__call__ != other.__call__

    def __lt__(self, other):
        if self.weight < other.weight:
            return True
        elif self.weight == other.weight:
            return self.name < other.name
        else:
            return False

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self
