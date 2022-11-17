import requests
import json
import csv
import time



# Gets a username given a userId
def getUserName(id):
    apiUrl = "https://api.jikan.moe/v4/users/userbyid/" + id;
    response = requests.get(apiUrl)
    #Stores response as dictionary
    r = json.loads(response.text)
    userName = r['data']['username']
    #prints json in a redable way
    #print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ':')))
    return userName
   


# Gets user list given a username via myAnimeList API
def getUserList(userName):
    apiUrl = "https://api.myanimelist.net/v2/users/" + str("UNTAMABLEPANDA") + "/animelist?limit=1000"
    headers = {'content-type': 'application/json','X-MAL-CLIENT-ID':'48209ad5e97c8f10374115fa0105418a'}
    response = requests.get(apiUrl, headers=headers)
    #Stores response as dictionary
    r = json.loads(response.text)
    
    userIdList = []
    #gets all anime id's for a user
    print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ':')))
    for anime in r["data"]:
        userIdList.append(anime['node']['id'])     
    
    return userIdList


#get details about anime given a ID through JIKAN
#WORK ON ASYNCH AWAIT FOR THIS
def getAnimeDetails(id):
    apiUrl = 'https://api.jikan.moe/v4/anime/' + str(id)
    response = requests.get(apiUrl)
     #Stores response as dictionary
    r = json.loads(response.text)
    
   # print(json.dumps(r["data"], sort_keys=True, indent=4, separators=(',', ':')))

    with open('test.csv', 'w') as testfile:
   
        # store the desired header row as a list
        # and store it in a variable
        fieldnames = r["data"]
        parsedResponse = r["data"]
        # pass the created csv file and the header
        # rows to the Dictwriter function
        writer = csv.DictWriter(testfile, fieldnames=fieldnames)
        
        # Now call the writeheader function,
        # this will write the specified rows as
        # headers of the csv file
        writer.writeheader()

        #print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ':')))
       #takes response and put into dictionary
        demographics = fieldnames['demographics']
        genres = fieldnames['genres']
        titles = fieldnames['titles'][0]
        studio = fieldnames['studios']
        producers = fieldnames['producers']
        broadcast = fieldnames['broadcast']
        aired = fieldnames['aired']
        animeDetails = {
            "id": id,
            "title":titles,
            "score":fieldnames['score'],
            "popularity" : fieldnames['popularity'],
            "members" : fieldnames['members'],
            "favorites" : fieldnames['favorites'],
            "demographics_id":  [d['mal_id'] for d in demographics],
            "demographics" :  [d['name'] for d in demographics],
            "genresId" :  [d['mal_id'] for d in genres],
            'genreName' : [d['name'] for d in genres],
            "duration": fieldnames['duration'],
            "studioId":[d['mal_id'] for d in studio],
            "studioName" : [d['name'] for d in studio],
            "rank" : fieldnames['rank'],
            "rating": fieldnames['rating'],
            "source": fieldnames['source'],
            "status": fieldnames['status'],
            "season": fieldnames['season'],
            "scoredBy" : fieldnames['scored_by'],
            "producerId":  [d['mal_id'] for d in producers],
            "producerName":  [d['name'] for d in producers],
            "producerType":  [d['type'] for d in producers],
            "episodes" : fieldnames['episodes'],
            "airing" : fieldnames['airing'],
            "broadcastDay" : broadcast['day'],
            "broadcastTime" : broadcast['time'],
            "broadcastTimezone" : broadcast['timezone'],
            "airedFrom" : aired['from'],
            "airedTo" : aired['to'],
            "type": fieldnames['type'],
        }
       # print(json.dumps(animeDetails, sort_keys=False, indent=4, separators=(',', ':')))
        print(animeDetails)
        return animeDetails
    
        
def printToCsv(dict):
        keys = dict[0].keys()

        with open('people.csv', 'a') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            dict_writer.writerows(dict)
    
        





def main():
    # userName = getUserName("18");
    # print(userName)
    userName= "MikuOlliet"
    userList = getUserList(userName);
    
    print(userList)
    userListDetails = []

    print(userList)

    for anime in userList:
        userListDetails.append(getAnimeDetails(anime))
        time.sleep(1)
   
    for anime in userListDetails:
        print(json.dumps(userListDetails, sort_keys=False, indent=4, separators=(',', ':')))

    printToCsv(userListDetails)
   
    
        
   # getAnimeDetails(userList[0])
    #print(json.dumps(userListDetails, sort_keys=False, indent=4, separators=(',', ':')))

if __name__ == "__main__":
    main()
    
    
