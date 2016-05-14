#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: mosquito
# Email: sensor.wen@gmail.commit
# Description: CI build for repo

from subprocess import getoutput, getstatusoutput, call
from urllib.request import urlretrieve
import urllib.error
import re
import os
import sys
import shutil
import fnmatch
import argparse

srcDir = os.path.join(os.getcwd(), 'build')
outDir = os.path.join(os.getcwd(), 'output')

if not os.path.isdir(srcDir):
    os.mkdir(srcDir)

def get_commit_list():
    '''Get all of commit.

    Returns:
        Return all of commit list.
    '''

    stdout = getoutput('/bin/git log --pretty=%h')
    if 'ghprbActualCommit' in os.environ:
        commitList = re.findall('\w{7}', stdout)[1:]
    else:
        commitList = re.findall('\w{7}', stdout)
    return commitList

def get_file_list(commit):
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

def parse_spec(specFile):
    '''Parse the Spec file contents.

    Args:
        specFile: A string of spec file path.

    Returns:
        Return the list contains the Spec file name and content. If the file
        is not found, it returns false.
    '''

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

    return re.findall('[Source|Patch]\d*:\s+(.*)', specContent)

def get_sources(itemList, output=srcDir, verb=None):
    '''Get source files from local and internet.

    Args:
        itemList: A list of source files.
        output: A string of temp directory.
        verb: A bool of verbose.
    '''

    for item in itemList:
        if not os.path.exists(os.path.join(output, item.split('/')[-1])):
            if item.split('://')[0] in ['http', 'https', 'ftp']:
                if verb:
                    print('\033[36mverb:\033[0m downloading {} file.'.format(item.split('/')[-1]))
                try:
                    urlretrieve(item, '{}/{}'.format(output, item.split('/')[-1]))
                    #call(['wget', '-q', '-P', output, item])
                except Exception as e:
                    print('\033[31merro:\033[0m downloading error. {}'.format(e))
            else:
                for src in find_files(item, 'rpms'):
                    if verb:
                        print('\033[36mverb:\033[0m copy {} file to build directory.'.format(src))
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

def build_rpm(srpmFile, release='23', arch='x86_64', output=outDir, opts='', verb=None):
    '''Build rpm.

    Args:
        srpmFile: A string of SRPM file path.
        release: A string of system release version.
        arch: A string of system architecture.
        output: A string of RPM file output directory.
        opts: A string of mock options.
        verb: A bool of verbose.

    Returns:
        Return the command running log.
    '''

    if verb:
        opts += ' --verbose'

    command = '/bin/mock --resultdir={} --root=fedora-{}-{}-rpmfusion {} {}'.format(
        output, release, arch, opts, srpmFile)
    return getstatusoutput(command)

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

def result(filename, content):
    '''Log build result to file.

    Args:
        filename: A string of filename.
        content: A string of content.
    '''

    result = 'success' if content[0] == 0 else 'fail'
    _, pkgname, release, arch = content

    with open(filename, mode='a+') as f:
        f.write('{} {} for fc{}-{}\n'.format(pkgname, result, release, arch))
        print('\033[32minfo:\033[0m Write build result to {} file.'.format(filename))

