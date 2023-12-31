from json import dumps

output = open('output.txt', 'w')

listparser = ['room_number', 'capacity', 'budget', 'credits', 'salary', 'year', 'tot_cred', 'start_hr', 'start_min', 'end_min']

def transformNoSQL(columnName, columnHeader, data):
    dicData = {}

    for i in range(len(data)):
        if(columnHeader[columnName][i] in listparser):
            dicData[columnHeader[columnName][i]] = int(data[i])
        else:
            dicData[columnHeader[columnName][i]] = data[i]
    
    output.write(f"db.getCollection('{columnName}').insertOne(\n")
    output.write(dumps(dicData)+'\n')
    output.write(");\n")

    print(f"db.getCollection('{columnName}').insertOne(")
    print(dumps(dicData))
    print(";")

def readFile(columnHeader):
    arq = open("smallRelationsInsertFile.sql", "r")

    for line in arq.readlines():

        wordParser = ""
        columnName = ""
        dataParser = ""
        dataLock = False
        wordDataLock = False
        data = []

        for char in line:

            if(char == "(" or dataLock):

                wordParser += char                
                dataLock = True

                if(char == "'"):
                    if(wordDataLock):
                        wordDataLock = False
                    else:
                        wordDataLock = True

                elif(wordDataLock): 
                    dataParser += char
                elif(not wordDataLock and len(dataParser) > 0):
                    data.append(dataParser)
                    dataParser = ""


            elif(char == " " or char == ';'):
                
                if(wordParser != "insert" and wordParser != "into" and wordParser != "values"):
                    columnName = wordParser

                wordParser = ""

            else:
                wordParser += char

        transformNoSQL(columnName, columnHeader, data)

columns = {
    "classroom" : ['building', 'room_number', 'capacity'],
    "department" : ['dept_name', 'building', 'budget'],
    "course" : ['course_id', 'title', 'dept_name', 'credits'],	
    "instructor" : ['ID', 'name', 'dept_name', 'salary'],
    "section" : ['course_id', 'sec_id', 'semester', 'year', 'building', 'room_number', 'time_slot_id'],
    "teaches" : ['ID', 'course_id', 'sec_id', 'semester', 'year'],
    "student" : ['ID', 'name', 'dept_name', 'tot_cred'],
    "takes" : ['ID', 'course_id', 'sec_id', 'semester', 'year', 'grade'],
    "advisor" : ['s_ID', 'i_ID'],
    "time_slot" : ['time_slot_id', 'day', 'start_hr', 'start_min', 'end_hr', 'end_min'],
    "prereq" : ['course_id', 'prereq_id']
}

readFile(columns)
output.close()