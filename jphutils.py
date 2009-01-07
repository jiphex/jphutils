#!/usr/bin/env python
# encoding: utf-8
"""
jphutils.py

Created by James Hannah on 2008-05-12.
Provided under the Modified BSD License - http://tinyurl.com/5toaqa

"""
import time
import sys
import logging
import hashlib

class LogPrinter:
    """LogPrinter class which serves to emulates a file object and logs
       whatever it gets sent to a Logger object at the INFO level.
       
    """
    def __init__(self):
        """Grabs the specific logger to use for logprinting."""
        self.ilogger = logging.getLogger('logprinter')
        il = self.ilogger
        logging.basicConfig()
        il.setLevel(logging.INFO)
    
    def write(self, text):
        """Logs written output to a specific logger"""
        self.ilogger.info(text)
    

# Annotation
def benchmark(func):
    """Decorator adding printing of time taken to run methods."""
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s completed in %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

# Annotation
def logprintinfo(func):
    """Wraps a method so that any calls made to print get logged instead"""
    def pwrapper(*arg):
        stdobak = sys.stdout
        lpinstance = LogPrinter()
        sys.stdout = lpinstance
        res = func(*arg)
        sys.stdout = stdobak
        return res
    return pwrapper

# Annotation wrapper annotation method
def unimplemented(defaultval = None):
    """Right, this one's going to look complicated at first.
       If you can first of all just look from the line that begins with the
       declaration of the unimp_wrapper function, that and the next 6 lines
       can be seen as a standard decorator.
       
       However, the decorator also takes an optional argument which is the
       other complicated bits. Python decorators are a bit clumsy where it
       comes to functions, the lines above this docstring and the last return
       are to deal with that, the argument given is returned from inside the 
       wrapper function.
       
       But but but, it's pretty annoying that you can't call @unimplemented
       with no arguments leaving out the brackets because then it turns into
       a normal decorator, which is what's handled by the two statements
       inside the if statement. This simply checks if the decorator call
       argument is a function itself (means that the decorator got called
       without the brackets). This has to return a function that returns None,
       (which the lambda is short for).
       
       Ok, sorted. Let me know if you don't get it.
       
       Examples:
       
       >>> @unimplemented
       ... def foo():
       ...     return "abc"
       ...
       >>> foo() == None
       True
       
       >>> @unimplemented(1337)
       ... def foo():
       ...     return "abc"
       ... 
       >>> foo() == 1337
       WARNING: Unimplemented function 'foo' executed!
       True
       
       """
    if callable(defaultval):
        return lambda *val: None
    else:
        # Actual annotation
        def unimp_wrapper(func):        
            # What we replace the function with
            def wrapper(*arg):
                print "WARNING: Unimplemented function '%s' executed!" %\
                                                              func.func_name
                return defaultval
            return wrapper
        return unimp_wrapper

def hashfile(filepath):
    """Takes a path to a file as it's argument, and returns a SHA1 hash of the
    file's contents.
    
    Example:
    
    >>> hashfile("/dev/null")
    'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    
    """
    openf = open(filepath, 'rb')
    hasher = hashlib.sha1()
    hasher.update(openf.read())
    openf.close()
    return hasher.hexdigest()

def __run_tests():
  import doctest
  doctest.testmod()

if(__name__ == "__main__"):
  __run_tests()
