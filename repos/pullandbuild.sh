#!/bin/bash

SPECLISTDIR="/tmp/FZUGLISTS/"
releases="29"

help()
{
    echo "Help:"
}

if [[ $# -eq 0 ]]; then
    echo "Options needed!"
    help
    exit 1;
fi

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -g|--gitrepo)
            GITREPO="$2"
            shift # past argument
            shift # past value
            ;;
        -o|--output)
            OUTPUT="$2"
            shift # past argument
            shift # past value
            ;;
        --push)
            PUSH=YES
            shift # past argument
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done

[[ -d ${SPECLISTDIR} ]] || mkdir ${SPECLISTDIR}
SPECLISTFILE="${SPECLISTDIR}$(date +%Y%m%d-%H%M%S).list"

if [ ! -z ${GITREPO+x} ]; then
    pushd $GITREPO
fi
git pull --rebase
git log --name-only --since="@{2 days ago}" --pretty=format: | grep "spec$"  >${SPECLISTFILE}

if [ ! -z ${OUTPUT+x} ]; then
    extraparam=" -o ${OUTPUT}"
fi

for rel in $releases ; do
    echo "Build for $rel"
    cat ${SPECLISTFILE} | tr '\n' ' ' | xargs ./repos/cibuild.py -a x86_64 -r $rel --createrepo --mock-opts '--dnf --define "_buildhost build.zh.fedoracommunity.org"' ${extraparam} -v
done
find ${OUTPUT} -iname "*.log" -exec rm {} \;
find ${OUTPUT} -iname "*debuginfo*" -exec rm {} \;
find ${OUTPUT} -iname "*debugsource*" -exec rm {} \;
for rel in $releases ; do
    pushd ${OUTPUT}/$rel/x86_64
        createrepo_c --update .
    popd
done

if [ ! -z ${GITREPO+x} ]; then
    popd
fi

