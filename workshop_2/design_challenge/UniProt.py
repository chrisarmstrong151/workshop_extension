# UniProt request directly from the example on their website
# Source: https://www.ebi.ac.uk/proteins/api/doc/#/proteins

# Requests
import requests

# Exiting
import sys




# The class to make the requests
class UniProt:


    """Regex functions"""
    

    # Searcher, file-independent
    def search(
        self,
        parameters,
        requestURL
    ):

        """Actual searching"""

        # Create a parameter list
        p_list = []

        for k, v in parameters.items():
            p_list.append(k + '=' + v)
        
        r = requests.get(requestURL + '?' + '&'.join(p_list), headers={ 'Accept' : 'application/xml' })

        if not r.ok:
            responseBody = r.text
            print(responseBody)
            r.raise_for_status()
            sys.exit()

        responseBody = r.text
        
        return(responseBody)