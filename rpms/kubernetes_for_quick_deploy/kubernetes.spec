%global debug_package %{nil}
%global pkgurl       https://dl.k8s.io/v%{version}/%{name}-server-linux-amd64.tar.gz
%global commit       7fa1c1756d8bc963f1a389f4a6937dc71f08ada2
%global shortcommit  %(c=%{commit}; echo ${c:0:7})

Name:          kubernetes
Version:       1.7.0
Release:       1%{?dist}
Summary:       Container cluster management
License:       ASL 2.0
URL:           https://k8s.io/kubernetes
Source0:       https://github.com/kubernetes/contrib/archive/master.tar.gz
Source3:       kubernetes-accounting.conf
Source4:       kubeadm.conf

ExclusiveArch: x86_64
BuildRequires: wget 
Requires:      %{name}-master = %{version}-%{release}
Requires:      %{name}-node = %{version}-%{release}

%description
%{summary}

##############################################
%package master
Summary:       Kubernetes services for master host
BuildRequires: systemd
Requires(pre): shadow-utils
Requires:      %{name}-client = %{version}-%{release}

# if node is installed with node, version and release must be the same
Conflicts:     %{name}-node < %{version}-%{release}
Conflicts:     %{name}-node > %{version}-%{release}

%description master
Kubernetes services for master host

##############################################
%package node
Summary:       Kubernetes services for node host
BuildRequires: systemd
Requires:      docker
Requires:      conntrack-tools
Requires(pre): shadow-utils
Requires:      socat
Requires:      %{name}-client = %{version}-%{release}

# if master is installed with node, version and release must be the same
Conflicts:     %{name}-master < %{version}-%{release}
Conflicts:     %{name}-master > %{version}-%{release}

%description node
Kubernetes services for node host

##############################################
%package kubeadm
Summary:       Kubernetes tool for standing up clusters
Requires:      %{name}-node = %{version}-%{release}
Requires:      containernetworking-cni

%description kubeadm
Kubernetes tool for standing up clusters

##############################################
%package client
Summary: Kubernetes client tools

%description client
Kubernetes client tools like kubectl

