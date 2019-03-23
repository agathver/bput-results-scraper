#!/usr/bin/env python3
# coding: utf-8

"""
Scraping the BPUT Results Website
 
(http://www.bputexam.in) sucks, we all know that._ 
 
This is an utility to fetch all marks and (possibly) preserve them in an 
"air-tight, sterilized, transparent, container" free from "viruses"
 
Simple interactive scraping project using lxml and requests, nothing fancy.
 
Perhaps, one day you will use this data for analytics and find the subject that 
sucks the most. Feel free to use this dump for whatever you want to do.

This code is MIT licensed.
"""
# In[1]:


# import 'em all!
import argparse
import requests
import lxml.html
import sys

# URL For student result page,
STUDENT_RESULT_URL = 'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx'


def results(session, input_page):
    parser = argparse.ArgumentParser(
        description='Show results from bputexam.in')

    parser.add_argument('exam_id')
    parser.add_argument('reg_no')

    args = parser.parse_args(sys.argv[2:])

    # Fill the first form
    student_info_form = input_page.forms[0]
    student_info_form.fields['ddlSession'] = args.exam_id

    # BPUT does not validate date of birth ;)
    student_info_form.fields['dpStudentdob'] = '2000-01-01'
    student_info_form.fields['txtRegNo'] = args.reg_no

    fields = {k: v for k, v in student_info_form.fields.items()}

    # delete buttons which are not clicked
    del fields['btnReset']

    # Submit the input page
    res = session.post(student_info_form.action, fields)

    intermediate_page = lxml.html.fromstring(res.text)
    intermediate_page.make_links_absolute(STUDENT_RESULT_URL)

    result_params = {k: v for k,
                     v in intermediate_page.forms[0].fields.items()}

    # From browser inspector, it's the ControlID. It does not change between
    # page refreshes
    result_params['__EVENTTARGET'] = 'gvResultSummary$ctl02$lnkViewResult'
    result_params['__EVENTARGUMENT'] = ''
    del result_params['btnView']
    del result_params['btnReset']

    # Submit the summary page
    result_res = session.post(intermediate_page.forms[0].action, result_params)
    result_page = lxml.html.fromstring(result_res.text)
    results_table = result_page.cssselect('#gvViewResult')[0]

    # Extract data from the table
    rows = results_table.cssselect('tr')
    # header = [str(th.text_content()).strip() for th in rows[0].cssselect('th')]
    data = [[str(td.text_content()).strip()
             for td in row.cssselect('td')] for row in rows[1:]]
    summary = data[-1]
    marks = data[:-1]

    name = result_page.cssselect('#lblName')[0].text_content()
    college = result_page.cssselect('#lblCollege')[0].text_content()
    exam_name = result_page.cssselect('#lblResultName')[0].text_content()
    branch = result_page.cssselect('#lblBranch')[0].text_content()

    # show results
    print(exam_name)
    print('\n')

    print('   Name:', name)
    print(' Branch:', branch)
    print('College:', college)
    print('\n')

    print("%8s    %50s    %7s    %5s" %
          ('Code', 'Subject', 'Credits', 'Grade'))
    print('-' * 8, '  ', '-' * 50, '  ', '-' * 7, '  ', '-' * 5)
    for sub in marks:
        print('%8s    %50s    %7s    %5s' % (sub[1], sub[2], sub[4], sub[5].strip(' *')))

    print('\n')

    print(summary[4])
    print(summary[5])


def list_exams(session, input_page):
    print("%20s    %4s" % ('Exam name', 'Code'))
    print('-' * 20, "  ", '-' * 4)

    options = iter(input_page.cssselect('#ddlSession > option'))
    next(options)
    for option in options:
        print('%20s    %4s' % (option.text, option.attrib['value']))


def main():

    parser = argparse.ArgumentParser(
        description='Shows BPUT results',
        usage='''get_bput_results <command> [<args>]

Sub commands:
   results         Show results
   list-exams      List all exam results which can be fetched from bputexam.in
''')

    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args(sys.argv[1:2])

    # BPUT Website needs a browser session, so we create a session and let `requests`
    # manage the cookie jar
    session = requests.Session()

    # Get initial data
    res = session.get(STUDENT_RESULT_URL)
    input_page = lxml.html.fromstring(res.text)
    input_page.make_links_absolute(STUDENT_RESULT_URL)

    command = args.command.replace('-', '_')

    if command not in globals():
        print('Unrecognized command')
        parser.print_help()
        exit(1)

    # use dispatch pattern to invoke method with same name
    globals()[command](session, input_page)


if __name__ == "__main__":
    main()
