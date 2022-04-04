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

# Goal 1
requiredNamed.add_argument(
    '-i', 
    '--id', 
    help = 'The Gene Ontology (GO) ID.',
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
        
        # Make the request and get the JSON.
        print('https://api.geneontology.org/api/bioentity/function/' + '2345235432523542345' + which_id)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        r = requests.get(
            url = 'https://api.geneontology.org/api/bioentity/function/' + '2345235432523542345' + which_id
        )
        print(r)
        processed_response = r.json()
        print('*************************************************')
        print(processed_response)
        # print(q)

        # Define a list to hold Panther Family values.
        panther_families = []

        # Go over each item in the processed response
        # and extract the family values.
        for t in processed_response:
            if 'panther_family' in t:
                panther_families.append(t['panther_family'])

        # No need for unique family values, but we'll
        # get them anyways.
        panther_families = list(set(panther_families))

        try:
        
            # Pick a random one to make the second request.
            random_panther_family = random.choice(panther_families)

            # Get rid of the portion of the string that cannot be used
            # to search.
            
            # Get rid of the portion of the string that cannot be used
            # to search.
            random_panther_family = random_panther_family.split(':')[1]

            # Make the second request using POST.
            r = requests.post(
                url = 'http://pantherdb.org/services/oai/pantherdb/familymsa?family=' + random_panther_family + 'CORRUPTEDSTUFF'
            )

            # Print the result and return it.
            processed_response = r.json()

            print(
                json.dumps(
                    obj = processed_response,
                    indent = 4,
                    sort_keys = True
                )
            )

            return processed_response
        
        except IndexError:

            print('Poorly formed request.  Quitting...')

            return -1
    

    # Strip the terms.
    def strip_terms(
        self
    ):

        # Open the file.
        with open('goslim_mouse.obo', 'r') as f:

            # Create a [Term] list.
            Term_list = []

            # Create a Term dict.
            Term_dict = {}
            
            # Go line-by-line.
            for line in f.readlines():
                
                # How do you avoid using a regular expression
                # to not read trash after [Term]?
                if line == '[Typedef]\n':
                    break
                
                # Only append 'id' and 'def' lines.
                if 'id: ' in line and 'alt_id: ' not in line:
                    Term_list.append(line.split('id: ')[1].strip())
                
                if 'name: ' in line:
                    Term_list.append(line.split('name: ')[1].strip())
                
                if 'def: "' in line:
                    
                    # Get rid of the double quotes.

                    # Split first.
                    split_up = line.split('def: ')[1].strip()

                    # Replace the double quotes.
                    split_up = split_up.replace('"', '')
                    
                    # Append.
                    Term_list.append(split_up)
            
            # Every 0th entry in Term_list is a GO ID,
            # every 1st entry in Term_list is a name,
            # and every 2nd entry in Term_list is a def.
            for i in range(0, len(Term_list), 3):
                
                # Add the GO ID first, then set values.
                Term_dict[Term_list[i]] = {}            
                Term_dict[Term_list[i]]['name'] = Term_list[i+1]
                Term_dict[Term_list[i]]['def'] = Term_list[i+2]
            
            # Kick it back.
            return Term_dict




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
    print('ID was found...')
    rqstr.make_request(
        which_id = args.id
    )