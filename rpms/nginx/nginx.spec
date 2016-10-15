%if ! 0%{?rhel} && ! 0%{?fedora}
%global  rhel %(%{__python} -c "import platform;print platform.dist()[1][0]")
%global  dist .el5
%endif
%global  debug_package       %{nil}
%global  _hardened_build     1
%global  nginx_user          nginx
%global  nginx_group         %{nginx_user}
%global  nginx_home          %{_localstatedir}/lib/nginx
%global  nginx_home_tmp      %{nginx_home}/tmp
%global  nginx_confdir       %{_sysconfdir}/nginx
%global  nginx_datadir       %{_datadir}/nginx
%global  nginx_logdir        %{_localstatedir}/log/nginx
%global  nginx_webroot       %{nginx_datadir}/html
%global  with_http2          1

# ngx_http_lua_module
%global  ngx_lua_version     0.10.6
%global  ndk_version         0.3.0
%global  with_ngx_lua        1

# ngx_echo module
%global  ngx_echo_version    0.60
%global  with_ngx_echo       1

# ModSecurity module
%if 0%{?rhel} == 5
%global  modsec_version      2.8.0
%else
%global  modsec_version      2.9.0
%endif
%global  with_modsec         1

# OWASP ModSecurity Core Rule Set (CRS)
%global  modsec_crs_version  2.2.9
%global  modsec_crs_commit   60c8bc920f6f21134e9aa2df2267e98cb37f8bcb
%global  modsec_crs_shortcommit %(c=%{modsec_crs_commit};echo ${c:0:7})
%global  with_modsec_crs     1

# FancyIndex module
%global  fancy_version       0.4.1
%global  with_fancy          1

# gperftools exist only on selected arches
%ifarch %{ix86} x86_64 ppc ppc64 %{arm}
%if 0%{?rhel} >= 6 || 0%{?fedora}
%global  with_gperftools     1
%endif
%endif

# AIO missing on some arches
%ifnarch aarch64
%global  with_aio            1
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global  with_systemd        1
%endif

# ModSecurity require libxml2 >= 2.6.29
%define libxml2_version 2.6.29
%define libxml2_build_path %{_tmppath}/libxml2-%{libxml2_version}
%define httpd_version 2.2.15
%define httpd_build_path %{_tmppath}/httpd-%{httpd_version}

Name:              nginx
Epoch:             1
Version:           1.11.5
%if 0%{?with_modsec}
Release:           1.modsec_%{modsec_version}%{?dist}
%else
Release:           1%{?dist}
%endif

Summary:           A high performance web server and reverse proxy server
Summary(zh_CN):    高性能 web 服务器和反向代理服务器
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://nginx.org

Source0:           http://nginx.org/download/%{name}-%{version}.tar.gz
Source1:           https://github.com/openresty/lua-nginx-module/archive/v%{ngx_lua_version}/lua-nginx-module-%{ngx_lua_version}.tar.gz
Source2:           https://github.com/simpl/ngx_devel_kit/archive/v%{ndk_version}/ngx_devel_kit-%{ndk_version}.tar.gz
Source3:           https://www.modsecurity.org/tarball/2.9.0/modsecurity-2.9.0.tar.gz
Source4:           https://www.modsecurity.org/tarball/2.8.0/modsecurity-2.8.0.tar.gz
Source5:           https://github.com/SpiderLabs/owasp-modsecurity-crs/archive/%{modsec_crs_commit}/owasp-modsecurity-crs-%{modsec_crs_shortcommit}.tar.gz
Source6:           https://github.com/aperezdc/ngx-fancyindex/archive/v%{fancy_version}/ngx-fancyindex-%{fancy_version}.tar.gz
Source7:           https://github.com/openresty/echo-nginx-module/archive/v%{ngx_echo_version}/echo-nginx-module-%{ngx_echo_version}.tar.gz
Source8:           ftp://xmlsoft.org/libxml2/old/libxml2-%{libxml2_version}.tar.gz
Source9:           http://archive.apache.org/dist/httpd/httpd-%{httpd_version}.tar.gz
Source10:          nginx.service
Source11:          nginx.logrotate
Source12:          nginx.conf
Source13:          nginx-upgrade
Source14:          nginx-upgrade.8
Source15:          nginx.init
Source16:          nginx.sysconfig
Source100:         index.html
Source101:         poweredby.png
Source102:         nginx-logo.png
Source103:         404.html
Source104:         50x.html

