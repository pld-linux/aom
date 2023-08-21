#
# Conditional build:
%bcond_without	wxwidgets	# wxWidgets based analyzer

%ifarch %{arm_with_neon}
%define		with_neon	1
%endif

Summary:	Royalty-free next-generation video format
Summary(pl.UTF-8):	Format wideo nowej generacji bez opłat licencyjnych
Name:		aom
Version:	3.6.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://aomedia.googlesource.com/aom/
# tarball is recreated with different md5 on each download
#Source0:	https://aomedia.googlesource.com/aom/+archive/v%{version}.tar.gz?fake=/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	2d2ea4f2ca4f4ed025983df98b791c31
Patch0:		%{name}-examples.patch
URL:		https://aomedia.org/
BuildRequires:	cmake >= 3.7
BuildRequires:	doxygen >= 1:1.8.10
BuildRequires:	graphviz
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.007
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

%package static
Summary:	Static AOM library
Summary(pl.UTF-8):	Statyczna biblioteka AOM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AOM library.

%description static -l pl.UTF-8
Statyczna biblioteka AOM.

%package apidocs
Summary:	API documentation for AOM library
Summary(pl.UTF-8):	Dokumentacja API biblioteki AOM
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for AOM library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki AOM.

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

%build
install -d builddir
cd builddir
# build/cmake/aom_install.cmake and .pc creation expect relative ..._{BINDIR,INCLUDEDIR,LIBDIR}
%cmake .. \
	-DCMAKE_INSTALL_BINDIR:PATH=bin \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
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
	%{cmake_on_off neon ENABLE_NEON} \
	-DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-gtk3-unicode-config

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_wxwidgets:install -p builddir/examples/analyzer $RPM_BUILD_ROOT%{_bindir}/aomanalyzer}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE PATENTS README.md
%attr(755,root,root) %{_bindir}/aomdec
%attr(755,root,root) %{_bindir}/aomenc
%attr(755,root,root) %{_libdir}/libaom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaom.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaom.so
%{_includedir}/aom
%{_pkgconfigdir}/aom.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaom.a

%files apidocs
%defattr(644,root,root,755)
%doc builddir/docs/html/*.{css,html,js,png}

%if %{with wxwidgets}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aomanalyzer
%endif
