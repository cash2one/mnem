'''
Created on 4 Apr 2016

@author: John Beard
'''

ERRORS = {
    'internal': 1,
    'mnemory-not-found': 2,
    'request-type-not-found': 3,
    'locale-not-found': 4
}

ERROR_STR = {
    'internal': "Internal error",
    'mnemory-not-found': "Mnemory not found",
    'request-type-not-found': "Request type not found",
    'locale-not-found': "Locale not found for mnemory"
}

def constructError(errKey, context):
    """
    Constructs a general error. Has at least the error code and
    description string, with an optional context if you have
    more details
    """

    try:
        err = {'error': {
            'code': ERRORS[errKey],
            'str' : ERROR_STR[errKey]
        }}
    except KeyError:
        # internal error if we can't even find the error key
        return constructError('internal', "Unknown error key: %s" % errKey)

    if (context):
        err['error']['context'] = context
    return err