Name:           monit
Version:        5.5.1
Release:        1
Summary:        Manages and monitors processes, files, directories and devices
Group:		Monitoring
License:        AGPLv3
URL:            http://www.tildeslash.com/monit
Source0:        http://www.tildeslash.com/monit/dist/monit-%{version}.tar.gz
Source2:        monit.logrotate
Source3:        monit.service
Source4:        monit-logging-conf

BuildRequires: flex
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: byacc
Requires(post):  systemd
Requires(post):  rpm-helper
Requires(preun): rpm-helper

%description
monit is a utility for managing and monitoring, processes, files, directories
and devices on a UNIX system. Monit conducts automatic maintenance and repair
and can execute meaningful causal actions in error situations.

%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

install -p -D -m0600 monitrc %{buildroot}%{_sysconfdir}/monitrc
install -p -D -m0755 monit %{buildroot}%{_bindir}/monit

# Log file & logrotate config
install -p -D -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/monit
mkdir -p %{buildroot}%{_localstatedir}/log
install -m0600 /dev/null %{buildroot}%{_localstatedir}/log/monit.log

# systemd service file
mkdir -p %{buildroot}%{_unitdir}
install -m0644 %{SOURCE3} %{buildroot}%{_unitdir}/monit.service

# Let's include some good defaults
mkdir -p %{buildroot}%{_sysconfdir}/monit.d
install -p -D -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/monit.d/logging

%{__sed} -i 's/# set daemon  120.*/set daemon 60  # check services at 1-minute intervals/' \
    %{buildroot}%{_sysconfdir}/monitrc

%{__sed} -i 's/#  include \/etc\/monit.d\/\*/include \/etc\/monit.d\/\*/' \
    %{buildroot}%{_sysconfdir}/monitrc

%post
%_post_service %{name}

# Moving old style configuration file to upstream's default location
[ -f %{_sysconfdir}/monit.conf ] &&
    touch -r %{_sysconfdir}/monitrc %{_sysconfdir}/monit.conf &&
    mv -f %{_sysconfdir}/monit.conf %{_sysconfdir}/monitrc 2> /dev/null || :

%preun
%_preun_service %{name}

%files
%doc CHANGES COPYING doc/PLATFORMS README
%config(noreplace) %{_sysconfdir}/monitrc
%config(noreplace) %{_sysconfdir}/monit.d/logging
%config(noreplace) %{_sysconfdir}/logrotate.d/monit
%config %ghost %{_localstatedir}/log/monit.log
%{_unitdir}/monit.service
%{_bindir}/%{name}
%{_mandir}/man1/monit.1*
