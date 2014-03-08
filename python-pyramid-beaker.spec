Summary: Beaker session factory backend for Pyramid
Name: python-pyramid-beaker
Version: 0.8
Release: 0.1%{?dist}
Source0: https://pypi.python.org/packages/source/p/pyramid_beaker/pyramid_beaker-0.8.tar.gz
License: BSD
Group: Development/Libraries
BuildArch: noarch
Url: http://docs.pylonsproject.org/projects/pyramid_beaker/en/latest/

BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-pyramid
Requires: python-beaker

%description
Provides a session factory for the `Pyramid <http://docs.pylonsproject.org>`_
web framework backed by the `Beaker <http://beaker.groovie.org/>`_ sessioning
system.

See the Pylons Project documentation for more information: 
http://docs.pylonsproject.org

%prep
%setup -q -n pyramid_beaker-%{version}

%build
python setup.py build

%install
python setup.py install --skip-build -O1 --root=$RPM_BUILD_ROOT

%files
%{python_sitelib}/pyramid_beaker
%{python_sitelib}/pyramid_beaker-*.egg-info
%doc README.txt

%changelog
* Mon Jan 20 2014 Vic Iglesias <viglesiasce@gmail.com> 0.8-0.1
- Initial release
