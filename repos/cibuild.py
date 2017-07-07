#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: mosquito
# Email: sensor.wen@gmail.com
# Description: CI build for repo

from subprocess import getoutput, getstatusoutput, call
from urllib.request import urlretrieve
from operator import itemgetter
import urllib.error
import re
import os
import sys
import rpm
import dnf
import json
import shutil
import fnmatch
import argparse
import requests

srcDir = os.path.join(os.getcwd(), 'build')
outDir = os.path.join(os.getcwd(), 'output')

def get_commit_list():
    '''Get all of commit.

    Returns:
        Return all of commit list.
    '''

    commit_list = getoutput('/bin/git rev-list -n100 --abbrev-commit HEAD').split()
    commit = getoutput('/bin/git rev-parse --short HEAD~')

    if os.getenv('GIT_PREVIOUS_COMMIT'):
        commit = os.getenv('GIT_PREVIOUS_COMMIT')[0:7]

    if os.getenv('ghprbActualCommit'):
        commit_list = commit_list[1:]
        code = call(['/bin/git', 'fetch', '-q'])
        master_commit_list = getoutput('/bin/git rev-list -n100 --abbrev-commit origin/master').split()
        inter_list = list(set(master_commit_list).intersection(set(commit_list)))
        inter_list.sort(key=commit_list.index)
        commit = inter_list[0]

    commit_list = commit_list[0:commit_list.index(commit)]
    commit_list.reverse()
    return commit_list

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
            echo('green', 'info:', ' Filter {} file.'.format(item))
            return False

    return True

def query_package(query):
    '''Query package name from remote repository.

    Args:
        query: A string of query.

    Returns:
        Return the list contains the RPM metadata. If the RPM is not found,
        it returns empty list.
    '''

    if 'repos' not in globals().keys():
        echo('green', 'info:', ' Initial metadata for repository.')
        global repos
        repos = dnf.Base()
        repos.read_all_repos()
        repos.fill_sack(load_available_repos=True)
    return list(repos.provides(query))

def parse_spec(specFile, cacheFile='.repocache.json'):
    '''Parse the Spec file contents.

    Args:
        specFile: A string of spec file path.

    Returns:
        Return the list contains the Spec file name and content. If the file
        is not found, it returns false.
    '''

    if os.path.exists(cacheFile):
        if 'repocache' not in globals().keys():
            echo('green', 'info:', ' Load cache from {} file.'.format(cacheFile))
            with open(cacheFile, 'r') as f:
                global repocache
                repocache = json.loads(f.read())
        return specFile, repocache[specFile]

    items = lambda t, c: re.findall('%s:\s+(.*)'%t, c)
    split_str = lambda l: [re.split('[\s,=|>=|<=]+', i) for i in l]
    flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]
    remove_ver = lambda l: [i for i in l if not re.match('^[0-9]', i)]
    decode = lambda v: v.decode() if v else v

    if os.path.exists(specFile) and specFile.endswith('.spec'):
        rpm_info = {}
        subpkgs, reqpkgs = [], []
        spec = rpm.spec(specFile)
        hdr = spec.sourceHeader

        reqlist = [decode(i) for i in hdr[rpm.RPMTAG_REQUIRES]]
        content = getoutput('/bin/rpmspec -P {}'.format(specFile))
        content = content[:content.index('%changelog')]

        # subpackages
        name = decode(hdr[rpm.RPMTAG_NAME])
        subpkgs.append(name)
        if re.search('%package', content):
            for i in re.findall('%package\s*(.+)', content):
                if i.startswith('-n'):
                    subpkgs.append(re.match('-n\s*(.*)', i).group(1))
                else:
                    subpkgs.append('{}-{}'.format(name, i))

        provpkgs = remove_ver(flat(split_str(items('Provides', content)))) + subpkgs

        # parse buildrequires
        for i in reqlist:
            if re.match('.*\((.*)\)', i):
                if len(query_package(i)) > 0:
                    reqpkgs.append(query_package(i)[0].name)
            else:
                reqpkgs.append(i)

        rpm_info = {
            "name": decode(hdr[rpm.RPMTAG_NAME]),
            "epoch": hdr[rpm.RPMTAG_EPOCHNUM],
            "version": decode(hdr[rpm.RPMTAG_VERSION]),
            "release": decode(hdr[rpm.RPMTAG_RELEASE]),
            "vendor": decode(hdr[rpm.RPMTAG_VENDOR]),
            "summary": decode(hdr[rpm.RPMTAG_SUMMARY]),
            "packager": decode(hdr[rpm.RPMTAG_PACKAGER]),
            "group": decode(hdr[rpm.RPMTAG_GROUP]),
            "license": decode(hdr[rpm.RPMTAG_LICENSE]),
            "url": decode(hdr[rpm.RPMTAG_URL]),
            "description": decode(hdr[rpm.RPMTAG_DESCRIPTION]),
            "sources": spec.sources,
            "patchs": [decode(i) for i in hdr[rpm.RPMTAG_PATCH]],
            "build_archs": [decode(i) for i in hdr[rpm.RPMTAG_BUILDARCHS]],
            "exclusive_archs": [decode(i) for i in hdr[rpm.RPMTAG_EXCLUSIVEARCH]],
            #"build_requires": [i.DNEVR()[2:] for i in rpm.ds(hdr, 'requires')],
            "build_requires": sorted(list(set(reqpkgs))),
            "requires": remove_ver(flat(split_str(items('\nRequires', content)))),
            "recommends": remove_ver(flat(split_str(items('Recommends', content)))),
            "supplements": [decode(i) for i in hdr[rpm.RPMTAG_SUPPLEMENTS]],
            "suggests": [decode(i) for i in hdr[rpm.RPMTAG_SUGGESTS]],
            "enhances": [decode(i) for i in hdr[rpm.RPMTAG_ENHANCES]],
            "provides": sorted(list(set(provpkgs))),
            "obsoletes": remove_ver(flat(split_str(items('Obsoletes', content)))),
            "conflicts": remove_ver(flat(split_str(items('Conflicts', content))))
        }

        return specFile, rpm_info
    return False

