from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
import numpy as np
import collections
import gc

from variable import *





##################################################################################

sampleFile = "sample.json"          # name of a 4-line .json file
originalFile = "isso.json"          # name of a 10K - line .json file


timeData = []                       # a list of tuples that contain data relatives to time that reader spend
browserData = []                    # a list about browser type that have been used
browserDataSimple = []              # a list of distinct browsers
country = []                        # a list of the countries

doc_ID_sample = '140228202800-6ef39a241f35301a9a42cd0ed21e5fb0'     # initial value of document ID for the sampleFile
doc_ID_isso = '140211154215-0f1d8b14a65ebfbc5f0a9ec478d47119'       # initial value of document ID for the originalFile

##################################################################################


def retrieveData ( filename, doc_ID ):

    """ Take the file's name and the document's ID and appends all the relative data into a list. """

    data = []

    with open(filename) as f:               # Open a file in .json format

        for line in f:                      # for each line of this file

            loadedLine = json.loads(line)   # load it to a variable

            try:                            # and if he is a reader of the specified document (doc_ID parameter)
                if ( loadedLine['env_type'] == 'reader' and loadedLine['subject_doc_id'] == doc_ID ):
                    data.append(loadedLine) # append this line to a a list named data
            except:
                pass

    #print("The Number of elements are: ", len(data))

    for element in data:                    # for each element of the list that created above
        country.append((element['visitor_country']))    # Create a list of the Countries that the users have read the file




def retrieveDataBrowser ( filename ):

    """ Take the file's name and produce two lists of the Browser's names that have been used in order to read the files """

    listOfData = []             # Create an empty local list

    with open(filename) as f:   # Open the .json file

        for line in f:          # for each line of the .json file

            loadedLine = json.loads(line)   # load it to a variable

            try:
                listOfData.append(loadedLine)   # and then add this data to the local list named listOfData
            except:
                continue

    for element in listOfData:                                                          # for each element of this list
        browserData.append(element['visitor_useragent'].split()[0])                        # add the browser full name (until the first whitespace) ex. Mozilla/4.0
        browserDataSimple.append(element['visitor_useragent'].split()[0].split('/')[0])    # add the distinct type of browser name ex. Mozilla (split in '/' and take the first element




def retrieveTime (filename):

    """ Take the file's name in .json format and produce a list of tuples ( visitorID, time Spend on Reading ) """

    timeDataList = []

    with open(filename) as f:               # Open the .json file

        for line in f:                      # and for each line

            loadedLine = json.loads((line)) # load it to a variable

            try:                            # if he is a reader who has spend more than 2 seconds in page (means that he read it)
                if ( loadedLine['env_type'] == 'reader' and loadedLine['event_type'] == 'pagereadtime' ):
                    timeDataList.append(loadedLine)     # add this line to the local list
            except:
                continue


    for element in timeDataList:                                                # for each element of the local list
        timeData.append(  ( element['visitor_uuid'] , element['event_readtime'] ) )   # add all the tuples of visitor's ID and the time
                                                                                      # that each one of them has spend on reading



def displayHistoBrowser ():

    """ Display a Histogram of the number of reading proccess in docs from browsers ex. 1000 views from Mozilla/5.0 """

    num = 0

    d = { x : num for x in browserData }        # Create a dictionary with keys all the types of browsers and values initialized to zero

    for i in range(len(browserData)):           # for each appearance of a browser type, add one to his value in the dictionary above
        d[browserData[i]] += 1

    plt.barh( range(len(d)), list(d.values()), align='center', alpha=0.2 )      # Plot the horizontal bar chart using the keys and the values from the dictionary
    plt.yticks(range(len(d)), list(d.keys()))                                   # add labels to the charts

    plt.show()         # show the chart


def displayHistoBrowserSimple ():

    """ Display a Histogram of the number of reading proccess in docs from distinct browsers ex. 1000 views from Mozilla """

    num = 0

    d = { x : num for x in browserDataSimple}   # Create a dictionary with keys all the types of distinct browsers and values initialized to zero

    for i in range(len(browserDataSimple)):     # for each appearance of a distinct browser type, add one to his value in the dictionary above
        d[browserDataSimple[i]] += 1

    plt.barh( range(len(d)), list(d.values()), align='center', alpha=0.2 )  # Plot the horizontal bar chart using the keys and the values from the dictionary
    plt.yticks(range(len(d)), list(d.keys()))                               # add labels to the charts

    plt.show()           # show the chart




