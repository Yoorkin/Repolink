import urllib.request
import json
import sys
import re

def printHelp():
    print('''
    Repolink <full-repo-name>
    Repolink list [-l] <user-name>
    Repolink search -u <user-name>
    Repolink search -r <repo-name>
    ''')

def searchUser(username,page):
    res = urllib.request.urlopen('https://github.com/search?p='+str(page)+'&q='+username+'&type=Users')    
    items = re.findall('(?<=/users/).+?(?=/hovercard)',str(res.read()))
    return items

def searchRepo(reponame,page):
    res = urllib.request.urlopen('https://github.com/search?p='+str(page)+'&q='+reponame)
    items = re.findall('(?<=<a class="muted-link" href="/).+?(?=/stargazers">)',str(res.read()))
    return items

def getRepoByFullName(fullname):
    url='https://api.github.com/repos/'+fullname
    res=urllib.request.urlopen(url)
    tmp=json.load(res)
    return tmp['clone_url']


def listRepoByUser(username):
    url='https://api.github.com/users/'+username+'/repos'
    res=urllib.request.urlopen(url)
    tmp=json.load(res)
    index=1
    items={}
    for t in tmp:
        item={}
        item['index']       = index
        item['name']        = t['name']
        item['clone_url']   = t['clone_url']
        item['stargazers']  = t['stargazers_count']
        item['watchers']    = t['watchers_count']
        item['forks']       = t['forks_count']
        items[index]        = item
        index+=1
    return items

def printUndefine():
    print("\033[31mRepolink: Undefined command. See 'Repolink -h.'\033[0m")

if __name__ == "__main__":
    count = len(sys.argv)-1
    if count == 1:
        if sys.argv[1]=='-h':
            printHelp()
        else :
            try:
                print(getRepoByFullName(sys.argv[1]))
            except urllib.error.HTTPError:
                print('\033[31mRepolink: Repository not found\033[0m')

    elif count == 2 and sys.argv[1] == 'list':
        items = listRepoByUser(sys.argv[2])
        for index in items:
            print(items[index]['name'])
    
    elif count == 3:
        cmd  = sys.argv[1]
        flag = sys.argv[2] 
        arg  = sys.argv[3]
        if cmd == 'list':
            items = listRepoByUser(arg)
            for index in items:
                print('\033[33m' + items[index]['name'] + '\033[0m')
                print('\033[32m' + str(items[index]['stargazers']) + ' Stars   ' + str(items[index]['forks']) + ' Forks   ' +str(items[index]['watchers'])+' Watchers\033[0m')
                print(items[index]['clone_url'])
                print()

        elif cmd == 'search':
            if flag == '-u':
                page = 1
                while(True):
                    print('Repolink: Searching ...')
                    for item in searchUser(arg,page):
                        print('\033[33m' + item + '\033[0m','https://github.com/' + item)
                    if(input('Press Enter to continue searching.')!=''):break
                    page+=1

            elif flag == '-r':
                page = 1
                while(True):
                    print('Repolink: Searching ...')
                    for item in searchRepo(arg,page):
                        print('\033[33m' + item + '\033[0m','https://github.com/' + item + '.git')
                        if(input('Press Enter to continue searching.')!=''):break
                        page+=1
            else:
                printUndefine
        else:
            printUndefine

    else:
        printUndefine

             



