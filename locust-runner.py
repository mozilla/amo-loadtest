#!/usr/bin/env python
import os
import re
import subprocess
import sys

env = re.compile(r'\$(?P<varname>[^\s$]+)')


class NoEnvVar(Exception):
    pass


def expand(m):
    varname = m.groupdict()['varname']
    value = os.environ.get(varname, None)
    if not value:
        raise NoEnvVar('${} was not defined or is empty'.format(varname))
    return value


if __name__ == '__main__':
    argv = sys.argv[1:]
    new_argv = ['locust']
    for val in argv:
        try:
            val = env.sub(expand, val)
        except NoEnvVar, exc:
            raise ValueError('{error}; command= {cmd}'.format(
                error=exc,
                cmd=' '.join(argv)))
        new_argv.append(val)
    retcode = subprocess.call(new_argv)
    sys.exit(retcode)
