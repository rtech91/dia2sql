DESTDIR := /opt/dia2sql

init:
	pip3 install -r requirements.txt

install:
	@mkdir -p $(DESTDIR)
	@mkdir -p $(DESTDIR)/app
	@mkdir -p $(DESTDIR)/sqlgen
	@mkdir -p $(DESTDIR)/diaparser
	@find app/ -name "*.py" -exec cp {} $(DESTDIR)/app \;
	@find sqlgen/ -name "*.py" -exec cp {} $(DESTDIR)/sqlgen \;
	@find diaparser/ -name "*.py" -exec cp {} $(DESTDIR)/diaparser \;
	@cp dia2sql.py -p $(DESTDIR)
	@ln -s $(DESTDIR)/dia2sql.py /usr/bin/dia2sql

remove:
	rm -r $(DESTDIR)

.PHONY: init test