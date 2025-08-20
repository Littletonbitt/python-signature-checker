#!/bin/bash

file_name_crt="$1"
file_name_crt_txt="$2"
file_name_pdf="$3"
file_name_html="$4"
file_name_txt="$5"


touch "$file_name_crt_txt"
touch "$file_name_txt"
openssl x509 -in "$file_name_crt" -text -out "$file_name_crt_txt"

pdftohtml -stdout "$file_name_pdf" > "$file_name_html"

sed -e 's/<[^>]*>//g' "$file_name_html" > "$file_name_txt"
