import os
from django.conf import settings

def writeToFile(contentFile, short_link):
    get_file = os.path.join(settings.MEDIA_ROOT, short_link)
    file = open(get_file,'w')    
    file.write(contentFile) 
    file.close() 
    return True

def readFile(short_link):
    get_file = os.path.join(settings.MEDIA_ROOT, short_link) 
    file = open(get_file,'r')
    content= file.read()
    file.close() 
    return content