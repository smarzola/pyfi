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

from algorithm import WpaAlgorithm
from algorithms.algorithm import WpaNotFound
from lib.helpers import cached_property
import os
import re

class Tele2(WpaAlgorithm):

    alg_name = 'tele2'

    @cached_property
    def config_re(self):
        return re.compile('^([0-9A-F]{6})\s+([0-9A-F]{6})\s+([0-9A-F]{6})\s+([0-9]{5})\s+([0-9A-F]{6})', re.MULTILINE)

    @cached_property
    def parsed_config(self):
        with open(os.path.join(os.path.dirname(__file__),'Tele2.txt')) as txt:
            no_colon_txt = txt.read().replace(':', '')
            matches = re.findall(self.config_re, no_colon_txt)
            config_dict = {}
            for match in matches:
                substruct = dict(start=match[1], end=match[2], sn1=match[3], base=match[4])
                if match[0] in config_dict:
                    config_dict[match[0]].append(substruct)
                else:
                    config_dict[match[0]]=[substruct, ]
        return config_dict

    def find_mac_position(self, wmac):
        struct = self.parsed_config.get(wmac[0:6])
        if struct is None:
            raise WpaNotFound('wmac not in range')
        deltas = []


    def run(self, network):
        print self.parsed_config
        return '2'

