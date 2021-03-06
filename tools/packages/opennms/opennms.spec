#
#  $Id$
#
# The version used to be passed from build.xml. It's hardcoded here
# the build system generally passes --define "version X" to rpmbuild.
%{!?version:%define version 1.3.10}
# The release number is set to 0 unless overridden
%{!?releasenumber:%define releasenumber 0}
# The install prefix becomes $OPENMS_HOME in the finished package
%{!?instprefix:%define instprefix /opt/opennms}
# I think this is the directory where the package will be built
%{!?packagedir:%define packagedir opennms-%version-%{releasenumber}}
# This is where the OPENNMS_HOME variable will be set on the remote 
# operating system. Not sure this is needed anymore.
%{!?profiledir:%define profiledir /etc/profile.d}
# This is where the "share" directory will link on RPM-based systems
%{!?sharedir:%define sharedir /var/opennms}
# This is where the "logs" directory will link on RPM-based systems
%{!?logdir:%define logdir /var/log/opennms}
# Where the OpenNMS Jetty webapp lives
%{!?jettydir:%define jettydir %instprefix/jetty-webapps}
# The directory for the OpenNMS webapp
%{!?servletdir:%define servletdir opennms}
# Where OpenNMS binaries live
%{!?bindir:%define bindir %instprefix/bin}

%{!?jdk:%define jdk jdk >= 2000:1.6}

%{!?extrainfo:%define extrainfo }
%{!?extrainfo2:%define extrainfo2 }
%{!?skip_compile:%define skip_compile 0}
%{!?enable_snapshots:%define enable_snapshots 1}

# keep RPM from making an empty debug package
%define debug_package %{nil}
# don't do a bunch of weird redhat post-stuff  :)
%define _use_internal_dependency_generator 0
%define __os_install_post %{nil}
%define __find_requires %{nil}
%define __perl_requires %{nil}
%global _binaries_in_noarch_packages_terminate_build 0
AutoReq: no
AutoProv: no

%define with_tests	0%{nil}
%define with_docs	1%{nil}

Name:			opennms
Summary:		Enterprise-grade Network Management Platform (Easy Install)
Release:		%releasenumber
Version:		%version
License:		LGPL/GPL
Group:			Applications/System
BuildArch:		noarch

Source:			%{name}-source-%{version}-%{releasenumber}.tar.gz
URL:			http://www.opennms.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-root

Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):		opennms-webui      >= %{version}-%{release}
Requires:		opennms-webui      >= %{version}-%{release}
Requires(pre):		opennms-core        = %{version}-%{release}
Requires:		opennms-core        = %{version}-%{release}
Requires(pre):		postgresql-server  >= 8.1
Requires:		postgresql-server  >= 8.1

# don't worry about buildrequires, the shell script will bomb quick  =)
BuildRequires:		%{jdk}

Prefix: %{instprefix}
Prefix: %{sharedir}
Prefix: %{logdir}

%description
OpenNMS is an enterprise-grade network management platform.

This package used to contain what is now in the "opennms-core" package.
It now exists to give a reasonable default installation of OpenNMS.

When you install this package, you will likely also need to install the
webapp package.

%{extrainfo}
%{extrainfo2}


%package core
Summary:	The core OpenNMS backend.
Group:		Applications/System
Requires(pre):	jicmp
Requires:	jicmp
Requires(pre):	jicmp6
Requires:	jicmp6
Requires(pre):	%{jdk}
Requires:	%{jdk}
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-auto-upgrade = %{version}-%{release}
Requires:	opennms-auto-upgrade = %{version}-%{release}
Obsoletes:	opennms < 1.3.11

%description core
The core OpenNMS backend.  This package contains the main OpenNMS
daemon responsible for discovery, polling, data collection, and
notifications (ie, anything that is not part of the web UI).

If you want to be able to view your data, you will need to install
the webapp package.

The logs and data directories are relocatable.  By default, they are:

  logs: %{logdir}
  data: %{sharedir}

If you wish to install them to an alternate location, use the --relocate rpm
option, like so:

  rpm -i --relocate %{logdir}=/mnt/netapp/opennms-logs opennms-core.rpm

%{extrainfo}
%{extrainfo2}


%if %{with_docs}
%package docs
Summary:	Documentation for the OpenNMS network management platform
Group:		Applications/System

%description docs
This package contains the API and user documentation
for OpenNMS.

%{extrainfo}
%{extrainfo2}

%endif

%package remote-poller
Summary:	Remote (Distributed) Poller for OpenNMS
Group:		Applications/System
Requires(pre):	%{jdk}
Requires:	%{jdk}
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp

%description remote-poller
The OpenNMS distributed monitor.  For details, see:
  http://www.opennms.org/index.php/Distributed_Monitoring

%{extrainfo}
%{extrainfo2}


%package jmx-config-generator
Summary:	Generate JMX Configuration
Group:		Applications/System
Requires(pre):	%{jdk}
Requires:	%{jdk}

%description jmx-config-generator
Generates configuration files for monitoring/collecting from
the Java Management Extensions.

%{extrainfo}
%{extrainfo2}


%package webapp-jetty
Summary:	Embedded web interface for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}
Provides:	opennms-webui = %{version}-%{release}
Obsoletes:	opennms-webapp < 1.3.11

%description webapp-jetty
The web UI for OpenNMS.  This is the Jetty version, which runs
embedded in the main OpenNMS core process.

%{extrainfo}
%{extrainfo2}


%package ncs
Summary:	Network Component Services for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-webapp-jetty = %{version}-%{release}
Requires:	opennms-webapp-jetty = %{version}-%{release}

%description ncs
NCS provides a framework for doing correlation of service events across
disparate nodes.

%{extrainfo}
%{extrainfo2}


