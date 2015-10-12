# If you use rhel, please add epel repository.
# If you use el6, please add epel and puias-computational repository.
# - http://puias.math.ias.edu/data/puias/computational/6/x86_64/
%if ! 0%{?rhel} && ! 0%{?fedora}
%global  rhel %(%{__python} -c "import platform;print platform.dist()[1][0]")
%global  dist .el5
%endif
%global  debug_package       %{nil}
%global  _hardened_build     1
%global  nginx_user          nginx
%global  nginx_group         %{nginx_user}
%global  nginx_home          %{_localstatedir}/lib/tengine
%global  nginx_home_tmp      %{nginx_home}/tmp
%global  nginx_confdir       %{_sysconfdir}/tengine
%global  nginx_datadir       %{_datadir}/tengine
%global  nginx_logdir        %{_localstatedir}/log/tengine
%global  nginx_webroot       %{nginx_datadir}/html
%global  with_http2          0

# ngx_http_lua_module
%global  ngx_lua_version     0.9.16
%global  with_ngx_lua_latest 1

# ModSecurity module
%if 0%{?rhel} == 5
%global  modsec_version      2.8.0
%else
%global  modsec_version      2.9.0
%endif
%global  with_modsec         1

# OWASP ModSecurity Core Rule Set (CRS)
%global  modsec_crs_version  2.2.9
%global  modsec_crs_commit   c63affc9dfa6294ecf8782ae4d1f1fb2c9fd5a18
%global  modsec_crs_shortcommit %(c=%{modsec_crs_commit};echo ${c:0:7})
%global  with_modsec_crs     1

# FancyIndex module
%global  fancy_version       0.3.5
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

Name:              tengine
Epoch:             1
Version:           2.1.1
%if 0%{?with_modsec}
Release:           3.modsec_%{modsec_version}%{?dist}
%else
Release:           3%{?dist}
%endif

Summary:           A high performance web server and reverse proxy server
Summary(zh_CN):    基于 Nginx 的高性能 Web 服务器和反向代理服务器
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://tengine.taobao.org

Source0:           http://tengine.taobao.org/download/%{name}-%{version}.tar.gz
Source1:           https://github.com/openresty/lua-nginx-module/archive/v%{ngx_lua_version}/lua-nginx-module-%{ngx_lua_version}.tar.gz
Source2:           https://www.modsecurity.org/tarball/2.9.0/modsecurity-2.9.0.tar.gz
Source3:           https://www.modsecurity.org/tarball/2.8.0/modsecurity-2.8.0.tar.gz
Source4:           https://github.com/SpiderLabs/owasp-modsecurity-crs/archive/%{modsec_crs_commit}/owasp-modsecurity-crs-%{modsec_crs_shortcommit}.tar.gz
Source5:           https://github.com/aperezdc/ngx-fancyindex/archive/v%{fancy_version}/ngx-fancyindex-%{fancy_version}.tar.gz
Source6:           ftp://xmlsoft.org/libxml2-%{libxml2_version}.tar.gz
Source7:           http://www.apache.org/dist/httpd/httpd-%{httpd_version}.tar.gz
Source10:          tengine.service
Source11:          tengine.logrotate
Source12:          tengine.conf
Source13:          tengine-upgrade
Source14:          tengine-upgrade.8
Source15:          tengine.init
Source16:          tengine.sysconfig
Source100:         index.html
Source101:         poweredby.png
Source102:         tengine-logo.png
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
# Tengine
BuildRequires:     lua-devel
%if 0%{?rhel} != 5
BuildRequires:     luajit-devel
%endif
BuildRequires:     jemalloc-devel
BuildRequires:     libatomic_ops-devel

Requires:          tengine-filesystem = %{epoch}:%{version}-%{release}
Requires:          GeoIP
Requires:          gd
Requires:          openssl
Requires:          pcre
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):     tengine-filesystem
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
Tengine is a web server originated by Taobao, the largest e-commerce
website in Asia. It is based on the Nginx HTTP server and has many
advanced features. Tengine has proven to be very stable and efficient
on some of the top 100 websites in the world, including taobao.com and
tmall.com.

%package filesystem
Group:             System Environment/Daemons
Summary:           The basic directory layout for the Tengine server
%if 0%{?rhel} != 5
BuildArch:         noarch
%endif
Requires(pre):     shadow-utils

%description filesystem
The %{name}-filesystem package contains the basic directory layout
for the Tengine server including the correct permissions for the
directories.

%package devel
Group:             System Environment/Daemons
Summary:           DSO tool for %{name}
%if 0%{?rhel} != 5
BuildArch:         noarch
%endif
Requires:          %{name} = %{version}-%{release}

%description devel
This package provides the DSO tool for %{name}.

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
%setup -q -a1 -a2 -a3 -a4 -a5 -a6 -a7
%if 0%{?fedora} > 21
pushd modsecurity-%{modsec_version}
%patch1 -p1
popd
%endif
%patch0 -p0

