### Web page Downloader ###

import sys
import urllib.request as urllib
from colorama import Fore, Back, Style
import re
import os

search_level = 0
url = ""
file_format = ""
files_to_download = []
save_directory = ''

def is_url(__str__):
    if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',__str__):
        return True
    return False

for x in range(0,len(sys.argv)):
    if sys.argv[x-1] == '-l' or sys.argv[x-1] == '-f' or sys.argv[x-1] == '-d':
        continue
    if sys.argv[x] == '-l':
        print ('search level  : ' , end = '')
        print (sys.argv[x+1])
        search_level = int(sys.argv[x+1])
    elif is_url(sys.argv[x]):
        print ("search url    : " , end = '' )
        print (sys.argv[x] )
        url = sys.argv[x]
    elif sys.argv[x] == '-f':
        print ("search format : " , end = '')
        print (sys.argv[x+1])
        file_format = sys.argv[x+1]
    elif sys.argv[x] == '-d':
        print ('saving into   : ' , end = '')
        print (sys.argv[x+1])
        save_directory = sys.argv[x+1]
        if not os.path.exists(save_directory):
            if input('directory does not exist create it (y/n)? : ') == 'y':
                os.makedirs(save_directory)
            else:
                sys.exit(0)

file_content = urllib.urlopen(url)
file_content = file_content.read().decode('utf-8' , 'ignore')
file_content = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)

for x in file_content:
    if x.endswith(file_format):
        files_to_download.append(x)

print(Fore.BLUE + Back.CYAN + 'from:')
print(Style.RESET_ALL)
print(file_content)
print(Fore.RED + Back.CYAN + 'downloading:')
print(Style.RESET_ALL)
print(files_to_download)

for x in files_to_download:
    print("downloading : " , end = '')
    print(x)
    print('\t as : ' , end = '')
    print(x[x.rfind("/")+1:] + '\n')
    urllib.urlretrieve(x , save_directory + '/' + x[x.rfind("/")+1:] )
