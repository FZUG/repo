TARGET?=$(shell ls *.te)
SHAREDIR?=/usr/share
#MODULE?=${TARGETS:=.pp.bz2}
#INSTALL=?=install

all: cil pp
cil: ${TARGET:%.te=%.cil}
pp: ${TARGET:%.te=%.pp.bz2}

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@; \
	bzip2 -f -9 $^

%.cil: %.pp
	@if [ -x /usr/libexec/selinux/hll/pp ]; then \
		echo Converting $^ -\> $@; \
		cat $^ | /usr/libexec/selinux/hll/pp > $@; \
		echo Compressing $@ -\> $@.bz2; \
		bzip2 -f -9 $@; \
	fi

%.pp: %.te
	make -f ${SHAREDIR}/selinux/devel/Makefile $@

clean:
	rm -rf tmp *.cil *.pp *.bz2

#install:
#AWK${INSTALL} -m 0644 ${TARGET} \
	#gawk${DESTDIR}${SHAREDIR}/targeted/modules
