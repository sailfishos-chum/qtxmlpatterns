%define _prefix /opt/qt5/

Name:       qt5-lgpl-qtxmlpatterns
Summary:    Qt XML Patterns library
Version:    5.15.8
Release:    1%{?dist}
License:    (LGPLv2 or LGPLv3) with exception or Qt Commercial
URL:        https://www.qt.io
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  qt5-lgpl-qtcore-devel
BuildRequires:  qt5-lgpl-qtxml-devel
BuildRequires:  qt5-lgpl-qtgui-devel
BuildRequires:  qt5-lgpl-qtnetwork-devel
BuildRequires:  qt5-lgpl-qtwidgets-devel
BuildRequires:  qt5-lgpl-qmake
BuildRequires:  fdupes
BuildRequires:  perl

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the XMLPatterns library


%package devel
Summary:    Qt XML Patterns - development files
Requires:   %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the XMLPatterns library development files


#### Build section

%prep
%setup -q -n %{name}-%{version}/upstream

# The original source assumes build happens within a monolithic tree.
# The tool used is syncqt, which complains a lot but really only wants
# to know where the mkspecs may be found. Hence the environment variable
# name is a little misleading.
#
# XXX: FOR THE LOVE OF ALL THAT MAY BE HOLY - DO NOT USE RPMBUILD AND
# ITS INTERNAL qmake MACRO. IT BREAKS THE BUILD!
%build
export QTDIR=%{_prefix}
touch .git
%{_prefix}/lib64/qt5/bin/qmake
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;

# We don't need qt5/Qt/
rm -rf %{buildroot}/%{_includedir}/qt5/Qt

#
%fdupes %{buildroot}/%{_includedir}



%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libQt5XmlPatterns.so.5
%{_libdir}/libQt5XmlPatterns.so.5.*
%{_qt5_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libQt5XmlPatterns.so
%{_libdir}/libQt5XmlPatterns.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5/
%{_datadir}/qt5/mkspecs/
%{_libdir}/cmake/


#### No changelog section, separate $pkg.changes contains the history

