# Below definitions are used to deliver config files from a particular branch
# of c/image, c/common, c/storage vendored in all of Buildah, Podman and Skopeo.
# These vendored components must have the same version. If it is not the case,
# pick the oldest version on c/image, c/common, c/storage vendored in
# Buildah/Podman/Skopeo.
%global skopeo_branch main
%global podman_branch main
%global buildah_branch main
%global image_branch  main
%global common_branch main
%global storage_branch main
%global shortnames_branch main
%global github_containers https://raw.githubusercontent.com/containers
Summary:        Common configuration and documentation for containers
Name:           containers-common
Version:        4.1
Release:        63%{?dist}
#Release:        %autorelease
Epoch:          4
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Requires: (fuse-overlayfs if fedora-release-identity-server)
# SourceN files fetched from upstream
# GPG key and registry configs taken from RH
Source1:        %{github_containers}/common/%{common_branch}/docs/containers.conf.5.md
Source2:        %{github_containers}/common/%{common_branch}/pkg/config/containers.conf
Source3:        %{github_containers}/common/%{common_branch}/pkg/seccomp/seccomp.json
Source4:        %{github_containers}/common/%{common_branch}/pkg/subscriptions/mounts.conf
Source5:        %{github_containers}/image/%{image_branch}/docs/containers-auth.json.5.md
Source6:        %{github_containers}/image/%{image_branch}/docs/containers-certs.d.5.md
Source7:        %{github_containers}/image/%{image_branch}/docs/containers-policy.json.5.md
Source8:        %{github_containers}/image/%{image_branch}/docs/containers-registries.conf.5.md
Source9:        %{github_containers}/image/%{image_branch}/docs/containers-registries.conf.d.5.md
Source10:       %{github_containers}/image/%{image_branch}/docs/containers-registries.d.5.md
Source11:       %{github_containers}/image/%{image_branch}/docs/containers-signature.5.md
Source12:       %{github_containers}/image/%{image_branch}/docs/containers-transports.5.md
Source13:       %{github_containers}/image/%{image_branch}/registries.conf
Source14:       %{github_containers}/common/%{common_branch}/docs/containers-mounts.conf.5.md
Source15:       %{github_containers}/shortnames/%{shortnames_branch}/shortnames.conf
Source16:       %{github_containers}/skopeo/%{skopeo_branch}/default.yaml
Source17:       %{github_containers}/skopeo/%{skopeo_branch}/default-policy.json
Source18:       %{github_containers}/storage/%{storage_branch}/docs/containers-storage.conf.5.md
Source19:       %{github_containers}/storage/%{storage_branch}/storage.conf
#Source20:       RPM-GPG-KEY-redhat-release
#Source21:       registry.access.redhat.com.yaml
#Source22:       registry.redhat.io.yaml
#Source23:       %{github_containers}/common/%{common_branch}/docs/Containerfile.5.md
Source23:       Containerfile.5.md
Source24:       %{github_containers}/common/%{common_branch}/docs/containerignore.5.md
Source25:       %{github_containers}/common/%{common_branch}/docs/links/.containerignore.5
BuildRequires:  go-md2man
Requires:       (container-selinux >= 2:2.162.1 if selinux-policy)
Recommends:     fuse-overlayfs
Provides:       skopeo-containers = %{epoch}:%{version}-%{release}
BuildArch:      noarch

%description
This package contains common configuration files and documentation for container
tools ecosystem, such as Podman, Buildah and Skopeo.

It is required because the most of configuration files and docs come from projects
which are vendored into Podman, Buildah, Skopeo, etc. but they are not packaged
separately.

%package extra
Summary:        Extra dependencies for Podman and Buildah
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       container-network-stack
#Requires: (slirp4netns if fedora-release-identity-server)
Requires:       iptables
Requires:       nftables
#Requires: oci-runtime
Recommends:     crun
#Requires: (crun if fedora-release-identity-server)
Recommends:     netavark
#Requires: (netavark if fedora-release-identity-server)
Recommends:     slirp4netns
Suggests:       containernetworking-plugins >= 0.9.1-1
Suggests:       qemu-user-static

%description extra
This subpackage will handle dependencies common to Podman and Buildah which are
not required by Skopeo.

%prep
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .
cp %{SOURCE7} .
cp %{SOURCE8} .
cp %{SOURCE9} .
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .
cp %{SOURCE13} .
cp %{SOURCE14} .
cp %{SOURCE15} 000-shortnames.conf
cp %{SOURCE16} .
cp %{SOURCE17} policy.json
cp %{SOURCE18} .
cp %{SOURCE19} .
cp %{SOURCE20} .
cp %{SOURCE21} .
cp %{SOURCE22} .
cp %{SOURCE23} .
cp %{SOURCE24} .
cp %{SOURCE25} .

%if 0%{?rhel} <= 8
sed -i 's/log_driver = "journald"/#log_driver = "journald"/' containers.conf
%endif

