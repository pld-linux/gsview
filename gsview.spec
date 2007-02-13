Summary:	GSview - a graphical interface for Ghostscript
Summary(pl.UTF-8):	GSview - graficzny interfejs do Ghostscripta
Name:		gsview
Version:	4.8
Release:	1
License:	Aladdin Free Public Licence (see LICENCE)
Group:		Applications
Source0:	ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/ghostgum/%{name}-%{version}.tar.gz
# Source0-md5:	21c81819af0eeb42ac5ee6499f4a7116
URL:		http://www.cs.wisc.edu/~ghost/gsview/
BuildRequires:	gtk+-devel
BuildRequires:	sed >= 4.0
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GSview is a graphical interface for Ghostscript. Ghostscript is an
interpreter for the PostScript page description language used by laser
printers. For documents following the Adobe PostScript Document
Structuring Conventions, GSview allows selected pages to be viewed or
printed.

%description -l pl.UTF-8
GSview to graficzny interfejs do Ghostscripta. Ghostscript to
interpreter języka opisu strony PostScript używanego przez drukarki
laserowe. Dla dokumentów zgodnych z konwencjami Adobe PostScript
Document Structuring Conventions GSview umożliwia podgląd i wydruk
wybranych stron.

%prep
%setup -q

%{__sed} -i -e 's/Terminal=.*/Terminal=false/g' \
	srcunx/gvxdesk.txt
echo "Categories=Qt;KDE;Graphics;Viewer;" >> srcunx/gvxdesk.txt

%build
#cdebug is ull because we pass debug flags in rpmoptflags
%{__make} -f srcunx/unx.mak \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	CDEBUG="" 

%install
# taken from spec from gsview, amazingly well designed spec it is
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir},%{_docdir},%{_sysconfdir}}
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} -f srcunx/unx.mak install \
	GSVIEW_BASE=$RPM_BUILD_ROOT%{_prefix}           \
	GSVIEW_BINDIR=$RPM_BUILD_ROOT%{_bindir}         \
	GSVIEW_MANDIR=$RPM_BUILD_ROOT%{_mandir}         \
	GSVIEW_DOCPATH=$RPM_BUILD_ROOT%{_docdir}        \
	GSVIEW_ETCPATH=$RPM_BUILD_ROOT%{_sysconfdir}

# desktop/icon files
install srcunx/gvxdesk.txt $RPM_BUILD_ROOT%{_desktopdir}/gsview.desktop
install binary/gsview48.png  $RPM_BUILD_ROOT%{_pixmapsdir}/gsview.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir /etc/gsview
%config(noreplace) %verify(not md5 mtime size) /etc/gsview/printer.ini
%{_docdir}/*
%{_mandir}/man1/*.1*
%{_desktopdir}/gsview.desktop
%{_pixmapsdir}/gsview.png
