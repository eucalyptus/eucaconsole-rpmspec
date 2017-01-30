# Copyright (c) 2012-2017 Hewlett Packard Enterprise Development LP
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

Name:           eucaconsole
Version:        4.3.0
Release:        0%{?build_id:.%build_id}%{?dist}
Summary:        Eucalyptus Management Console

# Main code is BSD
# Bundled javascript is BSD and MIT
# Bundled "Play" font is OFL
# various artwork is CC-BY-SA
License:        BSD and CC-BY-SA and MIT and OFL
URL:            https://github.com/eucalyptus/eucaconsole
Source0:        %{tarball_basedir}.tar.xz
Source1:        %{name}.init
Source2:        %{name}
Source3:        %{name}.sysconfig
Source4:        %{name}.tmpfiles

Patch0:         %{name}.default.ini.patch

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  m2crypto
BuildRequires:  pycryptopp >= 0.6
BuildRequires:  python2-boto >= 2.43.0
BuildRequires:  python-chameleon >= 2.5.3
BuildRequires:  python-dateutil
BuildRequires:  python2-devel
BuildRequires:  python-eventlet >= 0.15.2
BuildRequires:  python-greenlet >= 0.3.1
BuildRequires:  python-gunicorn
BuildRequires:  python-lxml
BuildRequires:  python-nose
BuildRequires:  python-pygments
BuildRequires:  python-pylibmc
BuildRequires:  python-pyramid
BuildRequires:  python-setuptools
BuildRequires:  python-simplejson
BuildRequires:  python-wtforms
BuildRequires:  systemd

# Add support for ``dd status=none''
# https://bugzilla.redhat.com/show_bug.cgi?id=965654
Requires:       coreutils >= 8.4-22
Requires:       eucaconsole-selinux
Requires:       mailcap
Requires:       openssl >= 1.0.1e-16
Requires:       pycryptopp >= 0.6
# This is an = because of the path encoded in /usr/bin/eucaconsole
Requires:       python-beaker18 = 1.8.1
Requires:       python-boto >= 2.43.0
Requires:       python-chameleon >= 2.5.3
Requires:       python-dateutil
Requires:       python-defusedxml
Requires:       python-dogpile-cache
Requires:       python-eventlet >= 0.15.2
Requires:       python2-funcsigs
Requires:       python-greenlet >= 0.3.1
Requires:       python-gunicorn
Requires:       python-lxml
Requires:       python-pylibmc
Requires:       python-pyramid
Requires:       python-pyramid-beaker
Requires:       python-pyramid-chameleon
Requires:       python-pyramid-layout
Requires:       python-python-magic
Requires:       python-simplejson
Requires:       python-wtforms
Requires:       m2crypto
Requires:       memcached
Requires:       nginx

# TODO:  patch config to write to syslog
# TODO:  ship a syslog config file
# TODO:  move static content to /usr/share/%{name}
# TODO:  change the nginx config to point to new location for static content


%description
The Eucalyptus Management Console is a web-based interface to a local
Eucalyptus cloud and/or AWS services.


%prep
%setup -q -n %{tarball_basedir}
cp -p %{SOURCE1} .
cp -p %{SOURCE2} %{name}.py
%patch0 -p0 -F3


%build
python2 setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python2 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install init script
install -d $RPM_BUILD_ROOT/etc/init.d
install -m 755 %{name}.init $RPM_BUILD_ROOT/etc/init.d/%{name}

# Install executable
install -d $RPM_BUILD_ROOT/usr/bin
install -m 755 %{name}.py $RPM_BUILD_ROOT/usr/bin/%{name}

# Install conf file
install -d $RPM_BUILD_ROOT/etc/%{name}
install -m 755 conf/console.default.ini $RPM_BUILD_ROOT/etc/%{name}/console.ini
install -m 755 conf/nginx.conf $RPM_BUILD_ROOT/etc/%{name}/nginx.conf
install -m 755 conf/memcached $RPM_BUILD_ROOT/etc/%{name}/memcached

# Install /run/eucaconsole for PID file and other data
install -d -m 0755 $RPM_BUILD_ROOT/var/run/eucaconsole
mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
install %{SOURCE4} $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

# Create log file
install -d $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/%{name}.log
touch $RPM_BUILD_ROOT/var/log/%{name}_startup.log

# Install nginx sysconf file
install -d $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%_sysconfdir/sysconfig/%{name}

%find_lang %{name}


#%check
#python2 setup.py test


