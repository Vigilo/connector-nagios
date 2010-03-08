NAME := connector_nagios
PKGNAME := vigilo-connector-nagios
#PREFIX = /usr
SYSCONFDIR := /etc
LOCALSTATEDIR := /var
VARDIR := $(LOCALSTATEDIR)/lib/$(PKGNAME)
DESTDIR = 

define find-distro
if [ -f /etc/debian_version ]; then \
	echo "debian" ;\
elif [ -f /etc/mandriva-release ]; then \
	echo "mandriva" ;\
else \
	echo "unknown" ;\
fi
endef
DISTRO := $(shell $(find-distro))
ifeq ($(DISTRO),debian)
	INITCONFDIR = /etc/default
else ifeq ($(DISTRO),mandriva)
	INITCONFDIR = /etc/sysconfig
else
	INITCONFDIR = /etc/sysconfig
endif

all: build settings.ini

settings.ini: settings.ini.in
	sed -e 's,@LOCALSTATEDIR@,$(LOCALSTATEDIR),g' $^ > $@

install:
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR) --record=INSTALLED_FILES
	# init
	install -p -m 755 -D pkg/init.$(DISTRO) $(DESTDIR)/etc/rc.d/init.d/$(PKGNAME)
	echo /etc/rc.d/init.d/$(PKGNAME) >> INSTALLED_FILES
	install -p -m 644 -D pkg/initconf.$(DISTRO) $(DESTDIR)$(INITCONFDIR)/$(PKGNAME)
	echo $(INITCONFDIR)/$(PKGNAME) >> INSTALLED_FILES

clean: clean_python
	rm -f settings.ini

include buildenv/Makefile.common
lint: lint_pylint
tests: tests_nose
