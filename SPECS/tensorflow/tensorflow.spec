Summary:        Array processing for numbers, strings, records, and objects
Name:           tensorflow
Version:        1.22.3
Release:        2%{?dist}
# The custom license is inside numpy/core/src/multiarray/dragon4.c.
License:        BSD AND ZLIB custom
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://numpy.org/
Source0:        https://github.com/numpy/numpy/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  build-essential
BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-requests
BuildRequires:  python3-packaging
BuildRequires:  python3-wheel
BuildRequires:  bazel
BuildRequires:  binutils
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%package -n     python3-tensorflow-cpu
Summary:        python-tensorflow-cpu
Requires:       python3

%description -n python3-tensorflow-cpu
Python 3 version.


%prep
%autosetup -p1

%build
bazel build 


%install
pip3 install --root %{buildroot}

%check
pip3 install nose pytest
mkdir -pv test
cd test
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} %python3 -c "import numpy; numpy.test()"

%files -n python3-numpy
%license LICENSE.txt
%{python3_sitelib}/*

%files -n python3-numpy-f2py
%{_bindir}/f2py
%{_bindir}/f2py3
%{_bindir}/f2py%{python3_version}

%changelog
* Thu Mar 02 2022 Riken Maharjan <rmaharjan@microsoft> - 1.8.2-1
- License verified
- Original version for CBL-Mariner
