%define module  connector-nagios
%define name    vigilo-%{module}
%define version 2.0.0
%define release 1%{?svn}

Name:       %{name}
Summary:    Vigilo-Nagios connector
Version:    %{version}
Release:    %{release}
Source0:    %{module}.tar.bz2
URL:        http://www.projet-vigilo.org
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2

BuildRequires:   python-setuptools
BuildRequires:   python-babel

Requires:   python >= 2.5
Requires:   python-setuptools
Requires:   vigilo-common vigilo-connector
Requires:   nagios
######### Dependance from python dependance tree ########
Requires:   vigilo-pubsub
Requires:   vigilo-connector
Requires:   vigilo-common
Requires:   python-setuptools
Requires:   python-twisted
Requires:   python-wokkel
Requires:   python-configobj
Requires:   python-babel
Requires:   python-zope-interface
Requires:   python-setuptools

Requires(pre): rpm-helper

Buildarch:  noarch


%description
Gateway from Nagios to the Vigilo message bus (XMPP) and back to Nagios.
This application is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q -n %{module}

%build
make PYTHON=%{_bindir}/python

%install
rm -rf $RPM_BUILD_ROOT
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	LOCALSTATEDIR=%{_localstatedir} \
	PYTHON=%{_bindir}/python

%find_lang %{name}


%pre
%_pre_useradd vigilo-nagios %{_localstatedir}/lib/vigilo/%{module} /bin/false
%_pre_groupadd nagios vigilo-nagios

%post
%_post_service %{name}

%preun
%_preun_service %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%{_bindir}/%{name}
%{_initrddir}/%{name}
%dir %{_sysconfdir}/vigilo/
%config(noreplace) %{_sysconfdir}/vigilo/%{module}
%config(noreplace) %{_sysconfdir}/sysconfig/*
%{python_sitelib}/*
%dir %{_localstatedir}/lib/vigilo
%attr(-,vigilo-nagios,vigilo-nagios) %{_localstatedir}/lib/vigilo/%{module}
%attr(-,vigilo-nagios,vigilo-nagios) %{_localstatedir}/run/%{name}


%changelog
* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr> - 1.0-1
- initial package
