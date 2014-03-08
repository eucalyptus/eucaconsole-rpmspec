Summary: Pyramid add-on for facilitating UI layout 
Name: python-pyramid-layout
Version: 0.8
Release: 0.1%{?dist}
Source0: https://pypi.python.org/packages/source/p/pyramid_layout/pyramid_layout-0.8.tar.gz
License: BSD
Group: Development/Libraries
BuildArch: noarch
Url: http://docs.pylonsproject.org/projects/pyramid_layout/en/latest/

BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-pyramid

%description
Pyramid Layout is an add-on for the Pyramid Web Framework which allows
developers to utilize the concept of a UI layout to your Pyramid
application. Different layouts may be registered for use in different
contexts of your application. The concept of panels is also introduced
to facilitate rendering of subsections of a page in a consistent way
across different views in a reusable way.

%prep
%setup -q -n pyramid_layout-%{version}

%build
python setup.py build

%install
python setup.py install --skip-build -O1 --root=$RPM_BUILD_ROOT

%files
%{python_sitelib}/*
%doc README.rst LICENSE.rst

%changelog
* Mon Jan 20 2014 Vic Iglesias <viglesiasce@gmail.com> 0.8-0.1
- Initial release
