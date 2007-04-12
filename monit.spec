%define name	monit
%define version	4.9
%define release 1

Summary: 	Process monitor and restart utility
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
License: 	GPL
Source0: 	http://www.tildeslash.com/monit/dist/%{name}-%{version}.tar.bz2
Source1:	monitrc
Source2:	rc.monit
Group: 		Monitoring
URL: 		http://www.tildeslash.com/monit/
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	flex, bison, openssl-devel
BuildRoot: 	%{_tmppath}/%{name}-buildroot

%description
Monit is a utility for managing and monitoring processes,
files, directories and devices on a Unix system. Monit conducts
automatic maintenance and repair and can execute meaningful causal
actions in error situations.

%prep
%setup -q

%build
%configure
%make

%install
%__rm -rf %{buildroot}

%makeinstall \
        MODE_PROGS=755 \
        BINDIR=%{buildroot}%{_bindir} \
        MANDIR=%{buildroot}%{_mandir}/man1

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}.d
install -m 600 %{SOURCE1} %{buildroot}%{_sysconfdir}/monitrc

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES.txt CONTRIBUTORS COPYING FAQ.txt LICENSE README README.SSL STATUS
%config(noreplace) %{_sysconfdir}/monitrc
%dir %{_sysconfdir}/%{name}.d
%{_initrddir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

