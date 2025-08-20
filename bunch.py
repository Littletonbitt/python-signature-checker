import os
import json
import glob
from datetime import datetime
import sys
import subprocess

#check workflow
#check touching and working with files

#firstly, create stream for writing and reading given files
#filename is a parameter from file
#read_filename is a string from .txt file which contains only one string

def get_json(scripts):
    try:
        temp_json = []
        for i in scripts:
            i = i.replace(".py", "").replace(".sh", "")
            temp_json.append(f"{i}.json")
        return temp_json
    except Exception as e:
        print(f"Error making json in get_json: {e}")
        return None

def get_file_crt(string):
    for i in range(len(string)):
        if string[i]=='.':
            return string[:i] + '.crt'


def get_new_filename(string):
    for i in range(len(string)):
        if string[i]=='.':
            return string[:i] + "_copy" + string[i:]

def get_crt_text(string):
    for i in range(len(string)):
        if string[i]=='.':
            return string[:i] + "_crt.txt"
    return "default.txt"

def get_html_txt(string):
    for i in range(len(string)):
        if string[i]=='.':
            return string[:i] + "_html.txt"

def get_pdf_html(string_pdf):
    for i in range(len(string_pdf)):
        if string_pdf[i]=='.':
            return string_pdf[:i] + "_pdf.html"


def read_filename():
    with open(string, "r") as f:
        text = f.read()
    new_filename = get_new_filename(text)
    new_filename_pdf = get_new_filename(text)
    with open(text, "r") as f:
        text_to = f.read()
    with open(new_filename, "w") as f:
        f.write(text_to)
    return [new_filename, new_filename_pdf]

def run_bash(string, *args) -> bool:
        try:
            cmd = ["/bin/bash", string] + list(args)
            result = subprocess.run(cmd, check=True)
            return result.returncode==0
        except subprocess.CalledProcessError as e:
            print(f"Error while executing {string} \n {e}")
            return False

def run_python(string, *args) -> bool:
    try:
        cmd = [sys.executable, string] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        stdout_output = result.stdout
        print(stdout_output)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error while executing {string} \n {e}")
        return False

def prepare_files():
    try:
        with open("prepare.txt", "r") as f:
            text = f.read()
        inf = text.split('\n')
        return inf
    except:
        return []

def run_scripts():
    scripts = ["get_cert.py", "openssl.sh","read_txt.py", "get_pdf.py", "get_sig.py", "check.py", "verify.py"]
    list_of_temp = prepare_files()
    list_json = get_json(scripts)
    list_of_files = [files for files in list_of_temp if files!='' and files!=' ']
    for i in range(0,len(list_of_files), 2):
        file_xml = list_of_files[i]
        file_pdf = list_of_files[i+1]
        file_bash_crt = get_file_crt(file_xml)
        file_bash_txt = get_crt_text(file_xml)
        file_pdf_html = get_pdf_html(file_pdf)
        file_html_txt = get_html_txt(file_pdf)
        for j in range(len(scripts)):
            if scripts[j].endswith('.py'):
                if scripts[j]=="get_cert.py":
                    run_python(scripts[j], file_xml, file_bash_crt)
                elif scripts[j]=="get_sig.py":
                    run_python(scripts[j], file_bash_txt)
                elif scripts[j]=="get_pdf.py":
                    run_python(scripts[j], file_html_txt)
                elif scripts[j]=="read_txt.py":
                    print(file_html_txt)
                    run_python(scripts[j], file_html_txt)
                elif scripts[j]=="check.py":
                    run_python(scripts[j], file_bash_crt, file_xml)
                else:
                    run_python(scripts[j], file_bash_crt)
            else:
                run_bash(scripts[j], file_bash_crt, file_bash_txt, file_pdf, file_pdf_html, file_html_txt)


if __name__=="__main__":
    run_scripts()
