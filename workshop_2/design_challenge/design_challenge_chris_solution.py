# Command line arguments
import argparse

# Nice printing for dictionaries
import json

from Regex import Regex
from UniProt import UniProt




# Initialize parser
parser = argparse.ArgumentParser(
    description = 'Search for regular expressions in a file.',
    add_help = False
)

# Adding arguments
# Source: https://stackoverflow.com/questions/39047075/reorder-python-argparse-argument-groups/39047348

requiredNamed = parser.add_argument_group('required named arguments')

requiredNamed.add_argument(
    '-m', 
    '--method', 
    help = 'Which regex search option to use.  The options are \'all_matches\', \'first_match\'.', 
    required = True
)

requiredNamed.add_argument(
    '-r', 
    '--regex', 
    help = 'The regex to use when searching --text.', 
    required = True
)

requiredNamed.add_argument(
    '-t', 
    '--text', 
    help = 'What text to search.  Should be a file.', 
    required = True
)




optional = parser.add_argument_group('optional arguments')

optional.add_argument(
    '-h', 
    '--help', 
    action = 'help', 
    help = 'Show this help message and exit.'
)

optional.add_argument(
    '-c', 
    '--comparison-file', 
    help = 'Which file to compare results to.'
)

optional.add_argument(
    '-n', 
    '--negatives-file', 
    help = 'Which file contains the true negatives.'
)

optional.add_argument(
    '-o', 
    '--objects', 
    action = 'store_true',
    help = 'Pass match objects from search.  Default is FALSE.',
)

optional.add_argument(
    '-p', 
    '--print-matches', 
    action = 'store_true',
    help = 'Print the match list.',
)

# optional.add_argument(
#     '-w', 
#     '--write-matches', 
#     action = 'store_true',
#     help = 'Write the matches to file.',
# )

# Read arguments from command line.
args = parser.parse_args()




# --- MAIN --- #




# Instantiate the class.
rgx = Regex()

# See if we can find the regex.
test = rgx.regex_search(
    return_match_objects = args.objects,
    search_method = args.method,
    search_regex = args.regex,
    search_text = args.text
)

# Get the unique results.
results = list(set(test))

# Get rid of the white space.
results = [i.strip() for i in results]

print(results)

# Make any requests?
if len(results) > 0:

    # Instantiate the class.
    nprt = UniProt()

    # Do a search for each protein.
    for p in results[0:2]:
        
        # Set the response format here.
        frmt = 'tab'
        
        # For 'tab' retrieval, MUST use 'limit'
        # parameter...        
        uprt_response = nprt.search(
            parameters = {
                'columns': 'genes',
                'format': frmt,
                'keywords': p,
                'limit': '100',
                'offset': '0'
            },
            requestURL = 'https://uniprot.org/uniprot/?query'
        )

        # Write the response.
        with open(p + '.' + frmt, 'w') as f:
            f.write(uprt_response)