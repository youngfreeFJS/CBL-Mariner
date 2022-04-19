Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.6.1
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Internet
URL:            https://alsa-project.org
Source0:        https://www.alsa-project.org/files/pub/lib/%{name}-%{version}.tar.bz2
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
Requires:       python3

%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/aserver
%{_libdir}/libasound.so.2*
%{_libdir}/libatopology.so.2*
%{_datadir}/alsa/

%files devel
%defattr(-,root,root)
%{_libdir}/libasound.so
%{_libdir}/libatopology.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/alsa.m4
%{_includedir}/*

%changelog
* Tue Apr 19 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.6.1-2
- Remove libtool archive files
- Add more specificity to the %%files sections
- Move unversioned shared libraries, pkgconfig files to devel subpackage
- Lint spec

* Tue Jan 4 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.2.6.1-1
- Update to version 1.2.6.1

* Wed May 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.2.2-2
- Replace python2 dependencies with python3
- License verified

* Thu May 28 2020 Andrew Phelps <anphel@microsoft.com> - 1.2.2-1
- Update to version 1.2.2 to fix CVE-2009-0035

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.9-2
- Added %%license line automatically

* Mon Mar 16 2020 Andrew Phelps <anphel@microsoft.com> - 1.1.9-1
- Update to version 1.1.9. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.1.7-1
- initial version, moved from Vivace
