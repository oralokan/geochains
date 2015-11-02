# expander.py
# author: oral okan
# date: november 1, 2015

import re

class Expander(object):
    '''
    Expands template lines in a string of text.

    A template line is a single line that can be used to describe multiple
    lines of text. Expanding a template line refers to replacing it with
    the lines that it describes.

    Template lines contain a given regular expression. The matched string
    is passed onto a callback function (provided to the Expander object).
    The callback returns a list of strings. Each of these strings is separately
    substituted in place of the matched string, in order to generate one of
    the lines defined by the template. Finally, the template line is replaced
    with these generated lines.

    Example:
        input = "[D] is a digit"
                "[L] is a letter"
                "this is not a template"

        The pattern we are searching for is "[.]"

        Suppose the callback function provided is like this:
            if matched_string == "[D]", return [0,1,2,3,4,5,6,7,8,9]
            if matched_string == "[L]", return [a,b,c,...,x,y,z]

        The output would now be like:
            "0 is a digit"
            "1 is a digit"
            ...
            "9 is a digit"
            "a is a letter"
            ...
            "z is a letter"
            "this is not a template"

    The lines are recursively expanded until no more matches remain.
    In the above example, the input
        "[D] : [L]"
    would be expanded to
        "0 : a"
        "0 : b"
        ...
        "9 : z"

    Note that, the ordering of the generated lines that derive from the same
    template line is unspecified.

    The usage of the class is as follows:
        1. Instantiate an Expander object
        2. Set the pattern
        3. Set the substitute_callback function
    '''


    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, pstr):
        def is_valid_input(in_str):
            # TODO: Do input validation
            if pstr == None:
                return False
            return True
        if is_valid_input(pstr):
            self.__pattern = pstr
            self.__rgx = re.compile(pstr)
        else:
            self.__pattern = None
            self.__rgx = None
            raise ValueError("Illegal pattern input, value set to None")

    def _expand_line(self, in_line):
        '''
        Expands a given template line.
        '''
        match = self.__rgx.search(in_line)
        if not match:
            return in_line      # ending condition

        subs_vals = self.substitute_callback(match.group())
        span = match.span()
        head = in_line[:span[0]]
        tail = in_line[span[1]:]

        gen_lines = []

        for val in subs_vals:
            gen_lines.append( head + val + tail )

        result = '\n'.join(gen_lines)

        # The only difference amongst the generated lines is the different
        # values we substituted. We can look at just the first line to
        # determine if we need further expansion

        needs_further_expansion = False
        if self.__rgx.search(gen_lines[0]):
            needs_further_expansion = True
        
        if needs_further_expansion:
            return self.expand(result)
        return result
        

    def expand(self, in_str):
        '''
        Expand template lines in the provided string.
        See the class' docstring for more information.
        '''
        lines = in_str.split('\n')
        expanded_lines = [self._expand_line(l) for l in lines]
        out_str = '\n'.join(expanded_lines) 
        return out_str