%build
mkdir -p man5
for FILE in $(ls *.5.md); do
    go-md2man -in $FILE -out man5/$(basename $FILE .md)
done

cp man5/containerignore.5 man5/.containerignore.5

%install
# install config and policy files for registries
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d}
install -dp %{buildroot}%{_sharedstatedir}/containers/sigstore
install -Dp -m0644 default.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d
install -Dp -m0644 storage.conf -t %{buildroot}%{_datadir}/containers
install -Dp -m0644 registries.conf -t %{buildroot}%{_sysconfdir}/containers
install -Dp -m0644 000-shortnames.conf -t %{buildroot}%{_sysconfdir}/containers/registries.conf.d
install -Dp -m0644 policy.json -t %{buildroot}%{_sysconfdir}/containers
#install -Dp -m0644 RPM-GPG-KEY-redhat-release -t %{buildroot}%{_sysconfdir}/pki/rpm-gpg
#install -Dp -m0644 registry.access.redhat.com.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d
#install -Dp -m0644 registry.redhat.io.yaml -t %{buildroot}%{_sysconfdir}/containers/registries.d


# install manpages
for FILE in $(ls -a man5 | grep 5); do
    install -Dp -m0644 man5/$FILE -t %{buildroot}%{_mandir}/man5
done

# install config files for mounts, containers and seccomp
install -m0644 mounts.conf %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 seccomp.json %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 containers.conf %{buildroot}%{_datadir}/containers/containers.conf

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/redhat.repo

%files
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%dir %{_sysconfdir}/containers/registries.d
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
#%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
#%{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
#%{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
%ghost %{_sysconfdir}/containers/storage.conf
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/Containerfile.5.gz
%{_mandir}/man5/containerignore.5.gz
%{_mandir}/man5/.containerignore.5.gz
%{_mandir}/man5/containers*.5.gz
%dir %{_datadir}/containers
%{_datadir}/containers/storage.conf
%{_datadir}/containers/containers.conf
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%files extra

%changelog
* Thu Dec 08 2022 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 4:1-63
- Initial import from Fedora
- License verified

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:1-62
- add cni-plugins and qemu-user-static deps to containers-common-extra

* Thu Oct 06 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-61
- add containers-common-extra subpackage

* Wed Oct 05 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-60
- local build

* Wed Aug 10 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-59
- local build

* Thu Jul 14 2022 Jonathan Wakely <jwakely@fedoraproject.org> 4:1-58
- Fix missing markup in Containerfile.5 man page

* Tue Apr 26 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-57
- local build

* Thu Apr 14 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-56
- local build

* Wed Mar 23 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-55
- local build

* Tue Mar 15 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-54
- comment out log_driver for rhel8 on copr

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-53
- fix build - don't delete what doesn't exist

* Mon Feb 14 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-52
- temporarily remove dockerfile manpages

* Tue Feb 08 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-51
- update config files

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-50
- Revert "handle md2man dep for c9s"

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-49
- handle md2man dep for c9s

* Wed Feb 02 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-48
- Check for docker manpage existence in %%post

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-47
- resolve docker manpage conflicts

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-46
- no error if man5 exists

* Fri Jan 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-45
- install containerfile and dockerfile manpages

* Wed Jan 26 2022 Daniel J Walsh <dwalsh@redhat.com> 4:1-44
- Update man pages and config files

* Mon Jan 24 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-43
- Depend on container-network-stack and switch to autospec

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> 4:1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-41
- Update to grab latest man pages and configuration files

* Mon Nov 29 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-40
- Update to grab latest man pages and configuration files

* Mon Nov 08 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-39
- Update to grab latest man pages and configuration files

* Thu Oct 21 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-38
- Update to grab latest man pages and configuration files

* Thu Oct 07 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-37
- Update to grab latest man pages and configuration files

* Tue Oct 05 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-36
- Add .containerignore.5 link

* Fri Oct 01 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-35
- Update to grab latest man pages and configuration files

* Sun Sep 26 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-34
- Update to grab latest man pages and configuration files

* Mon Sep 20 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-33
- Update to grab latest man pages and configuration files

* Tue Sep 14 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-32
- Update to grab latest man pages and configuration files

* Wed Sep 08 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-31
- Update to grab latest man pages and configuration files

* Wed Aug 25 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-30
- Add memfd_secret to seccomp.json

* Thu Aug 12 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-29
- Update to grab latest man pages and configuration files

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-28
- Add support for signed RHEL images, enabled by default

* Mon Jul 26 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-27
- Add support for signed RHEL images, enabled by default

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> 4:1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> 4:1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-24
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Tue Jun 29 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> 4:1-23
- containers-common-4:1-21
- fetch latest upstream configs

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-22
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-21
- Update to grab latest man pages and configuration files, also switch to
  using some main rather then master branches

* Thu Jun 10 2021 Daniel J Walsh <dwalsh@redhat.com> 4:1-20
- RPMAUTOSPEC: unresolvable merge