# removes -Werror in upstream build scripts.  -Werror conflicts with
# -D_FORTIFY_SOURCE=2 causing warnings to turn into errors.
Patch0:            nginx-auto-cc-gcc.patch

# lua_dump was changed
Patch1:            modsec_lua_dump.patch

# HTTP/2 patch
#Patch2:            http://nginx.org/patches/http2/patch.http2.txt

%if 0%{?rhel}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
%endif
BuildRequires:     GeoIP-devel
BuildRequires:     gd-devel
%if 0%{?with_gperftools}
BuildRequires:     gperftools-devel
%endif
BuildRequires:     libxslt-devel
BuildRequires:     openssl-devel
BuildRequires:     pcre-devel
%if 0%{?rhel} == 5
BuildRequires:     perl
%else
BuildRequires:     perl-devel
BuildRequires:     perl(ExtUtils::Embed)
%endif
BuildRequires:     zlib-devel
%if 0%{?with_modsec}
# Build reqs for mod_security
BuildRequires:     pcre-devel >= 5.0 curl-devel
BuildRequires:     lua-devel ssdeep-devel
BuildRequires:     apr-devel >= 1.2.0 apr-util-devel >= 1.2.0
%if 0%{?rhel} != 5
BuildRequires:     libxml2-devel >= 2.6.29 yajl-devel httpd-devel
%endif
%endif
# ngx_lua_module
BuildRequires:     lua-devel
%if 0%{?rhel} != 5
BuildRequires:     luajit-devel
%endif
BuildRequires:     libatomic_ops-devel

Requires:          nginx-filesystem = %{epoch}:%{version}-%{release}
Requires:          GeoIP
Requires:          gd
Requires:          openssl
Requires:          pcre
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):     nginx-filesystem
Provides:          webserver = %{version}
Provides:          %{name} = %{version}-%{release}

%if 0%{?with_modsec}
# So we can install rules from pkg
Provides:          mod_security = %{modsec_version}
%endif

%if 0%{?with_fancy}
Provides:          mod_fancyindex = %{fancy_version}
%endif

%if 0%{?with_systemd}
BuildRequires:     systemd-devel
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig, initscripts
Requires(postun):  initscripts
%endif

%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.

%package filesystem
Group:             System Environment/Daemons
Summary:           The basic directory layout for the Nginx server
%if 0%{?rhel} != 5
BuildArch:         noarch
%endif
Requires(pre):     shadow-utils

%description filesystem
The nginx-filesystem package contains the basic directory layout
for the Nginx server including the correct permissions for the
directories.

%if 0%{?with_modsec_crs}
%package modsec_crs
Group:             System Environment/Daemons
Summary:           ModSecurity Rules for %{name}
License:           ASL 2.0
URL:               https://github.com/SpiderLabs/owasp-modsecurity-crs
%if 0%{?rhel} != 5
BuildArch:         noarch
%endif
Requires:          %{name} = %{version}-%{release}

%description modsec_crs
This package provides the base rules for mod_security.
%endif


%prep
%setup -q -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9
%if 0%{?fedora} > 21
pushd modsecurity-%{modsec_version}
%patch1 -p1
popd
%endif
%patch0 -p0


%build
%if 0%{?with_modsec}
%if 0%{?rhel} == 5
# This is only safe in a mock environment.
pushd libxml2-%{libxml2_version}
./configure --prefix=%{libxml2_build_path}
make
make install
popd
pushd httpd-%{httpd_version}
./configure --prefix=%{httpd_build_path}
make
make install
popd
%endif

