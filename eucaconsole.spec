%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           eucaconsole
Version:        4.0.0
Release:        0.1%{?dist}
Summary:        Eucalyptus Management Console

# Main code is BSD
# Bundled javascript is BSD and MIT
# Bundled "Play" font is OFL
License:        BSD and MIT and OFL
URL:            http://github.com/eucalyptus/koala
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.init
Source2:        %{name}

BuildArch:      noarch

BuildRequires:  m2crypto
#BuildRequires:  python-beaker15
BuildRequires:  python-boto >= 2.21.0
BuildRequires:  python-chameleon >= 2.5.3
BuildRequires:  python-crypto
BuildRequires:  python-dateutil
BuildRequires:  python-gevent >= 0.13.8
BuildRequires:  python-greenlet >= 0.3.1
BuildRequires:  python-gunicorn
BuildRequires:  python-nose
BuildRequires:  python-pygments
BuildRequires:  python-pyramid
#BuildRequires:  python-pyramid-beaker
#BuildRequires:  python-pyramid-chameleon
#BuildRequires:  python-pyramid-layout
BuildRequires:  python-pyramid-tm
BuildRequires:  python-setuptools-devel
BuildRequires:  python-simplejson
BuildRequires:  python-wtforms
BuildRequires:  python2-devel

# RHEL 6
Requires:       openssl
Requires:       python-dateutil
Requires:       python-simplejson
Requires:       python-crypto
# EPEL 6
Requires:       m2crypto
Requires:       python-boto >= 2.21.0
Requires:       python-chameleon >= 2.5.3
Requires:       python-gevent >= 0.13.8
Requires:       python-greenlet >= 0.3.1
Requires:       python-gunicorn

# When switching to python-pyramid 1.5 add a dep on python-pyramid-chameleon
Requires:       python-pyramid < 1.5
Requires:       python-pyramid-tm
Requires:       python-wtforms

# Euca packaged
Requires:       python-beaker15
Requires:       python-pyramid-beaker
Requires:       python-pyramid-chameleon
Requires:       python-pyramid-layout

# python-pyramid-chameleon is basically built into python-pyramid 1.4; was
#    split out in 1.5.
# TODO:  Main executable needs to refer to the config file under /etc
# TODO:  remove pyramid_chameleon from pyramid.includes in config since we use pyramid 1.4
# TODO:  patch config to write to syslog
# TODO:  ship a syslog config file
# TODO:  move static content to /usr/share/%{name}
# TODO:  change the nginx config to point to new location for static content
# TODO:  write an init script
# TODO:  check if starting with version 4.0.0 is really a good idea


%description
TODO


%prep
%setup -q -n eucaconsole-%{version}
cp  $RPM_BUILD_ROOT

%build
python2 setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python2 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/%{name}
cp -p conf/console.default.ini $RPM_BUILD_ROOT/etc/%{name}/console.ini
cp -p %{name}.init $RPM_BUILD_ROOT/etc/init.d/%{name}
cp -p %{name} $RPM_BUILD_ROOT/etc/bin/%{name}

#%check
#python2 setup.py test


%files
%doc README.rst
%doc conf/nginx.conf
%{python_sitelib}/*
#/usr/share/%{name}/*
%config(noreplace) /etc/%{name}

%changelog
* Fri Jan 17 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 4.0.0-0.1
- Created
