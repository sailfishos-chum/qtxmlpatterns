%global qt_version 5.15.8

Summary: Qt5 - QtXmlPatterns component
Name: opt-qt5-qtxmlpatterns
Version: 5.15.8
Release: 1%{?dist}
# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}

BuildRequires: opt-qt5-qtdeclarative-devel

%description
The Qt XML Patterns module provides support for XPath, XQuery, XSLT,
and XML Schema validation.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%opt_qmake_qt5 %{?no_examples}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.LGPL*
%{_opt_qt5_libdir}/libQt5XmlPatterns.so.5*
%{_opt_qt5_archdatadir}/qml/QtQuick/XmlListModel/

%files devel
%{_opt_qt5_bindir}/xmlpatterns*
%{_opt_qt5_headerdir}/Qt*/
%{_opt_qt5_libdir}/libQt5*.so
%{_opt_qt5_libdir}/libQt5*.prl
%{_opt_qt5_libdir}/cmake/Qt5*/
%{_opt_qt5_libdir}/pkgconfig/Qt5*.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*.pri