%package plugins
Summary:	All Plugins for OpenNMS
Group:		Applications/System
Requires(pre):	opennms-plugin-provisioning-dns
Requires:	opennms-plugin-provisioning-dns
Requires(pre):	opennms-plugin-provisioning-link
Requires:	opennms-plugin-provisioning-link
Requires(pre):	opennms-plugin-provisioning-map
Requires:	opennms-plugin-provisioning-map
Requires(pre):	opennms-plugin-provisioning-rancid
Requires:	opennms-plugin-provisioning-rancid
Requires(pre):	opennms-plugin-provisioning-snmp-asset
Requires:	opennms-plugin-provisioning-snmp-asset
Requires(pre):	opennms-plugin-ticketer-centric
Requires:	opennms-plugin-ticketer-centric
Requires(pre):	opennms-plugin-ticketer-jira
Requires:	opennms-plugin-ticketer-jira
Requires(pre):	opennms-plugin-ticketer-otrs
Requires:	opennms-plugin-ticketer-otrs
Requires(pre):	opennms-plugin-ticketer-rt
Requires:	opennms-plugin-ticketer-rt
Requires(pre):	opennms-plugin-protocol-cifs
Requires:	opennms-plugin-protocol-cifs
Requires(pre):	opennms-plugin-protocol-dhcp
Requires:	opennms-plugin-protocol-dhcp
Requires(pre):	opennms-plugin-protocol-nsclient
Requires:	opennms-plugin-protocol-nsclient
Requires(pre):	opennms-plugin-protocol-radius
Requires:	opennms-plugin-protocol-radius
Requires(pre):	opennms-plugin-protocol-xml
Requires:	opennms-plugin-protocol-xml
Requires(pre):	opennms-plugin-protocol-xmp
Requires:	opennms-plugin-protocol-xmp

%description plugins
This installs all optional plugins for OpenNMS.

%{extrainfo}
%{extrainfo2}


%package plugin-provisioning-dns
Summary:	DNS Provisioning Adapter for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-provisioning-dns
The DNS provisioning adapter allows for updating dynamic DNS records based on
provisioned nodes.

%{extrainfo}
%{extrainfo2}


%package plugin-provisioning-link
Summary:	Link Provisioning Adapter for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-provisioning-link
The link provisioning adapter creates links between provisioned nodes based on naming
conventions defined in the link-adapter-configuration.xml file.  It also updates the
status of the map links based on data link events.

%{extrainfo}
%{extrainfo2}


%package plugin-provisioning-map
Summary:	Map Provisioning Adapter for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-provisioning-map
The map provisioning adapter will automatically create maps when nodes are provisioned
in OpenNMS.

%{extrainfo}
%{extrainfo2}


%package plugin-provisioning-rancid
Summary:	RANCID Provisioning Adapter for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-provisioning-rancid
The RANCID provisioning adapter coordinates with the RANCID Web Service by updating
RANCID's device database when OpenNMS provisions nodes.

%{extrainfo}
%{extrainfo2}


%package plugin-provisioning-snmp-asset
Summary:	SNMP Asset Provisioning Adapter for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-provisioning-snmp-asset
The SNMP asset provisioning adapter responds to provisioning events by updating asset
fields with data fetched from SNMP GET requests.

%{extrainfo}
%{extrainfo2}


%package plugin-ticketer-jira
Summary:       JIRA Ticketer Plugin for OpenNMS
Group:         Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre): opennms-core = %{version}-%{release}
Requires:      opennms-core = %{version}-%{release}

%description plugin-ticketer-jira
The JIRA ticketer plugin provides the ability to automatically create JIRA
issues from OpenNMS alarms.

%{extrainfo}
%{extrainfo2}


%package plugin-ticketer-otrs
Summary:       OTRS Ticketer Plugin for OpenNMS
Group:         Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre): opennms-core = %{version}-%{release}
Requires:      opennms-core = %{version}-%{release}

%description plugin-ticketer-otrs
The OTRS ticketer plugin provides the ability to automatically create OTRS
issues from OpenNMS alarms.

%{extrainfo}
%{extrainfo2}


%package plugin-ticketer-rt
Summary:       RT Ticketer Plugin for OpenNMS
Group:         Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre): opennms-core = %{version}-%{release}
Requires:      opennms-core = %{version}-%{release}

%description plugin-ticketer-rt
The RT ticketer plugin provides the ability to automatically create RT
tickets from OpenNMS alarms.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-cifs
Summary:	CIFS Poller Plugin for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-cifs
The CIFS protocol plugin provides a poller monitor for CIFS network shares.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-dhcp
Summary:	DHCP Poller and Detector Plugin for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-dhcp
The DHCP protocol plugin provides a daemon, provisioning detector, capsd plugin, and
poller monitor for DHCP.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-nsclient
Summary:	NSCLIENT Plugin Support for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-nsclient
The NSClient protocol plugin provides a capsd plugin and poller monitor for NSClient
and NSClient++.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-radius
Summary:	RADIUS Plugin Support for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-radius
The RADIUS protocol plugin provides a provisioning detector, capsd plugin, poller
monitor, and Spring Security authorization mechanism for RADIUS.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-xml
Summary:	XML Collector for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-xml
The XML protocol plugin provides a collector for XML data.

%{extrainfo}
%{extrainfo2}


%package plugin-protocol-xmp
Summary:	XMP Poller for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-protocol-xmp
The XMP protocol plugin provides a capsd plugin and poller monitor for XMP.

%{extrainfo}
%{extrainfo2}


%package plugin-collector-juniper-tca
Summary:	Juniper TCA Collector for OpenNMS
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	opennms-core = %{version}-%{release}
Requires:	opennms-core = %{version}-%{release}

%description plugin-collector-juniper-tca
The Juniper JCA collector provides a collector plugin for Collectd to collect data from TCA devices.

%{extrainfo}
%{extrainfo2}


%package auto-upgrade
Summary:	OpenNMS Upgrade Package
Group:		Applications/System
Requires(pretrans):	/bin/sh, /bin/mv, /bin/cp
Requires(pre):	rpm
Requires(post):	git >= 1.7, perl(Carp), perl(Cwd), perl(Error), perl(File::Basename), perl(File::Copy), perl(File::Find), perl(File::Path), perl(File::Slurp), perl(File::Spec), perl(File::Temp), perl(File::stat), perl(Getopt::Long), perl(Git), perl(IO::Handle), perl(Test::More)

%description auto-upgrade
Tools to deal with upgrading from a previous OpenNMS release.

