# TODO WikiURLFactory class


# a dang dummy function!
def make_url(language, title, ):
    url = ""
    url += "http://"
    url += language 
    url += ".wikipedia.org/w/api.php?"
    url += "action=query"
    url += "&format=xmlfm"
    url += "&titles=" + title
    url += "|Talk:" + title
    #url += "&prop=info|revisions|categories|images"
    url += "&prop=images|extlinks|categories|info"

    url += "&inprop=protection"
    ## THIS DOESN"T WORK. YOU CANT USE MULTIPLE PROPS
    #url += "&prop=extlinks"
    
    #url += "&inprop=protection|url|readable|subjectid|watched" # info properties
    #url += "&rvprop=userid|ids|timestamp|user|flags|comment|size" # revision properties
    return url