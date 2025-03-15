%if 0%{?rhel}
%global with_enca 0
%global with_libcue 0
%global with_rss 0
%else
%global with_enca 1
%global with_libcue 1
%global with_rss 0
%endif

%define _disable_ld_no_undefined 1
# Sanitizer is enabled because some people apparently see crashes
# when not using -O0
# https://gitlab.gnome.org/GNOME/tracker-miners/-/issues/7
# https://forum.openmandriva.org/t/gdm-takes-a-very-long-time-to-load/4596/9
# Can't reproduce this, but let's try to get some more information
# if that happens again
%global optflags %optflags -fsanitize=undefined -Wl,--allow-shlib-undefined,--unresolved-symbols=ignore-all

%define url_ver	%(echo %{version}|cut -d. -f1,2)
%global tracker_version 3.0.0

%global systemd_units tracker-extract.service tracker-miner-fs.service tracker-miner-rss.service tracker-writeback.service

#define beta rc

Name:		localsearch
Version:	3.9.rc
Release:	%{?beta:0.%{beta}.}1
Summary:	Localsearch and metadata extractors
Group:		Graphical desktop/GNOME

# libtracker-extract is LGPLv2+; the miners are a mix of GPLv2+ and LGPLv2+ code
License:	GPLv2+ and LGPLv2+
URL:		https://wiki.gnome.org/Projects/Tracker
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}%{?beta:.%{beta}}.tar.xz

BuildRequires:       a2x
BuildRequires:       asciidoc
BuildRequires:       xsltproc
BuildRequires:       docbook2x
BuildRequires:       docbook-xsl
BuildRequires:	meson
BuildRequires:	giflib-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:       pkgconfig(systemd)
BuildRequires:	systemd
BuildRequires:       pkgconfig(libnm)
%if 0%{?with_enca}
BuildRequires:	pkgconfig(enca)
%endif
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(flac)
BuildRequires:       pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gexiv2)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-tag-1.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:       pkgconfig(libavcodec)
BuildRequires:       pkgconfig(libavformat)
BuildRequires:       pkgconfig(libavutil)
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
BuildRequires:	pkgconfig(tinysparql-3.0)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	pkgconfig(zlib)

Requires:		tinysparql%{?_isa} >= %{tracker_version}

# tracker-miners was split out from tracker in 1.99.2
Obsoletes:	tracker < 1.99.2
Conflicts:	tracker < 1.99.2
Obsoletes:    tracker-miners < 3.7.90

Provides:            tracker-miners

%description
localsearch is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

This package contains various miners and metadata extractors for tracker.

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:.%{beta}}

%build
%meson -Dfunctional_tests=false \
       -Dmp3=true
%meson_build

%install
%meson_install

rm -rf %{buildroot}%{_datadir}/tracker-tests

%find_lang localsearch3

%post
%systemd_user_post %{systemd_units}

%files -f localsearch3.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/localsearch
%{_libdir}/localsearch-3.0/
%{_libexecdir}/localsearch*
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3*
%{_datadir}/dbus-1/services/org.freedesktop.LocalSearch*
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker*
%{_datadir}/localsearch3/
#{_datadir}/tracker3-miners/
#{_datadir}/tracker3/commands/
%{_mandir}/man1/localsearch*
%config(noreplace) %{_sysconfdir}/xdg/autostart/localsearch-3.desktop
%{_userunitdir}/localsearch*
