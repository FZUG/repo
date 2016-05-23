#!/bin/sh

set -e

DIRNAME=gpac-$(date +%Y%m%d)

git clone --depth 1 https://github.com/gpac/gpac.git ${DIRNAME}

rm -rf ${DIRNAME}/.git
rm -rf ${DIRNAME}/extra_lib

tar cJf ${DIRNAME}.tar.xz ${DIRNAME}
