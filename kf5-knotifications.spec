#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.106
%define		qtver		5.15.2
%define		kfname		knotifications

Summary:	Desktop notifications
Name:		kf5-%{kfname}
Version:	5.106.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	1c366d3a17dfc51724790517414db993
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Quick-devel >= %{qtver}
BuildRequires:	Qt5Speech-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	libcanberra-devel
BuildRequires:	libdbusmenu-qt5-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Speech >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kcoreaddons >= %{version}
Requires:	kf5-kwindowsystem >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KNotification is used to notify the user of an event. It covers
feedback and persistent events.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5DBus-devel >= %{qtver}
Requires:	Qt5Widgets-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5Notifications.so.5
%attr(755,root,root) %{_libdir}/libKF5Notifications.so.*.*
%dir %{_libdir}/qt5/qml/org/kde/notification
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/notification/libknotificationqmlplugin.so
%{_libdir}/qt5/qml/org/kde/notification/qmldir
%{_datadir}/dbus-1/interfaces/kf5_org.kde.StatusNotifierItem.xml
%{_datadir}/dbus-1/interfaces/kf5_org.kde.StatusNotifierWatcher.xml
%{_datadir}/qlogging-categories5/knotifications.categories
%{_datadir}/qlogging-categories5/knotifications.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KNotifications
%{_libdir}/cmake/KF5Notifications
%{_libdir}/libKF5Notifications.so
%{qt5dir}/mkspecs/modules/qt_KNotifications.pri
