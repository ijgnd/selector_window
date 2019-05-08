"""
combination and minimal adjustment of 
- https://raw.githubusercontent.com/renerocksai/sublimeless_zk/master/src/fuzzypanel.py
- https://github.com/renerocksai/sublimeless_zk/utils.py

Copyright (c): 2019 ijgnd
               2018 Rene Schallner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def process_search_string_withStart(search_terms,dict_,max):
    """inspired by find_in_files from sublimelesszk"""
    search_terms = split_search_terms_withStart(search_terms)
    results = []
    for lent in dict_.keys():
        for presence, atstart, term in search_terms:
            if term.islower():
                i = lent.lower()
            else:
                i = lent 
                
            # if presence and term not in i:
                # break
            # elif not presence and term in i:
                # break
                
            if presence:
                if term not in i:
                    break
                elif atstart and not i.startswith(term):
                    break
            else:   #not in 
                if term in i:
                    break
                elif atstart and i.startswith(term):
                    break
        else:
            results.append(lent)
    return results
    

def split_search_terms_withStart(search_string):
    """
    Split a search-spec (for find in files) into tuples:
    (posneg, string)
    posneg: True: must be contained, False must not be contained
    string: what must (not) be contained
    """
    in_quotes = False
    in_neg = False
    
    at_start = False
    
    pos = 0
    str_len = len(search_string)
    results = []
    current_snippet = ''
    
    literal_quote_sign = '"'
    exclude_sign = '!'
    startswith_sign = "_" 
    
    while pos < str_len:
        if search_string[pos:].startswith(literal_quote_sign):
            in_quotes = not in_quotes
            if not in_quotes:
                # finish this snippet
                if current_snippet:
                    results.append((in_neg, at_start, current_snippet))
                in_neg = False
                current_snippet = ''
            pos += 1
        elif search_string[pos:].startswith(exclude_sign) and not in_quotes and not current_snippet:
            in_neg = True
            pos += 1
        elif search_string[pos:].startswith(startswith_sign) and not in_quotes and not current_snippet:
            at_start = True
            pos += 1
        elif search_string[pos] in (' ', '\t') and not in_quotes:
            # push current snippet
            if current_snippet:
                results.append((in_neg, at_start, current_snippet))
            in_neg = False
            at_start = False
            current_snippet = ''
            pos += 1
        else:
            current_snippet += search_string[pos]
            pos += 1
    if current_snippet:
        results.append((in_neg, at_start, current_snippet))
    return [(not in_neg, at_start, s) for in_neg, at_start, s in results]
