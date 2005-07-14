#
Summary:	GSview is a graphical interface for Ghostscript.
Name:		gsview
Version:	4.7
Release:	1
License:	Aladdin Free Public Licence (see LICENCE)
Group:		Applications
Source0:	ftp://mirror.cs.wisc.edu/pub/mirrors/ghost/ghostgum/%{name}-%{version}.tar.gz
# Source0-md5:	ce6288cc8597d6b918498d6d02654bb7
URL:		http://www.cs.wisc.edu/~ghost/gsview
BuildRequires:	gtk+-devel
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GSview is a graphical interface for Ghostscript. Ghostscript is an
interpreter for the PostScript page description language used by laser
printers. For documents following the Adobe PostScript Document
Structuring Conventions, GSview allows selected pages to be viewed or
printed.

%prep
%setup -q -n %{name}-%{version}

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
# taken from spec frmo gsview, amazingly well designed spec it is
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir},%{_docdir},%{_sysconfdir}}
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

make -f srcunx/unx.mak install \
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
%config(noreplace) %verify(not md5 mtime size) /etc/gsview/printer.ini
%{_docdir}
%{_mandir}/man1/*.1*
%{_desktopdir}/gsview.desktop
%{_pixmapsdir}/gsview.png
