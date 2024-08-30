#!/usr/bin/tclsh

set arch "x86_64"
set base "tkhtml3-alpha-16-20200313"

file mkdir build/BUILD build/RPMS build/SOURCES build/SPECS build/SRPMS
file copy -force $base.tar.gz build/SOURCES
file copy -force htmltcl.c.patch build/SOURCES

set buildit [list rpmbuild --target $arch --define "_topdir [pwd]/build" -bb tkhtml3.spec]
exec >@stdout 2>@stderr {*}$buildit