def parse_args():
    '''Parser for command-line options.

    Returns:
        Return the Namespace object.
    '''

    parser = argparse.ArgumentParser(description='repository ci builder.')
    parser.add_argument('-o', '--output-dir', metavar='PATH', type=str,
                        dest='outDir', action='store', default=outDir,
                        help='set rpm package output directory (default: output)')
    parser.add_argument('-c', '--commit', metavar='COMMIT', type=str,
                        dest='commit', action='store', required=False,
                        help='build the specified commit')
    parser.add_argument('-f', '--file', metavar='FILE', type=str,
                        dest='file', action='append', default=[], required=False,
                        help='build the specified Spec file')
    parser.add_argument('-a', '--arch', metavar='ARCH', type=str,
                        dest='archs', action='append', required=False,
                        help='set architecture for build rpm package (default: x86_64, i386)')
    parser.add_argument('-r', '--release', metavar='RELEASE', type=str,
                        dest='releases', action='append', required=False,
                        help='set release version for build rpm package (default: 22, 23, 24)')
    parser.add_argument('-b', '--black-list', metavar='BLACKLIST', type=str,
                        dest='blacklist', action='append', required=False,
                        help='set blacklist, skip these items')
    parser.add_argument('--mock-opts', metavar='OPTs', type=str,
                        dest='mock', action='store', default='', required=False,
                        help='set mock command-line options')
    parser.add_argument('--rpmlint', dest='rpmlint', action='store_true',
                        help='check common problems in rpm package')
    parser.add_argument('--clean', dest='clean', action='store_true',
                        help='clean workspace before building')
    parser.add_argument('--result', metavar='PATH', type=str,
                        dest='result', action='store', required=False, default='result.log',
                        help='log bulid result to file (default: result.log)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='be verbose')
    parser.add_argument(dest='files', metavar='FILE', type=str, action='store', nargs='*')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    Archs = args.archs if args.archs else ['x86_64', 'i386']
    Releases = args.releases if args.releases else ['22', '23', '24']
    blackList = args.blacklist if args.blacklist else ['electron']
    args.file += args.files

    if not sys.stdin.isatty():
        args.file += sys.stdin.read().split()

    rootDir = args.outDir
    if 'REPO_ROOT' in os.environ:
        rootDir = os.environ['REPO_ROOT']

    mode = 'manual'
    if 'GIT_PREVIOUS_COMMIT' in os.environ or 'ghprbActualCommit' in os.environ:
        mode = 'ci'

    if args.clean:
        if args.verbose:
            print('\033[36mverb:\033[0m clean workspace.')
        getoutput('/bin/git clean -f -d -x')

    if os.path.exists(args.result):
        with open(args.result) as f:
            results = re.findall('rpms/.*.spec', f.read())

    for commit in get_commit_list():
        if ('GIT_PREVIOUS_COMMIT' in os.environ and \
           commit in os.environ['GIT_PREVIOUS_COMMIT']) or \
           ('ghprbActualCommit' in os.environ and \
           commit not in os.environ['ghprbActualCommit']):
            break

        commit = args.commit if args.commit else commit
        fileList = args.file if args.file else get_file_list(commit)

        for filePath in fileList:
            if filePath in results:
                print('\033[36mverb:\033[0m skip {} file.'.format(filePath))
                continue

            if parse_spec(filePath):
                specFile, specContent = parse_spec(filePath)
                if args.verbose:
                    print('\033[36mverb:\033[0m parser {} file.'.format(specFile))
            elif mode == 'ci':
                print('Unmodified spec file.')
                continue
            else:
                print('Unmodified spec file.')
                sys.exit()

            sourceList = get_source_list(specContent)
            get_sources(sourceList, verb=args.verbose)
            srpmFile = build_srpm(specFile)
            print('\033[32minfo:\033[0m Build SRPM -', srpmFile)

            for rel in Releases:
                for arch in Archs:
                    outDir = os.path.join(rootDir, rel, arch)
                    print('\033[32minfo:\033[0m Build RPM for fc{} - {}:\n'.format(rel, arch))
                    value, log = build_rpm(srpmFile, release=rel, arch=arch, output=outDir,
                                           opts=args.mock, verb=args.verbose)
                    print(log)
                    print('\033[32minfo:\033[0m Create metadata for fc{} - {}:\n'.format(rel, arch),
                          create_repo(outDir))
                    if args.rpmlint:
                        print('\033[32minfo:\033[0m Check RPM for fc{} - {}:\n'.format(rel, arch),
                              rpm_lint(outDir))
                    result(args.result, [value, specFile, rel, arch])

        if args.file or args.commit:
            break