def get_sources(itemList, output=srcDir, verb=None):
    '''Get source files from local and internet.

    Args:
        itemList: A list of source files.
        output: A string of temp directory.
        verb: A bool of verbose.
    '''

    for item in itemList:
        if not os.path.exists(os.path.join(output, item[0].split('/')[-1])):
            if item[0].split('://')[0] in ['http', 'https', 'ftp']:
                if verb:
                    echo('cyan', 'verb:', ' downloading {} file.'.format(item[0]))
                try:
                    urlretrieve(item[0], '{}/{}'.format(output, item[0].split('/')[-1]))
                    #call(['wget', '-q', '-P', output, item[0]])
                except Exception as e:
                    echo('red', 'erro:', ' downloading error. {}'.format(e))
                    sys.exit(1)
            else:
                for src in find_files(item[0], 'rpms'):
                    if verb:
                        echo('cyan', 'verb:', ' copy {} file to build directory.'.format(src))
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

def build_rpm(srpmFile, release='23', arch='x86_64', output=outDir, opts='',
              verb=None, quiet=None):
    '''Build rpm.

    Args:
        srpmFile: A string of SRPM file path.
        release: A string of system release version.
        arch: A string of system architecture.
        output: A string of RPM file output directory.
        opts: A string of mock options.
        verb: A bool of verbose.
        quiet: A bool of quiet.

    Returns:
        Return the command running log.
    '''

    if verb:
        opts += ' --verbose'
    elif quiet:
        opts += ' --quiet'

    command = '/bin/mock --resultdir={} --root=fedora-{}-{}-rpmfusion {} {}'.format(
        output, release, arch, opts, srpmFile)
    return getstatusoutput(command)

def rpm_lint(repoDir=outDir, time=10, verb=None):
    '''Check rpm files.

    Args:
        repoDir: A string of repository directory.
        time: A integer of time(minutes).
        verb: A bool of verbose.

    Returns:
        Return the check result.
    '''

    opts = '--info' if verb else ''
    command = '/bin/find {} -name "*.rpm" -and -ctime -{} | xargs ' \
              '/bin/rpmlint {}'.format(repoDir, round(time/60/24, 4), opts)
    return getoutput(command)

def create_repo(output=outDir, verb=None, quiet=None):
    '''Creates metadata of rpm repository.

    Args:
        output: A string of RPM metadata output directory.
        verb: A bool of verbose.
        quiet: A bool of quiet.

    Returns:
        Return the command running log.
    '''

    opts = ''
    if verb:
        opts += ' --verbose'
    elif quiet:
        opts += ' --quiet'

    return getoutput('/bin/createrepo_c {} -d -x *.src.rpm {}'.format(opts, output))

