# Software License Agreement (BSD License)
#
# Copyright (c) 2016, Clearpath Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Open Source Robotics Foundation, Inc. nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from distutils.version import LooseVersion
import os
import subprocess


def git_command(cwd, cmd):
    assert _git_client_executable is not None, "'git' not found"
    return _run_command([_git_client_executable] + cmd, cwd)


def git_version_gte(version):
    global _git_client_version
    if not _git_client_version:
        result = git_command(None, ['--version'])
        _git_client_version = result['output'].split()[-1]
    return LooseVersion(_git_client_version) >= LooseVersion(version)


def _run_command(cmd, cwd=None, env=None):
    result = {'cmd': ' '.join(cmd), 'cwd': cwd}
    try:
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        output, _ = proc.communicate()
        result['output'] = output.rstrip()
        result['returncode'] = proc.returncode
    except subprocess.CalledProcessError as e:
        result['output'] = e.output
        result['returncode'] = e.returncode
    if not isinstance(result['output'], str):
        result['output'] = result['output'].decode('utf-8')
    return result


def _find_executable(file_name):
    for path in os.getenv('PATH').split(os.path.pathsep):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
    return None


_git_client_executable = _find_executable('git')
_git_client_version = None