def displayHistoTime ():

    """ Display the top 10 reader's IDs with their time on spending reading docs """

    num = 0
    e = [ e[0] for e in timeData ]      # create a list of user IDs that have spend time on reading docs
    d = { x: num for x in e }           # create a dictionary using those IDs as keys with initial value to zero

    for i in range(len(timeData)):      # for each ID add his time spend for reading (for every doc)
        d[timeData[i][0]] += timeData[i][1]     # the second element of timeData is the time
                                                # and the first one is the user id

    a = sorted(d.items(), key=lambda kv: kv[1], reverse=True)       # sort this dictionary by value in reverse order
    top10List = []


    for i in range(10):                 # and create the top-10 list
        top10List.append(a[i])



    top10 = "           Reader                  Time\n\n"

    for i in range(len(top10List)):        # Create the string that will be printed
        top10 += str(top10List[i][0])
        top10 += "          "
        top10 += str(top10List[i][1])
        top10 += "\n"

    messagebox.showinfo( "Top-10 Readers", top10 )      # show the result in a messagebox






def displayHistoCountries():

    """ Display a Histogram of the number of visitors per country to a specific document """

    num = 0

    d = { x : num for x in country }        # Create a dictionary of the countries with values initialized to zero

    for i in range(len(country)):           # for each country view on a doc, add one more on its dictionary value
        d[country[i]]+=1


    plt.barh( range(len(d)), list(d.values()), align='center', alpha=0.2, color='g' )   # Plot the horizontal bar chart using the keys and the values from the dictionary
    plt.yticks(range(len(d)), list(d.keys()))       # Add labels to the values

    plt.show()      # Show the Histogram



def displayHistoContinents ():

    """ Display a Histogram of the number of visitors per Continent to a specific document """

    continets = ['AF', 'AS', 'EU', 'NA', 'SA', 'OC', 'AN']      # Create a list of the Continents
    num = 0

    d = { x : num for x in continents }                         # Create a dictionary of the continents with initial value to zero

    for i in range(len(country)):                               # for each country appearance
        d[cntry_to_cont[country[i]]] += 1                       # map the country to the continent using the given dictionary
                                                                # and add one reading appearance to the dictionary above

    plt.barh(range(len(d)), list(d.values()), align='center', alpha=0.2, color='r')     # Plot the horizontal bar chart using the keys and the values from the dictionary
    plt.yticks(range(len(d)), list(d.keys()))                   # Add labels to the values


    plt.show()              # Show the Histogram




def docToVisitor( filename, docID ) :

    """ Take the .json file's name and the document ID and return a list of distinct visitors to this document """

    visitorsList = []
    visitors = []

    with open(filename) as f:                   # Open the .json file

        for line in f:                          # For each line of the file

            loadedLine = json.loads((line))     # Load the line to a local var

            try:                                # and if he is a reader of the specified Document ID
                if ( loadedLine['env_type'] == 'reader' and loadedLine['subject_doc_id'] == docID ):
                    visitors.append(loadedLine) # add his info to the local list visitors
            except:
                pass

    for element in visitors:                    # for each element of the visitor List
        visitorsList.append( element['visitor_uuid'] )      # add his user ID to the visitorList


    return list(set(visitorsList))              # return a list of the distinct visitor ids that have read this document ID




def visitorToDoc( filename, visitorID ) :

    """ Take the .json file's name and the visitor ID and return a list of distinct documents that have been read from this user """

    docList = []
    docs = []

    with open(filename) as f:               # Open the .json file

        for line in f:                      # For each line of the file

            loadedLine = json.loads((line)) # Load it to a local var

            try:                            # If he is a reader with the specified id
                if ( loadedLine['env_type'] == 'reader' and loadedLine['visitor_uuid'] == visitorID ):
                    docs.append(loadedLine) # add this line to the docs list
            except:
                pass

    for element in docs:                    # for each element of the docs list
        docList.append( element['subject_doc_id'] )     # add the id of the documents that he has read in docList


    return list(set(docList))               # Return a distinct doc version of this list




