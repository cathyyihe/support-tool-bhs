import csv
import os

class Arff():
    def __init__(self,fileToRead,fileToWrite):
        self.fileToRead = fileToRead  #csv file name or absolute path to be open.
        self.fileToWrite = fileToWrite   #name as how you'll save your arff file.
        self.relation = str(os.path.basename(fileToRead))[:-4] #how you'll like to call your relation as.

    def generate_arff(self):
        dataType = [] # Stores data types 'nominal' and 'numeric'
        columnsTemp = [] # Temporary stores each column of csv file except the attributes
        uniqueTemp = [] # Temporary Stores each data cell unique of each column
        uniqueOfColumn = [] # Stores each data cell unique of each column
        dataTypeTemp = [] # Temporary stores the data type for cells on each column
        finalDataType = [] # Finally stores data types 'nominal' and 'numeric'
        attTypes = [] # Stores data type 'numeric' and nominal data for attributes
        p = 0 # pointer for each cell of csv file

        writeFile = open(self.fileToWrite, 'w')

        #Opening and Reading a CSV file
        f = open(self.fileToRead, 'r')
        reader = csv.reader(f)
        allData = list(reader)
        attributes = allData[0]
        totalCols = len(attributes)
        totalRows = len(allData)
        f.close()
        # print(allData)

        # Add a '?' for each empty cell
        for j in range(0,totalCols):
            for i in range(0,totalRows):
                if 0 == len(allData[i][j]):
                    allData[i][j] = "?"

        # check for comams or blanks and adds single quotes
        for j in range(0,totalCols):
            for i in range(1,totalRows):
                allData[i][j] = allData[i][j]
                if "\r" in allData[i][j] or '\r' in allData[i][j] or "\n" in allData[i][j] or '\n' in allData[i][j]:
                    allData[i][j] = allData[i][j].rstrip(os.linesep)
                    allData[i][j] = allData[i][j].rstrip("\n")
                    allData[i][j] = allData[i][j].rstrip("\r")
 

        # fin gives unique cells for nominal and numeric
        for j in range(0,totalCols):
            for i in range(1,totalRows):
                #delete "?" in attributes section
                if not (allData[i][j]=="?" or allData[i][j]== "'?'"):
                    if " " not in allData[i][j]:
                        columnsTemp.append(allData[i][j])
                    else:
                        columnsTemp.append(str("'"+allData[i][j]+"'"))
            # print(columnsTemp)
            for item in columnsTemp:
                if not (item in uniqueTemp):
                    uniqueTemp.append(item)
            uniqueOfColumn.append("{" + ','.join(uniqueTemp) + "}")
            uniqueTemp = []
            columnsTemp = []

        # Assigns numeric or nominal to each cell
        for j in range(1,totalRows):
            for i in range(0,totalCols):
                try:
                    if "%" in allData[j][i]:
                        allData[j][i]=str(eval(allData[j][i].strip("%"))/100)
                    if " " in allData[j][i]:
                        allData[j][i]=str("'"+allData[j][i]+"'")
                    allData[j][i]=allData[j][i].strip("~!@#$^&*()_+{}|:<>`-=[]\;',./")
                    if allData[j][i]=="?" \
                            or allData[j][i]=="'?'" \
                            or allData[j][i]==""\
                            or allData[j][i] == str(float(allData[j][i]))\
                            or allData[j][i] == str(int(allData[j][i])):
                        dataType.append("numeric")
                except ValueError or SyntaxError:
                        dataType.append("nominal")

        for j in range(0,totalCols):
            p = j
            for i in range(0,(totalRows-1)):
                dataTypeTemp.append(dataType[p])
                p += totalCols
            if "nominal" in dataTypeTemp:
                finalDataType .append("nominal")
            else:
                finalDataType .append("numeric")
            dataTypeTemp = []

        for i in range(0,len(finalDataType )):
            if finalDataType[i] == "nominal":
                attTypes.append(uniqueOfColumn[i])
            else:
                attTypes.append(finalDataType[i])

                
        # Show Relation
        writeFile.write("@relation " + self.relation + "\n\n")

        # Show Attributes
        for i in range(0,totalCols):
            writeFile.write("@attribute" + " " + attributes[i] + " " + attTypes[i] + "\n")

        # Show Data
        writeFile.write("\n@data\n")
        for j in range(1,totalRows):
            for i in range(totalCols):
                if " " in allData[j][i]:
                    allData[j][i]=str("'"+allData[j][i]+"'")
            writeFile.write(','.join(allData[j])+"\n")

        # print(self.fileToRead + " was converted to " + self.fileToWrite)

# Arff("mergedcsv13.csv","mergedcsv13.arff").generate_arff()
# Arff("anatesting.csv","anatesting.arff").generate_arff()
