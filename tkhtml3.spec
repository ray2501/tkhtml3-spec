%{!?directory:%define directory /usr}

%define buildroot %{_tmppath}/%{name}

Name:          tkhtml3
Summary:       Tk HTML / CSS rendering widget
Version:       3.0
Release:       alpha16.20200313
License:       BSD-3-Clause
Group:         Development/Libraries/Tcl
Source:        tkhtml3-alpha-16-20200313.tar.gz
Patch1:        htmltcl.c.patch
URL:           https://github.com/olebole/tkhtml3
BuildRequires: autoconf
BuildRequires: make
BuildRequires: tcl-devel >= 8.6
BuildRequires: tk-devel >= 8.6
Requires:      tcl >= 8.6
Requires:      tk >= 8.6
BuildRoot:     %{buildroot}

%description
Tkhtml3 is a Tk widget that displays content formatted according to the
HTML and CSS standards. Tkhtml3 is not an end-user application, it is
for Tcl programmers who wish to embed a standards-compliant HTML/CSS
implementation in their applications. 

%package -n hv3
Summary:	Html Viewer 3 - Tkhtml3 Web Browser
Group:		Applications/WWW
URL:		http://tkhtml.tcl.tk/hv3.html
Requires:	%{name} = %{version}-%{release}
Requires:	tcl >= 8.6
Requires:	tk
Requires:	tls
Requires:	tkimg
Requires:	tkhtml3
Provides:	wwwbrowser

%description -n hv3
Hv3 is a lightweight web browser with support for modern web standards
like HTML, CSS, HTTP and ECMAScript (a.k.a. javascript). It is based on
the Tkhtml3 HTML rendering widget and the tclsee Javascript rendering
widget.

%prep
%setup -q -n htmlwidget
%patch 1

%build
rm -rf $RPM_BUILD_ROOT

./configure \
	--prefix=%{directory} \
	--exec-prefix=%{directory} \
	--libdir=%{directory}/%{_lib} \
	--mandir=%{directory}/share/man \
	--with-tcl=%{directory}/%{_lib} \
	--with-tk=%{directory}/%{_lib} \
%ifarch x86_64
	--enable-64bits=yes \
%endif
	--enable-threads=yes
make 

%install
make DESTDIR=%{buildroot} pkglibdir=%{tcl_archdir}/%{name}%{version} install

install -d $RPM_BUILD_ROOT{%{_datadir}/hv3,%{_bindir}}
cp -a hv/*.tcl $RPM_BUILD_ROOT%{_datadir}/hv3
cp -a hv/index.html $RPM_BUILD_ROOT%{_datadir}/hv3
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/hv3
#!/bin/sh
exec %{_bindir}/wish %{_datadir}/hv3/hv3_main.tcl -statefile ${HOME}/.hv3.db ${1:+"$@"}
EOF

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%{tcl_archdir}/%{name}%{version}
%{directory}/share/man/mann

%files -n hv3
%doc hv/README hv/license.txt
%attr(755,root,root) %{_bindir}
%defattr(644,root,root,755)
%{_datadir}/hv3

%changelog
* Fri Apr 28 2017 Danilo Chang <ray2501@gmail.com> 3.0
- Remove HV3LIB, I don't know how to handle it correctly
