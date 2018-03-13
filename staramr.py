#!/usr/bin/env python
"""
Copyright Government of Canada 2018

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

-------------------------------------------------------------------------------

PURPOSE:

This software is used to scan input FASTA files against the ResFinder and PointFinder databases and produce a summary
of detected AMR genes.

USAGE:

staramr.py --help
staramr.py db --help
staramr.py search --help

staramr.py search --output-dir [OUTPUT_DIR] [INPUT_FILE] ..

EXAMPLE:

staramr.py db build
staramr.py search --output-dir out *.fasta

"""
import argparse
import logging
import sys
from os import path

from staramr.detection.AMRDetectionFactory import AMRDetectionFactory
from staramr.exceptions.CommandParseException import CommandParseException
from staramr.subcommand.Database import Database
from staramr.subcommand.Search import Search

logger = logging.getLogger("staramr")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

script_dir = path.dirname(path.realpath(sys.argv[0]))
script_name = path.basename(path.realpath(sys.argv[0]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do AMR detection for genes and point mutations')
    subparsers = parser.add_subparsers(dest='command', help='Subcommand for AMR detection.')

    Search(AMRDetectionFactory(), subparsers, script_dir, script_name)
    Database(subparsers, script_dir, script_name)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        try:
            args.run_command(args)
        except CommandParseException as e:
            logger.error(str(e))
            e.get_parser().print_help()