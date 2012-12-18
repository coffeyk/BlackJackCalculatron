'''
Created on Dec 17, 2012

@author: Kevin
'''

def staticTestBuilder(function, inp):
    '''
    Generate a test case for a function based 
    on it's current output over an input range. 
    '''
    print "def test%(functionName)s(self):" % {"functionName": function.__name__}
    for i in inp:
        assertString = "\tself.assertEqual(%(functionName)s(%(parameter)s), %(result)s)" % \
            {"functionName": function.__name__,
             "parameter": i,
             "result": function(i)}
        print assertString