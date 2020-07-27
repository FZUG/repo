%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           you-get
Version:        0.4.1456
Release:        1%{?dist}
Summary:        A YouTube/Youku/Niconico video downloader written in Python 3

License:        MIT
Group:          Applications/Multimedia
URL:            https://github.com/soimort/you-get
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       ffmpeg
Recommends:     rtmpdump
Recommends:     vlc
Recommends:     mpv
Provides:       python3-%{name} = %{version}-%{release}

%description
You-Get is a tiny command-line utility to download media contents (videos,
audios, images) from the Web, in case there is no other handy way to do it.

%package zsh-completion
Summary:        zsh completion files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       zsh

%description zsh-completion
This package installs %{summary}.

%package fish-completion
Summary:        fish completion files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       fish

%description fish-completion
This package installs %{summary}.

%prep
%autosetup

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# you-vlc
%{__cat} > %{buildroot}%{_bindir}/you-vlc << EOF
#!/usr/bin/env bash
if [ -x "%{_bindir}/vlc" ]; then
  %{_bindir}/%{name} --player vlc \$@
else
  echo "Please install vlc video player."
fi
EOF

# you-mpv
%{__cat} > %{buildroot}%{_bindir}/you-mpv << EOF
#!/usr/bin/env bash
if [ -x "%{_bindir}/mpv" ]; then
  %{_bindir}/%{name} --player mpv \$@
else
  echo "Please install mpv video player."
fi
EOF

# bash completion
pushd contrib/completion/
cp %{name}-completion.bash you-vlc-completion.bash
cp %{name}-completion.bash you-mpv-completion.bash
sed -i 's|%{name}|you-vlc|g' you-vlc-completion.bash
sed -i 's|%{name}|you-mpv|g' you-mpv-completion.bash
%{__install} -Dm644 %{name}-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
%{__install} -Dm644 you-vlc-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/you-vlc
%{__install} -Dm644 you-mpv-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/you-mpv

# zsh completion
cp _%{name} _you-vlc; cp _%{name} _you-mpv
sed -i '/compdef/s|%{name}|you-vlc=%{name}|;/player/d' _you-vlc
sed -i '/compdef/s|%{name}|you-mpv=%{name}|;/player/d' _you-mpv
%{__install} -Dm644 _%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
%{__install} -Dm644 _you-vlc %{buildroot}%{_datadir}/zsh/site-functions/_you-vlc
%{__install} -Dm644 _you-mpv %{buildroot}%{_datadir}/zsh/site-functions/_you-mpv

# fish completion
cp %{name}.fish you-vlc.fish; cp %{name}.fish you-mpv.fish
sed -i 's|%{name}|you-vlc|g' you-vlc.fish
sed -i 's|%{name}|you-mpv|g' you-mpv.fish
%{__install} -Dm644 %{name}.fish %{buildroot}%{_datadir}/fish/completions/%{name}.fish
%{__install} -Dm644 you-vlc.fish %{buildroot}%{_datadir}/fish/completions/you-vlc.fish
%{__install} -Dm644 you-mpv.fish %{buildroot}%{_datadir}/fish/completions/you-mpv.fish

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.txt
%attr(755,-,-) %{_bindir}/%{name}
%attr(755,-,-) %{_bindir}/you-vlc
%attr(755,-,-) %{_bindir}/you-mpv
%{python3_sitelib}/*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/you-vlc
%{_datadir}/bash-completion/completions/you-mpv

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/zsh/site-functions/_you-vlc
%{_datadir}/zsh/site-functions/_you-mpv

%files fish-completion
%{_datadir}/fish/completions/%{name}.fish
%{_datadir}/fish/completions/you-vlc.fish
%{_datadir}/fish/completions/you-mpv.fish

%changelog
* Mon Jul 27 14:01:39 GMT 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 0.4.1456-1
- update to 0.4.1456 upstream release
* Wed Dec 19 2018 Zamir SUN <sztsian@gmail.com> - 0.4.1193-1
- Update to 0.4.1193
* Sat Dec 17 2016 mosquito <sensor.wen@gmail.com> - 0.4.595-2
- Add you-mpv command
* Tue Dec 13 2016 mosquito <sensor.wen@gmail.com> - 0.4.595-1
- Initial build
