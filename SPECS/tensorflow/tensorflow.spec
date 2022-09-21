Summary:        TensorFlow is an open source machine learning framework for everyone.
Name:           tensorflow
Version:        2.8.3
Release:        1%{?dist}
License:        #####
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.tensorflow.org/
Source0:        https://github.com/tensorflow/tensorflow/archive/refs/tags/v%{Version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  build-essential
BuildRequires:  python3-devel
BuildRequires:  python3-requests
BuildRequires:  python3-packaging
BuildRequires:  python3-wheel
BuildRequires:  bazel
BuildRequires:  binutils
BuildRequires: pyproject-rpm-macros
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
TensorFlow is an open source machine learning framework for everyone.

%package -n     python3-tensorflow-cpu
Summary:        python-tensorflow-cpu
Requires:       python3

%description -n python3-tensorflow-cpu
Python 3 version.


%prep
%autosetup -p1

%build
echo $PWD
bazel build //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package %{builddir}

%install
echo $PWD
pushd %{builddir}
echo $PWD
echo $(ls)
#find the wheel
#%py3_install_wheel
#or 
%pyproject_install
#or
 
%check
pip3 install nose pytest
mkdir -pv test
cd test
#PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} %python3 -c "import numpy; numpy.test()"

%files -n python3-tensorflow
%license LICENSE
%{python3_sitelib}/*


%changelog
* Thu Mar 02 2022 Riken Maharjan <rmaharjan@microsoft> - 2.8.3-1
- License verified
- Original version for CBL-Mariner