# Use latest version module
%if 0%{?with_ngx_lua_latest}
rm -rf modules/ngx_http_lua_module
mv lua-nginx-module-%{ngx_lua_version} modules/ngx_http_lua_module
%endif

# Change server and library name
sed -i 's|nginx/|%{name}/|' src/core/nginx.h
sed -i -e '/NAME/s|nginx|%{name}|' \
    -e 's|nginx.pm|%{name}.pm|g' \
    -e 's|nginx.xs|%{name}.xs|' \
    src/http/modules/perl/Makefile.PL \
    auto/lib/perl/make
sed -i 's|nginx|%{name}|g' \
    src/http/modules/perl/nginx.{pm,xs}
mv src/http/modules/perl/{nginx,%{name}}.pm
mv src/http/modules/perl/{nginx,%{name}}.xs
%if 0%{?rhel} != 5
sed -i -E '/(embedding|get_sv)/s|nginx|%{name}|' \
%else
sed -i -r '/(embedding|get_sv)/s|nginx|%{name}|' \
%endif
    src/http/modules/perl/ngx_http_perl_module.c


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

# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
./configure \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{name} \
    --dso-tool-path=%{_sbindir}/dso_tool \
    --includedir=%{_includedir}/%{name} \
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
    --with-ipv6 \
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
    --with-jemalloc \
    --with-backtrace_module \
    --with-http_concat_module \
    --with-http_lua_module=shared \
    --with-lua-inc=%{_includedir} \
    --with-lua-lib=%{_libdir} \
%if 0%{?rhel} > 6 || 0%{?fedora}
    --with-luajit-inc=%{_includedir}/luajit-2.0 \
    --with-luajit-lib=%{_libdir} \
    --with-http_tfs_module=shared \
%endif
    --with-http_upstream_ip_hash_module=shared \
    --with-http_upstream_least_conn_module=shared \
    --with-http_upstream_session_sticky_module=shared \
%if 0%{?with_gperftools}
    --with-google_perftools_module \
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

%if 0%{?with_systemd}
install -p -D -m 0644 %{SOURCE10} \
    %{buildroot}%{_unitdir}/%{name}.service
%else
install -p -D -m 0755 %{SOURCE15} \
    %{buildroot}%{_initrddir}/%{name}
install -p -D -m 0644 %{SOURCE16} \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%endif

install -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/default.d
install -p -d -m 0700 %{buildroot}%{nginx_home}
install -p -d -m 0700 %{buildroot}%{nginx_home_tmp}
install -p -d -m 0700 %{buildroot}%{nginx_logdir}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}

install -p -m 0644 %{SOURCE12} \
    %{buildroot}%{nginx_confdir}
mv %{buildroot}%{nginx_confdir}/{nginx,%{name}}.conf.default
%if 0%{?rhel} < 7 && ! 0%{?fedora}
    sed -i 's|/run/%{name}.pid|/var/run/%{name}.pid|' %{buildroot}%{nginx_confdir}/%{name}.conf
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
install -m0644 modsecurity_crs_10_setup.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/modsecurity.d/modsecurity_crs_10_config.conf
install -m0644 base_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/base_rules/
install -m0644 optional_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/optional_rules/
install -m0644 experimental_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/experimental_rules/
install -m0644 slr_rules/* %{buildroot}%{_datadir}/%{name}/modsecurity.d/slr_rules/

# activate base_rules
for f in `ls %{buildroot}%{_datadir}/%{name}/modsecurity.d/base_rules/`; do
    ln -s %{_datadir}/%{name}/modsecurity.d/base_rules/$f %{buildroot}%{_sysconfdir}/%{name}/modsecurity.d/activated_rules/$f;
done
popd
%endif
%endif

install -p -m 0644 %{SOURCE100} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE101} %{SOURCE102} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE103} %{SOURCE104} \
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
    -s /sbin/nologin -c "Tengine web server" %{nginx_user}
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
%doc CHANGES{,.cn} README
%{!?_licensedir:%global license %doc}
%license LICENSE
%{nginx_datadir}/html/*
%{nginx_datadir}/modules/*
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
%config(noreplace) %{nginx_confdir}/browsers
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
%config(noreplace) %{nginx_confdir}/module_stubs
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

%files devel
%defattr(-,root,root,-)
%{_sbindir}/dso_tool
%{_includedir}/%{name}/*.h

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
* Fri Oct  2 2015 mosquito <sensor.wen@gmail.com> - 1:2.1.1-3.modsec_2.9.0
- support el5
* Thu Oct  1 2015 mosquito <sensor.wen@gmail.com> - 1:2.1.1-2.modsec_2.9.0
- add OWASP ModSecurity Core Rule Set
- change ngx_http_perl_module name
* Wed Sep 30 2015 mosquito <sensor.wen@gmail.com> - 1:2.1.1-1.modsec_2.9.0
- initial build
