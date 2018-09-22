### Web page Downloader ###

import sys
import urllib.request
from colorama import Fore, Back, Style
import re
import os

timeout_time = 2
search_level = 0
url = ""
file_format = ""
files_to_download = []
save_directory = ''

def find_links_of( url , search_level):
    for x in range(0,search_level):
        print("\t" , end = "")
    print(url)
    try:
        links = urllib.request.urlopen(url , timeout=timeout_time)
        links = links.read().decode('utf-8' , 'ignore')
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', links)
        return links
    except urllib.error.URLError:
        for x in range(0,search_level):
            print("\t" , end = "")
        print(Fore.RED + "Passing the link because of URL is unreachable")
        print(Style.RESET_ALL , end="")
        return []
    except KeyboardInterrupt:
        if input('\nAre you sure you want to quit (y/n)? : ') == 'y':
            sys.exit(0)
            print(Style.RESET_ALL , end="")
        print("Continue:")
        return []
    except:
        for x in range(0,search_level):
            print("\t" , end = "")
        print(Fore.RED + "The read operation timed out")
        return []

def is_url(__str__):
    if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',__str__):
        return True
    return False

def downloading(all , reqs , save_dir):
    if len(all) == 0 or len(reqs) == 0:
        print('nothing found')
        sys.exit(0)
    print(Fore.BLUE + Back.CYAN + 'from:')
    print(Style.RESET_ALL)
    print(all)
    print(Fore.RED + Back.CYAN + 'downloading:')
    print(Style.RESET_ALL)
    print(reqs)
    print("total of " ,  end = '')
    print(len(reqs) , end = " ")
    if input("files will be downloaded start download (y/n) ?") == 'y':
        for x in reqs:
            print("downloading : " , end = '')
            print(x)
            print('\t as : ' , end = '')
            print(x[x.rfind("/")+1:] + '\n')
            try:
                urllib.request.urlretrieve(x , save_dir + '/' + x[x.rfind("/")+1:] , timeout=timeout_time)
            except:
                print(Fore.RED + 'Download Failed')
                print(Style.RESET_ALL)

def help():
    print("grabbs files from a specified web page with specified format")
    print("usage: pyGrabber <website_url> <-f file_format> [-d save directory] [-l search level]")
    print("\toptions:")
    print("\t\t-f format\tsearch the pages for files with this format")
    print("\t\t-d directory\tsaves the downloade files into this directory")
    print("\t\t-l level\tint number to define deepness of search default is 0")

for x in range(0,len(sys.argv)):
    if "-h" in sys.argv or "--help" in sys.argv:
        help()
        sys.exit(0)
    if "-f" not in sys.argv or not is_url(sys.argv[1]):
        print("Bad input")
    if sys.argv[x-1] == '-l' or sys.argv[x-1] == '-f' or sys.argv[x-1] == '-d':
        continue
    if sys.argv[x] == '-l':
        print ('search level  : ' , end = '')
        print (sys.argv[x+1])
        search_level = int(sys.argv[x+1])
    elif is_url(sys.argv[x]):
        print ("search url    : " , end = '')
        print (sys.argv[x] )
        url = sys.argv[x]
    elif sys.argv[x] == '-f':
        print ("search format : " , end = '')
        print (sys.argv[x+1])
        file_format = sys.argv[x+1]
        if not file_format.startswith('.'):
            file_format = '.' + file_format
    elif sys.argv[x] == '-d':
        print ('saving into   : ' , end = '')
        print (sys.argv[x+1])
        save_directory = sys.argv[x+1]
        if not os.path.exists(save_directory):
            if input('directory does not exist create it (y/n)? : ') == 'y':
                os.makedirs(save_directory)
            else:
                sys.exit(0)

# file_content = urllib.request.urlopen(url , timeout=timeout_time)
# file_content = file_content.read().decode('utf-8' , 'ignore')
# file_content = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)

file_content = [url]
append_file_content = []

for x in range(0 , search_level):
    for y in range(0 , len(file_content)):
        try:
            new_links = find_links_of(file_content[y] , x)
            if new_links not in file_content and new_links not in append_file_content:
                append_file_content = append_file_content + new_links
            # append_file_content.append(find_links_of(file_content[y] , x))
        except TypeError:
            print(Fore.RED + "TypeError")
            print(Style.RESET_ALL , end="")
            pass
    file_content = append_file_content
    # or file_content = file_content = append_file_content + file_content it includes lower levels but scans lower levels many times
    append_file_content = []


for x in file_content:
    try:
        if x.endswith(file_format):
            files_to_download.append(x)
    except AttributeError:
        print(x)
        pass

downloading(file_content , files_to_download , save_directory)

# print("total of " end = '')
# print(len(files_to_download) , end = " ")
# print("files will be downloaded start download (y/n) ?")
#
# for x in files_to_download:
#     print("downloading : " , end = '')
#     print(x)
#     print('\t as : ' , end = '')
#     print(x[x.rfind("/")+1:] + '\n')
#     urllib.request.urlretrieve(x , save_directory + '/' + x[x.rfind("/")+1:] )
