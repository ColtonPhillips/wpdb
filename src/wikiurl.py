# TODO WikiURLFactory class


# a dang dummy function!
def make_url(language, title, ):
    url = "http://" + language + ".wikipedia.org/w/api.php?action=query&format=xmlfm&titles=" + title + "&prop=info|revisions|categories&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size"
    return url