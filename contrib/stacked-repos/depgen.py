# From: https://gist.github.com/rcludwick/3663979


'''
These functions take a dictionary of dependencies in the following way:
depdict = { 'a' : [ 'b', 'c', 'd'],
            'b' : [ 'c', 'd'],
            'e' : [ 'f', 'g']
            }
has_loop() will check for dep loops in the dep dict with true or false.
flatten() will create an ordered list of items according to the dependency structure.
Note:  To generate a list of dependencies in increasing order of dependencies, say for a build, run: flatten(MyDepDict)
'''

def _order(idepdict, val=None, level=0):
    '''Generates a relative order in a dep dictionary'''
    results = {}
    if val is None:
        for k,v in idepdict.items():
            for dep in v:
                results.setdefault(k,0)
                d = _order(idepdict, val=dep, level=level+1)
                for dk, dv in d.items():
                    if dv > results.get(dk,0):
                        results[dk] = dv
        return results
    else:
        results[val] = level
        deps = idepdict.get(val, None)
        if deps is None or deps == []:
            return { val: level }
        else:
            for dep in deps:
                d = _order(idepdict, val=dep, level=level+1)
                for dk, dv in d.items():
                    if dv > results.get(dk,0):
                        results[dk] = dv
            return results

def _invert(d):
    '''Inverts a dictionary'''
    i = {}
    for k,v in d.items():
        if isinstance(v, list):
            for dep in v:
                depl = i.get(dep, [])
                depl.append(k)
                i[dep] = depl
        else:
            depl = i.get(v, [])
            depl.append(k)
            i[v] = depl
    return i

def flatten(depdict):
    '''flatten() generates a list of deps in order'''
    #Generate an inverted deplist
    ideps = _invert(depdict)

    #generate relative order
    order = _order(ideps)

    #Invert the order
    iorder = _invert(order)

    #Sort the keys and append to a list
    output = [] 
    for key in sorted(iorder.keys()):
        output.extend(iorder[key])
    return output


def has_loop(depdict, seen=None, val=None):
    '''Check to see if a given depdict has a dependency loop'''
    if seen is None:
        for k, v in depdict.items(): 
            seen = []
            for val in v: 
                if has_loop(depdict, seen=list(seen), val=val):
                    return True
            
    else:
        if val in seen:
            return True
        else:
            seen.append(val)
            k = val
            v = depdict.get(k,[])
            for val in v:
                if has_loop(depdict, seen=list(seen), val=val):
                    return True
    
    return False            
            
if __name__ == "__main__":

    # 1 depends upon 2, 3, and 4,  2 depends upon 5, etc.
    deps = {
                1: [ 2, 3, 4] ,
                2: [ 5 ],
                3: [ 4 , 6 ],
                5: [8],
                6: [ 7 ],
                7: [ 4 ],
                8: [7, 6] 
            }
    
    f = flatten(deps)
    # 2, 3, and 4 must come before 1, 8 must come before 5, etc...
    assert f == [4, 7, 6, 3, 8, 5, 2, 1]

    assert not has_loop(deps)

    #Force a loop
    deps[8] = [ 4, 1 ] 
    assert has_loop(deps)
    
    print('f:', f)
