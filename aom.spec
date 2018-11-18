%bcond_with	wxwidgets

Summary:	Royalty-free next-generation video format
Name:		aom
Version:	1.0.0
Release:	2
License:	BSD
Group:		Libraries
URL:		http://aomedia.org/
# Source0:	https://aomedia.googlesource.com/aom/+archive/v%{version}.tar.gz
Source0:	v%{version}.tar.gz
# Source0-md5:	dd4689f0425e55dbc255eab73989dca5
Patch0:		%{name}-build.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libstdc++-devel
%{?with_wxwidgets:BuildRequires:	wxGTK3-devel}
BuildRequires:	yasm

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

%package devel
Summary:	Development files for aom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for aom the royalty-free next-generation video
format.

%prep
%setup -qc
%patch0 -p1

%{__sed} -i -e 's/v0\.1\.0/v%{version}/' CHANGELOG

%build
install -d build; cd build
%cmake \
   -DLIB_INSTALL_DIR=%{_libdir} \
   -DENABLE_CCACHE=1 \
   -DCMAKE_SKIP_RPATH=1 \
%ifnarch aarch64 %{arm} %{ix86} x86_64
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
%ifarch x86_64
   -DAOM_TARGET_CPU=x86_64 \
%endif
   -DCONFIG_WEBM_IO=1 \
   -DENABLE_DOCS=1 \
   %{?with_wxwidgets:-DCONFIG_ANALYZER=1} \
   ..

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_wxwidgets:install -pm 0755 build/examples/analyzer $RPM_BUILD_ROOT%{_bindir}/aomanalyzer}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG README.md PATENTS
%{?with_wxwidgets:%attr(755,root,root) %{_bindir}/aomanalyzer}
%attr(755,root,root) %{_bindir}/aomdec
%attr(755,root,root) %{_bindir}/aomenc
%attr(755,root,root) %{_libdir}/libaom.so.0

%files devel
%defattr(644,root,root,755)
%doc build/docs/html
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/libaom.so
%{_pkgconfigdir}/%{name}.pc
