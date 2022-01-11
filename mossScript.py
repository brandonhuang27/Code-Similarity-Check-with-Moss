import sys
import os
import subprocess
import shlex
import requests
import pandas as pd

# the main method which is run - invokes the moss script, then extracts the table from URL
def mossScript(moss, lang, filename1, filename2):
    resultsURL = invokeMoss(moss, lang, filename1, filename2)
    readURL(resultsURL)

# invokes Moss script and returns URL
def invokeMoss(moss, lang, filename1, filename2):
    args = ['perl', moss, "-l", lang]
    args_allFiles = args + getfilenames(filename1) + getfilenames(filename2)
    # remove duplicate files
    args = []
    [args.append(i) for i in args_allFiles if i not in args]
    p=subprocess.Popen(args,stdout=subprocess.PIPE)
    out = p.communicate()[0]
    outputString = out.decode('utf-8')
    return outputString.split("\n")[-2]

# get all files if directory passed in
def getfilenames(filepath):
    if "*" in filepath:
        lang = filepath.split(".")[-1]
        directory = filepath.split("*")[0]
        return [directory + i for i in os.listdir(directory) if lang in i.split(".")[-1]]
    return [filepath]

# reads URL, converts the table into a dataframe, and then records to a csv file
def readURL(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    #sorts the output
    sorted_table = df.sort_values(by='Lines Matched', ascending=False)
    print(sorted_table)
    sorted_table.to_csv('mossData.csv')

# to run Python script, enter command in terminal:
# python3 mossScript.py mossScript "moss.pl" [programming language] [file name 1] [file name 2]
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
