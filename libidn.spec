# TODO:
# - prepare package with web-files from contrib
#
Summary:	Internationalized string processing library
Summary(pl):	Biblioteka do przetwarzania umi�dzynarodowionych �a�cuch�w
Name:		libidn
Version:	0.2.1
Release:	2
License:	LGPL v2.1
Group:		Libraries
Source0:	ftp://alpha.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
# Source0-md5:	dedf4baabde459dc6263ca2f38d4f0f9
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Libidn is an implementation of the Stringprep, Punycode and IDNA
specifications defined by the IETF Internationalized Domain Names
(IDN) working group, used for internationalized domain names.

%description -l pl
GNU Libidn to implementacja specyfikacji Stringprep, Punycode i IDNA
zdefiniowanych przez grup� robocz� IETF Internationalized Domain Names
(IDN), zajmuj�c� si� umi�dzynarodowionymi nazwami domen.

%package devel
Summary:	Header files for libidn library
Summary(pl):	Pliki nag��wkowe biblioteki libidn
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for libidn library.

%description devel -l pl
Pliki nag��wkowe biblioteki libidn.

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
%patch -p1

%build
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libidn.a
