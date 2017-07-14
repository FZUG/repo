#!/bin/bash
#Description: Install TLS-based Kubernetes cluster from Scratch
#
#Service
# global - etcd, flanneld
# master - kube-apiserver, kube-scheduler, kube-controller-manager
# slave - docker, kubelet, kube-proxy
#
#Addons
# kubedns, dashboard, heapster, efk
#
#Client: KUBERNETES_MASTER=http://192.168.1.140:8080 kubectl -s master_ip
#Export Cert: openssl pkcs12 -export -in admin.crt -inkey admin.key -out admin.p12

function ENV() {
  export \
    Self=`pwd`/${BASH_SOURCE[0]} \
    K8S_PREFIX="/etc/kubernetes" \
    K8S_REPO="mosquito/kubernetes" \
    LOOP_IP="127.0.0.1" \
    NODE_IP=`ifconfig ens3 | awk 'NR==2{print $2}'` \
    MASTER_IP="192.168.1.140" \
    SLAVE_IP="192.168.1.141" \
    DNS_SERVER_IP="10.254.0.2" \
    DNS_DOMAIN="cluster.local" \
    ADDON_URL=$(lru_buhtig kubernetes/kubernetes cluster/addons)
}

function lru_buhtig() {
    if [ "0$1" != "0" ]; then
        github_raw_url="https://raw.githubusercontent.com"
        echo "${github_raw_url}/$1/master/$2"
    fi
}

function pkg_install() {
    if [ "0$1" != "0" ]; then
        echo "- installing" $@
        /bin/dnf -y install $@
    fi
}

function start_svc() {
    echo "-[$NODE_IP] start service" $@
    systemctl enable $@
    systemctl restart $@ &
    if [ "$NODE_IP" == "$MASTER_IP" ]; then
    	ssh root@${SLAVE_IP} "systemctl enable $@; systemctl restart $@ &" ||:
    fi
}

function prepare() {
    sysctl -w net.ipv4.ip_forward=1
    dnf copr enable $K8S_REPO -y
    >/tmp/command
    if [ "$NODE_IP" == "$MASTER_IP" ]; then
        test -f ~/.ssh/id_rsa || ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa -q
        ssh-copy-id root@${SLAVE_IP} ||:
    fi
}