%{extrainfo}
%{extrainfo2}


%prep

tar -xvzf $RPM_SOURCE_DIR/%{name}-source-%{version}-%{release}.tar.gz -C $RPM_BUILD_DIR
%define setupdir %{packagedir}

%setup -D -T -n %setupdir

##############################################################################
# building
##############################################################################

%build
rm -rf $RPM_BUILD_ROOT

pushd opennms-base-assembly/src/main/resources/contrib/config-tools
perl Makefile.PL PREFIX="%{_prefix}" INSTALLDIRS="vendor"
make

# nothing necessary

##############################################################################
# installation
##############################################################################

%install
#
# This next bit is to keep gprintify.py on Mandriva/Mandrake from screwing
# up the "echo" statements in the opennms init script.  See:
#	http://qa.mandriva.com/twiki/bin/view/Main/InitscriptHowto?skin=print
#
DONT_GPRINTIFY="yes, please do not"
export DONT_GPRINTIFY

export EXTRA_OPTIONS=""
if [ -e "settings.xml" ]; then
	export EXTRA_OPTIONS="-s `pwd`/settings.xml"
fi

if [ "%{skip_compile}" = 1 ]; then
	echo "=== SKIPPING COMPILE ==="
	if [ "%{enable_snapshots}" = 1 ]; then
		export EXTRA_OPTIONS="$EXTRA_OPTIONS -Denable.snapshots=true -DupdatePolicy=always"
	fi
	TOPDIR=`pwd`
	for dir in . opennms-tools; do
		pushd $dir
			"$TOPDIR"/compile.pl -N $EXTRA_OPTIONS -Dinstall.version="%{version}-%{release}" -Ddist.name="$RPM_BUILD_ROOT" -Dopennms.home="%{instprefix}" install
		popd
	done
else
	echo "=== RUNNING COMPILE ==="
	./compile.pl $EXTRA_OPTIONS -Dbuild=all -Dinstall.version="%{version}-%{release}" -Ddist.name="$RPM_BUILD_ROOT" \
	    -Dopennms.home="%{instprefix}" install
fi

echo "=== BUILDING ASSEMBLIES ==="
./assemble.pl $EXTRA_OPTIONS -Dbuild=all -Dinstall.version="%{version}-%{release}" -Ddist.name="$RPM_BUILD_ROOT" \
	-Dopennms.home="%{instprefix}" -Dbuild.profile=full install

pushd opennms-tools
	../compile.pl $EXTRA_OPTIONS -N -Dinstall.version="%{version}-%{release}" -Ddist.name="$RPM_BUILD_ROOT" \
	-Dopennms.home="%{instprefix}" install
popd

