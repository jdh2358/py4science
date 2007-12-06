#!/usr/bin/env python
"""Get BibTex references from preprint archives supported by SPIRES.

Usage:

  getbibtex preprint1 [preprint2 ....]

The list of preprints can also be fed in from standard input.

Preprint references can be given as:

 - name/number, as in hep-lat/0104015.

 This sets the archive name to 'name', and subsequent references can be given
 only as numbers. That is:

   hep-lat/n1 n2 n3 hep-ph/n4 n5
   
 will fetch n1,n2,n3 from hep-lat and n4,n5 from hep-ph.

 - numbers only. In this case, a preset default is used (you can change this
 value by editing getbibtex.py). The current default is: `%(def_archive)s`.

All archive names supported by SPIRES will work.
 
Output is given as a list of bibtex references, so you can simply do:

  getbibtex .... > mybiblio.bib

and mybiblio.bib will be a valid BibTex file.
"""

__author__ = "Fernando Perez <fperez@colorado.edu>"

#---------------------------------------------------------------------------
# Global defaults
def_archive = 'hep-lat'

import re,urllib,sys

#---------------------------------------------------------------------------
# Function definitions
def make_url(archive,number):
    """Make a SPIRES search url given an archive name and preprint number.

    make_url(archive,number) -> url string."""

    return ('http://www.slac.stanford.edu/spires/find/hep/www?'
            'eprint=%s&eprint=%s&format=wwwbriefbibtex'
            % (archive,number) )

def build_preprints_list():
    """Build the list of (archive,number) pairs from input parameters."""
    if len(sys.argv)>1:
        input_list = sys.argv[1:]
    else:
        input_list = sys.stdin.read().splitlines()
    pp_list = []
    archive = def_archive
    for item in input_list:
        if '/' in item:
            archive,number = item.split('/')
            pp_list.append([archive,number])
        else:
            pp_list.append([archive,item])
    return pp_list

#----------------------------------------------------------------------------
# Main code

# give user help if requested with -h... or --h...
try:
    if sys.argv[1].startswith('-h') or sys.argv[1].startswith('--h'):
        print __doc__ % globals()
        sys.exit()
except IndexError:
    pass

bibtex_re = re.compile( r'(@Article{.*})',re.DOTALL)

for archive,number in build_preprints_list():
    search_page = urllib.urlopen(make_url(archive,number)).read()
    try:
        print bibtex_re.search(search_page).group(1)
    except:
        print >> sys.stderr, 'ERROR: Failed to get results for:',archive,number
