from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import xml.etree.ElementTree as ET
import sys
import json
import os

def digits(crt_file):
    try:
        dictionary = {}
        with open(crt_file, "rb") as f:
            cert_data = f.read()
            certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
            serial_number_decimal = certificate.serial_number
            serial_number_hex = f"{serial_number_decimal:x}"
        
        dictionary['serial_number_decimal'] = serial_number_decimal
        dictionary['serial_number_hex'] = serial_number_hex
        return dictionary
    except Exception as e:
        print(f"Error while processing digits() in check.py using {crt_file}: {e}")
        return None

def read_pdf(to_open):
    try:
        tree = ET.parse('TEST.xml')
        root = tree.getroot()
        list_add = {}
        for elem in root.iter():
            if 'ДатаФормирования' in elem.tag:
                date = elem.text
                list_add['ДатаФормирования'] = date
            elif 'Фамилия' in elem.tag:
                surname = elem.text
                list_add['Фамилия'] = surname
            elif 'Имя' in elem.tag:
                name = elem.text
                list_add['Имя'] = name
            elif 'Отчество' in elem.tag:
                mid_name = elem.text
                list_add['Отчество'] = mid_name
            elif 'ДатаВремя' in elem.tag:
                date_time = elem.text
                list_add['ДатаВремя'] = date_time
            elif 'ДатаРождения' in elem.tag:
                birth = elem.text
                list_add['ДатаРождения'] = birth
            elif 'DigestMethod' in elem.tag:
                digest_alg = elem.get('Algorithm')
                list_add['DigestMethod'] = digest_alg
            elif 'SignatureMethod' in elem.tag:
                sig_alg = elem.get('Algorithm')
                list_add['SignatureMethod'] = sig_alg
        return list_add
    except FileNotFoundError:
        print("Error: 'sample_metadata.xml' not found. Please create a sample XML file.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")


if __name__=="__main__":
    crt_file = sys.argv[1]
    to_open = sys.argv[2]
    ans = digits(crt_file)
    ans_else = read_pdf(to_open)
    if ans is None:
        print(f"Something went wrong {crt_file} is empty")
        sys.exit(1)
    elif ans_else is None:
        print(f"Something went wrong {to_open} is empty")
        sys.exit(1)
    else:
        script_name = os.path.basename(__file__).replace('.py', '')
        output_file = f"{script_name}.json"
        data_to_write = [ans, ans_else]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=2)

        print(f"Data written to {output_file}")
        sys.exit(0)