# Build mod_security standalone module
pushd modsecurity-%{modsec_version}
#CPATH=%%{httpd_build_path}/include
#CFLAGS="%%{optflags} $(pcre-config --cflags) -I%%{httpd_build_path}/include" ./configure \
%if 0%{?rhel} == 5
%configure --with-libxml=%{libxml2_build_path} --with-apxs=%{httpd_build_path}/bin/apxs \
%else
%configure --with-yajl \
%endif
    --enable-pcre-match-limit=no \
    --enable-pcre-match-limit-recursion=no \
%if 0%{?rhel} > 6 || 0%{?fedora}
    --enable-pcre-jit --enable-pcre-study \
%endif
    --enable-standalone-module \
    --disable-mlogc \
    --with-ssdeep \
    --enable-lua-cache \
    --enable-shared

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd
%endif

# luajit and lua variable
%if 0%{?rhel} == 5
export LUA_LIB=%{_libdir}
export LUA_INC=%{_includedir}
%else
export LUAJIT_LIB=%{_libdir}
export LUAJIT_INC=%{_includedir}/luajit-2.0
%endif

# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
./configure \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{nginx_confdir}/%{name}.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --http-uwsgi-temp-path=%{nginx_home_tmp}/uwsgi \
    --http-scgi-temp-path=%{nginx_home_tmp}/scgi \
%if 0%{?with_systemd}
    --pid-path=/run/%{name}.pid \
    --lock-path=/run/lock/subsys/%{name} \
%else
    --pid-path=%{_localstatedir}/run/%{name}.pid \
    --lock-path=%{_localstatedir}/lock/subsys/%{name} \
%endif
    --user=%{nginx_user} \
    --group=%{nginx_group} \
%if 0%{?with_aio}
    --with-file-aio \
%endif
    --with-http_ssl_module \
%if 0%{?with_http2}
    --with-http_v2_module \
%else
    --with-http_spdy_module \
%endif
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module \
    --with-http_image_filter_module \
    --with-http_geoip_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_stub_status_module \
    --with-http_perl_module \
    --with-http_auth_request_module \
    --with-md5-asm \
    --with-sha1-asm \
    --with-mail \
    --with-mail_ssl_module \
    --with-pcre \
    --with-pcre-jit \
    --with-libatomic \
    --with-threads \
    --with-stream \
    --with-stream_ssl_module \
%if 0%{?with_gperftools}
    --with-google_perftools_module \
%endif
%if 0%{?with_ngx_lua}
    --add-module="ngx_devel_kit-%{ndk_version}" \
    --add-module="lua-nginx-module-%{ngx_lua_version}" \
%endif
%if 0%{?with_ngx_echo}
    --add-module="echo-nginx-module-%{ngx_echo_version}" \
%endif
%if 0%{?with_modsec}
    --add-module="modsecurity-%{modsec_version}/nginx/modsecurity" \
%endif
%if 0%{?with_fancy}
    --add-module="ngx-fancyindex-%{fancy_version}" \
%endif
    --with-debug \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --with-ld-opt="$RPM_LD_FLAGS -Wl,-E" # so the perl module finds its symbols

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
rm -rf %{buildroot}%{_sbindir}/%{name}.old

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/default.d
install -p -d -m 0700 %{buildroot}%{nginx_home}
install -p -d -m 0700 %{buildroot}%{nginx_home_tmp}
install -p -d -m 0700 %{buildroot}%{nginx_logdir}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}

%if 0%{?with_systemd}
install -p -D -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
%else
install -p -D -m 0755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 0644 %{SOURCE16} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%endif

install -p -D -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p    -m 0644 %{SOURCE12} %{buildroot}%{nginx_confdir}

%if 0%{?rhel} < 7 && ! 0%{?fedora}
    sed -i 's|run|var/run|' \
        %{buildroot}%{nginx_confdir}/%{name}.conf \
        %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%endif

%if 0%{?with_modsec}
pushd modsecurity-%{modsec_version}
    install -p -m 0644 modsecurity.conf-recommended \
        %{buildroot}%{nginx_confdir}/modsecurity.conf
    install -p -m 0644 unicode.mapping %{buildroot}%{nginx_confdir}/
