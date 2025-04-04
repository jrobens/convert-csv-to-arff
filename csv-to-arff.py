# Converts comma separated value (CSV) files
# to Attribute-Relation File Format (ARFF).
# where 'converts' means that an arff file is created and populated with
# the csv data. The csv file is not deleted or modified.
#
# @Author Ana Avila - github.com/anaavila
# @Date December, 2016 - January, 2017
#
# Python 3.6
#
# @Description
# Simple python program that reads a csv file, selects all its attributes
# and assigns its data type ("numeric" or "nominal").
# Selects unique data values for each nominal attribute, and
# inserts a '0' on each empty cell.
#
# This program was made to facilitate some csv data cleaning when I was
# trying to open a csv file in Weka, for a school research project.
# This program helps to clean the csv file by converting it to arff format
# when the csv file has some inconsistencies, such as having numeric and
# nominal values for the same attribute values, and when it has empty cells.
#
# @About the ARFF format and Weka Software
# ARFF file format is used with Weka, a machine learning software from the
# University of Waikato. Information about the ARFF file and Weka is on the
# University of Waikato website: https://www.cs.waikato.ac.nz/ml/weka/arff.html
#
#
# Note:
# You can open the arff file with a text editor
#

import csv
import os


def csv_to_arff(fileToRead, fileToWrite, relation):
    """
    Converts a CSV file to ARFF format, handling quoted fields, empty cells in data.

    Args:
        fileToRead (str): The name or absolute path of the CSV file to read.
        fileToWrite (str): The name of the ARFF file to create.
        relation (str): The relation name for the ARFF file.
    """

    dataType = []
    columnsTemp = []
    uniqueTemp = []
    uniqueOfColumn = []
    dataTypeTemp = []
    finalDataType = []
    attTypes = []
    p = 0

    try:
        with open(fileToRead, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            allData = list(reader)
    except FileNotFoundError:
        print(f"Error: File '{fileToRead}' not found.")
        return
    except Exception as e:
        print(f"Error reading file '{fileToRead}': {e}")
        return

    attributes = allData[0]
    totalCols = len(attributes)
    totalRows = len(allData)

    # Add '0' for empty cells
    for j in range(0, totalCols):
        for i in range(0, totalRows):
            if not allData[i][j]:
                allData[i][j] = "0"

    # Handle commas, blanks, and quotes
    for j in range(0, totalCols):
        for i in range(1, totalRows):
            allData[i][j] = allData[i][j].lower()
            allData[i][j] = allData[i][j].strip(os.linesep).strip("\n").strip("\r").replace('\'', r'\'').replace('\"',
                                                                                                                 r'\"')
            try:
                float(allData[i][j])
            except ValueError:
                allData[i][j] = '"' + allData[i][j] + '"'

    # Find unique cells for nominal and numeric
    for j in range(0, totalCols):
        for i in range(1, totalRows):
            columnsTemp.append(allData[i][j])
        uniqueTemp = list(dict.fromkeys(columnsTemp))
        uniqueOfColumn.append("{" + ','.join(uniqueTemp) + "}")
        columnsTemp = []

    # Assign numeric or nominal to each cell
    for j in range(1, totalRows):
        for i in range(0, totalCols):
            try:
                float(allData[j][i])
                dataType.append("numeric")
            except ValueError:
                dataType.append("nominal")

    for j in range(0, totalCols):
        p = j
        for i in range(0, (totalRows - 1)):
            dataTypeTemp.append(dataType[p])
            p += totalCols
        if "nominal" in dataTypeTemp:
            finalDataType.append("nominal")
        else:
            finalDataType.append("numeric")
        dataTypeTemp = []

    for i in range(0, len(finalDataType)):
        if finalDataType[i] == "nominal":
            attTypes.append(uniqueOfColumn[i])
        else:
            attTypes.append(finalDataType[i])

    # Write to ARFF file
    try:
        with open(fileToWrite, 'w', encoding='utf-8') as writeFile:
            writeFile.write("%\n% Comments go after a '%' sign.\n%\n")
            writeFile.write("%\n% Relation: " + relation + "\n%\n%\n")
            writeFile.write(
                "% Attributes: " + str(totalCols) + " " * 5 + "Instances: " + str(totalRows - 1) + "\n%\n%\n\n")
            writeFile.write("@relation \"" + relation + "\"\n\n")
            for i in range(0, totalCols):
                writeFile.write("@attribute" + " '" + attributes[i] + "' " + attTypes[i] + "\n")
            writeFile.write("\n@data\n")
            for i in range(1, totalRows):
                writeFile.write(','.join(allData[i]) + "\n")

        print(f"'{fileToWrite}' was converted from '{fileToRead}'")

    except Exception as e:
        print(f"Error writing to file '{fileToWrite}': {e}")


# Example usage:
csv_to_arff("gb-data-20221124.csv", "gb-data20221124.arff", "Green Bonds")
