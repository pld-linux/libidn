# TODO:
# - prepare package with web-files and java from contrib
#
# Conditional build:
%bcond_with	java	# build Java implementation
#
Summary:	Internationalized string processing library
Summary(pl):	Biblioteka do przetwarzania umiêdzynarodowionych ³añcuchów
Name:		libidn
Version:	0.5.13
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz
# Source0-md5:	733cddb52c40a5656053631d31fe3cc7
Patch0:		%{name}-info.patch
Patch1:		%{name}-python.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel >= 0.14.1
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-base
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	texinfo >= 4.7
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
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libidn library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libidn.

%package static
Summary:	Static libidn library
Summary(pl):	Statyczna biblioteka libidn
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libidn library.

%description static -l pl
Statyczna biblioteka libidn.

%package -n emacs-libidn-pkg
Summary:	IDN support files for emacs
Summary(pl):	Obs³uga IDN dla emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}

%description -n emacs-libidn-pkg
IDN support files for emacs.

%description -n emacs-libidn-pkg -l pl
Obs³uga IDN dla emacsa.

%package -n java-libidn
Summary:	Java implementation of libidn
Summary(pl):	Implementacja libidn w Javie
Group:		Libraries
Requires:	jre

%description -n java-libidn
Java implementation of libidn (internationalized domain names
library).

%description -n java-libidn -l pl
Implementacja libidn (biblioteki umiêdzynarodowionych nazw domen) w
Javie.

%package -n python-idn
Summary:	Python interface to libidn
Summary(pl):	Pythonowy interfejs do libidn
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-idn
Python interface to libidn (internationalized domain names library).

%description -n python-idn -l pl
Pythonowy interfejs do libidn (biblioteki umiêdzynarodowionych nazw
domen).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_java:--enable-java} \
	--with-lispdir=%{_emacs_lispdir}

%{__make}

%{__make} -C contrib/idn-python \
	INCLUDE="/usr/include/python2.4 -I/usr/include/python2.3 %{rpmcflags} -I../../lib -L../../lib/.libs"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D contrib/idn-python/idn.so $RPM_BUILD_ROOT%{py_sitedir}/idn.so

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README* THANKS TODO doc/libidn.html contrib
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

%if %{with java}
%files -n java-libidn
%defattr(644,root,root,755)
%{_datadir}/java/libidn*.jar
%endif

%files -n python-idn
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/idn.so
