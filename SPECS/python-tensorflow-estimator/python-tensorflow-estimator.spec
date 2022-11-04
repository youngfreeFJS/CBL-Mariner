%global pypi_name tensorflow-estimator
%global _description %{expand:
A high-level TensorFlow API that greatly simplifies machine learning programming}

Summary:        A high-level TensorFlow API that greatly simplifies machine learning programming
Name:           python-%{pypi_name}
Version:        2.0.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/tensorflow/estimator
Source0:        https://github.com/tensorflow/estimator/archive/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  bazel
BuildRequires:  python-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel


%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
cd estimator-%{version}

bazel build //tensorflow_estimator/tools/pip_package:build_pip_package
bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package /tmp/estimator_pkg

%install

cd estimator-%{version}
WHEEL_PACKAGE=$(find /tmp/estimator_pkg -name "tensor*.whl")
pip3 install --ignore-installed --upgrade --root %{WHEEL_PACKAGE} --no-dependencies


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Mon Apr 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-3
- Removed BR on "python3-pytest" to break a circular dependency. Replaced with build-time pip3 installation.

