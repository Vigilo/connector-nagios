%define module  connector-nagios
%define name    vigilo-%{module}
%define version 2.0.0
%define release 1%{?svn}%{?dist}

%define pyver 26
%define pybasever 2.6
%define __python /usr/bin/python%{pybasever}
%define __os_install_post %{__python26_os_install_post}
%{!?python26_sitelib: %define python26_sitelib %(python26 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:       %{name}
Summary:    Vigilo-Nagios connector
Version:    %{version}
Release:    %{release}
Source0:    %{module}.tar.bz2
URL:        http://www.projet-vigilo.org
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2

BuildRequires:   python26-distribute
BuildRequires:   python26-babel

Requires:   python26-distribute
Requires:   vigilo-common vigilo-connector
Requires:   nagios
######### Dependance from python dependance tree ########
Requires:   vigilo-pubsub
Requires:   vigilo-connector
Requires:   vigilo-common
Requires:   python26-distribute
Requires:   python26-twisted
Requires:   python26-wokkel
Requires:   python26-configobj
Requires:   python26-babel
Requires:   python26-zope-interface
Requires:   python26-distribute

Buildarch:  noarch


%description
Gateway from Nagios to the Vigilo message bus (XMPP) and back to Nagios.
This application is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q -n %{module}

%build
make PYTHON=%{__python}

%install
rm -rf $RPM_BUILD_ROOT
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	LOCALSTATEDIR=%{_localstatedir} \
	PYTHON=%{__python}

%find_lang %{name}


%pre
getent group vigilo-nagios >/dev/null || groupadd -r vigilo-nagios
getent passwd vigilo-nagios >/dev/null || useradd -r -g vigilo-nagios -G nagios -d %{_localstatedir}/lib/vigilo/%{module} -s /sbin/false vigilo-nagios
exit 0

%post
/sbin/chkconfig --add %{name} || :
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%preun
if [ $1 = 0 ]; then
	/sbin/service %{name} stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del %{name} || :
fi


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
%{python26_sitelib}/*
%dir %{_localstatedir}/lib/vigilo
%attr(-,vigilo-nagios,vigilo-nagios) %{_localstatedir}/lib/vigilo/%{module}
%attr(-,vigilo-nagios,vigilo-nagios) %{_localstatedir}/run/%{name}


%changelog
* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr> - 1.0-1
- initial package
