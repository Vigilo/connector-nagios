NAME := connector-nagios

all: build settings.ini

include buildenv/Makefile.common

settings.ini: settings.ini.in
	sed -e 's,@LOCALSTATEDIR@,$(LOCALSTATEDIR),g' $^ > $@

install: settings.ini $(PYTHON)
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR) --record=INSTALLED_FILES
	chmod a+rX -R $(DESTDIR)$(PREFIX)/lib*/python*/*
	# init
	install -p -m 755 -D pkg/init.$(DISTRO) $(DESTDIR)/etc/rc.d/init.d/$(PKGNAME)
	echo /etc/rc.d/init.d/$(PKGNAME) >> INSTALLED_FILES
	install -p -m 644 -D pkg/initconf.$(DISTRO) $(DESTDIR)$(INITCONFDIR)/$(PKGNAME)
	echo $(INITCONFDIR)/$(PKGNAME) >> INSTALLED_FILES

clean: clean_python
	rm -f settings.ini

lint: lint_pylint
tests: tests_nose