TOOLDIR="%{bindir}/config-tools"
pushd opennms-base-assembly/src/main/resources/contrib/config-tools
	make install PREFIX="$RPM_BUILD_ROOT%{_prefix}" INSTALLDIRS="vendor"
	find "$RPM_BUILD_ROOT%{_prefix}" -name perllocal.pod -exec rm -rf {} \;
	install -d -m 755 "$RPM_BUILD_ROOT$TOOLDIR"
	mv "$RPM_BUILD_ROOT%{_bindir}"/*.pl "$RPM_BUILD_ROOT$TOOLDIR"/
	cd "$RPM_BUILD_ROOT$TOOLDIR"
	ln -s opennms-pretrans.pl opennms-pre.pl
popd

echo "=== INSTALL COMPLETED ==="

echo "=== UNTAR BUILD ==="

mkdir -p $RPM_BUILD_ROOT%{instprefix}

tar zxvf $RPM_BUILD_DIR/%{name}-%{version}-%{release}/target$RPM_BUILD_ROOT.tar.gz -C $RPM_BUILD_ROOT%{instprefix}

echo "=== UNTAR BUILD COMPLETED ==="

### XXX is this needed?  (Most of) the current scripts don't use OPENNMS_HOME.
### /etc/profile.d

mkdir -p $RPM_BUILD_ROOT%{profiledir}
cat > $RPM_BUILD_ROOT%{profiledir}/%{name}.sh << END
#!/bin/bash

OPENNMS_HOME=%{instprefix}
if ! echo "\$PATH" | grep "\$OPENNMS_HOME/bin" >/dev/null 2>&1; then
	PATH="\$PATH:\$OPENNMS_HOME/bin"
fi

export OPENNMS_HOME PATH

END

%if %{with_docs}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr $RPM_BUILD_DIR/%{name}-%{version}-%{release}/opennms-doc/target/docbkx/html/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
rm -rf $RPM_BUILD_ROOT%{instprefix}/docs
cp README* $RPM_BUILD_ROOT%{instprefix}/etc/
rm -rf $RPM_BUILD_ROOT%{instprefix}/etc/README
rm -rf $RPM_BUILD_ROOT%{instprefix}/etc/README.build
%endif

install -d -m 755 $RPM_BUILD_ROOT%{logdir}
mv $RPM_BUILD_ROOT%{instprefix}/logs/.readme $RPM_BUILD_ROOT%{logdir}/
rm -rf $RPM_BUILD_ROOT%{instprefix}/logs

install -d -m 755 $RPM_BUILD_ROOT%{sharedir}
mv $RPM_BUILD_ROOT%{instprefix}/share/* $RPM_BUILD_ROOT%{sharedir}/
rm -rf $RPM_BUILD_ROOT%{instprefix}/share

rsync -avr --exclude=examples $RPM_BUILD_ROOT%{instprefix}/etc/ $RPM_BUILD_ROOT%{sharedir}/etc-pristine/
chmod -R go-w $RPM_BUILD_ROOT%{sharedir}/etc-pristine/

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 755 $RPM_BUILD_ROOT%{instprefix}/contrib/remote-poller/remote-poller.init      $RPM_BUILD_ROOT%{_initrddir}/opennms-remote-poller
install -m 640 $RPM_BUILD_ROOT%{instprefix}/contrib/remote-poller/remote-poller.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/opennms-remote-poller
rm -rf $RPM_BUILD_ROOT%{instprefix}/contrib/remote-poller

rm -rf $RPM_BUILD_ROOT%{instprefix}/lib/*.tar.gz

# core package files
find $RPM_BUILD_ROOT%{instprefix}/etc ! -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,%config(noreplace) ," | \
	grep -v '%{_initrddir}/opennms-remote-poller' | \
	grep -v '%{_sysconfdir}/sysconfig/opennms-remote-poller' | \
	grep -v 'ncs-northbounder-configuration.xml' | \
	grep -v 'drools-engine.d/ncs' | \
	grep -v '3gpp' | \
	grep -v 'dhcpd-configuration.xml' | \
	grep -v 'endpoint-configuration.xml' | \
	grep -v 'jira.properties' | \
	grep -v 'link-adapter-configuration.xml' | \
	grep -v 'mapsadapter-configuration.xml' | \
	grep -v 'nsclient-config.xml' | \
	grep -v 'nsclient-datacollection-config.xml' | \
	grep -v 'otrs.properties' | \
	grep -v '/rt.properties' | \
	grep -v 'snmp-asset-adapter-configuration.xml' | \
	grep -v 'xml-datacollection-config.xml' | \
	grep -v 'xmp-config.xml' | \
	grep -v 'xmp-datacollection-config.xml' | \
	grep -v 'tca-datacollection-config.xml' | \
	grep -v 'juniper-tca' | \
	grep -v -E '.jasper$' | \
	sort > %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{instprefix}/etc ! -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,," | \
	grep -E '.jasper$' | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{sharedir}/etc-pristine ! -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,," | \
	grep -v '%{_initrddir}/opennms-remote-poller' | \
	grep -v '%{_sysconfdir}/sysconfig/opennms-remote-poller' | \
	grep -v 'ncs-northbounder-configuration.xml' | \
	grep -v 'ncs.xml' | \
	grep -v 'drools-engine.d/ncs' | \
	grep -v '3gpp' | \
	grep -v 'dhcpd-configuration.xml' | \
	grep -v 'endpoint-configuration.xml' | \
	grep -v 'jira.properties' | \
	grep -v 'link-adapter-configuration.xml' | \
	grep -v 'mapsadapter-configuration.xml' | \
	grep -v 'nsclient-config.xml' | \
	grep -v 'nsclient-datacollection-config.xml' | \
	grep -v 'otrs.properties' | \
	grep -v '/rt.properties' | \
	grep -v 'snmp-asset-adapter-configuration.xml' | \
	grep -v 'xml-datacollection-config.xml' | \
	grep -v 'xmp-config.xml' | \
	grep -v 'xmp-datacollection-config.xml' | \
	grep -v 'tca-datacollection-config.xml' | \
	grep -v 'juniper-tca' | \
	sort > %{_tmppath}/files.pristine.opennms-core
find $RPM_BUILD_ROOT%{instprefix}/bin ! -type d | \
	sed -e "s|^$RPM_BUILD_ROOT|%attr(755,root,root) |" | \
	grep -v '/jmx-config-generator' | \
	grep -v '/remote-poller.sh' | \
	grep -v '/remote-poller.jar' | \
	grep -v 'bin/config-tools' | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{sharedir} ! -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,," | \
	grep -v 'etc-pristine' | \
	grep -v 'ncs-' | \
	grep -v 'nsclient-config.xsd' | \
	grep -v 'nsclient-datacollection.xsd' | \
	grep -v 'xmp-config.xsd' | \
	grep -v 'xmp-datacollection-config.xsd' | \
	grep -v 'tca-datacollection-config.xml' | \
	grep -v 'juniper-tca' | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{instprefix}/contrib ! -type d | \
	sed -e "s|^$RPM_BUILD_ROOT|%attr(755,root,root) |" | \
	grep -v 'xml-collector' | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{instprefix}/lib ! -type d | \
	sed -e "s|^$RPM_BUILD_ROOT|%attr(755,root,root) |" | \
	grep -v 'ncs-' | \
	grep -v 'provisioning-adapter' | \
	grep -v 'org.opennms.protocols.cifs' | \
	grep -v 'org.opennms.protocols.dhcp' | \
	grep -v 'jdhcp' | \
	grep -v 'jira' | \
	grep -v 'org.opennms.protocols.nsclient' | \
	grep -v 'org.opennms.protocols.radius' | \
	grep -v 'gnu-crypto' | \
	grep -v 'jradius' | \
	grep -v 'opennms-integration-otrs' | \
	grep -v 'opennms-integration-rt' | \
	grep -v 'org.opennms.protocols.xml' | \
	grep -v 'org.opennms.protocols.xmp' | \
	grep -v 'xmp' | \
	grep -v 'org.opennms.features.juniper-tca-collector' | \
	grep -v 'opennms_jmx_config_generator' | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{instprefix}/etc -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,%dir ," | \
	sort >> %{_tmppath}/files.main
find $RPM_BUILD_ROOT%{instprefix}/system ! -type d | \
	sed -e "s|^$RPM_BUILD_ROOT|%attr(755,root,root) |" | \
	sort >> %{_tmppath}/files.main

# jetty
find $RPM_BUILD_ROOT%{jettydir} ! -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,," | \
	grep -v '/WEB-INF/[^/]*\.xml$' | \
	grep -v '/WEB-INF/[^/]*\.properties$' | \
	grep -v '/WEB-INF/jsp/alarm/ncs' | \
	grep -v '/WEB-INF/jsp/ncs/' | \
	grep -v '/WEB-INF/lib/ncs' | \
	sort >> %{_tmppath}/files.jetty
find $RPM_BUILD_ROOT%{jettydir}/*/WEB-INF/*.xml | \
	sed -e "s,^$RPM_BUILD_ROOT,%config ," | \
	grep -v '/WEB-INF/ncs' | \
	sort >> %{_tmppath}/files.jetty
find $RPM_BUILD_ROOT%{jettydir} -type d | \
	sed -e "s,^$RPM_BUILD_ROOT,%dir ," | \
	sort >> %{_tmppath}/files.jetty

# add the opennms-core ones to main
cat %{_tmppath}/files.pristine.opennms-core >> %{_tmppath}/files.main

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/drools-engine.d/ncs"/* \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/ncs-northbounder-configuration.xml" | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-ncs

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/link-adapter-configuration.xml" \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/endpoint-configuration.xml" | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-provisioning-link

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/mapsadapter-configuration.xml" | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-provisioning-map

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/snmp-asset-adapter-configuration.xml" | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-provisioning-snmp-asset

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/dhcp*.xml | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-protocol-dhcp

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/jira.* | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-ticketer-jira

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/otrs.* | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-ticketer-otrs

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/rt.* | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-ticketer-rt

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/nsclient*.xml | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-protocol-nsclient

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/xml-*.xml \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/*datacollection*/3gpp* \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/snmp-graph.properties.d"/3gpp* | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-protocol-xml

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/xmp*.xml | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-protocol-xmp

