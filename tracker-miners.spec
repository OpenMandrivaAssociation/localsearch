%if 0%{?rhel}
%global with_enca 0
%global with_libcue 0
%global with_rss 0
%else
%global with_enca 1
%global with_libcue 1
%global with_rss 1
%endif

%define _disable_ld_no_undefined 1

%define url_ver	%(echo %{version}|cut -d. -f1,2)
%global tracker_version 2.2.0

%global systemd_units tracker-extract.service tracker-miner-fs.service tracker-miner-rss.service tracker-writeback.service

Name:		tracker-miners
Version:	2.3.3
Release:	1
Summary:	Tracker miners and metadata extractors
Group:		Graphical desktop/GNOME

# libtracker-extract is LGPLv2+; the miners are a mix of GPLv2+ and LGPLv2+ code
License:	GPLv2+ and LGPLv2+
URL:		https://wiki.gnome.org/Projects/Tracker
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	meson
BuildRequires:	giflib-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	systemd
%if 0%{?with_enca}
BuildRequires:	pkgconfig(enca)
%endif
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(gexiv2)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-tag-1.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
%if 0%{?with_libcue}
BuildRequires:	pkgconfig(libcue)
%endif
BuildRequires:	pkgconfig(libexif)
%if 0%{?with_rss}
BuildRequires:	pkgconfig(libgrss)
%endif
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(libgxps)
BuildRequires:	pkgconfig(libiptcdata)
BuildRequires:	pkgconfig(libosinfo-1.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(taglib_c)
BuildRequires:	pkgconfig(totem-plparser)
BuildRequires:	pkgconfig(tracker-sparql-2.0) >= %{tracker_version}
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	pkgconfig(zlib)

Requires:	tracker%{?_isa} >= %{tracker_version}

# tracker-miners was split out from tracker in 1.99.2
Obsoletes:	tracker < 1.99.2
Conflicts:	tracker < 1.99.2

%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

This package contains various miners and metadata extractors for tracker.

%prep
%autosetup -p1

%build
%meson -Dfunctional_tests=false \
       -Dsystemd_user_services=%{_userunitdir} \
       -Dmp3=true
%meson_build

%install
%meson_install

rm -rf %{buildroot}%{_datadir}/tracker-tests

%find_lang %{name}

%post
%systemd_user_post %{systemd_units}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/tracker-miners-2.0/
%{_libexecdir}/tracker*
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/tracker/
%{_datadir}/tracker-miners/
%{_mandir}/man1/tracker-*.1*
%config(noreplace) %{_sysconfdir}/xdg/autostart/tracker*.desktop
%{_userunitdir}/tracker*.service
