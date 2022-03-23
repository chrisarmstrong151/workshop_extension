# Command line arguments
import argparse

# Regular expressions
import re

#hi chris


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
    help = 'Which regex search option to use.  The options are \'all_matches\', \'first_match\', and \'split_on_matches\'.', 
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
    
    # quantify the quality of the match with
    # respect to a reference file.
    def quantify_matches(
        self,
        comparison_file,
        match_objects,
        negatives_file
    ):

        """true/false positive/negatives"""
        
        # Take match objects, see if they are in the
        # right position and are the right strings.

        try:
            
            # First, load the comparison file.
            with open(comparison_file, 'r') as f:

                # We may not have been passed the right thing.
                if not isinstance(test, type(re.finditer('1', '1'))):

                    raise TypeError('A match object was not passed!')

                else:
                
                    # Each line consists of a string, a start 
                    # position, and a stop position.
                    lines = [g.strip().split('\t') for g in f.readlines()]

                    # Make the lines into tuples.
                    lines = [tuple(i) for i in lines]

                    # Small lambda to compare results.
                    # Create a tuple which contains the information
                    # about the match.
                    matcher = lambda valid, strt, stp : (valid, strt, stp)

                    # Make the match objects into tuples (note the
                    # type conversion for the start and
                    # stop positions).
                    matchable = [matcher(mo.group(), str(mo.start()), str(mo.end())) for mo in match_objects]

                    # Lines and matchable both contain unique items,
                    # so we can work with sets without loss of
                    # generality.
                    lines = set(lines)
                    matchable = set(matchable)

                    # Print the matches?
                    if args.print_matches is True:
                        for i in matchable:
                            print(i)

                    # Identify the true/false positives/negatives.

                    # Use Venn to explain...
                    true_positives = matchable & lines
                    false_positives = matchable - true_positives
                    false_negatives = lines - true_positives

                    # True negatives only defined if a file was passed.
                    if args.negatives_file is not None:
                        
                        # Open the negatives file and assign the true negatives.
                        with open(negatives_file, 'r') as g:
                            
                            file_negatives = set([tuple(z) for z in [h.strip().split('\t') for h in g.readlines()]])

                            true_negatives = file_negatives - matchable

                            # Return a dictionary with each.
                            return {
                                'ntp': len(true_positives),
                                'nfp': len(false_positives),
                                'nfn': len(false_negatives),
                                'ntn': len(true_negatives)
                            }

                    else:
                        
                        # Return a dictionary with each.
                        return {
                            'ntp': len(true_positives),
                            'nfp': len(false_positives),
                            'nfn': len(false_negatives)
                        }
        
        except FileNotFoundError:

            print('File not found!  Quitting...')
    

    # regex search
    def regex_search(
        self,
        return_match_objects,
        search_method,
        search_regex,
        search_text,
    ):

        """Actual searching"""

        # Try to get the file and search it.
        try:

            # errors="ignore" required on windows
            # Source: https://stackoverflow.com/a/50709581
            with open(search_text, 'r', errors="ignore") as f:
            
                # Completely remove newlines, making one massive
                # string.
                massive = ''.join([i.strip() for i in f.readlines()])
                
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
                            string = massive
                        )

                    else:

                        return re.findall(
                            pattern = regex_update, 
                            string = massive
                        )

                elif search_method == 'first_match':

                    # Kick back only the matches, or the match objects?
                    if return_match_objects is True:

                        # Kick back the match object.
                        return re.search(
                            pattern = regex_update,
                            string = massive
                        )

                    else:

                        # Only kick back the group as a LIST
                        # to keep return types consistent
                        # with the 'all_matches' option.
                        return [
                            re.search(
                                pattern = regex_update,
                                string = massive
                            ).group()
                        ]
        
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

# # (Optional) For generating a match list.
# with open('matches.tsv', 'w') as f:
#     for m in test:
#         f.write(m.group() + '\t' + str(m.start()) + '\t' + str(m.end()) + '\n')

# Quantify how well we searched.
test_again = rgx.quantify_matches(
    comparison_file = args.comparison_file,
    match_objects = test,
    negatives_file = args.negatives_file
)

print(test_again)