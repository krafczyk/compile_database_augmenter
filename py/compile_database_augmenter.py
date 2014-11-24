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
import os;
import shutil;
import re;

parser = argparse.ArgumentParser(description="Command to augment compilation database with header file compilation flags");
parser.add_argument("-i", "--input-database", type=str, help="The filename of the input database. Default is 'compile_commands.json'")
parser.add_argument("-o", "--output-database", type=str, help="The filename of the output database. Default is the same as the input database file.")
parser.add_argument("-c", "--copy-database", type=str, help="The file name to copy the input database to. Default is the same as input-database but with .old on the end.")
parser.add_argument("-d", "--debug", type=int, help="Set the debug level. Default is 0.")

args = parser.parse_args()

input_database_filepath = ""
output_database_filepath = ""
copy_database_filepath = ""
debug = 0
if args.debug != None:
    debug = args.debug

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

#Check for the existence of the input database.
if not os.path.isfile(input_database_filepath):
    print "input database (%s) doesn't exist!" % input_database_filepath
    sys.exit(-1)

#First, copy the input database to the copy database location
shutil.copyfile(input_database_filepath, copy_database_filepath)

#Read in input database.
input_database_file = open(input_database_filepath, "r")
if input_database_file == None :
    print "There was a problem opening the input database file! (%s)" % input_database_filepath
    sys.exit(-1)

input_database = input_database_file.read();
input_database_file.close()

#Decode the input database.
decoded_input_database = json.loads(input_database)

decoded_output_database = decoded_input_database

#Compile some regex commands
c_command_match_unquoted = re.compile('.* -c [^" ]+ .*')
c_command_match_quoted = re.compile('.* -c "[^"]+" .*')
output_match_unquoted = re.compile('.* -o [^" ]+ .*')
output_match_quoted = re.compile('.* -o "[^"]+" .*')

for item in decoded_input_database:
    #We show some debugging info about the database entry
    if debug > 0:
        print "Database Item is:"
        print "Directory is:"
        print item[u'directory']
        print "Command is:"
        print item[u'command']
        print "File is:"
        print item[u'file']

    #In case -c or -o appears at the end of the command line, we make sure there is a space there
    command = "%s " % item[u'command']

    #We must test whether the filepath has spaces and hence is contained in a quoted string
    is_c_quoted = None
    if c_command_match_unquoted.match(command):
        is_c_quoted = False
    elif c_command_match_quoted.match(command):
        is_c_quoted = True

    if is_c_quoted == None:
        if debug > 0:
            print "Command for file (%s) is not compatible skipping.. (can't match -c option)" % item[u'file']
            continue

    is_o_quoted = None
    if c_command_match_unquoted.match(command):
        is_o_quoted = False
    elif c_command_match_quoted.match(command):
        is_o_quoted = True

    if is_o_quoted == None:
        if debug > 0:
            print "Command for file (%s) is not compatible skipping.. (can't match -o option)" % item[u'file']
            continue

    if debug > 2:
        if is_c_quoted:
            print "-c option is quoted"
        else:
            print "-c option is not quoted";

        if is_o_quoted:
            print "-o option is quoted"
        else:
            print "-o option is not quoted";

    #Now we replace -c filepath with -E filepath
    #And -o filepath with -o /dev/stdout
