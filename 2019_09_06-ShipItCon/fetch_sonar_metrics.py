import urllib, json, sys

class Info:
    def __init__(self, path, coverage, issues):
        print("Made Item" + path)
        self.path = path
        self.coverage = coverage
        self.issues = issues
        
def getSonarInfo(path, sonarInfo):
    print("Getting info for " + path)
    return sonarInfo.get(path)

## -- Update for your needs -- ##
projectKey = "org.yamcs:yamcs" # from sonar bottom right of project home page
churn_file_name = "code_churn.csv" # result from running code maat on svn
output_file_name = "output.csv" # output file name

print ("Getting Sonar Info for " + projectKey )

sonarInfo = {}
npages = -1
i = 1
while ((i < npages) or (npages = -1) :
     response = urllib.urlopen("https://sonarcloud.io/api/measures/component_tree?component=" +  + "&metricKeys=coverage,violations&additionalFields=metrics&p=" + str(i))
	 i = i + 1
     response = json.loads(response.read())
	 if(npages == -1):
		paging = response.get("paging")
		total = paging.get("total")
		pageSize = paging.get("pageSize")
		npages = (total//pageSize) + 1
     components = response.get("components")
     print (str(len(components)))
     for item in components :
         path = item.get("path")
         print(path)
         if not(("test" in path) or ("Test"in path)):
             measures = item.get("measures")
             issues = 0
             coverage = 0
             for measure in measures :
                 value = measure.get("value")
                 metric = measure.get("metric")
                 if metric=="violations" :
                    issues = value
                 else :
                    coverage = value
             sonarInfo[path] = Info(path, coverage, issues)
        
print ("Finished Getting Sonar Info for " + str(len(sonarInfo)) + " items")
    

output_file = open(output_file_name, mode='a+')
changes_file = open(churn_file_name,"r").readlines()
for line in changes_file : 
    if((".java" in line) and not("test" in line)) :
        splitLine = line.split(",")
        file = splitLine[0]
        info = getSonarInfo(file,sonarInfo)
        if(info) :
            out = file + "," + splitLine[1] + "," + splitLine[2] + "," + str(info.coverage) + "," + str(info.issues) + "\n"
            output_file.write(out)