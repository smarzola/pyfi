# pyfi
# Copyright (C) 2012  simock85
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Network(object):
    def __init__(self, *args, **kw):
        self.__dict__.update(kw)

class WpaNotFound(Exception):
    def __init__(self, msg):
        self.msg = 'Wpa Not Found: ' + msg

class WpaAlgorithm(object):

    alg_name = None

    def run(self, network):
        """please override this guy"""
        return