find "$RPM_BUILD_ROOT%{sharedir}/etc-pristine"/tca*.xml \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/datacollection"/juniper-tca* \
     "$RPM_BUILD_ROOT%{sharedir}/etc-pristine/snmp-graph.properties.d"/juniper-tca* | \
     sed -e "s,^$RPM_BUILD_ROOT,," > %{_tmppath}/files.pristine.opennms-plugin-collector-juniper-tca

%clean
rm -rf $RPM_BUILD_ROOT

##############################################################################
# file setup
##############################################################################

%files
%defattr(664 root root 775)
%{instprefix}/etc/examples/Juniper/mcg/3gpp.kpis.xml
%{instprefix}/etc/examples/Juniper/mcg/MCG-xml-datacollection-config.xml
%{instprefix}/etc/examples/Juniper/mcg/MCG-collectd-configuration.xml

%files core -f %{_tmppath}/files.main
%defattr(664 root root 775)
%attr(755,root,root)	%{profiledir}/%{name}.sh
%attr(755,root,root) %{logdir}
			%{instprefix}/data
			%{instprefix}/deploy

%if %{with_docs}
%files docs
%defattr(644 root root 755)
%{_docdir}/%{name}-%{version}
%endif

%files remote-poller
%attr(755,root,root) %config %{_initrddir}/opennms-remote-poller
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/opennms-remote-poller
%attr(755,root,root) %{bindir}/remote-poller.sh
%{instprefix}/bin/remote-poller.jar

%files jmx-config-generator
%attr(755,root,root) %{bindir}/jmx-config-generator
%{instprefix}/lib/opennms_jmx_config_generator.jar

%files ncs -f %{_tmppath}/files.pristine.opennms-ncs
%defattr(644 root root 755)
%{instprefix}/lib/ncs-*.jar
%{jettydir}/%{servletdir}/WEB-INF/lib/ncs-*
%config(noreplace) %{instprefix}/etc/drools-engine.d/ncs/*
%config(noreplace) %{instprefix}/etc/ncs-northbounder-configuration.xml
%{sharedir}/xsds/ncs-*.xsd
%config %{jettydir}/%{servletdir}/WEB-INF/ncs*.xml
%config %{jettydir}/%{servletdir}/WEB-INF/jsp/alarm/ncs-*
%config %{jettydir}/%{servletdir}/WEB-INF/jsp/ncs
%dir %{sharedir}/etc-pristine/drools-engine.d/ncs
%{sharedir}/etc-pristine/drools-engine.d/ncs/*
%{sharedir}/etc-pristine/ncs-northbounder-configuration.xml

%files webapp-jetty -f %{_tmppath}/files.jetty
%defattr(644 root root 755)
#%config %{jettydir}/opennms-remoting/WEB-INF/*.xml
%config %{jettydir}/%{servletdir}/WEB-INF/*.properties

%files plugins

%files plugin-provisioning-dns
%defattr(664 root root 775)
%{instprefix}/lib/opennms-dns-provisioning-adapter*.jar

%files plugin-provisioning-link -f %{_tmppath}/files.pristine.opennms-plugin-provisioning-link
%defattr(664 root root 775)
%{instprefix}/lib/opennms-link-provisioning-adapter*.jar
%config(noreplace) %{instprefix}/etc/link-adapter-configuration.xml
%config(noreplace) %{instprefix}/etc/endpoint-configuration.xml
%{sharedir}/etc-pristine/link-adapter-configuration.xml
%{sharedir}/etc-pristine/endpoint-configuration.xml

%files plugin-provisioning-map -f %{_tmppath}/files.pristine.opennms-plugin-provisioning-map
%defattr(664 root root 775)
%{instprefix}/lib/opennms-map-provisioning-adapter*.jar
%{instprefix}/etc/examples/mapsadapter-configuration.xml
%config(noreplace) %{instprefix}/etc/mapsadapter-configuration.xml
%{sharedir}/etc-pristine/mapsadapter-configuration.xml

%files plugin-provisioning-rancid
%defattr(664 root root 775)
%{instprefix}/lib/opennms-rancid-provisioning-adapter*.jar

%files plugin-provisioning-snmp-asset -f %{_tmppath}/files.pristine.opennms-plugin-provisioning-snmp-asset
%defattr(664 root root 775)
%{instprefix}/lib/opennms-snmp-asset-provisioning-adapter*.jar
%config(noreplace) %{instprefix}/etc/snmp-asset-adapter-configuration.xml
%{sharedir}/etc-pristine/snmp-asset-adapter-configuration.xml

%files plugin-protocol-cifs
%defattr(664 root root 775)
%{instprefix}/lib/org.opennms.protocols.cifs*.jar

%files plugin-ticketer-jira -f %{_tmppath}/files.pristine.opennms-plugin-ticketer-jira
%defattr(664 root root 775)
%{instprefix}/lib/jira-*.jar
%config(noreplace) %{instprefix}/etc/jira.properties
%{sharedir}/etc-pristine/jira.properties

%files plugin-ticketer-otrs -f %{_tmppath}/files.pristine.opennms-plugin-ticketer-otrs
%defattr(664 root root 775)
%{instprefix}/lib/opennms-integration-otrs-*.jar
%config(noreplace) %{instprefix}/etc/otrs.properties
%{sharedir}/etc-pristine/otrs.properties

%files plugin-ticketer-rt -f %{_tmppath}/files.pristine.opennms-plugin-ticketer-rt
%defattr(664 root root 775)
%{instprefix}/lib/opennms-integration-rt-*.jar
%config(noreplace) %{instprefix}/etc/rt.properties
%{sharedir}/etc-pristine/rt.properties

%files plugin-protocol-dhcp -f %{_tmppath}/files.pristine.opennms-plugin-protocol-dhcp
%defattr(664 root root 775)
%config(noreplace) %{instprefix}/etc/dhcp*.xml
%{instprefix}/lib/jdhcp-*.jar
%{instprefix}/lib/org.opennms.protocols.dhcp*.jar
%{sharedir}/etc-pristine/dhcp*.xml
%{sharedir}/xsds/dhcp*.xsd

%files plugin-protocol-nsclient -f %{_tmppath}/files.pristine.opennms-plugin-protocol-nsclient
%defattr(664 root root 775)
%config(noreplace) %{instprefix}/etc/nsclient*.xml
%{instprefix}/etc/examples/nsclient*.xml
%{instprefix}/lib/org.opennms.protocols.nsclient*.jar
%{sharedir}/etc-pristine/nsclient*.xml
%{sharedir}/xsds/nsclient*.xsd

%files plugin-protocol-radius
%defattr(664 root root 775)
%{instprefix}/lib/gnu-crypto*.jar
%{instprefix}/lib/jradius-*.jar
%{instprefix}/lib/org.opennms.protocols.radius*.jar

%files plugin-protocol-xml -f %{_tmppath}/files.pristine.opennms-plugin-protocol-xml
%defattr(664 root root 775)
%config(noreplace) %{instprefix}/etc/xml-*.xml
%config(noreplace) %{instprefix}/etc/*datacollection*/3gpp*
%config(noreplace) %{instprefix}/etc/snmp-graph.properties.d/3gpp*
%{instprefix}/lib/org.opennms.protocols.xml-*.jar
%attr(755,root,root) %{instprefix}/contrib/xml-collector/*.pl
%{sharedir}/etc-pristine/xml-*.xml
%{sharedir}/etc-pristine/*datacollection*/3gpp*
%{sharedir}/etc-pristine/snmp-graph.properties.d/3gpp*

