#!/usr/bin/python
#coding: utf8
##
##-----------------##
## ANALYSER MODULE #############################################################
##-----------------##
## -> Extract information from a selection of articles
##
##
## TODO:
##  - centralize functions that fetch information online => [DONE]
##  - centralize functions that fetch information from articles pdf => [DONE]
##  - centralize functions that display informations as figures
##  - Write new CLI header
##  - implement GUI
##


##-------------##
## IMPORTATION ##
##-------------##
import online_retrieval
import local_retrieval
import figure_generation
















def main(argv):
	##
	## The main function, called when the script
	## is executed.
	##
	## -> parse command line arguments and run
	## 	  BIBOT
	##
    ## => USE FOR DEV
    ##


    ## Header
    print "===== BIBOT FULL VERSION 1.0 ======="
    print "|       ___  _ ___  ____ ___       |"
    print "|       |__] | |__] |  |  |        |"
    print "|       |__] | |__] |__|  |        |"
    print "|                                  |"
    print "==================================="


    ## importation
    import glob
    import pickle

    ## parameters
    online_test = False
    local_test = False
    test_figure = True


    ## online retrieval test
    if(online_test):
        test_pmid = [20824298,8578965,26231345,26253095,9023703,18576343,1496164
        ,1972576,8531373,15328883,10827414,2229518,1983326,7541811,16578972,17695193
        ,26494586,11296454,15485020,9627951,24943141,24097316,23158630,22766054
        ,8056476,16503880]


        pmid_to_info = {}
        for pmid in test_pmid:
            truc = online_retrieval.get_meta_information(pmid)
            pmid_to_info[pmid] = truc

            print truc['institution']


            """
            print "[+] => "+str(pmid)
            truc = online_retrieval.article_accessibility(pmid)
            for item in truc:
                print "\t-> "+str(item)
            """
        pickle.dump(pmid_to_info, open("meta_information.pkl", "wb"))


    ## local retrieval test
    if(local_test):

        articles_pdf = glob.glob("pdf_test/*.pdf")

        for pdf_file in articles_pdf:
            #local_retrieval.convert_pdf_to_text(pdf_file)
            text_file = pdf_file.replace(".pdf", ".txt")

            try:
                truc = local_retrieval.get_number_of_patients_from_article(text_file)
                print truc
            except:
                pass

    ## test figure generation
    if(test_figure):
        meta = pickle.load(open("meta_information.pkl", "rb" ))

        """
        figure_generation.plot_publication_evolution(meta)
        figure_generation.plot_country_repartition(meta)
        figure_generation.plot_article_type(meta)
        figure_generation.plot_keyword_repartition(meta)
        """

        figure_generation.generate_meta_table(meta)



if __name__ == '__main__':

    import sys
    main(sys.argv[1:])
