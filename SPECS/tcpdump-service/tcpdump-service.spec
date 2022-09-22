%global debug_package   %{nil}

Summary:        Systemd service that starts tcpdump
Name:           tcpdump-service
Version:        0.1
Release:        1%{?dist}
License:        gpl2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
Source0:        https://github.com/madler/pigz/archive/v%{version}.tar.gz#/pigz-%{version}.tar.gz
Source1:        tcpdump-service.service
Requires:       tcpdump

%description
tcpdump-service calls tcpdump on startup, preserves logs at /home/azureuser/tcpdumpfile.pcap

%prep
%autosetup -n pigz-%{version}

%install
install -p -m 644 %{SOURCE1} %{_unitdir}

%preun
%systemd_preun tcpdump-service.service

%post
%systemd_post tcpdump-service.service

%files
%{_unitdir}/tcpdump-service.service

%changelog
* Thu Sep 22 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.1-1
- init
