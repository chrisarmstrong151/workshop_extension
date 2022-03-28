# Command line arguments
import argparse

# Nice printing for dictionaries
import json

# Regular expressions
import re




# Initialize parser.
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




# The class to make the requests
class Regex:


    """Regex functions"""
    

    # Searcher, file-independent
    def searcher(
        self,
        return_match_objects,
        search_method,
        search_regex,
        search_text,
    ):

        """Actual searching"""
        
        # Kick back the matches, but first, fix
        # the regex to search for.

        # Complex...
        # Source: https://stackoverflow.com/a/55810892
        regex_update = rf"{search_regex}"

        # Tell the user what the search string is.
        print('\nSearch string: ' + regex_update + '\n')
    
        # Do a search based on the method provided.
        if search_method == 'all_matches':
            
            # Kick back only the matches, or the match objects?
            if return_match_objects is True:

                # Use the iterable.
                # Source: https://stackoverflow.com/questions/4697882/how-can-i-find-all-matches-to-a-regular-expression-in-python/4697884#4697884
                return re.finditer(
                    pattern = regex_update,
                    string = search_text
                )

            else:

                return re.findall(
                    pattern = regex_update, 
                    string = search_text
                )

        elif search_method == 'first_match':

            # Kick back only the matches, or the match objects?
            if return_match_objects is True:

                # Kick back the match object.
                return re.search(
                    pattern = regex_update,
                    string = search_text
                )

            else:

                # Only kick back the group as a LIST
                # to keep return types consistent
                # with the 'all_matches' option.
                return [
                    re.search(
                        pattern = regex_update,
                        string = search_text
                    ).group()
                ]
    

    # regex search
    def regex_search(
        self,
        return_match_objects,
        search_method,
        search_regex,
        search_text,
    ):

        """Try to load a file"""

        # Try to get the file and search it.
        try:

            # errors="ignore" required on windows
            # Source: https://stackoverflow.com/a/50709581
            with open(search_text, 'r', errors = 'ignore') as f:
            
                # Completely remove newlines, making one massive
                # string.
                massive = ''.join([i.strip() for i in f.readlines()])

                # Ask for the matches.
                return self.searcher(
                    return_match_objects = return_match_objects,
                    search_method = search_method,
                    search_regex = search_regex,
                    search_text = massive
                )
        
        except FileNotFoundError:

            print('File not found!  Quitting...')




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

# print(test)
# print(len(test))

print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

# Create a dictionary to hold the database name
# and IDs.
db_links = {}

# Process a list of possible hits.
for t in test:
    
    print('---------------------------')
    
    # The HTML structure reveals that the database IDs
    # occur within a <tbody></tbody> structure.  In particular,
    # database IDs are LINKED, so look for the database name
    # and the database link only.
    print(t)
    # We can split on the <sup>i</sup> match.
    structured_search = rgx.searcher(
        return_match_objects = True,
        search_method = 'all_matches',
        search_regex = '(.*?)<sup>i</sup>(.*?)<\/tr>',
        search_text = t
    )

    for m in structured_search:
        print('***************************')
        print(m.group())

        # Get the position of the match, then partition
        # the string based on this position.
        match_position = m.group().index('<sup>i</sup>')
        print('match_position: ' + str(match_position))
        
        print('@@@@@@@@@@@@@@')
        dbname = m.group()[0:match_position]
        links = m.group()[match_position+12:]
        print(dbname)
        print('%%%%%%%%%%%%%%%%%%%%%')
        print(links)
        print('###################')
        
        # Now find the last '>' FROM THE END.
        # Source: https://www.tutorialspoint.com/python/string_rfind.htm
        last_char_search = dbname.rfind('>')

        if last_char_search != -1:
            
            # Just keep the last part of the string
            # past the match.
            print('DATABASE NAME')
            print(dbname[last_char_search+1:])

            # Add to the results.
            if dbname[last_char_search+1:] not in db_links:
                db_links[dbname[last_char_search+1:]] = []
            
            # Find the links after the sup tags.
            links_search = rgx.searcher(
                return_match_objects = True,
                search_method = 'all_matches',
                search_regex = '(.*?)<a (.*?)>(.*?)<\/a>',
                search_text = links
            )

            # Go over each potential link match.
            for lm in links_search:

                # Split on the </a>.
                a_split = lm.group().split('</a>')

                for a in a_split:

                    # Now just keep characters from the
                    # right side, like above.
                    last_char_search_links = a.rfind('>')

                    if last_char_search_links != -1:

                        # Append.
                        print('Attempt to append...')
                        print(db_links[dbname[last_char_search+1:]])
                        print(a[last_char_search+1:])
                        db_links[dbname[last_char_search+1:]].append(a[last_char_search_links+1:])
                        print('~~~~~~~~')
                        print(a[last_char_search_links+1:])

    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

# Quick and dirty method to get the unique values
# from db_links.
db_links_keys = db_links.keys()

pretty = {}

for k in db_links_keys:
    pretty[k] = list(set(db_links[k]))

# Print it nice and pretty.
print(
    json.dumps(
        pretty,
        indent = 4,
        sort_keys = True
    )
)