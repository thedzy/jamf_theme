# jamf_theme
This will apply a monochromatic colour theme to your Jamf instance using colour values that you specify.

This can be useful for differntialing different instances to avoid errors as each instance will have noticable visual appearance.

Last tested version 10.11

## Options:
```--version             show program's version number and exit
-h, --help            show this help message and exit
-c, --contrast        add contrast to colour prior to shifting/gain
-d, --debug           see the value changes and do not commit the changes
-v, --verbose         see the value changes and do not commit the changes (redundant if using --debug)

Your file will differ depending on your operating system.:
The default here is Linux
-f STYLEFILE, --file=STYLEFILE
    The file that will be read and written.  Default: /usr/local/jss/tomcat/webapps/ROOT/ui/styles/main.css

Colour shifting values (stackable with gain):
increase/decrease values relative to thier initial values,
ie. 1.0 is 100% of the normal red/green/blue
ie. using 1.0 for all colours will leave no shift and produce grey

-r REDSHIFT, --redshift=REDSHIFT
    Percentage gain of red
-g GRNSHIFT, --greenshift=GRNSHIFT
    Percentage gain of green
-b BLUSHIFT, --blueshift=BLUSHIFT
    Percentage gain of blue

Colour gain values (stackable with shift):
These increases/decreases the rgb by a fixed value,
ie. 0 will have a RGB value no higher than the normal red/green/blue
ie. using 0 for all colours will leave no gain and produce grey

-R REDGAIN, --redgain=REDGAIN
    numeric gain of red
-G GRNGAIN, --greengain=GRNGAIN
    numeric gain of green
-B BLUGAIN, --bluegain=BLUGAIN
    numeric gain of blue
```

## Notes:
1. **Using --contrast is highly recommended, I might just make it default at some point.**
2. Make a backup for your css.  Although this will back it up for you, on second run, if you don't restore it, it will wipe it out.
3. Always restore from backup before attempting to change as it will attempt to change the changes.  This can have some cool effect like increasing the cintrat more.

## Screenshots:
### Blue
```jamf_theme.py -b 1.2 -B 20 -c```
![Blue](https://raw.githubusercontent.com/thedzy/jamf_theme/images/jamf_theme_blue.jpg)

### Red
```jamf_theme.py -r 1.2 -R 20 -c```
![Red](https://raw.githubusercontent.com/thedzy/jamf_theme/images/jamf_theme_red.jpg)

### Teal
![Teal](https://raw.githubusercontent.com/thedzy/jamf_theme/images/jamf_theme_teal.jpg)

### Purple
![Purple](https://raw.githubusercontent.com/thedzy/jamf_theme/images/jamf_theme_purple.jpg)

_Relocated from Python repo.  This is it's new home_
