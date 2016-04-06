'''
Created on 6 Apr 2016

@author: John Beard
'''


def stringLongestBetween(s, l, r, keepEnds):
    start, e = s.find(l), s.rfind(r)

    if (keepEnds):
        e = e + len(r)
    else:
        start = start + len(l)
    return s[start: e]

def stripJsonp(jsonp):
    return stringLongestBetween(jsonp, "(", ")", False)
