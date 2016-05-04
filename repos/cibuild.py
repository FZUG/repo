#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: mosquito
# Email: sensor.wen@gmail.commit
# Description: CI build for repo

from subprocess import getoutput, call
from urllib.request import urlretrieve
import re
import os
import sys
import shutil
import fnmatch

Archs = 'x86_64', 'i386'
Releases = '22', '23'
blackList = 'electron',
srcDir = os.path.join(os.getcwd(), 'build')
outDir = os.path.join(os.getcwd(), 'output')

getoutput('/bin/git clean -f -d -x')
if not os.path.isdir(srcDir):
    os.mkdir(srcDir)

def get_commit_list():
    '''Get all of commit.

    Returns:
        Return all of commit list.
    '''

    stdout = getoutput('/bin/git log --pretty=%h')
    return re.findall('\w{7}', stdout)

def get_file_list(commit=os.environ['GIT_COMMIT']):
    '''Get modified files for commit.

    Args:
        commit: commit string.

    Returns:
        Return list that modified files for commit.
    '''

    stdout = getoutput('/bin/git show --pretty="%h: %s" --name-status {}'.format(commit))
    return list(filter(black_item, re.findall('rpms.*', stdout)))

def black_item(item):
    '''Fliter blacklist entry.

    Args:
        item: A string of item.
    '''
    for black in blackList:
        if re.match('.*' + black + '.*', item):
            return False
        else:
            return True

def parse_spec(fileList):
    '''Parse the Spec file contents.

    Args:
        fileList: A list of file path.

    Returns:
        Return the list contains the Spec file name and content. If the file
        is not found, it returns false.
    '''

    for specFile in fileList:
        if os.path.exists(specFile) and str(specFile).endswith('.spec'):
            return specFile, getoutput('/bin/rpmspec -P {}'.format(specFile))

    return False

def get_source_list(specContent):
    '''Get source and patch files list.

    Args:
        specContent: A string of Spec file content.

    Returns:
        Return the list contains source and patch files list.
    '''

    return re.findall('[Source|Patch]\d+:\s+(.*)', specContent)

def get_sources(itemList, output=srcDir):
    '''Get source files from local and internet.

    Args:
        itemList: A list of source files.
        output: A string of temp directory.
    '''

    for item in itemList:
        if not os.path.exists(os.path.join(output, item.split('/')[-1])):
            if item.split('://')[0] in ['http', 'https', 'ftp']:
                urlretrieve(item, '{}/{}'.format(output, item.split('/')[-1]))
                #call(['wget', '-q', '-P', output, item])
            else:
                for src in find_files(item, 'rpms'):
                    shutil.copy(src, output)

def find_files(pattern, path=os.getcwd()):
    '''Search specify file.

    Args:
        pattern: Filename regular expression.
        path: Search path.

    Yields:
        Returns the target path of the file generator.
    '''

    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(root, filename)

def build_srpm(specFile, output='build'):
    '''Build source rpm.

    Args:
        specFile: A string of the Spec filename.
        output: A string of the SRPM file output directory.

    Returns:
        Return the SRPM filename.
    '''

    command = '/bin/rpmbuild ' \
        '-D "_topdir ." ' \
        '-D "_builddir {out}" ' \
        '-D "_buildrootdir {out}" ' \
        '-D "_rpmdir {out}" ' \
        '-D "_sourcedir {out}" ' \
        '-D "_specdir {out}" ' \
        '-D "_srcrpmdir {out}" ' \
        '-bs {}'.format(specFile, out=output)
    return re.search('build.*', getoutput(command)).group()

def build_rpm(srpmFile, release='23', arch='x86_64', output=outDir):
    '''Build rpm.

    Args:
        srpmFile: A string of SRPM file path.
        release: A string of system release version.
        arch: A string of system architecture.
        output: A string of RPM file output directory.

    Returns:
        Return the command running log.
    '''

    command = '/bin/mock --resultdir={} --root=fedora-{}-{}-rpmfusion {}'.format(
        output, release, arch, srpmFile)
    return getoutput(command)

def rpm_lint(repoDir=outDir, time=10):
    '''Check rpm files.

    Args:
        repoDir: A string of repository directory.
        time: A integer of time(minutes).

    Returns:
        Return the check result.
    '''

    command = '/bin/find {} -name "*.rpm" -and -ctime -{} | xargs ' \
              '/bin/rpmlint -i'.format(repoDir, round(time/60/24, 4))
    return getoutput(command)

def create_repo(output=outDir):
    '''Creates metadata of rpm repository.

    Args:
        output: A string of RPM metadata output directory.

    Returns:
        Return the command running log.
    '''

    return getoutput('/bin/createrepo_c {}'.format(output))

if __name__ == '__main__':
    rootDir = outDir
    if len(sys.argv) > 1:
        rootDir = sys.argv[1]
    elif 'REPO_ROOT' in os.environ:
        rootDir = os.environ['REPO_ROOT']

    for commit in get_commit_list():
        if commit in os.environ['GIT_PREVIOUS_COMMIT']:
            break

        fileList = get_file_list(commit)
        if parse_spec(fileList):
            specFile, specContent = parse_spec(fileList)
        else:
            print('Unmodified spec file.')
            sys.exit()

        sourceList = get_source_list(specContent)
        get_sources(sourceList)
        srpmFile = build_srpm(specFile)
        print('-> Build SRPM:', srpmFile)

        for rel in Releases:
            for arch in Archs:
                outDir = os.path.join(rootDir, rel, arch)
                print('-> Build RPM for fc{} - {}:\n'.format(rel, arch),
                      build_rpm(srpmFile, release=rel, arch=arch, output=outDir))
                print('-> Create metadata for fc{} - {}:\n'.format(rel, arch),
                      create_repo(outDir))

        print('-> Check RPM for fc{} - {}:\n'.format('23', 'i386'),
              rpm_lint(os.path.join(rootDir, '23', 'i386')))
