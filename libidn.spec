# TODO:
# - prepare package with web-files from contrib
#
Summary:	Internationalized string processing library
Summary(pl):	Biblioteka do przetwarzania umiêdzynarodowionych ³añcuchów
Name:		libidn
Version:	0.3.5
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz
# Source0-md5:	916fb4b90e76edd5b6cb24a027399466
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.8
BuildRequires:	libtool
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Libidn is an implementation of the Stringprep, Punycode and IDNA
specifications defined by the IETF Internationalized Domain Names
(IDN) working group, used for internationalized domain names.

%description -l pl
GNU Libidn to implementacja specyfikacji Stringprep, Punycode i IDNA
zdefiniowanych przez grupê robocz± IETF Internationalized Domain Names
(IDN), zajmuj±c± siê umiêdzynarodowionymi nazwami domen.

%package devel
Summary:	Header files for libidn library
Summary(pl):	Pliki nag³ówkowe biblioteki libidn
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for libidn library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libidn.

%package static
Summary:	Static libidn library
Summary(pl):	Statyczna biblioteka libidn
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libidn library.

%description static -l pl
Statyczna biblioteka libidn.

%prep
%setup -q
%patch0 -p1

# we don't have libtool 1.5a
%{__perl} -pi -e 's/AC_LIBTOOL_TAGS//' configure.ac
# incompatible with ksh
rm -f m4/libtool.m4

%build
# blegh, lt incompatible with ksh - must rebuild
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README THANKS TODO doc/libidn.html contrib
%attr(755,root,root) %{_bindir}/idn
%attr(755,root,root) %{_libdir}/libidn.so.*.*.*
%{_mandir}/man1/idn.1*
%{_infodir}/libidn.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libidn.so
%{_libdir}/libidn.la
%{_includedir}/*.h
%{_pkgconfigdir}/libidn.pc
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libidn.a
