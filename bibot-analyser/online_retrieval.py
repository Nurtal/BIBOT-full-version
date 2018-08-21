#!/usr/bin/python
#coding: utf8


##
## => Retrieve information online
##
## -> Use pmid to retrieve informations
## from the pubmed database through the Bio.Entrez API
##
## -> Parse html page from the ncbi to find links to
## external resources
##
## TODO:
##  -> Break the dependence to the Bio.Entrez lib
##


def get_meta_information(pmid):
    """
    -> Parse meta data of the article to get the
        - title
        - journal
        - date
        - author list
        - article type
        - institution
        - Abstract
        - Country journal
        - Language
        - Keywords

    -> return a dictionnary with meta information

    -> TODO:
        optimisation of the institution extraction
    """

    ## importation
    from Bio import Entrez
    from Bio.Entrez import efetch, read

    ## parameters
    Entrez.email = 'murlock.raspberypi@gmail.com'
    title = "NA"
    journal = "NA"
    date = "NA"
    author_list = "NA"
    article_type = "NA"
    institue = "NA"
    language = "NA"
    abstract = "NA"
    keywords = "NA"
    journal_country = "NA"
    meta_information = {}

    ##-------------##
    ## Access data #############################################################
    ##-------------##

    ## Parse XML response #----------------------------------------------------#
    handle = efetch(db='pubmed', id=pmid, retmode='xml', )
    xml_data = read(handle)
    article_data = xml_data['PubmedArticle'][0]['MedlineCitation']["Article"]
    publication_data = xml_data[u'PubmedArticle'][0][u'MedlineCitation']

    ## Get the article type #--------------------------------------------------#
    try:
        article_type = article_data['PublicationTypeList'][0]
    except:
        pass

    ## get the article title #-------------------------------------------------#
    try:
        title = article_data['ArticleTitle']
    except:
        pass

    ## get the publication language #------------------------------------------#
    try:
        language = article_data['Language']
    except:
        pass

    ## get the journal country #-----------------------------------------------#
    try:
        journal_country = publication_data[u'MedlineJournalInfo'][u'Country']
    except:
        pass

    ## get the list of keywords #----------------------------------------------#
    try:
        keywords = publication_data[u'KeywordList']
        if(len(keywords) == 0):
            keywords = "NA"
    except:
        keywords = "NA"
        pass

    ## get the abstract #------------------------------------------------------#
    try:
        abstract = article_data['Abstract']['AbstractText'][0]
    except:
        pass

    ## get the date #----------------------------------------------------------#
    if(len(article_data['ArticleDate'])> 0):
        date_data = article_data['ArticleDate'][0]
        date = str(date_data['Day'])+"/"+str(date_data['Month'])
        date += "/"+str(date_data['Year'])
    else:
        try:
            date_data = article_data['Journal']['JournalIssue']['PubDate']
            date = str(date_data['Year'])
        except:
            pass

    ## get the institute #-----------------------------------------------------#
    try:
        institue =  article_data['AuthorList'][0]['AffiliationInfo']
        institue = institue[0]['Affiliation']
    except:
        institue = "NA"
        pass

    ## get the list of author #------------------------------------------------#
    try:
        author_data = article_data['AuthorList']
        author_list = ""
        for author in author_data:
            try:
                author_list += author['LastName']+" "+author['Initials']+", "
            except:
                pass
        author_list = author_list[:-2]
    except:
        pass

    ## get the journal name #--------------------------------------------------#
    try:
        journal = article_data['Journal']['Title']
    except:
        pass


    ##-----------------------##
    ## structure information ###################################################
    ##-----------------------##
    meta_information['title'] = title
    meta_information['journal'] = journal
    meta_information['date'] = date
    meta_information['author_list'] = author_list
    meta_information['article_type'] = article_type
    meta_information['institution'] = institue
    meta_information['language'] = language
    meta_information['asbtract'] = abstract
    meta_information['keywords'] = keywords
    meta_information['journal_country'] = journal_country

    ## return information
    return meta_information





def article_accessibility(pmid):
    """
    -> Scan the web page corresponfing
    to the pmid entry on the ncbi server,
    find where the full article can be retrieve
    (url link) and return the list of url found.
    """

    ## importation
    import requests
    from bs4 import BeautifulSoup
    import re

    ## parameters
    external_sources = []
    target_url = "https://www.ncbi.nlm.nih.gov/pubmed/?term="+str(pmid)

    ## Get links from the
    ## Full Text Sources part of the web page
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    match_external_r = re.search('<h4>Full Text Sources</h4><ul>(.+)</a></li></ul><h4>Medical</h4>', r.text)
    if(match_external_r):
        r_list = match_external_r.group(1)
        links = re.findall('href=\"http[s]{0,1}://.{2,180}\" ref=', r_list)
        for elt in links:
            source = elt.replace("\" ref=", "")
            source = source.replace("href=\"", "")
            external_sources.append(source)

    return external_sources