##############################################
%prep
%setup -q -n contrib-master
wget -O %{name}.tar.gz %{pkgurl}
tar xf %{name}.tar.gz
strip %{name}/server/bin/* &>/dev/null ||:

%build

##############################################
%install
pushd %{name}
install -m 755 -d %{buildroot}%{_bindir}

echo "+++ INSTALLING hyperkube"
install -p -m 755 -t %{buildroot}%{_bindir} server/bin/hyperkube

echo "+++ INSTALLING kube-apiserver"
install -p -m 754 -t %{buildroot}%{_bindir} server/bin/kube-apiserver

echo "+++ INSTALLING kubeadm"
install -p -m 755 -t %{buildroot}%{_bindir} server/bin/kubeadm
install -d -m 0755 %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d
install -p -m 0644 -t %{buildroot}%{_sysconfdir}/systemd/system/kubelet.service.d %{SOURCE4}

binaries=(kube-controller-manager kube-scheduler kube-proxy kubelet kubectl)
for bin in "${binaries[@]}"; do
  echo "+++ HARDLINKING ${bin} to hyperkube"
  ln %{buildroot}%{_bindir}/hyperkube %{buildroot}%{_bindir}/${bin}
done

# install the bash completion
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions/
server/bin/kubectl completion bash > %{buildroot}%{_datadir}/bash-completion/completions/kubectl
popd

# Optimize config
cat >> init/systemd/environ/kubelet <<EOF
KUBELET_ARGS="--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0 --cgroup-driver=systemd --cluster-dns=10.254.0.2 --cluster-domain=cluster.local. --hairpin-mode=promiscuous-bridge --serialize-image-pulls=false"

#KUBELET_ARGS="--experimental-bootstrap-kubeconfig=/etc/kubernetes/bootstrap.kubeconfig --kubeconfig=/etc/kubernetes/kubelet.kubeconfig --require-kubeconfig --cert-dir=/etc/kubernetes/pki"
EOF

cat >> init/systemd/environ/apiserver <<EOF
# --authorization-mode=[AlwaysDeny|AlwaysAllow|ABAC|RBAC]
KUBE_API_ARGS="--authorization-mode=AlwaysAllow --service-node-port-range=30000-32767 --enable-swagger-ui=true --apiserver-count=3 --audit-log-maxage=30 --audit-log-maxbackup=3 --audit-log-maxsize=100 --audit-log-path=/tmp/k8s-audit.log --event-ttl=1h"

#KUBE_API_ARGS="--runtime-config=rbac.authorization.k8s.io/v1beta1 --kubelet-https=true --experimental-bootstrap-token-auth --token-auth-file=token.csv --tls-cert-file=kube.pem --tls-private-key-file=kube-key.pem --client-ca-file=ca.pem --service-account-key-file=ca-key.pem --etcd-cafile=ca.pem --etcd-certfile=kube.pem --etcd-keyfile=kube-key.pem"
EOF

cat >> init/systemd/environ/controller-manager <<EOF
KUBE_CONTROLLER_MANAGER_ARGS="--address=127.0.0.1 --service-cluster-ip-range=10.254.0.0/16 --cluster-name=kubernetes "
#KUBE_CONTROLLER_MANAGER_ARGS+="--cluster-signing-cert-file=ca.pem --cluster-signing-key-file=ca-key.pem --service-account-private-key-file=ca-key.pem --root-ca-file=ca.pem --leader-elect=true"
EOF

cat >> init/systemd/environ/proxy <<EOF
#KUBE_PROXY_ARGS="--bind-address=Local_IP --hostname-override=Local_IP --kubeconfig=/etc/kubernetes/kube-proxy.kubeconfig --cluster-cidr=10.254.0.0/16"
EOF

cat >> init/systemd/environ/scheduler <<EOF
KUBE_SCHEDULER_ARGS="--leader-elect=true --address=127.0.0.1"
EOF

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -t %{buildroot}%{_sysconfdir}/%{name} init/systemd/environ/*

# install service files
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} init/systemd/*.service

# install the place the kubelet defaults to put volumes
install -d %{buildroot}%{_sharedstatedir}/kubelet

# place contrib/init/systemd/tmpfiles.d/kubernetes.conf to /usr/lib/tmpfiles.d/kubernetes.conf
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
install -p -m 0644 -t %{buildroot}/%{_tmpfilesdir} init/systemd/tmpfiles.d/kubernetes.conf
mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

# enable CPU and Memory accounting
install -d -m 0755 %{buildroot}/%{_sysconfdir}/systemd/system.conf.d
install -p -m 0644 -t %{buildroot}/%{_sysconfdir}/systemd/system.conf.d %{SOURCE3}

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

##############################################
%pre master
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post master
%systemd_post kube-apiserver kube-scheduler kube-controller-manager

%preun master
%systemd_preun kube-apiserver kube-scheduler kube-controller-manager

%postun master
%systemd_postun

%pre node
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post node
%systemd_post kubelet kube-proxy
# If accounting is not currently enabled systemd reexec
if [[ `systemctl show docker kubelet | grep -q -e CPUAccounting=no -e MemoryAccounting=no; echo $?` -eq 0 ]]; then
  systemctl daemon-reexec
fi

%preun node
%systemd_preun kubelet kube-proxy

%postun node
%systemd_postun

##############################################
%files
# empty as it depends on master and node

%files master
%attr(754, -, kube) %caps(cap_net_bind_service=ep) %{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kube-scheduler
%{_bindir}/hyperkube
%{_unitdir}/kube-apiserver.service
%{_unitdir}/kube-controller-manager.service
%{_unitdir}/kube-scheduler.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/scheduler
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%{_tmpfilesdir}/kubernetes.conf
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files node
%{_bindir}/kubelet
%{_bindir}/kube-proxy
%{_bindir}/hyperkube
%{_unitdir}/kube-proxy.service
%{_unitdir}/kubelet.service
%dir %{_sharedstatedir}/kubelet
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%config(noreplace) %{_sysconfdir}/systemd/system.conf.d/kubernetes-accounting.conf
%{_tmpfilesdir}/kubernetes.conf
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files kubeadm
%{_bindir}/kubeadm
%dir %{_sysconfdir}/systemd/system/kubelet.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/kubelet.service.d/kubeadm.conf

%files client
%{_bindir}/kubectl
%{_bindir}/hyperkube
%{_datadir}/bash-completion/completions/kubectl

%changelog
* Fri Jul  7 2017 mosquito <sensor.wen@gmail.com> - 1.7.0-1
- Initial build
