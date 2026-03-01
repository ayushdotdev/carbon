import polib

po = polib.pofile("locales/en/LC_MESSAGES/messages.po")

for entry in po:
    if entry.msgid:
        entry.msgstr = entry.msgid

po.save()
