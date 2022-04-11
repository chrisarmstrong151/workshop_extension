# Regular expressions
import re




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
        # print('\nSearch string: ' + regex_update + '\n')
    
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