def result(filename, content):
    '''Log build result to file.

    Args:
        filename: A string of filename.
        content: A string of content.
    '''

    result = 'success' if content[0] == 0 else 'fail'
    _, pkgname, release, arch = content

    if filename == '-':
        _pkgname = re.match('.*/(.*-[0-9]{1,2}).*', pkgname).group(1)
        pkgname = _pkgname + '.net' if re.match('.*\.net', pkgname) else _pkgname
        return pkgname.ljust(35), \
               'fc{}-{}'.format(release, arch).ljust(13), \
               result
    else:
        with open(filename, mode='a+') as f:
            f.write('{} fc{}-{} {}\n'.format(pkgname, release, arch, result))
            echo('green', 'info:', ' Write build result to {} file.'.format(filename))

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
    parser.add_argument('--mock-opts', metavar='OPTIONS', type=str,
                        dest='mock', action='store', default='', required=False,
                        help='set mock command-line options')
    parser.add_argument('--createrepo', dest='createrepo', action='store_true',
                        help='run createrepo to create repository')
    parser.add_argument('--rpmlint', dest='rpmlint', action='store_true',
                        help='check common problems in rpm package')
    parser.add_argument('--clean', dest='clean', action='store_true',
                        help='clean workspace before building')
    parser.add_argument('--cache', dest='cache', action='store_true',
                        help='create metadata cache')
    parser.add_argument('--result', metavar='PATH', type=str,
                        dest='result', action='store', required=False, default='result.log',
                        help='log bulid result to file (default: result.log)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='be verbose')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help='be quiet')
    parser.add_argument(dest='files', metavar='FILE', type=str, action='store', nargs='*')
    return parser.parse_args()

def echo(color=None, *args):
    '''Output log with color.

    Args:
        color: A string of color.
        *args: A tuple that include multi content parameters.
    '''

    if args:
        msg1, msg2 = args[0], ' '.join(args[1:])
    else:
        msg1, msg2 = color, ''

    if color == 'red':
        print('\033[31m{}\033[0m{}'.format(msg1, msg2))
    elif color == 'green':
        print('\033[32m{}\033[0m{}'.format(msg1, msg2))
    elif color == 'yellow':
        print('\033[33m{}\033[0m{}'.format(msg1, msg2))
    elif color == 'blue':
        print('\033[34m{}\033[0m{}'.format(msg1, msg2))
    elif color == 'cyan':
        print('\033[36m{}\033[0m{}'.format(msg1, msg2))
    elif color and args:
        print('{} {} {}'.format(color, msg1, msg2))
    else:
        print('{}'.format(msg1))

def resolve_depends(pkglist, depdict, verb=None):
    '''Resolve dependencies.

    Args:
        pkglist: A list of pkgname.
        depdict: The dict contains the buildrequires, provides and srpm path.
        verb: A bool of verbose.

    Returns:
        Return the list contains the srpm path.
    '''

    _tasks, _specs = [], []
    tasks, specs = [], []
    for pkg in pkglist:
        score = 0
        for dep in depdict[pkg][0]:
            for pkg2 in pkglist:
                if pkg == pkg2:
                    continue
                if dep in depdict[pkg2][1]:
                    score += 1
        _tasks.append({'pkg': depdict[pkg][2], 'score': score})
        _specs.append({'spec': depdict[pkg][3], 'score': score})

    tasks_by_score = sorted(_tasks, key=itemgetter('score'))
    specs_by_score = sorted(_specs, key=itemgetter('score'))
    for i in tasks_by_score:
        tasks.append(i['pkg'])
    for i in specs_by_score:
        specs.append(i['spec'])

    echo('green', 'info:', ' Resolve dependencies.')
    if verb:
        echo('cyan', 'verb:', ' build task {}.'.format(tasks))
    return tasks, specs

def repo_cache(output=None, verb=None):
    '''Create repository cache.

    Args:
        output: A string of output filename.
        verb: A bool of verbose.
    '''

    cacheDict = {}
    for i in find_files('*.spec', 'rpms'):
        if verb:
            echo('cyan', 'verb:', ' cached {} file.'.format(i))
        specFile, specDict = parse_spec(i)
        cacheDict.update({specFile: specDict})

    with open(output, 'w') as f:
        json.dump(cacheDict, f)

def send_comment(content):
    '''Send comment to Github.

    Args:
        content: A string of comments.

    Returns:
        Return json response from Github API.
    '''

    pr_url = 'https://api.github.com/repos/FZUG/repo/issues/%s/comments'
    pr_num = os.getenv('ghprbPullId')
    pr_token = os.getenv('PR_TOKEN')
    session = requests.session()
    session.headers['Authorization'] = 'token %s' % pr_token
    comment = json.dumps({"body": content})
    resp = session.post(pr_url % pr_num, data=comment)
    return resp.json()

if __name__ == '__main__':
    args = parse_args()
    Archs = args.archs if args.archs else ['x86_64', 'i386']
    Releases = args.releases if args.releases else ['24', '25']
    blackList = args.blacklist if args.blacklist else ['electron']
    args.file += args.files

    if args.cache:
        cacheFile = '.repocache.json'
        if os.path.exists(cacheFile):
            echo('green', 'info:', ' The repo cache exists.')
        else:
            echo('green', 'info:', ' Create repo cache.')
            repo_cache(cacheFile, args.verbose)
        sys.exit()

    if not sys.stdin.isatty():
        args.file += sys.stdin.read().split()

    rootDir = args.outDir
    if 'REPO_ROOT' in os.environ:
        rootDir = os.environ['REPO_ROOT']

    mode = 'manual'
    if 'GIT_PREVIOUS_COMMIT' in os.environ or 'ghprbActualCommit' in os.environ:
        mode = 'ci'
    echo('green', 'info:', ' Running as {} mode.'.format(mode))

    if args.clean:
        if args.verbose:
            echo('cyan', 'verb:', ' clean workspace.')
        getoutput('/bin/git clean -f -d -x')

    if not os.path.isdir(srcDir):
        os.mkdir(srcDir)

    results = []
    if os.path.exists(args.result):
        if args.verbose:
            echo('cyan', 'verb:', ' load build result from {} file.'.format(args.result))
        with open(args.result) as f:
            results = re.findall('rpms/.*.spec', f.read())

    deps = {}
    resultList, pkgs = [], []
    for commit in get_commit_list():
        commit = args.commit if args.commit else commit
        fileList = args.file if args.file else get_file_list(commit)

        for filePath in fileList:
            if mode == 'manual' and filePath in results:
                if args.verbose:
                    echo('cyan', 'verb:', ' skip {} file.'.format(filePath))
                continue

            if parse_spec(filePath):
                specFile, specDict = parse_spec(filePath)
                if args.verbose:
                    echo('cyan', 'verb:', ' parser {} file.'.format(specFile))
            elif mode == 'ci':
                echo('green', 'info:', 'Unmodified spec file in commit.')
                continue
            else:
                echo('green', 'info:', 'Unmodified spec file in commit.')
                sys.exit()

            get_sources(specDict['sources'], verb=args.verbose)
            srpmFile = build_srpm(specFile)
            echo('green', 'info:', ' Build SRPM -', srpmFile)

            if re.match('.*\.net', srpmFile):
                key = specDict['name'] + '.net'
            else:
                key = specDict['name']

            # queue
            pkgs.append(key)
            deps.update({key: [specDict['build_requires'], specDict['provides'], srpmFile, specFile],})

        if args.file or args.commit:
            break

    tasks, specs = resolve_depends(pkgs, deps, verb=args.verbose)
    for task in tasks:
        for rel in Releases:
            for arch in Archs:
                outDir = os.path.join(rootDir, rel, arch)
                echo('green', 'info:', ' Build RPM {} for fc{} - {}:'.format(task, rel, arch))
                value, log = build_rpm(task, release=rel, arch=arch, output=outDir,
                                       opts=args.mock, verb=args.verbose, quiet=args.quiet)
                echo(log)
                if args.createrepo:
                    echo('green', 'info:', ' Create metadata for fc{} - {}:\n'.format(rel, arch),
                         create_repo(outDir, verb=args.verbose, quiet=args.quiet))
                if args.rpmlint:
                    echo('green', 'info:', ' Check RPM {} for fc{} - {}:\n'.format(task, rel, arch),
                         rpm_lint(outDir, verb=args.verbose))
                if mode == 'manual':
                    result(args.result, [value, specs[tasks.index(task)], rel, arch])
                resultList.append(result('-', [value, task, rel, arch]))

    build_result = '** Build result **\n'
    echo('cyan', '\n** Build result **')
    for i in resultList:
        build_result += '%s\n' % ''.join(i)
        echo(''.join(i))

    # Sent build result
    if os.getenv('ghprbActualCommit') and send_comment(build_result).get('id'):
        echo('green', 'info:', 'Comment sent successfully.')
