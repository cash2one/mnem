'''
Created on 3 Apr 2016

@author: John Beard
'''

class RequestLoader(object):
    '''
    A class to manage custom requests - provides one or more of:
        - Request references to external resources that  user can visit with
          some external program
        - Request data consisitng of retreived and presented data that the 
          user caan consume directly
    '''

    def __init__(self):
        pass

    def getRequestReference(self, query):
        '''
        Gets the request reference for this query
        '''
        raise NotImplementedError

    def getRequestData(self, query):
        '''
        Gets structured data from the given query
        '''
        raise NotImplementedError