popd
install -d %{buildroot}%{nginx_confdir}/modsecurity.d/{activated,local}_rules
cat >> %{buildroot}%{nginx_confdir}/modsecurity.conf << EOF
# ModSecurity Core Rules Set and Local configuration
IncludeOptional %{_sysconfdir}/%{name}/modsecurity.d/*.conf
IncludeOptional %{_sysconfdir}/%{name}/modsecurity.d/activated_rules/*.conf
IncludeOptional %{_sysconfdir}/%{name}/modsecurity.d/local_rules/*.conf
EOF

%if 0%{?with_modsec_crs}
pushd owasp-modsecurity-crs-*
install -d %{buildroot}%{_datadir}/%{name}/modsecurity.d/{base,optional,experimental,slr}_rules
install -m 0644 modsecurity_crs_10_setup.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/modsecurity.d/modsecurity_crs_10_config.conf
install -m 0644 base_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/base_rules/
install -m 0644 optional_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/optional_rules/
install -m 0644 experimental_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/experimental_rules/
install -m 0644 slr_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/slr_rules/

# activate base_rules
for f in `ls %{buildroot}%{_datadir}/%{name}/modsecurity.d/base_rules/`; do
    ln -s %{_datadir}/%{name}/modsecurity.d/base_rules/$f %{buildroot}%{_sysconfdir}/%{name}/modsecurity.d/activated_rules/$f;
done
popd
%endif
%endif

install -p -m 0644 %{S:100} %{S:101} %{S:102} %{S:103} %{S:104} \
    %{buildroot}%{nginx_webroot}

install -p -D -m 0644 %{_builddir}/%{name}-%{version}/man/nginx.8 \
    %{buildroot}%{_mandir}/man8/%{name}.8

install -p -D -m 0755 %{SOURCE13} %{buildroot}%{_bindir}/%{name}-upgrade
install -p -D -m 0644 %{SOURCE14} %{buildroot}%{_mandir}/man8/%{name}-upgrade.8

for i in ftdetect indent syntax; do
    install -p -D -m644 contrib/vim/${i}/nginx.vim \
        %{buildroot}%{_datadir}/vim/vimfiles/${i}/%{name}.vim
done


%pre filesystem
getent group %{nginx_group} > /dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} > /dev/null || \
    useradd -r -d %{nginx_home} -g %{nginx_group} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi
%endif
if [ $1 -ge 1 ]; then
    # Make sure these directories are not world readable.
    chmod 700 %{nginx_home}
    chmod 700 %{nginx_home_tmp}
    chmod 700 %{nginx_logdir}
fi

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun %{name}.service
if [ $1 -ge 1 ]; then
    /usr/bin/%{name}-upgrade &>/dev/null ||:
fi
%else
if [ $1 -eq 1 ]; then
    /sbin/service %{name} upgrade ||:
fi
%endif

%files
%defattr(-,root,root,-)
%doc CHANGES README
%{!?_licensedir:%global license %doc}
%license LICENSE
%{nginx_datadir}/html/*
%{_bindir}/%{name}-upgrade
%{_sbindir}/%{name}
%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%{_datadir}/vim/vimfiles/syntax/%{name}.vim
%{_datadir}/vim/vimfiles/indent/%{name}.vim
%{_mandir}/man3/%{name}.3pm*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/%{name}-upgrade.8*
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/%{name}.conf
%config(noreplace) %{nginx_confdir}/%{name}.conf.default
%if 0%{?with_modsec}
%config(noreplace) %{nginx_confdir}/modsecurity.conf
%config(noreplace) %{nginx_confdir}/unicode.mapping
%dir %{nginx_confdir}/modsecurity.d/activated_rules/
%dir %{nginx_confdir}/modsecurity.d/local_rules/
%endif
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{perl_vendorarch}/auto/%{name}
%{perl_vendorarch}/%{name}.pm
%{perl_vendorarch}/auto/%{name}/%{name}.so
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}

%files filesystem
%dir %{nginx_datadir}
%dir %{nginx_datadir}/html
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%dir %{nginx_confdir}/default.d

%if 0%{?with_modsec_crs}
%files modsec_crs
%defattr(-,root,root,-)
%doc owasp-modsecurity-crs-*/{CHANGES,INSTALL,README.md}
%{!?_licensedir:%global license %doc}
%license owasp-modsecurity-crs-*/LICENSE
%{nginx_confdir}/modsecurity.d/modsecurity_crs_10_config.conf
%{nginx_confdir}/modsecurity.d/activated_rules/
%{nginx_datadir}/modsecurity.d/base_rules/
%{nginx_datadir}/modsecurity.d/optional_rules/
%{nginx_datadir}/modsecurity.d/experimental_rules/
%{nginx_datadir}/modsecurity.d/slr_rules/
%endif