%files plugin-protocol-xmp -f %{_tmppath}/files.pristine.opennms-plugin-protocol-xmp
%defattr(664 root root 775)
%config(noreplace) %{instprefix}/etc/xmp*.xml
%{instprefix}/lib/org.opennms.protocols.xmp-*.jar
%{instprefix}/lib/xmp-*.jar
%{sharedir}/etc-pristine/xmp*.xml
%{sharedir}/xsds/xmp*.xsd

%files plugin-collector-juniper-tca -f %{_tmppath}/files.pristine.opennms-plugin-collector-juniper-tca
%defattr(664 root root 775)
%config(noreplace) %{instprefix}/etc/tca*.xml
%config(noreplace) %{instprefix}/etc/datacollection/juniper-tca*
%config(noreplace) %{instprefix}/etc/snmp-graph.properties.d/juniper-tca*
%{instprefix}/lib/org.opennms.features.juniper-tca-collector-*.jar
%{sharedir}/etc-pristine/tca*.xml
%{sharedir}/etc-pristine/datacollection/juniper-tca*
%{sharedir}/etc-pristine/snmp-graph.properties.d/juniper-tca*

%files auto-upgrade
%defattr(644 root root 755)
%attr(755,root,root) %{bindir}/config-tools/*.pl
%{perl_vendorlib}
%{perl_vendorarch}
%{_mandir}/man3/OpenNMS::Config*

%pre auto-upgrade
rpm -q --queryformat='\%{version}-\%{release}' opennms-core 2>/dev/null | grep -v 'is not installed' | sort -u | head -n 1 > /tmp/git-setup.opennms-core

%post auto-upgrade
"$RPM_INSTALL_PREFIX0/bin/config-tools/git-setup.pl" "$RPM_INSTALL_PREFIX0" "opennms-core" "%{version}-%{release}" 1>&2

%post docs
printf -- "- making symlink for $RPM_INSTALL_PREFIX0/docs... "
if [ -e "$RPM_INSTALL_PREFIX0/docs" ] && [ ! -L "$RPM_INSTALL_PREFIX0/docs" ]; then
	echo "failed: $RPM_INSTALL_PREFIX0/docs is a real directory, but it should be a symlink to %{_docdir}/%{name}-%{version}."
else
	rm -rf "$RPM_INSTALL_PREFIX0/docs"
	ln -sf "%{_docdir}/%{name}-%{version}" "$RPM_INSTALL_PREFIX0/docs"
	echo "done"
fi

%postun docs
if [ "$1" = 0 ]; then
	if [ -L "$RPM_INSTALL_PREFIX0/docs" ]; then
		rm -f "$RPM_INSTALL_PREFIX0/docs"
	fi
fi

%pretrans core
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-core" "%{version}-%{release}" 1>&2

%pre core
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-core" "%{version}-%{release}" 1>&2

# clean out old jasper files
rpm -ql opennms-core | grep -v 'etc-pristine' | grep -v '/subreports/' | grep -E '.jasper$' | while read FILE; do
	echo "- deleting compiled jasper file $FILE..."
	rm -f "$FILE" || :
done

%post core
if [ -n "$DEBUG" ]; then
	env | grep RPM_INSTALL_PREFIX | sort -u
fi

if [ "$RPM_INSTALL_PREFIX0/logs" != "$RPM_INSTALL_PREFIX2" ]; then
	printf -- "- making symlink for $RPM_INSTALL_PREFIX0/logs... "
	if [ -e "$RPM_INSTALL_PREFIX0/logs" ] && [ ! -L "$RPM_INSTALL_PREFIX0/logs" ]; then
		echo "failed: $RPM_INSTALL_PREFIX0/logs is a real directory or file, but it should be a symlink to $RPM_INSTALL_PREFIX2."
		echo "Your OpenNMS install may not function properly."
	else
		rm -rf "$RPM_INSTALL_PREFIX0/logs"
		ln -sf "$RPM_INSTALL_PREFIX2" "$RPM_INSTALL_PREFIX0/logs"
		echo "done"
	fi
fi

if [ "$RPM_INSTALL_PREFIX0/share" != "$RPM_INSTALL_PREFIX1" ]; then
	printf -- "- making symlink for $RPM_INSTALL_PREFIX0/share... "
	if [ -e "$RPM_INSTALL_PREFIX0/share" ] && [ ! -L "$RPM_INSTALL_PREFIX0/share" ]; then
		echo "failed: $RPM_INSTALL_PREFIX0/share is a real directory, but it should be a symlink to $RPM_INSTALL_PREFIX1."
		echo "Your OpenNMS install may not function properly."
	else
		rm -rf "$RPM_INSTALL_PREFIX0/share"
		ln -sf "$RPM_INSTALL_PREFIX1" "$RPM_INSTALL_PREFIX0/share"
		echo "done"
	fi
fi

printf -- "- moving *.sql.rpmnew files (if any)... "
if [ `ls $RPM_INSTALL_PREFIX0/etc/*.sql.rpmnew 2>/dev/null | wc -l` -gt 0 ]; then
	for i in $RPM_INSTALL_PREFIX0/etc/*.sql.rpmnew; do
		mv $i ${i%%%%.rpmnew}
	done
fi
echo "done"

printf -- "- checking for old update files... "

JAR_UPDATES=`find $RPM_INSTALL_PREFIX0/lib/updates -name \*.jar   -exec rm -rf {} \; -print 2>/dev/null | wc -l`
CLASS_UPDATES=`find $RPM_INSTALL_PREFIX0/lib/updates -name \*.class -exec rm -rf {} \; -print 2>/dev/null | wc -l`
let TOTAL_UPDATES=`expr $JAR_UPDATES + $CLASS_UPDATES`
if [ "$TOTAL_UPDATES" -gt 0 ]; then
	echo "FOUND"
	echo ""
	echo "WARNING: $TOTAL_UPDATES old update files were found in your"
	echo "$RPM_INSTALL_PREFIX0/lib/updates directory.  They have been deleted"
	echo "because they should now be out of date."
	echo ""
else
	echo "done"
fi

rm -f $RPM_INSTALL_PREFIX0/etc/configured
for dir in /etc /etc/rc.d; do
	if [ -d "$dir" ]; then
		ln -sf $RPM_INSTALL_PREFIX0/bin/opennms $dir/init.d/opennms
		break
	fi
done

for LIBNAME in jicmp jicmp6 jrrd; do
	if [ `grep "opennms.library.${LIBNAME}" "$RPM_INSTALL_PREFIX0/etc/libraries.properties" 2>/dev/null | wc -l` -eq 0 ]; then
		LIBRARY_PATH=`rpm -ql "${LIBNAME}" 2>/dev/null | grep "/lib${LIBNAME}.so\$" | head -n 1`
		if [ -n "$LIBRARY_PATH" ]; then
			echo "opennms.library.${LIBNAME}=${LIBRARY_PATH}" >> "$RPM_INSTALL_PREFIX0/etc/libraries.properties"
		fi
	fi
done

"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-core" "%{version}-%{release}" 1>&2

printf -- "- cleaning up \$OPENNMS_HOME/data... "
if [ -d "$RPM_INSTALL_PREFIX0/data" ]; then
	rm -rf "$RPM_INSTALL_PREFIX0/data"
fi
echo "done"

echo ""
echo " *** Installation complete.  You must still run the installer at"
echo " *** \$OPENNMS_HOME/bin/install to be sure your database is up"
echo " *** to date before you start OpenNMS.  See the install guide at"
echo " *** http://www.opennms.org/wiki/Installation:RPM and the"
echo " *** release notes for details."
echo ""

%posttrans core
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-core" "%{version}-%{release}" 1>&2

%postun core

if [ "$1" = 0 ]; then
	for dir in logs share; do
		if [ -L "$RPM_INSTALL_PREFIX0/$dir" ]; then
			rm -f "$RPM_INSTALL_PREFIX0/$dir"
		fi
	done
fi

%pretrans remote-poller
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-remote-poller" "%{version}-%{release}" 1>&2

%pre remote-poller
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-remote-poller" "%{version}-%{release}" 1>&2

%post remote-poller
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "remote-poller" "%{version}-%{release}" 1>&2

%posttrans remote-poller
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-remote-poller" "%{version}-%{release}" 1>&2

%pretrans webapp-jetty
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-webapp-jetty" "%{version}-%{release}" 1>&2

%pre webapp-jetty
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-webapp-jetty" "%{version}-%{release}" 1>&2

%post webapp-jetty
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "webapp-jetty" "%{version}-%{release}" 1>&2

%posttrans webapp-jetty
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-webapp-jetty" "%{version}-%{release}" 1>&2

%pretrans ncs
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-ncs" "%{version}-%{release}" 1>&2

%pre ncs
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-ncs" "%{version}-%{release}" 1>&2

%post ncs
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "ncs" "%{version}-%{release}" 1>&2

%posttrans ncs
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-ncs" "%{version}-%{release}" 1>&2

%pretrans plugin-provisioning-dns
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-dns" "%{version}-%{release}" 1>&2

%pre plugin-provisioning-dns
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-dns" "%{version}-%{release}" 1>&2

%post plugin-provisioning-dns
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-dns" "%{version}-%{release}" 1>&2

%posttrans plugin-provisioning-dns
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-dns" "%{version}-%{release}" 1>&2

%pretrans plugin-provisioning-link
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-link" "%{version}-%{release}" 1>&2

%pre plugin-provisioning-link
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-link" "%{version}-%{release}" 1>&2

%post plugin-provisioning-link
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-link" "%{version}-%{release}" 1>&2

%posttrans plugin-provisioning-link
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-link" "%{version}-%{release}" 1>&2

%pretrans plugin-provisioning-map
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-map" "%{version}-%{release}" 1>&2

%pre plugin-provisioning-map
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-map" "%{version}-%{release}" 1>&2

%post plugin-provisioning-map
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-map" "%{version}-%{release}" 1>&2

%posttrans plugin-provisioning-map
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-map" "%{version}-%{release}" 1>&2

%pretrans plugin-provisioning-rancid
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-rancid" "%{version}-%{release}" 1>&2

%pre plugin-provisioning-rancid
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-rancid" "%{version}-%{release}" 1>&2

%post plugin-provisioning-rancid
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-rancid" "%{version}-%{release}" 1>&2

%posttrans plugin-provisioning-rancid
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-rancid" "%{version}-%{release}" 1>&2

%pretrans plugin-provisioning-snmp-asset
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-snmp-asset" "%{version}-%{release}" 1>&2

%pre plugin-provisioning-snmp-asset
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-snmp-asset" "%{version}-%{release}" 1>&2

%post plugin-provisioning-snmp-asset
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-snmp-asset" "%{version}-%{release}" 1>&2

%posttrans plugin-provisioning-snmp-asset
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-provisioning-snmp-asset" "%{version}-%{release}" 1>&2

%pretrans plugin-ticketer-jira
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-jira" "%{version}-%{release}" 1>&2

%pre plugin-ticketer-jira
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-jira" "%{version}-%{release}" 1>&2

%post plugin-ticketer-jira
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-jira" "%{version}-%{release}" 1>&2

%posttrans plugin-ticketer-jira
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-jira" "%{version}-%{release}" 1>&2

%pretrans plugin-ticketer-otrs
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-otrs" "%{version}-%{release}" 1>&2

%pre plugin-ticketer-otrs
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-otrs" "%{version}-%{release}" 1>&2

%post plugin-ticketer-otrs
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-otrs" "%{version}-%{release}" 1>&2

%posttrans plugin-ticketer-otrs
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-otrs" "%{version}-%{release}" 1>&2

%pretrans plugin-ticketer-rt
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-rt" "%{version}-%{release}" 1>&2

%pre plugin-ticketer-rt
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-rt" "%{version}-%{release}" 1>&2

%post plugin-ticketer-rt
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-rt" "%{version}-%{release}" 1>&2

%posttrans plugin-ticketer-rt
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-ticketer-rt" "%{version}-%{release}" 1>&2

%pretrans plugin-protocol-dhcp
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-dhcp" "%{version}-%{release}" 1>&2

%pre plugin-protocol-dhcp
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-dhcp" "%{version}-%{release}" 1>&2

%post plugin-protocol-dhcp
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-dhcp" "%{version}-%{release}" 1>&2

%posttrans plugin-protocol-dhcp
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-dhcp" "%{version}-%{release}" 1>&2

%pretrans plugin-protocol-nsclient
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-nsclient" "%{version}-%{release}" 1>&2

%pre plugin-protocol-nsclient
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-nsclient" "%{version}-%{release}" 1>&2

%post plugin-protocol-nsclient
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-nsclient" "%{version}-%{release}" 1>&2

%posttrans plugin-protocol-nsclient
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-nsclient" "%{version}-%{release}" 1>&2

%pretrans plugin-protocol-radius
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-radius" "%{version}-%{release}" 1>&2

%pre plugin-protocol-radius
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-radius" "%{version}-%{release}" 1>&2

%post plugin-protocol-radius
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-radius" "%{version}-%{release}" 1>&2

%posttrans plugin-protocol-radius
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-radius" "%{version}-%{release}" 1>&2

%pretrans plugin-protocol-xml
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xml" "%{version}-%{release}" 1>&2

%pre plugin-protocol-xml
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xml" "%{version}-%{release}" 1>&2

%post plugin-protocol-xml
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xml" "%{version}-%{release}" 1>&2

%posttrans plugin-protocol-xml
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xml" "%{version}-%{release}" 1>&2

%pretrans plugin-protocol-xmp
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xmp" "%{version}-%{release}" 1>&2

%pre plugin-protocol-xmp
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xmp" "%{version}-%{release}" 1>&2

%post plugin-protocol-xmp
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xmp" "%{version}-%{release}" 1>&2

%posttrans plugin-protocol-xmp
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-protocol-xmp" "%{version}-%{release}" 1>&2

%pretrans plugin-collector-juniper-tca
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
if ! [ -x "$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" ]; then
	echo "This is the first time git-managed OpenNMS is being installed or upgraded."
	# on a first install, if we're upgrading save etc/ for git-setup.pl
	# this avoids anything in etc/ as being marked as .rpmnew
	if [ -d "$RPM_INSTALL_PREFIX0/etc" ] && [ ! -d "$RPM_INSTALL_PREFIX0/.etc-pretrans" ]; then
		echo "An existing $RPM_INSTALL_PREFIX0/etc was found.  Making sure it's prepared for gitification."
		[ -x /bin/mv ] && /bin/mv "$RPM_INSTALL_PREFIX0/etc" "$RPM_INSTALL_PREFIX0/.etc-pretrans"
		if [ -x /bin/cp ] && [ -x /bin/mkdir ] && [ -d "$RPM_INSTALL_PREFIX0/share/etc-pristine" ]; then
			echo "Preparing $RPM_INSTALL_PREFIX0/etc for git-setup."
			mkdir -p "$RPM_INSTALL_PREFIX0/etc"
			cp -pR "$RPM_INSTALL_PREFIX0/share/etc-pristine"/* "$RPM_INSTALL_PREFIX0/etc/"
		fi
	fi
	exit 0;
fi
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pretrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-collector-juniper-tca" "%{version}-%{release}" 1>&2

%pre plugin-collector-juniper-tca
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-pre.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-collector-juniper-tca" "%{version}-%{release}" 1>&2

%post plugin-collector-juniper-tca
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-post.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-collector-juniper-tca" "%{version}-%{release}" 1>&2

%posttrans plugin-collector-juniper-tca
RPM_INSTALL_PREFIX0=`rpm -q --queryformat '%{INSTALLPREFIX}' opennms-core`
"$RPM_INSTALL_PREFIX0/bin/config-tools/opennms-posttrans.pl" "$RPM_INSTALL_PREFIX0" "opennms-plugin-collector-juniper-tca" "%{version}-%{release}" 1>&2

