# _*_ coding: utf-8 _*_

from fabric.api import run, local


def test():
    local('ls -l')