%changelog
* Sat Oct 15 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.5-1.modsec_2.9.0
- update to upstream release 1.11.5
- Remove --with-ipv6 option, IPv6 support is configured automatically

* Mon Sep 26 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.4-1.modsec_2.9.0
- update to upstream release 1.11.4
- update ngx_fancyindex 0.4.1
- update ngx_lua 0.10.6
- update ngx_echo 0.60

* Mon Aug  1 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.3-1.modsec_2.9.0
- update to upstream release 1.11.3

* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.2-1.modsec_2.9.0
- update to upstream release 1.11.2
- update ngx_fancyindex 0.4.0

* Fri Jun  3 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.1-1.modsec_2.9.0
- update to upstream release 1.11.1

* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 1:1.11.0-1.modsec_2.9.0
- update to upstream release 1.11.0
- update ngx_lua 0.10.5
- update ngx_devel_kit 0.3.0
- update ngx_echo 0.59

* Fri May  6 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.15-1.modsec_2.9.0
- update to upstream release 1.9.15

* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.14-1.modsec_2.9.0
- update to upstream release 1.9.14

* Thu Mar 31 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.13-1.modsec_2.9.0
- update to upstream release 1.9.13
- update ngx_lua 0.10.2
- update ngx_devel_kit 0.3.0rc1
- update ngx_echo 0.59rc1

* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.12-1.modsec_2.9.0
- update to upstream release 1.9.12
- update ngx_lua 0.10.1-rc1

* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.11-1.modsec_2.9.0
- update to upstream release 1.9.11
- update ngx_lua 0.10.1-rc0

* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.10-1.modsec_2.9.0
- update to upstream release 1.9.10
- update ngx_lua 0.10.0
- update ngx_fancyindex 0.3.6

* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.9-1.modsec_2.9.0
- update to upstream release 1.9.9
- update ngx_lua 0.9.20
- update OWASP ModSecurity Core Rule Set to 60c8bc9

* Sat Nov 21 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.7-1.modsec_2.9.0
- update to upstream release 1.9.7

* Thu Oct 29 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.6-1.modsec_2.9.0
- update to upstream release 1.9.6

* Mon Oct  5 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.5-3.modsec_2.9.0
- support el5
- add ngx_lua, ngx_echo module

* Thu Oct  1 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.5-2.modsec_2.9.0
- add OWASP ModSecurity Core Rule Set

* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.5-1.modsec_2.9.0
- update to upstream release 1.9.5

* Mon Sep 07 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.4-1.modsec_2.9.0
- update to upstream release 1.9.4

* Fri Jul 03 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-10
- switch back to /bin/kill in logrotate script due to SELinux denials

