#
# Conditional build:
%bcond_without	wxwidgets	# wxWidgets based analyzer

Summary:	Royalty-free next-generation video format
Summary(pl.UTF-8):	Format wideo nowej generacji bez opłat licencyjnych
Name:		aom
%define	basever	1.0.0
%define	subver	errata1
Version:	%{basever}.%{subver}
Release:	1
License:	BSD
Group:		Libraries
# tarball is recreated with different md5 on each download
#Source0:	https://aomedia.googlesource.com/aom/+archive/v%{basever}-%{subver}.tar.gz?fake=/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	5b22f5d026057ded5339bd17fd214e8a
Patch0:		%{name}-build.patch
URL:		https://aomedia.org/
BuildRequires:	cmake >= 3.5
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
%{?with_wxwidgets:BuildRequires:	wxGTK3-unicode-devel}
BuildRequires:	yasm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Alliance for Open Media's focus is to deliver a next-generation
video format that is:
- Interoperable and open;
- Optimized for the Internet;
- Scalable to any modern device at any bandwidth;
- Designed with a low computational footprint and optimized for
  hardware;
- Capable of consistent, highest-quality, real-time video delivery;
  and
- Flexible for both commercial and non-commercial content, including
  user-generated content.

%description -l pl.UTF-8
Celem Alliance for Open Media jest dostarczenie nowej generacji
formatu wideo, który jest:
- interoperacyjny i otwarty
- zoptymalizowany dla Internetu
- skalowalny na dowolne współczesne urządzenie przy dowolnym paśmie
- zaprojektowany z myślą o małym narzucie obliczeniowym,
  zoptymalizowany dla sprzętu
- umożliwiający spójne udostępnianie wysokiej jakości obrazu w czasie
  rzeczywistym
- elastyczny zarówno dla treści komercyjnych, jak i niekomercyjnych, w
  tym wygenerowanych przez użytkownika.

%package devel
Summary:	Development files for AOM
Summary(pl.UTF-8):	Pliki programistyczne AOM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for AOM the royalty-free next-generation video
format.

%description devel -l pl.UTF-8
Pliki programistyczne AOM - formatu obrazu nowej generacji, bez opłat
licencyjnych.

%package gui
Summary:	Graphical analyzer for AOM
Summary(pl.UTF-8):	Graficzny analizator formatu AOM
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description gui
Graphical analyzer for AOM.

%description gui -l pl.UTF-8
Graficzny analizator formatu AOM.

%prep
%setup -qc
%patch0 -p1

%{__sed} -i -e 's/^Next Release/v%{version}/' CHANGELOG

%build
install -d builddir
cd builddir
%cmake .. \
	-DLIB_INSTALL_DIR=%{_libdir} \
%ifnarch aarch64 %{arm} %{ix86} %{x8664}
	-DAOM_TARGET_CPU=generic \
%endif
%ifarch %{arm}
	-DAOM_TARGET_CPU=arm \
%endif
%ifarch aarch64
	-DAOM_TARGET_CPU=arm64 \
%endif
%ifarch %{ix86}
	-DAOM_TARGET_CPU=x86 \
%endif
%ifarch %{x8664}
	-DAOM_TARGET_CPU=x86_64 \
%endif
	-DCMAKE_SKIP_RPATH=1 \
	%{?with_wxwidgets:-DCONFIG_ANALYZER=1} \
	-DCONFIG_WEBM_IO=1 \
	-DENABLE_CCACHE=1 \
	-DENABLE_DOCS=1 \
	-DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-gtk3-unicode-config

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_wxwidgets:install -pm 0755 builddir/examples/analyzer $RPM_BUILD_ROOT%{_bindir}/aomanalyzer}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE PATENTS README.md
%attr(755,root,root) %{_bindir}/aomdec
%attr(755,root,root) %{_bindir}/aomenc
%attr(755,root,root) %{_libdir}/libaom.so.0

%files devel
%defattr(644,root,root,755)
%doc builddir/docs/html/*
%attr(755,root,root) %{_libdir}/libaom.so
%{_includedir}/aom
%{_pkgconfigdir}/aom.pc

%if %{with wxwidgets}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aomanalyzer
%endif
