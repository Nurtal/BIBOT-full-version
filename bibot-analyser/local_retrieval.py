#!/usr/bin/python
#coding: utf8


##
## => Retrieve information from local pdf file
##
## -> Convert pdf to text
##
## -> Parse information directly from text
##
## TODO:
##  -> Break the dependence to the pdf converter library
##




def convert_pdf_to_text(pdf_file):
    """
    Extract text from a pdf file and save it
    in a text file.

    use textract module, a lot of dependencies are
    needed to install this stuff.
    """

    ## importation
    import textract

    ## parameters
    output_file_name = pdf_file.split(".")
    output_file_name = output_file_name[0]+".txt"

    ## conversion
    try:
        text = textract.process(pdf_file)
        txt_file = open(output_file_name,"w")
        txt_file.write(text.decode('ascii','ignore'))
        txt_file.close()
        print "[*] "+str(pdf_file) +" converted"
    except:
        print "[!] Can't read "+str(pdf_file)



def get_number_of_patients_from_article(article_file):
    """
    => Get number of patients describe in artcile.
        can be tricky, use results with caution.

    IN PROGRESS

    """

    ## importation
    import nltk
    import re
    import operator

    ## parameters
    number_of_patients = "NA"
    count_to_match = {}

    full_text = ""
    recording = True
    pass_the_reference = False
    text_data = open(article_file, "r")
    for line in text_data:
        line = line.rstrip()
        line = line.decode('utf8')

        ## Try to exlude Fig legend
        fig_match = re.search("^Fig\. \d", line)
        if(fig_match):
            recording = False
        else:
            recording = True

        if(line != "" and recording and not pass_the_reference):
            full_text += line +" "

        ## Try to catch the Bib reference part and
        ## not include it in full text
        if(re.search('^REFERENCES|[Rr]eferences', line)):
            recording = False
            pass_the_reference = True
    text_data.close()

    ## play with nltk
    full_text = full_text[:-1]
    tokens = nltk.word_tokenize(full_text)
    global_text = nltk.Text(tokens)
    #global_text.concordance('921', lines=75, width=150)


    ##-----------------------##
    ## CASE REPORT DETECTION ##
    ##-----------------------##
    ## i.e deal with one patient
    case_report_match = False
    case_report_match_1 = re.search('[W,w]{1}e (report|present){1} (a|the){1} case', full_text)

    ## carreful with this stuff
    ## have to control the stuff, if only this case is True
    ## then assume we've got only one patient but otherwise give priority
    ## to more robust pattern.
    case_report_match_2 = re.search('[A,a]{1} [0-9]{1,2}-year[s]{0,1}-old (\w+)', full_text)

    case_report_match_list = [case_report_match_1, case_report_match_2]
    for match in case_report_match_list:
        if(match):
            number_of_patients = 1
            case_report_match = True

    ## Detect False case match (i.e multiple case in the same paper)
    false_case_match = re.findall('([P,p]atient|[C,c]ase) [0-9]{1} [A,a]{1} [0-9]{1,2}-year[s]{0,1}-old (\w+)', full_text)
    if(false_case_match):
        count = 0
        for match in false_case_match:
            count += 1
        if(count not in count_to_match.keys()):
            count_to_match[count] = 1
        else:
            count_to_match[count] += 1

        case_report_match = False



    ##----------------------------##
    ## MULTIPLE PATIENT DETECTION ##
    ##----------------------------##
    ## Beat case report, if we trigger the two
    ## detection, prefer the largest number of patient
    ## (more chance to catch by accident detail on one patient among
    ## a large study than miss catch large number of patient in a case report)


    multiple_patient_match_1 = re.search('([0-9]{1,4}) [P,p]atients', full_text)
    if(multiple_patient_match_1):
        for match in re.findall('([0-9]{1,4}) [P,p]atients', full_text):
            if(match not in count_to_match.keys()):
                count_to_match[match] = 1
            else:
                count_to_match[match] += 1

    multiple_patient_match_3 = re.findall(' ([0-9]{1,4}) \w+ ([P,p]atients|[C,c]ases)', full_text)
    if(multiple_patient_match_3):
        for match in multiple_patient_match_3:
            if(match[0] not in count_to_match.keys()):
                count_to_match[match[0]] = 1
            else:
                count_to_match[match[0]] += 1

    ## try to catch values from other studies
    ## TODO : work on the REGEX, capture more than one word between the
    ## bib reference and the number of patients
    false_multiple_match = re.search('[R,r]ecent (study|studies) \[.{1,3}\] \w+ ([0-9]{1,4}) ([P,p]atients|[C,c]ases)', full_text)
    if(false_multiple_match):
        for match in re.findall('[R,r]ecent (study|studies) \[.{1,3}\] \w+ ([0-9]{1,4}) ([P,p]atients|[C,c]ases)', full_text):
            if(match[1] in count_to_match.keys() and count_to_match[match[1]] > 0):
                count_to_match[match[1]] -= 1

    false_multiple_match_2 = re.findall('and ([0-9]{1,4}) ((?:[A-Za-z]+\s){0,}[A-Za-z]+)', full_text)
    if(false_multiple_match_2):
        for match in false_multiple_match_2:
            if(re.search('[P,p]atients|[C,c]ases', match[1])):
                if(match[0] in count_to_match.keys() and count_to_match[match[0]] > 0):
                    count_to_match[match[0]] -= 1

    false_multiple_match_2 = re.search('[R,r]ecent (?:[A-Za-z]+\s){0,}[A-Za-z]+ (study|studies) (?:[A-Za-z]+\s){0,}[A-Za-z]+ ([0-9]{1,4}) (\w+){0,} ([P,p]atients|[C,c]ases)', full_text)
    if(false_multiple_match_2):
        for match in re.findall('[R,r]ecent (?:[A-Za-z]+\s){0,}[A-Za-z]+ (study|studies) (?:[A-Za-z]+\s){0,}[A-Za-z]+ ([0-9]{1,4}) (\w+){0,} ([P,p]atients|[C,c]ases)', full_text):
            if(match[1] in count_to_match.keys() and count_to_match[match[1]] > 0):
                count_to_match[match[1]] -= 1

    false_multiple_match_2 = re.findall('((?:[A-Za-z]+\s){0,}[A-Za-z]+) ([0-9]{1,4}) ((?:[A-Za-z]+\s){0,}[A-Za-z]+)', full_text)
    if(false_multiple_match_2):
        for match in false_multiple_match_2:
            check_1 = False
            check_2 = False
            first_part = match[0]
            count = match[1]
            second_part = match[2]

            ## Before catched number
            if(re.search('study|studies|report|reports', first_part)):
                if(re.search('[R,r]ecent*', first_part)):
                    check_1 = True
                elif(re.search('[R,r]eported', first_part)):
                    check_1 = True

            ## After catched number
            if(re.search('[P,p]atients|[C,c]ases', second_part)):
                check_2 = True

            if(check_1 and check_2):
                if(count in count_to_match.keys() and count_to_match[count] > 0):
                    count_to_match[count] -= 1

    ## Deal with bib ref inserted in text
    false_multiple_match_2 = re.findall('[R,r]eported by (?:[A-Za-z]+\s){0,}[A-Za-z]+ (?:etal.){0,} \[[0-9]{1,}\] (?:[A-Za-z]+\s){0,}[A-Za-z]+ ([0-9]{1,4}) ((?:[A-Za-z]+\s){0,}[A-Za-z]+)', full_text)
    for match in false_multiple_match_2:
        count = match[0]
        last_part = match[1]
        if(re.search('[P,p]atients|[C,c]ases', last_part)):
            if(count in count_to_match.keys() and count_to_match[count] > 0):
                count_to_match[count] -= 1

    false_multiple_match_2 = re.findall('((?:[A-Za-z]+\s){0,}[A-Za-z]+) ([0-9]{1,4}) ((?:[A-Za-z0-9]+\s){0,}[A-Za-z0-9]+) (\[[0-9]{1,})', full_text)
    for match in false_multiple_match_2:
        count = match[1]
        if(re.search('[P,p]atients|[C,c]ases', match[2])):
            if(count in count_to_match.keys() and count_to_match[count] > 0):
                count_to_match[count] -= 1

    if(len(count_to_match) > 0 and not case_report_match):
        count_to_match_sorted = sorted(count_to_match.items(), key=operator.itemgetter(1))
        if(int(count_to_match_sorted[-1][0]) > 0 and count_to_match_sorted[-1][1] > 0):
            number_of_patients = int(count_to_match_sorted[-1][0])

        ## return NA if all catched sentences give different numbers
        if(len(count_to_match) > 1 and (int(count_to_match_sorted[-1][1]) == int(count_to_match_sorted[0][1])) and not case_report_match):
            number_of_patients = "NA"

        ## return NA if the catched match count is not the stronger but enconter execo
        ## values
        if(len(count_to_match) > 1 and not case_report_match):
            same_match_value_found = False
            cmpt_match = 0
            for value in count_to_match.values():
                if(int(value) == int(count_to_match_sorted[-1][1])):
                    cmpt_match += 1
            if(cmpt_match > 1):
                same_match_value_found = True
                number_of_patients = "NA"


    return number_of_patients