* Tue Jun 16 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-9
- fix path to png in error pages (#1232277)
- optimize png images with optipng

* Sun Jun 14 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-8
- replace /bin/kill with /usr/bin/systemctl kill in logrotate script (#1231543)
- remove After=syslog.target in nginx.service (#1231543)
- replace ExecStop with KillSignal=SIGQUIT in nginx.service (#1231543)

* Wed Jun 03 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.1-1.modsec_2.9.0
- update to upstream release 1.9.1
- Feature: the "reuseport" parameter of the "listen" directive
- Feature: the $upstream_connect_time variable

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.8.0-7
- Perl 5.22 rebuild

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-6
- revert previous change

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-5
- move default server to default.conf (#1220094)

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-4
- add TimeoutStopSec=5 and KillMode=mixed to nginx.service
- set worker_processes to auto
- add some common options to the http block in nginx.conf
- run nginx-upgrade on package update
- remove some redundant scriptlet commands
- listen on ipv6 for default server (#1217081)

* Wed Apr 29 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.0-1.modsec_2.9.0
- update to upstream release 1.9.0
- add --with-stream and --with-threads

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-3
- improve nginx-upgrade script

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-2
- add --with-pcre-jit

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-1
- update to upstream release 1.8.0

* Thu Apr 09 2015 mosquito <sensor.wen@gmail.com> - 1:1.7.12-1.modsec_2.9.0
- update to upstream release 1.7.12

* Sun Mar 29 2015 mosquito <sensor.wen@gmail.com> - 1:1.7.11-1.modsec_2.9.0
- update to upstream release 1.7.11

* Sat Mar 07 2015 mosquito <sensor.wen@gmail.com> - 1:1.7.10-3.modsec_2.9.0
- Update fancyindex to 0.3.5
- add --with-http_auth_request_module

* Thu Mar 05 2015 mosquito <sensor.wen@gmail.com> - 1:1.7.10-2.modsec_2.9.0
- Update mod_security to 2.9.0

* Sun Feb 15 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.7.10-1
- update to upstream release 1.7.10
- remove systemd conditionals

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-4
- fix package ownership of directories

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-3
- add vim files (#1142849)

* Mon Sep 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-2
- create nginx-filesystem subpackage (patch from Remi Collet)
- create /etc/nginx/default.d as a drop-in directory for configuration files
  for the default server block
- clean up nginx.conf

* Wed Sep 17 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-1
- update to upstream release 1.6.2
- CVE-2014-3616 nginx: virtual host confusion (#1142573)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.6.1-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-2
- add logic for EPEL 7

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-1
- update to upstream release 1.6.1
- (#1126891) CVE-2014-3556: SMTP STARTTLS plaintext injection flaw

* Wed Jul 02 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.6.0-3
- Fix FTBFS on aarch64 (#1115559)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.0-1
- update to upstream release 1.6.0

* Tue Mar 18 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.7-1
- update to upstream release 1.4.7

* Wed Mar 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.6-1
- update to upstream release 1.4.6

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-2
- avoid multiple index directives (#1065488)

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-1
- update to upstream release 1.4.5

* Wed Nov 20 2013 Peter Borsa <peter.borsa@gmail.com> - 1:1.4.4-1
- Update to upstream release 1.4.4
- Security fix BZ 1032267

* Sun Nov 03 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.3-1
- update to upstream release 1.4.3

* Fri Aug 09 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 1:1.4.2-3
- Add in conditionals to build for non-systemd targets

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.2-2
- Perl 5.18 rebuild

* Fri Jul 19 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.2-1
- update to upstream release 1.4.2

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.1-3
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 1:1.4.1-2
- rebuild for new GD 2.1.0

* Tue May 07 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.1-1
- update to upstream release 1.4.1 (#960605, #960606):
  CVE-2013-2028 stack-based buffer overflow when handling certain chunked
  transfer encoding requests

* Sun Apr 28 2013 Dan Horák <dan[at]danny.cz> - 1:1.4.0-2
- gperftools exist only on selected arches

* Fri Apr 26 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.0-1
- update to upstream release 1.4.0
- enable SPDY module (new in this version)
- enable http gunzip module (new in this version)
- enable google perftools module and add gperftools-devel to BR
- enable debugging (#956845)
- trim changelog

* Tue Apr 02 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.8-1
- update to upstream release 1.2.8

* Fri Feb 22 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-2
- make sure nginx directories are not world readable (#913724, #913735)

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-1
- update to upstream release 1.2.7
- add .asc file

* Tue Feb 05 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-6
- use 'kill' instead of 'systemctl' when rotating log files to workaround
  SELinux issue (#889151)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-5
- uncomment "include /etc/nginx/conf.d/*.conf by default but leave the
  conf.d directory empty (#903065)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-4
- add comment in nginx.conf regarding "include /etc/nginf/conf.d/*.conf"
  (#903065)

* Wed Dec 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-3
- use correct file ownership when rotating log files

* Tue Dec 18 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-2
- send correct kill signal and use correct file permissions when rotating
  log files (#888225)
- send correct kill signal in nginx-upgrade

* Tue Dec 11 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-1
- update to upstream release 1.2.6

* Sat Nov 17 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.5-1
- update to upstream release 1.2.5

* Sun Oct 28 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.4-1
- update to upstream release 1.2.4
- introduce new systemd-rpm macros (#850228)
- link to official documentation not the community wiki (#870733)
- do not run systemctl try-restart after package upgrade to allow the
  administrator to run nginx-upgrade and avoid downtime
- add nginx man page (#870738)
- add nginx-upgrade man page and remove README.fedora
- remove chkconfig from Requires(post/preun)
- remove initscripts from Requires(preun/postun)
- remove separate configuration files in "/etc/nginx/conf.d" directory
  and revert to upstream default of a centralized nginx.conf file
  (#803635) (#842738)

* Fri Sep 21 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.3-1
- update to upstream release 1.2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.1-2
- Perl 5.16 rebuild

* Sun Jun 10 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.1-1
- update to upstream release 1.2.1

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.0-2
- Perl 5.16 rebuild

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.0-1
- update to upstream release 1.2.0

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-4
- add nginx-upgrade to replace functionality from the nginx initscript
  that was lost after migration to systemd
- add README.fedora to describe usage of nginx-upgrade
- nginx.logrotate: use built-in systemd kill command in postrotate script
- nginx.service: start after syslog.target and network.target
- nginx.service: remove unnecessary references to config file location
- nginx.service: use /bin/kill instead of "/usr/sbin/nginx -s" following
  advice from nginx-devel
- nginx.service: use private /tmp

* Mon May 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-3
- fix incorrect postrotate script in nginx.logrotate

* Thu Apr 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-2
- renable auto-cc-gcc patch due to warnings on rawhide

* Sat Apr 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-1
- update to upstream release 1.0.15
- no need to apply auto-cc-gcc patch
- add %%global _hardened_build 1

* Thu Mar 15 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.14-1
- update to upstream release 1.0.14
- amend some %%changelog formatting

* Tue Mar 06 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.13-1
- update to upstream release 1.0.13
- amend --pid-path and --log-path

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-5
- change pid path in nginx.conf to match systemd service file

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-3
- fix %%pre scriptlet

* Mon Feb 20 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-2
- update upstream URL
- replace %%define with %%global
- remove obsolete BuildRoot tag, %%clean section and %%defattr
- remove various unnecessary commands
- add systemd service file and update scriptlets
- add Epoch to accommodate %%triggerun as part of systemd migration

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.12-1
- Update to 1.0.12

* Thu Nov 17 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.10-1
- Bugfix: a segmentation fault might occur in a worker process if resolver got a big DNS response. Thanks to Ben Hawkes.
- Bugfix: in cache key calculation if internal MD5 implementation wasused; the bug had appeared in 1.0.4.
- Bugfix: the module ngx_http_mp4_module sent incorrect "Content-Length" response header line if the "start" argument was used. Thanks to Piotr Sikora.

* Thu Oct 27 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.8-1
- Update to new 1.0.8 stable release

* Fri Aug 26 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.5-1
- Update nginx to Latest Stable Release

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-3
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-2
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53.5
- Extract out default config into its own file (bug #635776)

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-4
- Revert ownership of log dir

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-3
- Change ownership of /var/log/nginx to be 0700 nginx:nginx
- update init script to use killproc -p
- add reopen_logs command to init script
- update init script to use nginx -q option

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-2
- Fix linking of perl module

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-1
- Update to new stable 0.8.53

* Sat Jul 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-2
- add Provides: webserver (bug #619693)

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-1
- Update to new stable 0.7.67
- fix bugzilla #591543

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.65-2
- Mass rebuild with perl-5.12.0

* Mon Feb 15 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.65-1
- Update to new stable 0.7.65
- change ownership of logdir to root:root
- add support for ipv6 (bug #561248)
- add random_index_module
- add secure_link_module

* Fri Dec 04 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.64-1
- Update to new stable 0.7.64
