#!/usr/bin/env python

# zohocsvhtmltomarkdown.py: Converts a Zoho forum CSV backup file to Markdown.
# 
# Zoho forum dumps consist of a CSV file that contains multiple columns and one 
# of the columns contains a forums posting or comment as HTML. 
# 
# This script creates a new CSV file where the HTML is converted to Markdown. It
# also creates a Markdown file for each content cell.
# 
# This works well with small forum dumps, but if you have a large forum with many 
# comments you will have a Mardown file for each comment.
# 
# Columns are expected to be in this order:
# 
# Forum Name, Category Name,Topic Title, Permalink, Posted Time, Content, Author,
# Attachments, Votes
# 
# How to run this?
# 
# Create a Python virutalenv and install the following libraries:
# 
# * backports.csv==1.0.1
# * html2text==2016.5.29
# * Markdown==2.6.6
# 
# Source the environment, and then edit the file and change CSV_FILE_NAME & 
# NEW_CSV_FILE_NAME to suit the file you have.
# 
# Run the script like so:
# 
# ``` python zohocsvhtmltomarkdown.py ```
# 
# Or
#
# ``` ./zohocsvhtmltomarkdown.py ```

__author__      = "Mick Timony"
__copyright__   = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Mick Timony"
__email__ = "mick+githubmiscrepo@gmail.com"
__status__ = "Prototype"

import io
import sys

import backports.csv as csv
import html2text

from markdown import markdown

CSV_FILE_NAME = 'forums.csv' # the file to import
NEW_CSV_FILE_NAME = 'forums_markdown.csv' # the file to create

# some content fields are bigger than csv.field_size_limit
csv.field_size_limit(sys.maxsize)
with io.open(CSV_FILE_NAME, 'r') as csvfile, io.open(NEW_CSV_FILE_NAME, 'w') as writecsvfile:
    reader = csv.reader(csvfile, delimiter=u',', quotechar=u'"')
    writer = csv.writer(writecsvfile)
    counter = 0
    for row in reader:
        col_number = 0
        my_row = []
        for col in row:
            if col_number == 3:
                # use the permalink as the file name
                title = col
                
            col_number = col_number + 1
            if col_number == 6:# & counter != 0:
                # aha, a content field!
                h = html2text.HTML2Text()
                markdown_col = h.handle(col)
                my_row.append(markdown_col)
                with io.open(title + ".md", 'a') as writecontentfile:
                    writecontentfile.write(markdown_col)
            else:
                my_row.append(col)
        writer.writerow(my_row)
