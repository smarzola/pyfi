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

from algorithms import algs
from algorithms.algorithm import Network
from optparse import OptionParser

mapped_algs = dict([(klass.alg_name, klass()) for klass in algs])

def main():
    usage = "Usage: %prog [options] algorithm_name \nImplemented algorithms: "
    usage += ', '.join(mapped_algs.keys())
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--ssid', help='set the wireless essid', action='store', dest='essid')
    parser.add_option('-w', '--wmac', help='set the wireless mac address', action='store', dest='wmac')
    (options, args) = parser.parse_args()
    if not args or args[0] not in mapped_algs.keys() or options.wmac is None and options.essid is None:
        parser.print_help()
        exit(0)

    network = Network(essid=options.essid, wmac=options.wmac)
    alg = mapped_algs[args[0]]
    print alg.run(network)

if __name__ == '__main__':
    main()