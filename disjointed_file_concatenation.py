from xlwings import *
import os


directory = input("Input Master Sheet Directory: ")
os.chdir(directory)
docs = os.listdir(directory)

total_list = []

#specify column labels to check for
columnList = [['Company & Business Unit', 'Company', 'location', 'Location'],
              ['Business Unit description'],
              ['Site'],
              ['Status'],
              ['Not on Master'],
              ['Fleet Number', 'Unit #', 'UNIT', 'Unit ID', 'Unit Number'],
              ['Asset ID'],
              ['Child Number'],
              ['Hours'],
              ['KM'],
              ['Rego', 'rego', 'Regis', 'regis', 'FADL03', 'REGO'],
              ['Rego expiry', 'expiry'],
              ['Sighted', 'sighted', 'Collected', 'collected', 'captured', 'Captured'],
              ['Asset Validated in system'],
              ['Photo uploaded', 'photo', 'Photo'],
              ['Status Code JDE'],
              ['Exception Raised', 'Exception', 'exception'],
              ['Asset Amendment required'],
              ['Asset Not on Register required'],
              ['Maintenance data validated'],
              ['Preventative Maintenance Schedule Set Up'],
              ['Signed Off by Site'],
              ['Comment', 'comment'],
              ['Type', 'type', 'TYPE'],
              ['Close-out status'],
              ['Responsibility'],
              ['Action']]

for document in docs:

    #open workbook
    wbook = Workbook(directory + '\\' + document)

    #check for total encompassing range of site master
    sheetVals = Range('Asset Status', 'A1:AZ1000').value
    final = 'A1'
    finalx = 0
    finaly = 0
    for x in range(len(sheetVals)):
        for y in range(len(sheetVals[x])):
            if not sheetVals[x][y] is None:
                if x > finalx:
                    finalx = x
                if y > finaly:
                    finaly = y
    if not finaly > 25:
        final = chr(finaly + 97) + str(finalx + 1)
    else:
        final = 'A' + chr(finaly + 97 - 25) + str(finalx + 1)

    #select the values to be filtered
    sheetVals = Range('Asset Status', 'A1:' + final).value

    finalVals = []

    #build the finalVals list to be of the correct size
    for _ in range(len(sheetVals)):
        finalVals.append([])

    #init flag
    flag = False
    #filter the columns and append them to finalVals if found
    for stringset in columnList:
        flag = False
        for columnNum in range(len(sheetVals[0])):
            if not sheetVals[0][columnNum] is None:
                if flag is False:
                    for string in stringset:
                        if sheetVals[0][columnNum].find(string) != -1:
                            for rowNum in range(len(sheetVals)):
                                finalVals[rowNum].append(sheetVals[rowNum][columnNum])
                            flag = True
                            break
            if columnNum == len(sheetVals[0]) - 1 and flag is False:
                for rowNum in range(len(sheetVals)):
                        finalVals[rowNum].append('')
                        finalVals[0][len(finalVals[0])-1] = stringset[0]

    #Add the site name as a column
    for rowNum in range(len(sheetVals)):
        finalVals[rowNum].append(document[:-5])
        finalVals[0][len(finalVals[0])-1] = document[:-5]

    del(finalVals[0])

    wbook.close()
    total_list.append(finalVals)

wbook = Workbook()

index = 2
topRow = []
for group in columnList:
    topRow.append(group[0])
topRow.append('Fleet_Master')
Range('A1').value = topRow
for site in total_list:
    Range('A' + str(index)).value = site
    index += len(site)
