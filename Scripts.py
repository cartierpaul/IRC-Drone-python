# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/Scripts
import Config
from Functions import PrintWelcome
from Vars import CONFIG_FILE

def Run():
    PrintWelcome()
    try:
        cfg = Config.Config()
        cfg.read(CONFIG_FILE)
    except IOError:
        print "[-] Eroare la citirea fisierului config: '" + CONFIG_FILE + "'"
        return

    if not len(cfg.bots):
        print '[-] Nu am gasit nici un bot in cfg.'
        return
    cfg.showread()
    cfg.run()