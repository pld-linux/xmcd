# TODO:
#  - make xmcd work (cda is ok)
Summary:	Motif (tm) CD Audio Player
Summary(pl):	Odtwarzacz CD
Name:		xmcd
Version:	3.3.2
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://www.ibiblio.org/tkan/download/xmcd/%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	8808c754db69b1d6eca060c2a6d1be99
URL:		http://www.amb.org/xmcd/	
Patch0:		%{name}-Imakefile-motif.patch
Patch1:		%{name}-install.sh-nonroot.patch
BuildRequires:	XFree86-devel
BuildRequires:	flac-devel
BuildRequires:	motif-devel
BuildRequires:	ncurses-devel
BuildRequires:	sed >= 4.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/usr/X11R6/lib/X11

%description
Xmcd is a full-featured CD Player utility package including xmcd, a CD
Player for the X window system using the Motif graphical user
interface; and cda, a command-line driven, text mode CD Player which
also features a curses-based, screen-oriented mode. Both utilities
transform your CD-ROM, CD-R or CD-RW drive into a stereo CD player,
allowing you to play audio CDs on your computer.

%description -l pl
Xmcd to pakiet do odtwarzania p³yt CD o du¿ych mo¿liwo¶ciach
zawieraj±cy xmcd - program dla X11 i cda - program dzia³aj±cy w trybie
tekstowym. Cda mo¿e dzia³aæ w trybie pe³noekranowym jak i byæ
sterowany z linii poleceñ. Obydwa te programy pozwalaj± przekszta³ciæ
Twój napêd CD-ROM, CD-R b±d¼ CD-RW w stereofoniczny odtwarzacz p³yt
kompaktowych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
xmkmf
%{__make} Makefiles
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I.. -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
BATCH_BINDIR=$RPM_BUILD_ROOT%{_bindir}
BATCH_LIBDIR=$RPM_BUILD_ROOT%{_libdir}
BATCH_XMCDLIB=$RPM_BUILD_ROOT%{_libdir}/xmcd
BATCH_MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1
export BATCH_BINDIR BATCH_LIBDIR BATCH_XMCDLIB BATCH_MANDIR
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/app-defaults

sed -i -e s,FILE=/tmp,FILE=%{tmpdir},g install.sh

chmod +x ./install.sh
./install.sh -b -n

cp -f misc_d/start.sh $RPM_BUILD_ROOT%{_bindir}/.xmcd_start
ln -sf ./.xmcd_start $RPM_BUILD_ROOT%{_bindir}/xmcd
ln -sf ./.xmcd_start $RPM_BUILD_ROOT%{_bindir}/cda
cp -f libdi_d/config.sh $RPM_BUILD_ROOT%{_libdir}/xmcd/config/config.sh
cp -f misc_d/discog.htm $RPM_BUILD_ROOT%{_libdir}/xmcd/discog/discog.html
cp -f misc_d/genidx.sh $RPM_BUILD_ROOT%{_libdir}/xmcd/scripts/genidx
cp -f xmcd_d/XMcd.ad $RPM_BUILD_ROOT%{_libdir}/app-defaults/XMcd

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Before first use run %{_libdir}/xmcd/config/config.sh to configure"

%files
%defattr(644,root,root,755)
%doc docs_d/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_bindir}/.xmcd_start
%dir %{_libdir}/xmcd
%dir %{_libdir}/xmcd/bin*
%attr(755,root,root) %{_libdir}/xmcd/bin*/[!R]*
%{_libdir}/xmcd/bin*/README
%{_libdir}/xmcd/[chps]*
%{_libdir}/xmcd/discog
%{_libdir}/app-defaults/XMcd
%{_libdir}/%{name}/app-defaults
%{_mandir}/man1/*
