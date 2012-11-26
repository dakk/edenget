xgettext --language=Python --keyword=_ --output=locale/edenget.pot MainWindow.py
msginit --input=locale/edenget.pot --locale=locale/en_US
msginit --input=locale/edenget.pot --locale=locale/it_IT

mkdir -p locale/en_US/LC_MESSAGES
mkdir -p locale/it_IT/LC_MESSAGES

msgfmt --output-file=locale/it_IT/LC_MESSAGES/edenget.mo locale/it_IT.po
msgfmt --output-file=locale/en_US/LC_MESSAGES/edenget.mo locale/en_US.po


LANG=fr_FR python pywine.py
