# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Willow Garage, Inc.
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
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
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
#
# Revision $Id: packages.py 14291 2011-07-13 03:24:43Z kwc $
# $Author: kwc $

import os

################################################################################
# Enviroment

# Global, usually set in setup
ROS_ROOT         = "ROS_ROOT"
ROS_PACKAGE_PATH = "ROS_PACKAGE_PATH"
ROS_HOME         = "ROS_HOME"

## directory in which log files are written
ROS_LOG_DIR      ="ROS_LOG_DIR"
## directory in which test result files are written
ROS_TEST_RESULTS_DIR = "ROS_TEST_RESULTS_DIR"

# Utilities
def _resolve_path(p):
    """
    @param path: path string
    @type  path: str
    Catch-all utility routine for fixing ROS environment variables that
    are a single path (e.g. ROS_ROOT).  Currently this just expands
    tildes to home directories, but in the future it may encode other
    behaviors.
    """
    if p and p[0] == '~':
        return os.path.expanduser(p)
    return p
    
def _resolve_paths(paths):
    """
    @param paths: path string with OS-defined separator (i.e. ':' for Linux)
    @type  paths: str
    Catch-all utility routine for fixing ROS environment variables that
    are paths (e.g. ROS_PACKAGE_PATH).  Currently this just expands
    tildes to home directories, but in the future it may encode other
    behaviors.
    """
    splits = [p for p in paths.split(os.pathsep) if p]
    return os.pathsep.join([_resolve_path(p) for p in splits])

#Public API

def get_ros_root(env=None):
    """
    Get the current ROS_ROOT.
    @param env: override environment dictionary
    @type  env: dict
    """
    if env is None:
        env = os.environ
    return env.get(ROS_ROOT, None)

def get_ros_package_path(env=None):
    """
    Get the current ROS_PACKAGE_PATH.
    @param env: (optional) environment override.
    @type  env: dict
    """
    if env is None:
        env = os.environ
    return env.get(ROS_PACKAGE_PATH, None)

def get_ros_home(env=None):
    """
    Get directory location of '.ros' directory (aka ROS home).
    possible locations for this. The ROS_LOG_DIR environment variable
    has priority. If that is not set, then ROS_HOME/log is used. If
    ROS_HOME is not set, $HOME/.ros/log is used.

    @param env: override os.environ dictionary
    @type  env: dict
    @return: path to use use for log file directory
    @rtype: str
    """
    if env is None:
        env = os.environ
    if ROS_HOME in env:
        return env[ROS_HOME]
    else:
        #slightly more robust than $HOME
        return os.path.join(os.path.expanduser('~'), '.ros')
    
def get_log_dir(env=None):
    """
    Get directory to use for writing log files. There are multiple
    possible locations for this. The ROS_LOG_DIR environment variable
    has priority. If that is not set, then ROS_HOME/log is used. If
    ROS_HOME is not set, $HOME/.ros/log is used.

    @param env: override os.environ dictionary
    @type  env: dict
    @return: path to use use for log file directory
    @rtype: str
    """
    if env is None:
        env = os.environ
    if ROS_LOG_DIR in env:
        return env[ROS_LOG_DIR]
    else:
        return os.path.join(get_ros_home(env), 'log')

def get_test_results_dir(env=None):
    """
    Get directory to use for writing test result files. There are multiple
    possible locations for this. The ROS_TEST_RESULTS_DIR environment variable
    has priority. If that is set, ROS_TEST_RESULTS_DIR is returned.
    If ROS_TEST_RESULTS_DIR is not set, then ROS_HOME/test_results is used. If
    ROS_HOME is not set, $HOME/.ros/test_results is used.

    @param env: environment dictionary (defaults to os.environ)
    @type  env: dict
    @return: path to use use for log file directory
    @rtype: str
    """
    if env is None:
        env = os.environ
        
    if ROS_TEST_RESULTS_DIR in env:
        return env[ROS_TEST_RESULTS_DIR]
    else:
        return os.path.join(get_ros_home(env), 'test_results')

def compute_package_paths(ros_root, ros_package_path):
    """
    Get the paths to search for packages in reverse precedence order (i.e. last path wins).

    @param ros_root: value of ROS_ROOT parameter
    @type  ros_root: str
    @param ros_package_path: value of ROS_PACKAGE_PATH parameter
    @type  ros_package_path: str
    @return: paths to search in reverse order of precedence
    @rtype: [str]
    """
    if ros_package_path:
        return list(reversed([x for x in ros_package_path.split(os.pathsep) if x])) + [ros_root]
    else:
        return [ros_root]

def on_ros_path(p, env=None):
    """
    Check to see if filesystem path is on paths specified in ROS
    environment (ROS_ROOT, ROS_PACKAGE_PATH).

    @param p: path
    @type  p: str
    @return: True if p is on the ROS path (ROS_ROOT, ROS_PACKAGE_PATH)
    """
    if env is None:
        env = os.environ
        
    package = os.path.realpath(_resolve_path(p))
    paths = [p for p in compute_package_paths(get_ros_root(env), get_ros_package_path(env))]
    paths = [os.path.realpath(_resolve_path(x)) for x in paths]
    return bool([x for x in paths if package == x or package.startswith(x + os.sep)])
