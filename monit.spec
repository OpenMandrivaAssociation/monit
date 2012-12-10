%define name	monit
%define version	5.3.2
%define rel 1

Summary: 	Process monitor and restart utility
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel %{rel}
License: 	GPLv3+
Source0: 	http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
Source2:	rc.monit
# Config tweaks: enable logging and include /etc/monit.d by default
# AdamW 2010/01
Patch0:		monit-5.1-config.patch
Group: 		Monitoring
URL: 		http://www.tildeslash.com/monit/
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	flex, bison, openssl-devel

%description
Monit is a utility for managing and monitoring processes,
files, directories and devices on a Unix system. Monit conducts
automatic maintenance and repair and can execute meaningful causal
actions in error situations.

%prep
%setup -q
%patch0 -p1 -b .config

%build
%configure2_5x
%make

%install
%makeinstall_std

%__install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}.d
%__install -m 600 monitrc %{buildroot}%{_sysconfdir}/monitrc

%__install -d -m 755 %{buildroot}%{_initrddir}
%__install -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc COPYING README
%config(noreplace) %{_sysconfdir}/monitrc
%dir %{_sysconfdir}/%{name}.d
%{_initrddir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*


%changelog
* Thu Feb 16 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.3.2-1mdv2011.0
+ Revision: 775106
- version update 5.3.2

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.1-3mdv2011.0
+ Revision: 612923
- the mass rebuild of 2010.1 packages

* Mon Apr 19 2010 Funda Wang <fwang@mandriva.org> 5.1.1-2mdv2010.1
+ Revision: 536603
- rebuidl

* Thu Feb 25 2010 Lev Givon <lev@mandriva.org> 5.1.1-1mdv2010.1
+ Revision: 511359
- Update to 5.1.1.
- Update to 5.1.

* Thu Jan 28 2010 Adam Williamson <awilliamson@mandriva.org> 5.0.3-2mdv2010.1
+ Revision: 497711
- add config.patch to tweak config file: enable logging and include
  files in /etc/monit.d by default
- two tweaks to the initscript:
  	+ tell it to actually run as a daemon
  	+ monit should start after every other service in case it's set to
  	  monitor any of them (thanks Scott Storck from monit ML)

* Sat Aug 08 2009 Frederik Himpe <fhimpe@mandriva.org> 5.0.3-1mdv2010.0
+ Revision: 411821
- Update to new version 5.0.3
- Use configuration file included in source tarball
- Add LSB headers to init script

* Tue Feb 05 2008 Lev Givon <lev@mandriva.org> 4.10.1-1mdv2008.1
+ Revision: 162796
- Update to 4.10.1.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 4.9-2mdv2008.1
+ Revision: 119874
- rebuild b/c of missing subpackage on ia32

