# TODO:
# - prepare package with web-files from contrib and JNI (contrib/java, needs move to jdk)
#
# Conditional build:
%if "%{pld_release}" == "ac"
%bcond_with	dotnet		# don't build C# binding
%bcond_with	java		# don't build Java implementation
%else
%bcond_without	dotnet		# don't build C# binding
%bcond_without	java		# don't build Java implementation
%endif
%bcond_without	python		# don't build python interface
%bcond_without	static_libs	# static library
#
%ifnarch %{ix86} %{x8664} alpha %{arm} hppa ppc s390 s390x sparc sparcv9 sparc64
%undefine	with_dotnet
%endif
%ifarch i386
%undefine	with_dotnet
%endif

%{?with_java:%{?use_default_jdk}}

Summary:	Internationalized string processing library
Summary(pl.UTF-8):	Biblioteka do przetwarzania umiędzynarodowionych łańcuchów
Name:		libidn
Version:	1.43
Release:	1
License:	GPL v2+ or LGPL v3+ (library), GPL v3+ (utilities)
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
# Source0-md5:	4a32cafa4e9de86943fbae9a75c41f01
Patch0:		%{name}-info.patch
Patch1:		%{name}-python.patch
URL:		http://www.gnu.org/software/libidn/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-tools >= 0.21
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	help2man
%{?with_java:%buildrequires_jdk}
BuildRequires:	libtool >= 2:2
%{?with_dotnet:BuildRequires:	mono}
%{?with_dotnet:BuildRequires:	mono-csharp}
BuildRequires:	perl-base
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel >= 1:2.3}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-build >= 4.6
%{?with_java:BuildRequires:	rpm-javaprov}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 2.021
BuildRequires:	texinfo >= 4.7
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# is it correct?
%define		_emacs_lispdir	%{_datadir}/emacs/site-lisp

%description
GNU Libidn is an implementation of the Stringprep, Punycode and IDNA
specifications defined by the IETF Internationalized Domain Names
(IDN) working group, used for internationalized domain names.

%description -l pl.UTF-8
GNU Libidn to implementacja specyfikacji Stringprep, Punycode i IDNA
zdefiniowanych przez grupę roboczą IETF Internationalized Domain Names
(IDN), zajmującą się umiędzynarodowionymi nazwami domen.

%package devel
Summary:	Header files for libidn library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libidn
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libidn library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libidn.

%package static
Summary:	Static libidn library
Summary(pl.UTF-8):	Statyczna biblioteka libidn
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libidn library.

%description static -l pl.UTF-8
Statyczna biblioteka libidn.

%package apidocs
Summary:	API documentation for libidn library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libidn
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libidn library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libidn.

%package -n dotnet-libidn
Summary:	C# binding for libidn
Summary(pl.UTF-8):	Wiązanie C# dla libidn
License:	LGPL v2.1+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n dotnet-libidn
C# binding for libidn.

%description -n dotnet-libidn -l pl.UTF-8
Wiązanie C# dla libidn.

%package -n emacs-libidn-pkg
Summary:	IDN support files for emacs
Summary(pl.UTF-8):	Obsługa IDN dla emacsa
License:	GPL v3+
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}

%description -n emacs-libidn-pkg
IDN support files for emacs.

%description -n emacs-libidn-pkg -l pl.UTF-8
Obsługa IDN dla emacsa.

%package -n java-libidn
Summary:	Java implementation of libidn
Summary(pl.UTF-8):	Implementacja libidn w Javie
License:	LGPL v2.1+
Group:		Libraries
Requires:	jre

%description -n java-libidn
Java implementation of libidn (internationalized domain names
library).

%description -n java-libidn -l pl.UTF-8
Implementacja libidn (biblioteki umiędzynarodowionych nazw domen) w
Javie.

%package -n python-idn
Summary:	Python interface to libidn
Summary(pl.UTF-8):	Pythonowy interfejs do libidn
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-idn
Python interface to libidn (internationalized domain names library).

%description -n python-idn -l pl.UTF-8
Pythonowy interfejs do libidn (biblioteki umiędzynarodowionych nazw
domen).

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__rm} po/stamp-po

# avoid different builds having different timestamps
# see http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2008-August/020363.html
d='$Date: 2012-05-24 11:40:06 $'
d=${d#?Date: }; d=${d%%%% *}; d=$(date -d "$d" '+%d %B %Y')
%{__sed} -i -e "s,@value{UPDATED},$d,g" doc/libidn.texi

# remove it when "linking libtool libraries using a non-POSIX archiver ..." warning is gone
# (after libidn or libtool change)
%{__sed} -i -e '/AM_INIT_AUTOMAKE/s/-Werror//' configure.ac

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4 -I lib/gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	%{?with_dotnet:--enable-csharp=mono}%{!?with_dotnet:--disable-csharp} \
	--with-lispdir=%{_emacs_lispdir} \
%if %{with java}
	JAR="%{java_home}/bin/jar" \
	JAVAC="%{java_home}/bin/javac" \
	JAVADOC="%{java_home}/bin/javadoc" \
	--enable-java \
	--with-java-prefix="%{java_home}"
%endif

%{__make}

%if %{with python}
%{__make} -C contrib/idn-python \
	INCLUDE="%{py_incdir} %{rpmcflags} -I../../lib -L../../lib/.libs"
%{__mv} contrib/idn-python/idn.so python-idn.so
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
install -D python-idn.so $RPM_BUILD_ROOT%{py_sitedir}/idn.so
%endif

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

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
%doc AUTHORS ChangeLog FAQ NEWS README* THANKS contrib/web
%attr(755,root,root) %{_bindir}/idn
%attr(755,root,root) %{_libdir}/libidn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libidn.so.12
%{_mandir}/man1/idn.1*
%{_infodir}/libidn.info*
%{_infodir}/libidn-*.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libidn.so
%{_libdir}/libidn.la
%{_includedir}/idn-*.h
%{_includedir}/idna.h
%{_includedir}/pr29.h
%{_includedir}/punycode.h
%{_includedir}/stringprep.h
%{_includedir}/tld.h
%{_pkgconfigdir}/libidn.pc
%{_mandir}/man3/idn_*.3*
%{_mandir}/man3/idna_*.3*
%{_mandir}/man3/pr29_*.3*
%{_mandir}/man3/punycode_*.3*
%{_mandir}/man3/stringprep*.3*
%{_mandir}/man3/tld_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libidn.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/reference/html/*

%if %{with dotnet}
%files -n dotnet-libidn
%defattr(644,root,root,755)
# why not in gac? does it work here?
%{_libdir}/Libidn.dll
%endif

%files -n emacs-libidn-pkg
%defattr(644,root,root,755)
%{_emacs_lispdir}/*.el

%if %{with java}
%files -n java-libidn
%defattr(644,root,root,755)
%{_javadir}/libidn*.jar
%endif

%if %{with python}
%files -n python-idn
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/idn.so
%endif
