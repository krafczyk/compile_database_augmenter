#    compile_database_augmenter - Program to augment clang compilation database with compile rules for header files
#    Copyright (C) 2014  Matthew Krafczyk
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#!/usr/bin/python

import json;

import argparse;

import sys;

parser = argparse.ArgumentParser(description="Command to augment compilation database with header file compilation flags");
parser.add_argument("-i", "--input-database", type=str, help="The filename of the input database. Default is 'compile_commands.json'")
parser.add_argument("-o", "--output-database", type=str, help="The filename of the output database. Default is the same as the input database file.")
parser.add_argument("-c", "--copy-database", type=str, help="The file name to copy the input database to. Default is the same as input-database but with .old on the end.")

args = parser.parse_args()

input_database_filepath = ""
output_database_filepath = ""
copy_database_filepath = ""

if args.input_database != None:
    input_database_filepath = args.input_database
else:
    input_database_filepath = "compile_commands.json"

if args.output_database != None:
    output_database_filepath = args.output_database
else:
    output_database_filepath = input_database_filepath

if args.copy_database != None:
    copy_database_filepath = args.copy_database
else:
    copy_database_filepath = "%s.old" % input_database_filepath;

#Check that the copy location isn't the same as the output location!
if copy_database_filepath == output_database_filepath:
    print "Cannot have the copy database file path the same as the output database filepath"
    sys.exit(-1)

#First, copy the input database to the copy database location
