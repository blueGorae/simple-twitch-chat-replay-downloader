import requests 
import json
import sys


def doubleDigit(num):
    if num < 10 :
        return '0'+str(num)
    else:
        return str(num)

class DataLoader:
    
    def __init__(self, c_id) :
        self.c_id = c_id 

    def scrapChattingLog(self, v_id, isSaveFile = False):
        
        if sys.version_info[0] == 2:
            reload(sys)
            sys.setdefaultencoding('utf-8')
        
        
        videoId = v_id
        clientId = self.c_id
        
        
        nextCursor = ''
        
        params = {}
        params['client_id'] = clientId
        
        if isSaveFile : 
            f = open(videoId+".txt", 'wt')

        i = 0
        
        while True :
            if i == 0 :
                URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?content_offset_seconds=0' 
                i += 1
            else:
                URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor=' 
                URL +=  nextCursor   
                
        
            
            response = requests.get(URL, params=params)
            
            j = json.loads(response.text)
            
            for k in range(0,len(j["comments"])):
                timer = j["comments"][k]["content_offset_seconds"]
                
                timeMinute = int(timer/60)
                
                if timeMinute >= 60 :
                    timeHour = int(timeMinute/60)
                    timeMinute %= 60
                else :
                    timeHour = int(timeMinute/60)
        
                timeSec = int(timer%60)
                
                time = doubleDigit(timeHour)+':'+doubleDigit(timeMinute)+':'+doubleDigit(timeSec)
                user = j["comments"][k]["commenter"]["display_name"]
                chat = j["comments"][k]["message"]["body"]
                
                if isSaveFile : 
                    f.write('[')
                    f.write(str(time))
                    f.write(']')
                    f.write(' ')
                    f.write('<')
                    f.write(str(user))
                    f.write('>')
                    f.write(' ')
                    f.write(str(chat))
                    f.write("\n")

            if '_next' not in j:
                break
            
            nextCursor = j["_next"]
                
        f.close()
    
    
if __name__ == "__main__":
    dataloader = DataLoader(sys.argv[2])
    dataloader.scrapChattingLog(sys.argv[1], True)
    