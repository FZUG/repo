%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           you-get
Version:        0.4.595
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

# bash completion
%{__install} -Dm644 contrib/completion/%{name}-completion.bash \
    %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# zsh completion
%{__install} -Dm644 contrib/completion/_%{name} \
    %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
sed -i '/compdef/s|%{name}|you-vlc=%{name}|;/player/d' contrib/completion/_%{name}
%{__install} -Dm644 contrib/completion/_%{name} \
    %{buildroot}%{_datadir}/zsh/site-functions/_you-vlc

# fish completion
%{__install} -Dm644 contrib/completion/%{name}.fish \
    %{buildroot}%{_datadir}/fish/completions/%{name}.fish

%check
%{__python3} setup.py test

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.txt
%attr(755,-,-) %{_bindir}/%{name}
%attr(755,-,-) %{_bindir}/you-vlc
%{python3_sitelib}/*
%{_datadir}/bash-completion/completions/%{name}

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/zsh/site-functions/_you-vlc

%files fish-completion
%{_datadir}/fish/completions/%{name}.fish

%changelog
* Tue Dec 13 2016 mosquito <sensor.wen@gmail.com> - 0.4.595-1
- Initial build
