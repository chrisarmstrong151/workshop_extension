# Command line arguments
import argparse

# Nice printing
import json

# Picking a random Panther family
import random

# Requests
import requests




# Initialize parser.
parser = argparse.ArgumentParser(
    description = 'Make a call to GO.',
    add_help = False
)

# Adding arguments
# Source: https://stackoverflow.com/questions/39047075/reorder-python-argparse-argument-groups/39047348

requiredNamed = parser.add_argument_group('required named arguments')




optional = parser.add_argument_group('optional arguments')

optional.add_argument(
    '-h', 
    '--help', 
    action = 'help', 
    help = 'Show this help message and exit.'
)
optional.add_argument(
    '-s', 
    '--server', 
    help = 'The server to send the request to.  Default is \'https://api.geneontology.org/api/\''
)

# Read arguments from command line.
args = parser.parse_args()

# Set the server name.
if args.server is None:
    args.server = 'http://api.geneontology.org/'




# The class to make the requests
class Requestor:

    def look_for_identity(
        self,
        search_value,
        searchable_dict
    ):

        # Simple search.
        for k, v in searchable_dict.items():
            if k == search_value:
                
                result = {
                    search_value: searchable_dict[k] 
                }
                
                # Print the result, then return it.
                print(
                    json.dumps(
                        obj = result,
                        indent = 4,
                        sort_keys = True
                    )
                )
                
                # return IS a break...
                return result
    
    def make_request(
        self,
        which_id
    ):
    
        # Make the request and get the JSON.
        
        # Missing some code here...

        # Go over each item in the processed response
        # and extract the family values.
        for t in processed_response:
            if 'panther_family' in t:
                panther_families.append(t['panther_family'])

        # No need for unique family values, but we'll
        # get them anyways.
        panther_families = list(set(panther_families))

        # Pick a random one to make the second request.
        random_panther_family = random.choice(panther_families)

        # Get rid of the portion of the string that cannot be used
        # to search.
        
        # Missing some code here...

        print(
            json.dumps(
                obj = processed_response,
                indent = 4,
                sort_keys = True
            )
        )

        return processed_response




# --- MAIN --- #




# Instantiate the class
rqstr = Requestor()

# See if we can find the identity.
test = rqstr.look_for_identity(
    search_value = args.id,
    searchable_dict = rqstr.strip_terms()
)

# Only make an API request if the identity was found.
if test is not None:
    rqstr.make_request(
        which_id = args.id
    )