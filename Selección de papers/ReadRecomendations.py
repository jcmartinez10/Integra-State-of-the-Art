import json

def readPaperRecomendations:

    #process search query results going as far back as 5 years


    #For every result get first row of recommended papers

    with open('paper01s.json') as f:
      data = json.load(f)

    print(data)


    #For the papers as a whole get all references in a new list, assign score for times a paper is cited



    #Select top T number of articles
