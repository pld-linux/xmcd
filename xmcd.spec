Summary:	Motif (tm) CD Audio Player
Summary(pl):	Odtwarzacz CD
Name:		xmcd
Version:	3.0.2
Release:	1
License:	GPL
Group:		X11/Applications/Sound
#Source0:	http://www.ibiblio.org/tkan/download/xmcd/%{version}/src/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	3a4bfe86ca44486adddfb7b0e1a41388
URL:		http://www.ibiblio.org/tkan/xmcd/main.html
Patch0:		%{name}-Imakefile-motif.patch
Patch1:		%{name}-install.sh-nonroot.patch
BuildRequires:	XFree86-devel
BuildRequires:	motif-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/lib/X11

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
%setup -q -n %{name}-3.0
%patch0 -p1
%patch1 -p1

%build
xmkmf
%{__make} Makefiles
%{__make} "CCOPTIONS=%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
BATCH_BINDIR=$RPM_BUILD_ROOT%{_bindir}
BATCH_LIBDIR=$RPM_BUILD_ROOT%{_libdir}
BATCH_XMCDLIB=$RPM_BUILD_ROOT%{_libdir}/xmcd
BATCH_MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1
export BATCH_BINDIR BATCH_LIBDIR BATCH_XMCDLIB BATCH_MANDIR
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/app-defaults

sed -e s?FILE=/tmp?FILE=%{tmpdir}?g install.sh > install2.sh
mv -f install2.sh install.sh

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
%dir %{_libdir}/xmcd
%dir %{_libdir}/bin*
%attr(755,root,root) %{_libdir}/xmcd/bin*/[!R]*
%{_libdir}/xmcd/bin*/README
%{_libdir}/xmcd/[chps]*
%{_libdir}/xmcd/discog
%{_libdir}/app-defaults/XMcd
%{_mandir}/man1/*