function runfunc() {
    echo "- run $1 function on remote"
    Command=$(cat $Self | python3 -c "
import sys,re
content=sys.stdin.read()
func={}
for i in re.findall('function.+?{.*?\n}\n', content, re.S):
    func.update({re.search('function (.*)\(', i).group(1): i})
print(func['$1'])
")
    echo "$Command; $1; echo \$\$ >/tmp/pid" >> /tmp/command
}

function runfuncpost() {
    Target=${1:-$SLAVE_IP}
    scp /tmp/command root@${Target}:/tmp/
    ssh root@${Target} "bash /tmp/command" ||:
    while true; do
        _pid=`ssh root@${Target} "cat /tmp/pid"`
        ssh root@${Target} "test -d /proc/${_pid}" || break
        sleep 5
    done
    >/tmp/command
}

function gencert() {
    echo "-[$NODE_IP] generate certificates and keys"
    mkdir -p ${K8S_PREFIX}/pki; cd ${K8S_PREFIX}/pki
    # generate the ca.key and ca.crt, apiserver needs x509_v3
    cat > ca_ssl.cnf <<EOF
[req]
x509_extensions = v3_ca
distinguished_name = req_distinguished_name
[req_distinguished_name]
[v3_ca]
basicConstraints = critical,CA:true,pathlen:2
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOF
    openssl req -x509 -new -nodes -days 5000 \
        -subj "/C=CN/ST=BeiJing/L=BeiJing/O=k8s/OU=System/CN=kubernetes" \
        -extensions v3_ca -config ca_ssl.cnf \
        -newkey rsa:2048 -keyout ca.key -out ca.crt
    # generate the server.key and server.crt for kube-apiserver, etcd
    cat > master_ssl.cnf <<EOF
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[v3_req]
[usr_cert]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth,clientAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster
DNS.5 = kubernetes.default.svc.cluster.local
IP.1 = $LOOP_IP
IP.2 = $MASTER_IP
IP.3 = $SLAVE_IP
IP.4 = 10.254.0.1
EOF
    openssl genrsa -out server.key 2048
    openssl req -new -key server.key \
        -subj "/C=CN/ST=BeiJing/L=BeiJing/O=k8s/OU=System/CN=kubernetes" \
        -config master_ssl.cnf -out server.csr
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
        -extensions usr_cert -extfile master_ssl.cnf -out server.crt -days 5000
    # generate the client.key and client.crt for kube-proxy
    openssl genrsa -out client.key 2048
    openssl req -new -key client.key -out client.csr \
        -subj "/C=CN/ST=BeiJing/L=BeiJing/O=k8s/OU=System/CN=system:kube-proxy"
    openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 5000 -out client.crt
    # generate the admin.key and admin.crt for kubectl
    openssl genrsa -out admin.key 2048
    openssl req -new -key admin.key -out admin.csr \
        -subj "/C=CN/ST=BeiJing/L=BeiJing/O=system:masters/OU=System/CN=admin"
    openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 5000 -out admin.crt
    # clean
    rm -rf *.csr ca.srl *_ssl.cnf
    # copy cert and key to slave
    ssh root@${SLAVE_IP} "mkdir -p ${K8S_PREFIX}/pki" ||:
    scp ca.crt server* client* admin* root@${SLAVE_IP}:${K8S_PREFIX}/pki/
}

function genkubeconfig() {
    echo "-[$NODE_IP] generate kubeconfig files"
    test -f "/bin/kubectl" || pkg_install kubernetes-client
    # kube-apiserver use token.csv; kubelet use bootstrap.kubeconfig
    cd ${K8S_PREFIX}
    # generate TLS Bootstrapping Token (master)
    BOOTSTRAP_TOKEN=$(head -c 16 /dev/urandom | od -An -t x | tr -d ' ')
    cat > token.csv <<EOF
${BOOTSTRAP_TOKEN},kubelet-bootstrap,10001,"system:kubelet-bootstrap"
EOF
    # create bootstrap.kubeconfig for kubelet
    KUBE_APISERVER="https://${MASTER_IP}:6443"
    kubectl config set-cluster kubernetes \
        --certificate-authority=${K8S_PREFIX}/pki/ca.crt \
        --embed-certs=true --server=${KUBE_APISERVER} \
        --kubeconfig=bootstrap.kubeconfig
    kubectl config set-credentials kubelet-bootstrap \
        --token=${BOOTSTRAP_TOKEN} --kubeconfig=bootstrap.kubeconfig
    kubectl config set-context default \
        --cluster=kubernetes --user=kubelet-bootstrap --kubeconfig=bootstrap.kubeconfig
    kubectl config use-context default --kubeconfig=bootstrap.kubeconfig

    # create kube-proxy.kubeconfig for kube-proxy
    kubectl config set-cluster kubernetes \
        --certificate-authority=${K8S_PREFIX}/pki/ca.crt \
        --embed-certs=true --server=${KUBE_APISERVER} \
        --kubeconfig=kube-proxy.kubeconfig
    kubectl config set-credentials kube-proxy \
        --client-certificate=${K8S_PREFIX}/pki/client.crt \
        --client-key=${K8S_PREFIX}/pki/client.key \
        --embed-certs=true --kubeconfig=kube-proxy.kubeconfig
    kubectl config set-context default \
        --cluster=kubernetes --user=kube-proxy --kubeconfig=kube-proxy.kubeconfig
    kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig

    # create kubectl kubeconfig, save to ~/.kube/config
    # The file is used to Join slave($K8S_PREFIX/kubelet.kubeconfig) and/or kubectl command.
    kubectl config set-cluster kubernetes \
        --certificate-authority=${K8S_PREFIX}/pki/ca.crt \
        --embed-certs=true --server=${KUBE_APISERVER}
    kubectl config set-credentials admin \
        --client-certificate=${K8S_PREFIX}/pki/admin.crt \
        --client-key=${K8S_PREFIX}/pki/admin.key --embed-certs=true
    kubectl config set-context kubernetes \
        --cluster=kubernetes --user=admin
    kubectl config use-context kubernetes
    cp ~/.kube/config ./kubelet.kubeconfig
    chmod 755 ./kubelet.kubeconfig

    # copy bootstrap.kubeconfig and kube-proxy.kubeconfig to slave
    scp bootstrap.kubeconfig kube-proxy.kubeconfig kubelet.kubeconfig \
      root@${SLAVE_IP}:${K8S_PREFIX}
}

# $1 file, $2 pkgname, $3 svcname, $4 sed
#function chconf() {
#    test -f $1 || pkg_install $2
#    sed -i ''$3'' $1
#}

function apiserver_config() {
    # --anonymous-auth=true
    echo "-[$NODE_IP] config apiserver"
    test -f "${K8S_PREFIX}/apiserver" || pkg_install kubernetes-master
    test -f "${K8S_PREFIX}/apiserver.bak" || mv ${K8S_PREFIX}/apiserver{,.bak}
    cat > "${K8S_PREFIX}/apiserver" <<EOF
KUBE_API_ADDRESS="--advertise-address=$MASTER_IP --bind-address=$MASTER_IP --insecure-bind-address=$MASTER_IP"
KUBE_ETCD_SERVERS="--etcd-servers=https://$MASTER_IP:2379,https://$SLAVE_IP:2379"
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"
KUBE_ADMISSION_CONTROL="--admission-control=ServiceAccount,NamespaceLifecycle,NamespaceExists,LimitRanger,ResourceQuota"
KUBE_API_ARGS="--authorization-mode=RBAC --runtime-config=rbac.authorization.k8s.io/v1beta1 --kubelet-https=true --experimental-bootstrap-token-auth --token-auth-file=${K8S_PREFIX}/token.csv --service-node-port-range=30000-32767 --tls-cert-file=${K8S_PREFIX}/pki/server.crt --tls-private-key-file=${K8S_PREFIX}/pki/server.key --client-ca-file=${K8S_PREFIX}/pki/ca.crt --service-account-key-file=${K8S_PREFIX}/pki/ca.key --etcd-cafile=${K8S_PREFIX}/pki/ca.crt --etcd-certfile=${K8S_PREFIX}/pki/server.crt --etcd-keyfile=${K8S_PREFIX}/pki/server.key --enable-swagger-ui=true --apiserver-count=3 --audit-log-maxage=30 --audit-log-maxbackup=3 --audit-log-maxsize=100 --event-ttl=1h"
EOF
}

function controller_manager_config() {
    # --anonymous-auth=true
    echo "-[$NODE_IP] config controller-manager"
    test -f "${K8S_PREFIX}/controller-manager" || pkg_install kubernetes-master
    test -f "${K8S_PREFIX}/controller-manager.bak" || mv ${K8S_PREFIX}/controller-manager{,.bak}
    cat > "${K8S_PREFIX}/controller-manager" <<EOF
KUBE_CONTROLLER_MANAGER_ARGS="--address=127.0.0.1 --service-cluster-ip-range=10.254.0.0/16 --cluster-name=kubernetes --cluster-signing-cert-file=${K8S_PREFIX}/pki/ca.crt --cluster-signing-key-file=${K8S_PREFIX}/pki/ca.key --service-account-private-key-file=${K8S_PREFIX}/pki/ca.key --root-ca-file=${K8S_PREFIX}/pki/ca.crt --leader-elect=true"
EOF
}

function global_config() {
    echo "-[$NODE_IP] global config"
    test -f "${K8S_PREFIX}/config.bak" || mv ${K8S_PREFIX}/config{,.bak}
    cat > "${K8S_PREFIX}/config" <<EOF
KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=true"
KUBE_MASTER="--master=http://${MASTER_IP}:8080"
EOF
}

function etcd_config() {
    echo "-[$NODE_IP] config etcd"
    test -f "/etc/etcd/etcd.conf" || pkg_install etcd
    test -f "/etc/etcd/etcd.conf.bak" || mv /etc/etcd/etcd.conf{,.bak}
    cat > "/etc/etcd/etcd.conf" <<EOF
#[member]
ETCD_NAME=NODE_NAME
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://${NODE_IP}:2380"
ETCD_LISTEN_CLIENT_URLS="https://${NODE_IP}:2379,http://127.0.0.1:2379"
#[cluster]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://${NODE_IP}:2380"
ETCD_INITIAL_CLUSTER="infra1=https://${MASTER_IP}:2380,infra2=https://${SLAVE_IP}:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_ADVERTISE_CLIENT_URLS="https://${NODE_IP}:2379"
#[security]
ETCD_CERT_FILE="${K8S_PREFIX}/pki/server.crt"
ETCD_KEY_FILE="${K8S_PREFIX}/pki/server.key"
ETCD_PEER_CERT_FILE="${K8S_PREFIX}/pki/server.crt"
ETCD_PEER_KEY_FILE="${K8S_PREFIX}/pki/server.key"
ETCD_TRUSTED_CA_FILE="${K8S_PREFIX}/pki/ca.crt"
ETCD_PEER_TRUSTED_CA_FILE="${K8S_PREFIX}/pki/ca.crt"
EOF
    if [ "$NODE_IP" == "$MASTER_IP" ]; then
        sed -i 's|NODE_NAME|infra1|' /etc/etcd/etcd.conf
    else
        sed -i 's|NODE_NAME|infra2|' /etc/etcd/etcd.conf
    fi
}

function flanneld_config() {
    echo "-[$NODE_IP] flanneld config"
    test -f "/etc/sysconfig/flanneld" || pkg_install flannel docker
    test -f "/etc/sysconfig/flanneld.bak" || mv /etc/sysconfig/flanneld{,.bak}
    cat > "/etc/sysconfig/flanneld" <<EOF
FLANNEL_ETCD_ENDPOINTS="https://${MASTER_IP}:2379,https://${SLAVE_IP}:2379"
FLANNEL_ETCD_PREFIX="/kube-centos/network"
FLANNEL_OPTIONS="-iface=ens3 -etcd-cafile=${K8S_PREFIX}/pki/ca.crt -etcd-certfile=${K8S_PREFIX}/pki/server.crt -etcd-keyfile=${K8S_PREFIX}/pki/server.key"
EOF
    ETC_OPTS="--cert-file ${K8S_PREFIX}/pki/server.crt --key-file ${K8S_PREFIX}/pki/server.key --ca-file ${K8S_PREFIX}/pki/ca.crt"
    etcdctl $ETC_OPTS mkdir "/kube-centos/network"
    etcdctl $ETC_OPTS mk "/kube-centos/network/config" \
        '{"Network":"172.17.0.0/16","SubnetLen":24,"Backend":{"Type":"vxlan"}}'
}

function kubelet_config() {
    echo "-[$NODE_IP] kubelet config"
    test -f "${K8S_PREFIX}/kubelet" || pkg_install kubernetes-node
    test -f "${K8S_PREFIX}/kubelet.bak" || mv ${K8S_PREFIX}/kubelet{,.bak}
    cat > "${K8S_PREFIX}/kubelet" <<EOF
KUBELET_ADDRESS="--address=${NODE_IP}"
KUBELET_HOSTNAME="--hostname-override=${NODE_IP}"
KUBELET_API_SERVER="--api-servers=http://$MASTER_IP:8080"
KUBELET_ARGS="--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0 --cgroup-driver=systemd --cluster-dns=${DNS_SERVER_IP} --cluster-domain=${DNS_DOMAIN}. --hairpin-mode=promiscuous-bridge --serialize-image-pulls=false --bootstrap-kubeconfig=${K8S_PREFIX}/bootstrap.kubeconfig --kubeconfig=${K8S_PREFIX}/kubelet.kubeconfig --require-kubeconfig --cert-dir=${K8S_PREFIX}/pki"
EOF
    # create cluster_role_binding for kubelet-bootstrap user
    kubectl create clusterrolebinding kubelet-bootstrap \
        --clusterrole=system:node-bootstrapper \
        --user=kubelet-bootstrap &>/dev/null ||:
    # Join slave [master]:
    #   kubectl get csr
    #   kubectl certificate approve node-csr-XXX
    #   kubectl get nodes
}

function proxy_config() {
    echo "-[$NODE_IP] proxy config"
    test -f "${K8S_PREFIX}/proxy" || mv ${K8S_PREFIX}/proxy{,.bak}
    echo "KUBE_PROXY_ARGS='--bind-address=${NODE_IP} --hostname-override=${NODE_IP} --kubeconfig=${K8S_PREFIX}/kube-proxy.kubeconfig --cluster-cidr=10.254.0.0/16'" > ${K8S_PREFIX}/proxy
}

function base_deploy() {
    prepare
    gencert
    etcd_config
      # run some functions on slave node by `runfunc`
      # https://stackoverflow.com/questions/11003418/
      echo "lru_buhtig ENV  pkg_install   etcd_config" | \
        sed -E "s|\s+|\n|g" | xargs -n1 -i bash -c "runfunc {}"
      runfuncpost
    start_svc etcd
    sleep 10
    flanneld_config
      echo "lru_buhtig ENV pkg_install flanneld_config" | \
        tr [:blank:] "\n" | xargs -n1 -i bash -c "runfunc {}"
      runfuncpost
    start_svc flanneld
}

function master_deploy() {
    prepare
    genkubeconfig
    global_config
    apiserver_config
    controller_manager_config
    start_svc kube-apiserver kube-scheduler kube-controller-manager
}

function slave_deploy() {
    prepare
    if [ "0$1" == "0" ]; then
        global_config
        kubelet_config
        proxy_config
    else
        echo "lru_buhtig ENV pkg_install  global_config kubelet_config proxy_config" | \
          sed -E "s|\s+|\n|g" | xargs -n1 -i bash -c "runfunc {}"
        runfuncpost $1
    fi
    start_svc docker kubelet kube-proxy
}

function kubedns_deploy() {
    echo "- install kubedns addon"
    export KUBERNETES_MASTER="http://${MASTER_IP}:8080"
    wget -qO- ${ADDON_URL}/dns/kubedns-sa.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/dns/kubedns-cm.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/dns/kubedns-svc.yaml.sed | \
        sed 's|$DNS_SERVER_IP|'${DNS_SERVER_IP}'|' | kubectl create -f -
    wget -qO- ${ADDON_URL}/dns/kubedns-controller.yaml.sed | \
        sed 's|gcr.io/google_containers|4admin2root|; s|$DNS_DOMAIN|'${DNS_DOMAIN}'|g' | \
        kubectl create -f -
    sleep 10  # waiting pod
    ################## check service ##################
    echo "- check kube-dns service"
    kubectl get pod -n kube-system | grep "kube-dns"
    kubectl --kubeconfig=${K8S_PREFIX}/kubelet.kubeconfig run curl \
        --image=radial/busyboxplus:curl -- sh -c "while true; do sleep 1; done"
    _pod=`kubectl get pod -o custom-columns=NAME:.metadata.name | grep curl`
    sleep 10  # waiting pod
    kubectl exec $_pod -- sh -c "nslookup kubernetes.default; nslookup kube-dns.kube-system"
    kubectl delete deploy curl
}

function dashboard_deploy() {
    # dashboard with RBAC: https://github.com/kubernetes/dashboard/issues/1803
    echo "- install dashboard addon"
    export KUBERNETES_MASTER="http://${MASTER_IP}:8080"
    wget -qO- $(lru_buhtig rootsongjc/kubernetes-handbook \
        manifests/dashboard/dashboard-rbac.yaml) | kubectl create -f -
    wget -qO- ${ADDON_URL}/dashboard/dashboard-service.yaml | \
        sed '/ports/i\  type: NodePort' | kubectl create -f -
    wget -qO- ${ADDON_URL}/dashboard/dashboard-controller.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|;
            /containers/i\      serviceAccountName: dashboard' | kubectl create -f -
    sleep 10
    ################## check service ##################
    kubectl cluster-info | grep dashboard
    curl -i `kubectl get svc kubernetes-dashboard -o yaml -n kube-system|awk '/clusterIP/{print $2}'`
}

function heapster_deploy() {
    # https://github.com/kubernetes/heapster/blob/master/docs/influxdb.md
    echo "- install heapster addon"
    test -f "/bin/patch" || pkg_install patch
    export KUBERNETES_MASTER="http://${MASTER_IP}:8080"
    ADDON_URL=$(lru_buhtig kubernetes/heapster deploy/kube-config)
    touch /tmp/grafana.ini
    kubectl create configmap grafana-config-file --from-file=grafana=/tmp/grafana.ini -n kube-system
    wget -qP /tmp ${ADDON_URL}/influxdb/grafana.yaml
    echo "23a24,25
>         - mountPath: /etc/grafana
>           name: grafana-config-vol
45a48,53
>       - name: grafana-config-vol
>         configMap:
>           name: grafana-config-file
>           items:
>           - key: grafana
>             path: grafana.ini" | patch -o- /tmp/grafana.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|' | kubectl create -f -
    wget -qO- ${ADDON_URL}/influxdb/heapster.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|' | kubectl create -f -
    wget -qO- ${ADDON_URL}/rbac/heapster-rbac.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/influxdb/influxdb.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|' | kubectl create -f -
    sleep 10
    ################## check service ##################
    kubectl get pod -n kube-system | grep -E 'heapster|monitoring'
    kubectl cluster-info | grep grafana
}

function efk_deploy() {
    echo "- install EFK addon"
    export KUBERNETES_MASTER="http://${MASTER_IP}:8080"
    ADDON_URL=$(lru_buhtig kubernetes/kubernetes cluster/addons/fluentd-elasticsearch)
    wget -qO- ${ADDON_URL}/es-clusterrole.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/es-serviceaccount.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/es-clusterrolebinding.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/es-service.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/es-controller.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|' | kubectl create -f -
    wget -qO- ${ADDON_URL}/fluentd-es-clusterrole.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/fluentd-es-serviceaccount.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/fluentd-es-clusterrolebinding.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/fluentd-es-ds.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|; /search/s|:[1-9].*$|:1.23|' | kubectl create -f -
    wget -qO- ${ADDON_URL}/kibana-service.yaml | kubectl create -f -
    wget -qO- ${ADDON_URL}/kibana-controller.yaml | \
        sed 's|gcr.io/google_containers|4admin2root|' | kubectl create -f -
    # daemonset: create label for slave nodes
    kubectl label nodes $MASTER_IP beta.kubernetes.io/fluentd-ds-ready=true
    kubectl label nodes $SLAVE_IP beta.kubernetes.io/fluentd-ds-ready=true
    sleep 10
    ################## check service ##################
    kubectl get pod -n kube-system | grep -E 'elasticsearch|fluentd|kibana'
    kubectl cluster-info | grep -E 'elasticsearch|fluentd|kibana'
    echo "Optimizing and caching bundles for kibana and statusPage. This may take a few minutes."
    # kubectl logs kibana-logging-XXX -n kube-system -f
}

function main() {
    case $1 in
    "gencert")
        gencert
        ;;
    "kubeconfig")
        genkubeconfig
        ;;
    "base")
        base_deploy
        ;;
    "master")
        master_deploy
        ;;
    "slave")
        slave_deploy $2
        ;;
    "kubedns")
        kubedns_deploy
        ;;
    "dashboard")
        dashboard_deploy
        heapster_deploy
        ;;
    "heapster")
        heapster_deploy
        ;;
    "efk")
        efk_deploy
        ;;
    *)
        echo "args: base|master|slave|kubedns|dashboard|heapster|efk|gencert|kubeconfig"
        ;;
    esac
}

export -f runfunc
ENV
main $1 $2
