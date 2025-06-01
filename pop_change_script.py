"""Using arcpy to calculate population change based on user specifications"""
#Goals: 1. List all numerical fields from file for user to choose, 2. process input and compute total value of selected field, 
#maximum value of selected field, average value of selected field, return results to user, 3. calculate percent population change 
#from 2000 to 2010 for each state, if necessary create population change field,  add values to this field

#importing libraries
import arcpy 

#setting workspace
arcpy.env.workspace= "C:\\Users\\kfear\\Python"

#allowing overwriting of exisiting files
arcpy.env.overwriteOutput=True

#Goal 1. List all numerical fields from file for user to choose

#import and shapefile
statesFile="states2010.shp"

#find all numerical fields and make them into a list
numFlds=arcpy.ListFields(statesFile, '','Double')+ arcpy.ListFields(statesFile, '','Integer')+  arcpy.ListFields(statesFile, '','Float')

#ask user which one they want
count=0
for aFld in numFlds:
    print(count, aFld.name)
    count +=1
choice= int(input("Please choose a field by typing the number of the field: \n"))

#create cursor for the chosen field
numeric_field_search=arcpy.da.SearchCursor(statesFile,[numFlds[choice].name])

#Goal 2. process input and compute total value of selected field, 
#maximum value of selected field, average value of selected field, return results to user
# compute total value of this field
# compute max value of field
# get average of field
total=0
maximum=-999 #do this incase the value is negative
avgcount=0
for aRow in numeric_field_search:
    value= aRow[0]
    total +=value
    avgcount+=1
    if value > maximum:
        maximum = value

avg=total/avgcount

#return results to the user
print("The sum of the field is:",total)
print("The maximum value of the chosen field is", maximum)
print("The average value of the chosen field is", avg)

#Delete cursor
del numeric_field_search

#Goal 3. calculate percent population change from 2000 to 2010 for each state, if necessary create population change field,  add values to this field

#check if popchg field exists or not, delete if it does
for aFld in numFlds:
    if aFld.name=="popchg":
        print("Popchg field already exists, deleting it now")
        arcpy.DeleteField_management(statesFile,["popchg"])

#Create population change field
arcpy.AddField_management(statesFile,"popchg","Double","10","3")

#Calculate percentage pop change and add the value to the pop change field 
pop_chg_update_cursor=arcpy.da.UpdateCursor(statesFile, ["POP2000", "POP2010", "popchg"])
for aRow in pop_chg_update_cursor:
    pop2000=aRow[0]
    pop2010=aRow[1]
    popchg=(pop2010-pop2000)/pop2000*100
    aRow[2]=popchg
    pop_chg_update_cursor.updateRow(aRow)

#Delete cursor
del pop_chg_update_cursor
