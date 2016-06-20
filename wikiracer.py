#!/usr/bin/env python
#
# title          : wikiracer.py
# description    : a simple, automated wikiracer
# author         : Selwyn-Lloyd McPherson (selwyn.mcpherson@gmail.com)
# python_version : 3.5.0
# ==============================================================================

import json
import time
import wikipedia
from pyfiglet import Figlet

def refinesearch(coordinates):
    '''
    Function: refinesearch()
    Return: dict of coordinates

    This function processes the initial settings to make sure the start and end positions are resolved to 
    specific pages. It is essentially a disambiguation routine.
    '''

    for position, page in coordinates.items():  
        candidates = wikipedia.search(page)
        if len(candidates) == 0:                # Nothing found, abort
            print('Sorry, I couldn\'t understand you input! Try again\n')
            raise SystemExit()                  # More than one found, query the user
        elif len(candidates) > 1:
            print('\nFound a few for {page}. . . Which would you like?\n'.format(page=page))

            # Print the options
            for idx,choice in enumerate(candidates):
                print('[{name}]: {term}'.format(name=idx, term=choice))
            
            choicenum = int(input('\nYour choice (numerical)?\n\n> '))

            # Cndidates the input
            while choicenum < 0 or choicenum > len(candidates):     # Yes, this will break with ASCII input but
                print('Sorry, I didn\'t get that')                  # let's forget about that try/except code
                choicenum = int(input('Which would you like?\n> '))
            
            coordinates[position] = candidates[choicenum]

    return coordinates

def readinput():
    '''
    Function: readinput()
    Return: dict of start and end pages

    Two methods are implemented here, reading from a file and CLI / on-the-fly input
    '''

    # Interrogative to determine the input method

    response = None

    while not response:
        # Not a particular reason to convert to int here, but it seems prettier
        response = int(input('Do you wish to \n1: Type a filename or \n2: Manually choose articles?\n> '))

        if response not in [1,2]:
            print('Sorry, I didn\'t understand your response!')
            response = None

    if response == 1:           # Filename
        fn = input('Enter the filename: ')
        try:
            settings = json.load(open(fn,'r'))
            start = settings['start']
            end = settings['end']
        except:             # Manual entry
            print('Sorry, file not found. Ending. . .')
            raise SystemExit()
    elif response == 2:         # CLI
        start = input('Starts with: ')
        end = input('Ends with: ')

    coordinates = refinesearch({'start': start, 'end': end})        # Narrow the choices if necessary

    return coordinates

def followpath(coords):
    '''
    Function: followpath(coords,path-list())
    Return: Path (list)
    
    The function that executes searches on links presented in the main body of the 
    Wikipedia page. We use a queue here to keep track of the path. A recursive algorithm
    is perfectly suited for a depth first search but that approach won't work here. So 
    we need to maintain and traverse the graph this way.
    '''

    queue = [(coords['start'], [coords['start']])]
    seen = set()

    while queue:
        (vertex, path) = queue.pop(0)
        offset = ''.join(['.' for p in path])

        # Attempt to grey he links on the current page. Sometimes, disambiguation pages work slightly differently
        # and occasionally, for whatever reason, a PageError is thrown, though very rarely and apparently randomly.
        # So we'll make sure to check for that

        try:
            links = wikipedia.page(vertex).links

        except wikipedia.exceptions.DisambiguationError as e:
            links = e.options                           # If disambiguation, add each
        except wikipedia.exceptions.PageError:          # Not sure why this occurs but it seems random
            print('{page} failed (PageError). . .'.format(page=vertex))
        except:
            print('{page} failed (Unknown). . .'.format(page=vertex))

        # Traverse each link not already seen
        for link in set(links) - set(seen):             # Avoid infinite loop [2]
            seen.add(link)

            print('{offset} {title} ({path})'.format(offset=offset,title=link,path=path))

            if link == coords['end']:
                path.append(link)
                return (path,len(seen))
            else:
                queue.append((link, path + [link]))



def main():
    ''' 
    Function: main()
    Return: None

    Main control routinee. This is quite script-y and certainly some of these elements could
    be extracted as functions, but it's such a small project that it's reasonable to leave 
    this as is
    '''

    # Introduction
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('W i k i R a c e r !'))

    # Initialization
    settings = None
    response = None

    coordinates = readinput()                           # Initialize start and end

    print('Working the path \nFrom: {start}\nTo: {end}'.format(start=coordinates['start'],end=coordinates['end']))

    print('\nTracing. . .')

    start = time.time()
    (resultpath,seen) = followpath(coordinates)
    duration = time.time() - start

    print('\nPath: {p}'.format(p=resultpath))
    print('Time elapsed: {t}'.format(t=duration))
    print('Total pages seen: {s} seconds'.format(s=seen))

if __name__ == "__main__":
    main()
