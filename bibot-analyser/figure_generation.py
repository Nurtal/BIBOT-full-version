#!/usr/bin/python
#coding: utf8


##
## => Generate tables and figures at different format
##
##
##
## TODO:
##  -> plot publication evolution over time => [DONE]
##  -> plot country repartition (journal) => [DONE]
##  -> plot publication type repartition => [DONE]
##  -> plot keyword repartition => [DONE]
##  -> Generate big table => [DONE]
##  -> Generate html report => [DONE]
##
##  -> Generate pdf report
##  -> Generate latex report
##  -> plot country repartition (author)
##  -> plot keywords by country
##
##
##  -> check usage condition for each visualisation lib
##



def plot_publication_evolution(meta_information):
    """
    plot evolution of the number of publication
    over time
    """

    ## importation
    import matplotlib.pyplot as plt

    ## parameters
    year_to_nb_of_articles = {}

    ## Select information from
    ## meta information
    for pmid in meta_information.keys():
        date = meta_information[pmid]['date']
        if(str(date) != "NA" and len(date) >= 4):
            date = date[-4:]
            if(date not in year_to_nb_of_articles):
                year_to_nb_of_articles[date] = 1
            else:
                year_to_nb_of_articles[date] += 1

    ## Generate and save figure
    plt.bar(year_to_nb_of_articles.keys(), year_to_nb_of_articles.values(),
            color='b',
            align='center',
            width=0.3)
    plt.xticks(rotation=45)
    plt.savefig("images/time_evolution.png")
    plt.close()



def plot_country_repartition(meta_information):
    """
    Plot a pie chart with the repartition of
    journal's country
    """

    ## importation
    import matplotlib.pyplot as plt

    ## parameters
    country_to_nb_of_articles = {}

    ## Select information from
    ## meta information
    for pmid in meta_information.keys():

        country = meta_information[pmid]['journal_country']
        if(str(country) != "NA"):
            if(country not in country_to_nb_of_articles):
                country_to_nb_of_articles[country] = 1
            else:
                country_to_nb_of_articles[country] += 1

    ## Generate Pie chart
    plt.figure(1, figsize=(6,6))
    labels = country_to_nb_of_articles.keys()
    fracs = country_to_nb_of_articles.values()
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.savefig("images/country_repartition.png")
    plt.close()



def plot_article_type(meta_information):
    """
    Plot a pie chart with the repartition of
    article type
    """

    ## importation
    import matplotlib.pyplot as plt

    ## parameters
    type_to_nb_of_articles = {}

    ## Select information from
    ## meta information
    for pmid in meta_information.keys():

        type = meta_information[pmid]['article_type']
        if(str(type) != "NA"):
            if(type not in type_to_nb_of_articles):
                type_to_nb_of_articles[type] = 1
            else:
                type_to_nb_of_articles[type] += 1

    ## Generate Pie chart
    plt.figure(1, figsize=(6,6))
    labels = type_to_nb_of_articles.keys()
    fracs = type_to_nb_of_articles.values()
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.savefig("images/article_type_repartition.png")
    plt.close()


def plot_keyword_repartition(meta_information):
    """
    Plot keyword repartition in a pie chart
    """

    ## importation
    import matplotlib.pyplot as plt

    ## parameters
    keywords_to_nb_of_articles = {}

    ## Select information from
    ## meta information
    for pmid in meta_information.keys():
        keywords = meta_information[pmid]['keywords']

        if(len(keywords) > 0 and str(keywords) != "NA"):
            for word in keywords[0]:

                if(word not in keywords_to_nb_of_articles.keys()):
                    keywords_to_nb_of_articles[word] = 1
                else:
                    keywords_to_nb_of_articles[word] += 1

    ## Generate and save figure
    plt.figure(1, figsize=(6,6))
    labels = keywords_to_nb_of_articles.keys()
    fracs = keywords_to_nb_of_articles.values()
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.savefig("images/keywords_repartition.png")
    plt.close()



def generate_meta_table(meta_information):
    """
    IN PROGRESS
    """

    ## parmaeters
    table_file = open("table_file.tsv", "w")

    ## Get the header
    header = "pmid\ttitle\tauthors\tinstitution\tdate\tjournal\tcountry\tlanguage\n"

    ## get data
    text = ""
    for pmid in meta_information.keys():
        line = str(pmid)+"\t"+meta_information[pmid]['title']+"\t"
        line += meta_information[pmid]['author_list']+"\t"
        line += meta_information[pmid]['institution']+"\t"
        line += meta_information[pmid]['date']+"\t"
        line += meta_information[pmid]['journal']+"\t"
        line += meta_information[pmid]['journal_country']+"\t"
        line += meta_information[pmid]['language'][0]+"\n"
        text += line
    text = text[:-1]

    ## write data into file
    table_file.write(header.encode('utf8'))
    table_file.write(text.encode('utf8'))
    table_file.close()





def write_html_report(meta_information):
    """
    => Write a html report from meta information
        - Generate and plot figures
    => TODO:
        - use to debug online retrieval (specific information retrieval)
        - Add some javascript
        - Paillettes
    """

    ##------------------##
    ## Generate Figures ########################################################
    ##------------------##
    plot_publication_evolution(meta_information)
    plot_country_repartition(meta_information)
    plot_article_type(meta_information)
    plot_keyword_repartition(meta_information)


    ##--------------##
    ## Write Report ############################################################
    ##--------------##
    report_file = open("report.html", "w")
    report_file.write("<html>\n")
    report_file.write("<head>\n\t<title>BIBOT</title>\n</head>\n")
    report_file.write("<body>\n")
    report_file.write("\t<h1>BIBOT analyser</h1>\n")

    ## include Figures
    report_file.write("\t<img src=\"images/time_evolution.png\">\n")
    report_file.write("\t<img src=\"images/country_repartition.png\">\n")
    report_file.write("\t<img src=\"images/keywords_repartition.png\">\n")
    report_file.write("\t<img src=\"images/article_type_repartition.png\">\n")

    ## write table
    report_file.write("<table>\n")
    report_file.write("<tr>\n")
    report_file.write("<th>PMID</th>\n")
    report_file.write("<th>Title</th>\n")
    report_file.write("<th>Date</th>\n")
    report_file.write("<th>Authors</th>\n")
    report_file.write("<th>Journal</th>\n")
    report_file.write("<th>Journal Country</th>\n")
    report_file.write("<th>Languages</th>\n")
    report_file.write("<th>Article Type</th>\n")
    report_file.write("<th>Institutions</th>\n")
    report_file.write("<th>Keywords</th>\n")
    report_file.write("</tr>\n")

    for pmid in meta_information.keys():
        information = meta_information[pmid]

        language = ""
        if(information['language'] != "NA"):
            for elt in information['language']:
                language += str(elt)+","
            language = language[:-1]

        keywords = ""
        if(information['keywords'] != "NA"):
            for elt in information['keywords'][0]:
                keywords += elt +","
            keywords = keywords[:-1]

        report_file.write("<tr>\n")
        report_file.write("<td>"+str(pmid)+"</td>\n")
        report_file.write("<td>"+information['title'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['date'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['author_list'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['journal'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['journal_country'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+language.encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['article_type'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+information['institution'].encode('utf8')+"</td>\n")
        report_file.write("<td>"+keywords.encode('utf8')+"</td>\n")
        report_file.write("</tr>\n")
    report_file.write("</table>\n")

    report_file.write("</body>\n")
    report_file.write("</html>")
    report_file.close()
