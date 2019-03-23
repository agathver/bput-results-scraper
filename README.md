# BPUT Result Scraper

Scrapes BPUT website to find all your results.

## Setup

_Use the given pipenv configuration to get started quickly_

The project uses Python 3 and the following dependencies (included in Pipfile):
- requests
- lxml
- cssselect

## Usage

    usage: get_bput_results <command> [<args>]

    Sub commands:
    results         Show results
    list-exams      List all exam results which can be fetched from bputexam.in

    Shows BPUT results

    positional arguments:
    command     Subcommand to run

    optional arguments:
    -h, --help  show this help message and exit


## The story of scraping bputexam.in

_[bputexam.in][1] sucks, we all know that._ 
 
This is an utility to fetch all marks and (possibly) preserve them in an 
"air-tight, sterilized, transparent, container" free from "viruses"
 
Simple interactive scraping project using lxml and requests, nothing fancy.
 
Perhaps, one day you will use this data for analytics and find the subject that 
sucks the most. Feel free to use this code for whatever you want to do.

### A bit about scraping sites using ASP.NET Forms

It's a nightmare. Complicated with the fact that bputexam.in uses Telerik.UI
controls, which exposes a bunch of its own hidden states.

[Scraping Websites Based on ViewStates with Scrapy][2] from ScrapingHub blog,
explains a bit about various ASP.NET hidden inputs and their significance. 

#### Submitting forms

In order to simulate a form submission, you need to submit all ASP.NET hidden
fields: `__VIEWSTATE`, `__VIEWSTATEENCRYPTED`, and `__VIEWSTATEGENERATOR`.

Moar doks:

 - https://msdn.microsoft.com/en-us/library/ms972976.aspx
 - https://msdn.microsoft.com/en-us/library/bb386448.aspx
 

_bputexam.in uses `VIEW_STATE` encryption, so it's not possible to tamper it. So
we have to pass the viewstate as is._

After a bit of fiddling with Firefox's network debug tool, I came up with the
"magic fields".

#### Triggering an onClick (POST-back), server-side

Yuck, why? But it's ASP.NET, so you have a special post request to trigger an
`onClick`, this is represented by the special parameter `__EVENTTARGET`.
The value of this field is an ASP.NET ControlID.

Moar doks:

 - https://www.codeproject.com/Articles/134614/Way-To-Know-Which-Control-Has-Raised-PostBack
 
Another trick is the case of multiple submit buttons, Forms from lxml, by 
default include all submit buttons in fields. We need to delete the ones which
we are not clicking, before making a request.


## LICENSE

MIT 

_Use this code however you want (abiding by the license terms, ofcourse),
but make sure to follow proper web scraping etiquette._

By using this code, you agree not to hold me (Amitosh Swain Mahapatra)
responsible for any mishappening, misconduct, breach of contract, material
damage of any amount or legal ramifications happening due to deploying this
work.

[1]: http://www.bputexam.in
[2]: https://blog.scrapinghub.com/2016/04/20/scrapy-tips-from-the-pros-april-2016-edition/