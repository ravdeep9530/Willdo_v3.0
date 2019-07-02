import sys
import urllib.request
from include.Variable import __storagePath__
from Generic import Generic
from Json_evaluation import log
class Url:
    def callApi(filePath=__storagePath__,filename="",url="http://sussociety.cc:8080/bower_components/images/banner.jpg"):
        try:
            extn=""
            _filename=""
            extn=(url[-5:].split('.')[1])
            if filename=="":

                _filename=str(url[-10:].split('.')[0])
                _filename=_filename.replace('/','_')
                #print(_filename)
            else:
                _filename=filename

            if extn is None or extn=="":
                return "Http path is not valid!!"

            #print(filePath+"/"+_filename+"."+extn)
            _filename=Generic.prefixTimeStamp(_filename,"_")
            _filename=_filename.replace(' ','_').replace(':','.')
            fileContent = urllib.request.urlopen(url)
            with open(filePath+"/"+_filename+"."+extn,'wb') as output:
                output.write(fileContent.read())
            return str(filePath+"/"+_filename+"."+extn)
        except Exception as e:
            log("Error_Url_callApi@"+str(e))
            return "-1"
    def urlRequest(url):
        return urllib.request.urlopen(url)