%files -f %{name}.lang
%doc README.rst
%{python_sitelib}/*
/usr/share/%{name}
%config(noreplace) /etc/%{name}
%{_bindir}/%{name}
/etc/init.d/%{name}
%config(noreplace) /etc/sysconfig/%{name}
%{_tmpfilesdir}/%{name}.conf
%attr(-,eucaconsole,eucaconsole) %dir /var/run/%{name}
%attr(-,eucaconsole,eucaconsole) /var/log/%{name}.log
%attr(-,eucaconsole,eucaconsole) /var/log/%{name}_startup.log


%pre
getent group eucaconsole >/dev/null || groupadd -r eucaconsole
getent passwd eucaconsole >/dev/null || \
    useradd -r -g eucaconsole -d /var/run/eucaconsole \
    -c 'Eucalyptus Console' eucaconsole

%post
/sbin/chkconfig --add eucaconsole

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service eucaconsole stop >/dev/null 2>&1
    /sbin/chkconfig --del eucaconsole
fi


%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service eucaconsole condrestart >/dev/null 2>&1 || :
fi

%changelog
* Mon Jan 30 2017 Garrett Holmstrom <gholms@fedoraproject.org> - 4.3.0
- Update beaker requirement to 1.8.1 (GUI-2845)

* Mon Nov 7 2016 Kamal Gill <kamal.gill@hpe.com> - 4.4.0
- Update python-boto minimum version to 2.43.0 (GUI-2806)

* Fri Sep  9 2016 Garrett Holmstrom <gholms@hpe.com> - 4.4.0
- Removed el6 support
- Added python-lxml dependency (GUI-2753)

* Tue Aug 9 2016 Matt Bacchi <mbacchi@hpe.com> - 4.3.0
- Version bump (4.3.0)

* Tue Jul 12 2016 Garrett Holmstrom <gholms@hpe.com> - 4.3.0
- Added eucaconsole-selinux dependency

* Wed May  4 2016 Matt Bacchi <mbacchi@hpe.com> - 4.3.0
- Update beaker requirement to 1.8 (GUI-2429)
- Add python2-funcsigs requirement (dragged in by beaker 1.8)
- Replace python-crypto with pycryptopp (GUI-1659)
- python-pyramid-layout updated to 1.0 on el7, cannot update on el6 because
- python-pyramid 1.4 is the latest available in epel6 repo

* Tue Apr 12 2016 Garrett Holmstrom <gholms@hpe.com> - 4.3.0
- Fixed file list and BuildRequires
- Reorganized Requires/BuildRequires
- Removed Obsoletes: eucalyptus-console < 4.0

* Wed Mar 30 2016 Garrett Holmstrom <gholms@hpe.com> - 4.3.0
- Added tmpfiles.d (GUI-2455)

* Thu Mar 10 2016 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.2
- replace gevent with eventlet
- rename patch files, prefix with eucaconsole

* Fri Feb 5 2016 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.2
- update dependencies for RHEL 7 (but add conditionals to allow building on el6)

* Tue Dec 22 2015 David Kavanagh <dak@hpe.com> - 4.2.1
- Install and manage memcached for use by eucaconsole

* Mon Dec  7 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.1
- Version bump (4.2.1)

* Tue Aug  4 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Install and manage nginx for use by eucaconsole.

* Wed Jul 29 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Version bump (4.2.0)

* Thu Jun  4 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.2.0
- Added /usr/share/eucaconsole

* Fri Apr 17 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.1
- Bumped python-beaker15 dep to 1.5.4-8.4 (GUI-1638)

* Mon Mar 30 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.1
- Version bump (4.1.1)

* Mon Mar 23 2015 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Re-added missing python-boto dependency (GUI-1614)

* Wed Dec 17 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Replaced python-gevent BuildRequires with python-gevent1 as well

* Tue Dec 16 2014 David Kavanagh <dak@eucalyptus.com> - 4.1.0
- Replaced python-gevent dependency with python-gevent1

* Tue Dec 9 2014 David Kavanagh <dak@eucalyptus.com> - 4.1.0
- added memcached config file to package

* Fri Nov 28 2014 David Kavanagh <dak@eucalyptus.com> - 4.1.0
- updated boto version to 2.34.0

* Fri Oct 31 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Replaced python-magic dependency with python-python-magic [GUI-1407]

* Tue Sep 23 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Require python-dogpile-cache

* Mon Sep 22 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.2
- Version bump (4.0.2)

* Fri Aug 29 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0
- Added python-pylibmc dependency [GUI-1083]
- Added python-magic dependency [GUI-1040]
* Tue Jul  8 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.1-0
- Switched to xz-compressed sources

* Mon Jul  7 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.1.0-0
- Updated to 4.1.0

* Mon Jul  7 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.1-0
- Switched to monolithic source tarball naming

* Tue Jun 17 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.1-0
- Updated to 4.0.1

* Wed May 28 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Require coreutils >= 8.4-22 [RH:965654]

* Tue May 27 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0
- Obsolete eucalyptus-console < 4.0

* Fri May 16 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0.1
- Require version of openssl that works for the console

* Fri Jan 17 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0.1
- Created
