# TODO:
# - prepare package with web-files and java from contrib
#
Summary:	Internationalized string processing library
Summary(pl):	Biblioteka do przetwarzania umiêdzynarodowionych ³añcuchów
Name:		libidn
Version:	0.3.7
Release:	2
License:	LGPL v2.1
Group:		Libraries
Source0:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz
# Source0-md5:	3ec822e38dda0d1eadd032d82a5b238c
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.8
BuildRequires:	libtool
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# is it correct?
%define		_emacs_lispdir	%{_datadir}/emacs/site-lisp

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

%package -n emacs-libidn-pkg
Summary:	IDN support files for emacs
Summary(pl):	Obs³uga IDN dla emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}

%description -n emacs-libidn-pkg
IDN support files for emacs.

%description -n emacs-libidn-pkg -l pl
Obs³uga IDN dla emacsa.

%prep
%setup -q
%patch0 -p1

# we don't have libtool 1.5a
%{__perl} -pi -e 's/AC_LIBTOOL_TAGS//' configure.ac
# we don't have cvs texinfo
%{__perl} -pi -e 's/\@ordf\{\}/a/' doc/libidn.texi
# incompatible with ksh
rm -f m4/libtool.m4

%build
# blegh, lt incompatible with ksh - must rebuild
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-lispdir=%{_emacs_lispdir}

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

%files -n emacs-libidn-pkg
%defattr(644,root,root,755)
%{_emacs_lispdir}/*.el
