TARGET?=$(shell ls *.te)
SHAREDIR?=/usr/share
#MODULE?=${TARGETS:=.pp.bz2}
#INSTALL=?=install

all: ${TARGET:%.te=%.pp.bz2}

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@
	bzip2 -9 $^

%.pp: %.te
	make -f ${SHAREDIR}/selinux/devel/Makefile $@

clean:
	rm -rf tmp *.pp *.pp.bz2

#install:
#AWK${INSTALL} -m 0644 ${TARGET} \
	#gawk${DESTDIR}${SHAREDIR}/targeted/modules
