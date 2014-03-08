Summary: Bindings for the Chameleon templating system for the Pyramid web framework
Name: python-pyramid-chameleon
Version: 0.1
Release: 0.1%{?dist}
Source0: https://pypi.python.org/packages/source/p/pyramid_chameleon/pyramid_chameleon-0.1.tar.gz
License: BSD
Group: Development/Libraries
BuildArch: noarch
Url: http://docs.pylonsproject.org/projects/pyramid_chameleon/en/latest/

BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-pyramid

%description
These are bindings for the Chameleon templating system for the Pyramid web framework. 
See http://docs.pylonsproject.org/projects/pyramid_chameleon/en/latest/ for documentation.

%prep
%setup -q -n pyramid_chameleon-%{version}

%build
python setup.py build

%install
python setup.py install --skip-build -O1 --root=$RPM_BUILD_ROOT

%files
%{python_sitelib}/pyramid_chameleon
%{python_sitelib}/pyramid_chameleon-*.egg-info
%doc README.rst COPYRIGHT.txt

%changelog
* Mon Feb 17 2014 Vic Iglesias <viglesiasce@gmail.com> 0.1-0.1
- Initial release
