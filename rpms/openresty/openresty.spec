# If you use rhel, please add epel repository.
# If you use el6, please add epel-testing repository.
%if ! 0%{?rhel} && ! 0%{?fedora}
%global  rhel %(%{__python} -c "import platform;print platform.dist()[1][0]")
%global  dist .el5
%endif
%global  debug_package       %{nil}
%global  _hardened_build     1
%global  nginx_user          nginx
%global  nginx_group         %{nginx_user}
%global  nginx_home          %{_localstatedir}/lib/openresty
%global  nginx_home_tmp      %{nginx_home}/tmp
%global  nginx_confdir       %{_sysconfdir}/openresty
%global  nginx_datadir       %{_datadir}/openresty
%global  nginx_logdir        %{_localstatedir}/log/openresty
%global  nginx_webroot       %{nginx_datadir}/html
%global  with_http2          1

# provides filter
# the modern macros for Provides and Requires Filtering
# do not work for EPEL 5 or older.
%if 0%{?rhel} > 6 || 0%{?fedora}
%global  __provides_exclude  (luajit|json)
%else
%{?filter_setup:
%filter_from_provides /luajit/d; /json/d; /parser/d;
%filter_setup}
%endif

# nginx mainline version
%global  ngx_version         1.11.2
%global  with_ngx_mainline   1

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
%global  fancy_version       0.4.0
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

Name:              openresty
Epoch:             1
Version:           1.9.15.1
%if 0%{?with_modsec}
Release:           1.modsec_%{modsec_version}%{dist}
%else
Release:           1%{?dist}
%endif

Summary:           a fast Web App Server by extending Nginx
Summary(zh_CN):    基于 Nginx 的高性能 Web 应用服务器
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://openresty.org

Source0:           https://openresty.org/download/ngx_%{name}-%{version}.tar.gz
Source1:           https://openresty.org/download/ngx_%{name}-%{version}.tar.gz.asc
Source2:           http://nginx.org/download/nginx-%{ngx_version}.tar.gz
Source3:           http://nginx.org/download/nginx-%{ngx_version}.tar.gz.asc
Source4:           https://www.modsecurity.org/tarball/2.9.0/modsecurity-2.9.0.tar.gz
Source5:           https://www.modsecurity.org/tarball/2.8.0/modsecurity-2.8.0.tar.gz
Source6:           https://github.com/SpiderLabs/owasp-modsecurity-crs/archive/%{modsec_crs_commit}/owasp-modsecurity-crs-%{modsec_crs_shortcommit}.tar.gz
Source7:           https://github.com/aperezdc/ngx-fancyindex/archive/v%{fancy_version}/ngx-fancyindex-%{fancy_version}.tar.gz
Source8:           ftp://xmlsoft.org/libxml2/old/libxml2-%{libxml2_version}.tar.gz
Source9:           https://archive.apache.org/dist/httpd/httpd-%{httpd_version}.tar.gz
Source10:          openresty.service
Source11:          openresty.logrotate
Source12:          openresty.conf
Source13:          openresty-upgrade
Source14:          openresty-upgrade.8
Source15:          openresty.init
Source16:          openresty.sysconfig
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
# OpenResty ngx_postgres, ngx_drizzle
BuildRequires:     lua-devel
BuildRequires:     libatomic_ops-devel
BuildRequires:     readline-devel
BuildRequires:     libpqxx-devel

Requires:          openresty-filesystem = %{epoch}:%{version}-%{release}
Requires:          GeoIP
Requires:          gd
Requires:          openssl
Requires:          pcre
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):     openresty-filesystem
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
ngx_openresty is a full-fledged web application server by bundling the
standard nginx core, lots of 3rd-party nginx modules, as well as most of
their external dependencies.

%package filesystem
Group:             System Environment/Daemons
Summary:           The basic directory layout for the OpenResty server
%if 0%{?rhel} != 5
BuildArch:         noarch
%endif
Requires(pre):     shadow-utils

%description filesystem
The %{name}-filesystem package contains the basic directory layout
for the OpenResty server including the correct permissions for the
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
%setup -q -a2 -a4 -a5 -a6 -a7 -a8 -a9 -n %{name}-%{version}
%if 0%{?fedora} > 21
pushd modsecurity-%{modsec_version}
%patch1 -p1
popd
%endif
%if 0%{?rhel} != 5
%patch0 -p0 -d nginx-%{ngx_version}
%endif

# Change server and library name
%if 0%{?with_ngx_mainline}
pushd nginx-%{ngx_version}
%else
pushd bundle/nginx-*/
%endif
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
popd
%if 0%{?with_ngx_mainline}
rm -rf bundle/nginx-*
mv nginx-%{ngx_version} bundle/
%endif


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
    --with-threads \
    --with-libatomic \
    --with-stream \
    --with-stream_ssl_module \
    --with-lua51 \
    --with-luajit \
    --with-http_postgres_module \
    --with-pg_config=%{_bindir}/pg_config \
    --with-http_iconv_module \
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

#    --with-libdrizzle=/path/to/drizzle
#    --with-http_drizzle_module
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

install -p -D -m 0644 %{_builddir}/%{name}-%{version}/bundle/nginx-*/man/nginx.8 \
    %{buildroot}%{_mandir}/man8/%{name}.8

install -p -D -m 0755 %{SOURCE13} %{buildroot}%{_bindir}/%{name}-upgrade
install -p -D -m 0644 %{SOURCE14} %{buildroot}%{_mandir}/man8/%{name}-upgrade.8

for i in ftdetect indent syntax; do
    install -p -D -m644 bundle/nginx-*/contrib/vim/${i}/nginx.vim \
        %{buildroot}%{_datadir}/vim/vimfiles/${i}/%{name}.vim
done

# resty tool
sed -i '10,300s|nginx|%{name}|g' %{buildroot}%{_datadir}/%{name}/bin/resty
ln -sfv %{_datadir}/%{name}/bin/resty %{buildroot}%{_bindir}/resty


%pre filesystem
getent group %{nginx_group} > /dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} > /dev/null || \
    useradd -r -d %{nginx_home} -g %{nginx_group} \
    -s /sbin/nologin -c "OpenResty web server" %{nginx_user}
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
%doc bundle/nginx-*/{CHANGES,README} README.markdown
%{!?_licensedir:%global license %doc}
%license bundle/nginx-*/LICENSE
%{nginx_datadir}/resty.index
%{nginx_datadir}/bin/*
%{nginx_datadir}/pod/*
%{nginx_datadir}/html/*
%{nginx_datadir}/luajit/*
%{nginx_datadir}/lualib/*
%exclude %{nginx_datadir}/nginx/
%{_bindir}/resty
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
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.15.1-1.modsec_2.9.0
- update to upstream release 1.11.2
- update ngx_fancyindex 0.4.0
* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> - 1:1.9.7.2-1.modsec_2.9.0
- update to upstream release 1.9.10
- update ngx_fancyindex 0.3.6
* Mon Oct  5 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.3.1-3.modsec_2.9.0
- support el5
- don't provide luajit library
* Thu Oct  1 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.3.1-2.modsec_2.9.0
- add OWASP ModSecurity Core Rule Set
- change ngx_http_perl_module name
* Tue Sep 29 2015 mosquito <sensor.wen@gmail.com> - 1:1.9.3.1-1.modsec_2.9.0
- initial build
- update to upstream release 1.9.5