def distinctVisitors( filename ):

    """ Create a List of the distinct visitors of all the .json file """

    visitors = []
    distinctVisitor = []

    with open(filename) as f:

        for line in f:

            loadLine = json.loads(line)

            try:
                visitors.append(loadLine)
            except:
                pass


    for i in range(len(visitors)):
        distinctVisitor.append( visitors[i]['visitor_uuid'] )


    return list(set(distinctVisitor))




def distinctDocs( filename ):

    """ Create a List of the distinct documents that exist in the .json file """

    docs = []
    distinctDocList = []

    with open(filename) as f:

        for line in f:

            loadLine = json.loads(line)

            try:
                if( loadLine['event_type'] ==  'pageread' ):
                    docs.append(loadLine)
            except:
                pass


    for i in range(len(docs)):
        distinctDocList.append( docs[i]['subject_doc_id'] )


    return list(set(distinctDocList))






def sortDocuments( dicDocs ):

    a = sorted(dicDocs.items(), key=lambda kv: kv[1], reverse=True)  # sort this dictionary by value in reverse order
    top10List = []

    for i in range(10):  # and create the top-10 list
        top10List.append(a[i])

    top10 = "              Document ID                  -----                     Number of Readers\n\n"

    for i in range(len(top10List)):  # Create the string that will be printed
        top10 += str(top10List[i][0])
        top10 += "          "
        top10 += str(top10List[i][1])
        top10 += "\n"

    messagebox.showinfo("Top-10 Readers", top10)  # show the result in a messagebox


def alsoLike( sortDocuments ):

    readDoc = 0
    reader = 0

    distinctVisitorList = distinctVisitors(originalFile)
    distinctDocList = distinctDocs(originalFile)

    dicReader = { x: reader for x in distinctVisitorList }
    dicDocs   = { x: readDoc for x in distinctDocList }

    messagebox.showinfo("Message to the User", "Please Wait ... about two minutes!!!\n\n[ Intel Core i7 @ 2.60 GHz]\n\nThen an another message box will provide you your request!")


    for i in range(len(distinctVisitorList)):
        dv = visitorToDoc( originalFile, distinctVisitorList[i] )
        try:
            for visitorID in dv:
                dicDocs[visitorID] += 1
        except:
            pass


    sortDocuments(dicDocs)








def retriveJSON ( id ):

    """ Retrieve all needed data from the JSON file """

    global timeData
    global browserData
    global browserDataSimple
    global country

    timeData = []               # Initializes the global variables
    browserData = []
    browserDataSimple = []
    country = []

    doc_ID_isso = id            # Set the new Document ID

    retrieveData(originalFile, doc_ID_isso)     # Retrieve all relative Data from the .json file
    retrieveDataBrowser(originalFile)
    retrieveTime(originalFile)




if __name__ == '__main__':


    retriveJSON(doc_ID_isso)


    root = Tk()

    root.title("Document Tracker")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    ttk.Button(mainframe, text="Country Histo", command=displayHistoCountries).grid(column=1, row=1)
    ttk.Button(mainframe, text="Continents Histo", command=displayHistoContinents).grid(column=1, row=2)

    ttk.Button(mainframe, text="Browser (Full)", command=displayHistoBrowser).grid(column=2, row=1)
    ttk.Button(mainframe, text="Browser (Distinct)", command=displayHistoBrowserSimple).grid(column=2, row=2)

    ttk.Button(mainframe, text="Top-10 Readers", command=displayHistoTime).grid(column=3, row=1)


    ttk.Label(mainframe, text="Document ID: ").grid(column=1, row=3, sticky=E)

    entry = Entry(mainframe, width=35, textvariable=doc_ID_isso)
    entry.grid(column=2, row=3, sticky=W)


    ttk.Button(mainframe, text="Update Data SET", command=lambda: retriveJSON(entry.get())).grid(column=3, row=3)


    ttk.Button(mainframe, text="Top10 Docs Readed", command=lambda: alsoLike(sortDocuments)).grid(column=3, row=4)


    for child in mainframe.winfo_children(): child.grid_configure(padx=30, pady=30)

    root.mainloop()


    collected = gc.collect()
    print( "Garbage collector: collected %d objects." % (collected) )