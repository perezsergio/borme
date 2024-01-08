# BORME registry scrapping

This repo provides a collection of scripts that can be used to
scrap the BORME registry website, https://www.boe.es/diario_borme/ ,
to obtain a list of the legal acts published in the BORME at a given date.

The script `spyder.py` downloads all the pdfs of the BORME registry website 
corresponding to a given date.
The script `crawler.py` parses the text of the downloaded pdfs to obtain the
relevant information.
More often than not you may want to execute these 2 scripts, 
one after the other, to download then parse the pdfs for a given date.
This is exactly what the script `main.py` does.

## How to use it
Every script has the same CLI, which includes a very helpful help message.
```bash
python3 src/borme/main.py --help
```

Basically, the user must specify a date or list of dates to the script,
and there are 2 ways of doing it:
```bash
# passing the dates directly in the command line
python3 main.py 20231127 20231128 20231201
# providing a path to a file that stores the dates
echo '20231127\n20231128\n20231201' > dates.txt ; python3 main.py -f dates.txt 
```

In any case, the dates must always have the format **YYYYMMDD**.

## Logs
This repo makes a generous use of logs, which are preferred over exceptions 
and printing messages directly to stdout.
The reasoning behind this is that the script should never raise an exception and 
stop executing.
Instead we want the script to skip over the problematic parts and
simply inform the user that there was some problem, and where it is located.

This behavior helps automation: 
if we pass the script a list of 100 dates,
we want the script to finish executing and log 
the dates where the scrapping was and wasn't successful.
We do not want under any circumstances to find out that the script
stopped executing on the 23rd pdf of the 34th date because of a minor 
parsing error.

For example, if we pass these dates to the `main` script:
```bash
python3 main.py 20231201 20231202 20231203 202312004
```
The logs will inform us that the execution was successful for the first date (2023-12-01),
but no pdfs could be found for the next 2 dates
(BORME was not published for 2023-12-02 and 2023-12-03), 
and that the script cannot recognize the last date
(there is a typo: 202312004 instead of 20231204)


## Act parsing
After cleaning and parsing the pdf text, the curated data has the form of a jsonl object.
Each legal act is a json object with the fields 
`{"id", "company_name", "region_name", "borme_date", "description"}`.
The description contains all the text that could not be classified in any other fields.
Ideally we would want to structure the data further
by parsing the contents of the description field.
However, this is not trivial.

Sometimes, there are multiple legal acts contained under a single id.
For example, the legal act *Constitución*, which records the creation a new company,
always appears together with other acts, like *nombramientos* (appointments).
There are many other tricky cases.
For example, whenever a company goes out of business (*acto de disolución*) 
this always appears together with the act *ceses/dimisiones*,
and it always appears last, which makes it difficult to find this acts.

For these reasons it is not easy to find a way to completely structure the data.
A solution would require some domain specific knowledge,
like the restrictions of the form used to submit a legal act.
Any naive methods will inevitably lead to mistakes. 
For example, if we considered that the first word of each act is the act type
then we would not record any acts of the type *ceses/dimisiones*.
Therefore we chose to leave untouched all the data that we were not 
completely confident structuring.
This way we leave room for a future solution without 
compromising the quality of the data.
