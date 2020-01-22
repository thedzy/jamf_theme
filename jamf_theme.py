#!/usr/bin/env python3

"""
Script:	jamf_theme.py
Date:	2018-11-18
Platform: MacOS/Linux
Description:
Converts your jamf instance into a monochromatic colour scheme

"""
__author__ = 'thedzy'
__copyright__ = 'Copyright 2018, thedzy'
__license__ = 'GPL'
__version__ = '1.2'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Developer'

import json
import math
import optparse
import os
import re


def main(stylefile, redshift, grnshift, blushift, redgain, grngain, blugain, contrast, debug, verbose):
    if debug:
        print('File: ' + stylefile,
              'redshift: ' + str(redshift),
              'grnshift: ' + str(grnshift),
              'blushift: ' + str(blushift),
              'redgain: ' + str(redgain),
              'grngain: ' + str(grngain),
              'blugain: ' + str(blugain),
              'contrast: ' + str(contrast),
              'debug: ' + str(debug),
              'verbose: ' + str(verbose))

    pattern = '#[0-9a-fA-F]{3,6}'
    try:
        with open(stylefile, 'r') as cssfile:
            data = cssfile.read().replace('\n', '')
        hexvalues = list(set(re.findall(pattern, data)))
    except FileNotFoundError as err:
        print(err)
        print('Could not load ' + stylefile)
        print('Verify file exists and is readable by this user, or run under elevated permissions')
        exit()

    if debug:
        print('Found values: ')
        print(json.dumps(hexvalues, indent=4, sort_keys=True))

    for oldhex in hexvalues:
        brightness = colour_contrast_hex(oldhex)

        if contrast:
            # Use a sin wave to create a curve in the brightness, as opposed to a linear escalation
            brightness = (math.sin((brightness / (256 / 3.14159)) - 1.570796327) + 1) * 128

        red = int((brightness * redshift) + redgain)
        if red > 255:
            red = 255
        if red < 0:
            red = 0

        grn = int((brightness * grnshift) + grngain)
        if grn > 255:
            grn = 255
        if grn < 0:
            grn = 0

        blu = int((brightness * blushift) + blugain)
        if blu > 255:
            blu = 255
        if blu < 0:
            blu = 0

        # Convert rgb to hex
        newhex = '#{:02x}{:02x}{:02x}'.format(red, grn, blu)

        if debug or verbose:
            print('Old Hex: ' + oldhex + ', Brightness: ' + str(int(brightness)))
            print('New RGB: ' + str(red) + ', ' + str(grn) + ', ' + str(blu))
            print('New Hex: ' + newhex)
            print('=' * 80)

        data = re.sub(oldhex, newhex, data)

    if not debug:
        try:
            # Move original to preserve
            if os.path.isfile(stylefile):
                stylefile_name, stylefile_ext = os.path.splitext(stylefile)
                stylefile_bak = stylefile_name + '_bak' + stylefile_ext
                os.rename(stylefile, stylefile_bak)
                print('File backed up to ' + stylefile_bak)
        except:
            print('Could not backup file' + stylefile_bak)
            print('Verify path exists and is writable by this user, or run under elevated permissions')
            exit()

        try:
            # Write new file
            with open(stylefile, 'w') as cssfile:
                cssfile.write(str(data))
                cssfile.close()
            print(stylefile + ' written')
        except:
            print('Could not write ' + stylefile)
            print('Verify file exists and is writable by this user, or run under elevated permissions')
            exit()

    else:
        print('No file written')

    print('Do not restart jamf, force reload or reload from source in your browser')
    exit()


def colour_contrast_hex(hex):
    """
    Returns the perceived brightness of a colour based on its hex value
    :param hex: Hex value of the colour
    :return: (int) The perceived brightness (0-255)
    """
    rawhex = hex.lstrip('#')
    if len(rawhex) == 6:
        red, green, blue = tuple(int(rawhex[i:i + 2], 16) for i in (0, 2, 4))

    if len(rawhex) == 3:
        red, green, blue = tuple(int((rawhex[i] + rawhex[i]), 16) for i in (0, 1, 2))

    contrast = ((red * 299) + (green * 587) + (blue * 114)) / 1000
    return contrast


if __name__ == '__main__':
    parser = optparse.OptionParser(
        '%prog [options]\n '
        '%prog will apply a monochromatic colour theme to your Jamd instance using colour values that you specify.',
        version='%prog 1.0')

    parser_group_file = optparse.OptionGroup(parser, 'Your file will differ depending on your operating system.',
                                             'The default here is Linux')
    parser_group_file.add_option('-f', '--file',
                                 action='store', dest='stylefile',
                                 default='/usr/local/jss/tomcat/webapps/ROOT/ui/styles/main.css',
                                 help='The file that will be read and written.  '
                                      'Default: /usr/local/jss/tomcat/webapps/ROOT/ui/styles/main.css')
    parser.add_option_group(parser_group_file)

    parser_group_shift = optparse.OptionGroup(parser, 'Colour shifting values (stackable with gain)',
                                              'increase/decrease values relative to thier initial values, '
                                              'ie. 1.0 is 100% of the normal red/green/blue, '
                                              'ie. using 1.0 for all colours will leave no shift and produce grey')
    parser_group_shift.add_option('-r', '--redshift',
                                  action='store', type='float', dest='redshift',
                                  help='Percentage gain of red', default=1.0)
    parser_group_shift.add_option('-g', '--greenshift',
                                  action='store', type='float', dest='grnshift',
                                  help='Percentage gain of green', default=1.0)
    parser_group_shift.add_option('-b', '--blueshift',
                                  action='store', type='float', dest='blushift',
                                  help='Percentage gain of blue', default=1.0)
    parser.add_option_group(parser_group_shift)

    parser_group_gain = optparse.OptionGroup(parser, 'Colour gain values (stackable with shift)',
                                             'These increases/decreases the rgb by a fixed value, '
                                             'ie. ie. 0 will have a RGB value no higher than the normal red/green/blue, '
                                             'ie. using 0 for all colours will leave no gain and produce grey')
    parser_group_gain.add_option('-R', '--redgain',
                                 action='store', type='int', dest='redgain',
                                 help='numeric gain of red', default=0)
    parser_group_gain.add_option('-G', '--greengain',
                                 action='store', type='int', dest='grngain',
                                 help='numeric gain of green', default=0)
    parser_group_gain.add_option('-B', '--bluegain',
                                 action='store', type='int', dest='blugain',
                                 help='numeric gain of blue', default=0)
    parser.add_option_group(parser_group_gain)

    parser.add_option('-c', '--contrast',
                      action='store_true', dest='contrast', default=False,
                      help='add contrast to colour prior to shifting/gain')

    parser.add_option('-d', '--debug',
                      action='store_true', dest='debug', default=False,
                      help='see the value changes and do not commit the changes')

    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='see the value changes and do not commit the changes (redundant if using --debug)')

    options, args = parser.parse_args()

    main(options.stylefile,
         options.redshift, options.grnshift, options.blushift,
         options.redgain, options.grngain, options.blugain,
         options.contrast, options.debug, options.verbose)
