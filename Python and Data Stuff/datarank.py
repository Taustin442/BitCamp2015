#Rank sketchy areas in DC crime data

from sets import Set
import csv
import operator
import urllib, urllib2, json

def decode_address_to_coordinates(address):
        params = {
                'address' : address,
                'sensor' : 'false',
        }  
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' \
              + urllib.urlencode(params) + "&key=AIzaSyD3EP515KhhM_8-DynbR10EcSg8D8c7KFs"
        print url
        response = urllib2.urlopen(url)
        result = json.load(response)
        #try:
        print result['results']
        return result['results'][0]['geometry']['location']
        #except:
        #        return None
            
def buildRankMap(filename):
    rankMap = {}
    with open(filename, 'r') as infile:
        for line in infile:
            weight = float(line.strip().split(',')[0])
            crime = line.strip().split(',')[1]
            rankMap[crime] = weight
    return rankMap

def buildMethodWeightMap(filename):
    methodWeightMap = {}
    with open(filename, 'r') as infile:
        for line in infile:
            weight = float(line.strip().split(',')[0])
            method = line.strip().split(',')[1]
            methodWeightMap[method] = weight
    return methodWeightMap

def buildClusterNameMap(filename):
    clusterNameMap = {}
    with open(filename, 'r') as infile:
        for line in infile:
            number = line.strip().split(':')[0]
            places = line.strip().split(':')[1].strip().split(',')
            clusterNameMap[number] = places
    return clusterNameMap

def main():
    #print decode_address_to_coordinates("3299 14TH STREET NW, DC")
    records = {}
    crimeRankMap = buildRankMap("dataweights.txt")
    #crimeRankMap = {"SEX ABUSE": 7,
    #                "THEFT F/AUTO": 3.5,
    #                "ASSAULT W/DANGEROUS WEAPON": 8,
    #                "BURGLARY": 2,
    #                "MOTOR VEHICLE THEFT": 4,
    #                "ARSON": 5,
    #                "ROBBERY": 3,
    #                "HOMICIDE": 11,
    #                "THEFT/OTHER": 1}
    clusterNameMap = buildClusterNameMap("clusternumbers.txt")
    methodWeightMap = buildMethodWeightMap("methodweights.txt")
    
    for i in ("1", "2", "3"):
        with open("crime_incidents_201"+i+".csv", 'rb') as csvfile:
            reader = csv.reader(csvfile)
            #skip first line containing column names
            next(reader)
            data = list(reader)
            rowtitles = "CCN,REPORTDATETIME,SHIFT,OFFENSE,METHOD,LASTMODIFIEDDATE,BLOCKSITEADDRESS,BLOCKXCOORD,BLOCKYCOORD,WARD,ANC,DISTRICT,PSA,NEIGHBORHOODCLUSTER,BUSINESSIMPROVEMENTDISTRICT,BLOCK_GROUP,CENSUS_TRACT,VOTING_PRECINCT,START_DATE,END_DATE"\
                        .split(',')
            for row in data:
                ccn = row[0]
                records[ccn] = dict((y, x) for x,y in zip(row, rowtitles)) 

#    for key in crimeRankMap.keys():
#        print key + " -> " + str(crimeRankMap[key])
    test_data = {}
    for key in records.keys():
        #cluster = records[key]["NEIGHBORHOODCLUSTER"]
        cluster = records[key]["BLOCKSITEADDRESS"]
        crime = records[key]["OFFENSE"]
        method = records[key]["METHOD"]
        
        if not cluster in test_data.keys():
            test_data[str(cluster)] = 1
        else:
            try:
                test_data[str(cluster)] += methodWeightMap[method]*crimeRankMap[crime]
            except KeyError:
                print "KeyError: " + method + " " + crime
                break
    #remove empty key
    test_data.pop('', None)
    sortedSketch = sorted(test_data.items(), key=operator.itemgetter(1))

    for t in sortedSketch:
        print t
        #for place in clusterNameMap[t[0]]:
        #    print place.strip() + "," + str(t[1])
        #print str(clusterNameMap[t[0]]) + " -> " + str(t[1])
        
    #print "meow"

main()
