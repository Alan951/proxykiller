import winreg as regedit
import ctypes

class DisableProxyTask:

    INTERNET_SETTINGS = regedit.OpenKey(regedit.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, regedit.KEY_ALL_ACCESS)
    CONNECTION_SETTINGS = regedit.OpenKey(regedit.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections', 0, regedit.KEY_ALL_ACCESS)

    def startTask(self):
        proxy = self.disableProxy()
        script = self.disableScript()

        return (proxy, script)

    def isProxyEnabled(self):
        isEnabled = self.getValueOfKey(self.INTERNET_SETTINGS, 'ProxyEnable')

        if(isEnabled == 1):
            return True
        else:
            return False

    def disableProxy(self):
        if(not self.isProxyEnabled()):
            return False

        self.setKey(self.INTERNET_SETTINGS, 'ProxyEnable', 0)

        # software proxy uses refresh cache
        INTERNET_OPTION_REFRESH = 37
        INTERNET_OPTION_SETTINGS_CHANGED = 39

        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

        internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
        internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)

        if(self.isProxyEnabled()):
            print('[ProxyKiller] - Proxy killed!')
            return True

    def disableScript(self):
        value = self.getValueOfKey(self.CONNECTION_SETTINGS, 'DefaultConnectionSettings')
        if value[8] != 1:
            val = bytearray(value)
            val[8] = 1
            self.setKey(self.CONNECTION_SETTINGS, 'DefaultConnectionSettings', val)
            print('[ScriptKiller] - Scripts killed!')
            return True
        else:
            return False
            

    def setKey(self, registry, key, value):
        _, regType = self.getValueAndType(registry, key)

        regedit.SetValueEx(registry, key, 0, regType, value)

    def getValueAndType(self, registry, key):
        value, regType = regedit.QueryValueEx(registry, key)

        return value, regType

    def getValueOfKey(self, registry, key):
        value, regType = self.getValueAndType(registry, key)

        return value


if __name__ == '__main__':
    dbt = DisableProxyTask()
    dbt.disableProxy()
