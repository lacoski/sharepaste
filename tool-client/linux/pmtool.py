#! /usr/bin/python3

import requests
import sys, getopt

PART_TO_API = "/userzone/create_tool_guest/"
# print("This is the name of the script: ", sys.argv[0])
# print("This is the name of the script: ", sys.argv[1])
# print("This is the name of the script: ", sys.argv[2])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))

def main():
    if sys.stdin.isatty():
        print('Fail - Content null')
        print('Ex: cat `<file>` | python3 pmtool.py `<URL>` `<PORT>`')
        sys.exit(0)
    elif len(sys.argv) < 2:
        print('Fail - argv not found')
        print('Ex: cat `<file>` | python3 pmtool.py `<URL>` `<PORT>`')
        sys.exit(0)
    elif not sys.argv[1]:
        print('Fail - null URL')
        print('Ex: cat `<file>` | python3 pmtool.py `<URL>` `<PORT>`')
        sys.exit(0)
    elif not sys.argv[2]:
        print('Fail - null Port')
        print('Ex: cat `<file>` | python3 pmtool.py `<URL>` `<PORT>`')
        sys.exit(0)

    URL = "http://{0}:{1}{2}".format(sys.argv[1], sys.argv[2], PART_TO_API])

    content=''
    for line in sys.stdin:        
        content += line

    data = {
            'paste_name': 'Up from PMtool',
            'content_paste':content,        
            'type_content_paste':'BASH',
            }

    r = requests.post(URL, data = data)
    pasteme_url = r.text
    print("Pastebin Short link is: {0}".format(pasteme_url))
    # sudo cp pmtool.py /usr/local/bin/pmtool

if __name__ == "__main__":
    main()
