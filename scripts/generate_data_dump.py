# encoding: utf-8

"""
Erzeugt einen Datenbank-Dump

Copyright (c) 2012 Marian Steinbach

Hiermit wird unentgeltlich jeder Person, die eine Kopie der Software und
der zugehörigen Dokumentationen (die "Software") erhält, die Erlaubnis
erteilt, sie uneingeschränkt zu benutzen, inklusive und ohne Ausnahme, dem
Recht, sie zu verwenden, kopieren, ändern, fusionieren, verlegen,
verbreiten, unterlizenzieren und/oder zu verkaufen, und Personen, die diese
Software erhalten, diese Rechte zu geben, unter den folgenden Bedingungen:

Der obige Urheberrechtsvermerk und dieser Erlaubnisvermerk sind in allen
Kopien oder Teilkopien der Software beizulegen.

Die Software wird ohne jede ausdrückliche oder implizierte Garantie
bereitgestellt, einschließlich der Garantie zur Benutzung für den
vorgesehenen oder einen bestimmten Zweck sowie jeglicher Rechtsverletzung,
jedoch nicht darauf beschränkt. In keinem Fall sind die Autoren oder
Copyrightinhaber für jeglichen Schaden oder sonstige Ansprüche haftbar zu
machen, ob infolge der Erfüllung eines Vertrages, eines Delikts oder anders
im Zusammenhang mit der Software oder sonstiger Verwendung der Software
entstanden.
"""

import sys
sys.path.append('./')
import os
import config
import subprocess
import datetime
import shutil


def execute(cmd):
    output, error = subprocess.Popen(
        cmd.split(' '), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    if error is not None and error.strip() != '':
        print >> sys.stderr, "Command: " + cmd
        print >> sys.stderr, "Error: " + error


def create_dump(folder):
    """
    Drops dumps in folder/config.DB_NAME
    """
    cmd = (config.MONGODUMP_CMD + ' --db ' + config.DB_NAME +
            ' --out ' + folder)
    for collection in config.DB_DUMP_COLLECTIONS:
        thiscmd = cmd + ' --collection ' + collection
        execute(thiscmd)


def compress_folder(folder):
    now = datetime.datetime.now()
    filename = 'dump_' + now.strftime('%Y-%m-%d') + '.tar.bz2'
    cmd = ('tar cjf ' + filename + ' ' + folder +
            os.sep + config.DB_NAME + os.sep)
    execute(cmd)
    shutil.rmtree(folder + os.sep + config.DB_NAME)
    shutil.move(filename, 'webapp/daten/')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a database dump')
    parser.add_argument('-f', '--tempfolder', dest='folder', metavar='FOLDER', type=str,
                       help=('an integer for the accumulator. Default: %s' %
                        config.DB_DUMP_TEMPFOLDER),
                       default=config.DB_DUMP_TEMPFOLDER)

    args = parser.parse_args()
    create_dump(args.folder)
    compress_folder(args.folder)
