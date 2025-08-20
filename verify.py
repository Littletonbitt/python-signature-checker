import sys
import os
import json

def get_finally_cert(get_cert):
    try:
        list_ans = []
        with open(get_cert, "r") as f:
            text = f.read()
        list_ans = text.split("\n")
        return list_ans[1:len(list_ans)]
    except Exception as e:
        print(f"Error while processing {get_cert} in verify.py: {e}")
        sys.exit(1)


def verify(to_open, get_cert):
    try:
        serial_number_decimal_check = serial_number_hex = surname_check = name = mid_name = ""
        birth = date_creation = date = sig_method = digest_method = ""
        serial_number_decimal_sig = publisher = date_since = date_after = subj = ""
        surname_pdf = name_pdf = mid_name_pdf = birth_pdf = subj_pdf = ""
        serial_number_cert = publisher_pdf = date_before_pdf = date_after_pdf = ""
        subj_read = serial_number_read = date_before_read = date_after_read = ""
        with open('check.json', 'r', encoding='utf-8') as f:
            data_check = json.load(f)
        with open('get_sig.json', 'r', encoding='utf-8') as f:
            data_sig = json.load(f)
        with open('get_pdf.json', 'r', encoding='utf-8') as f:
            data_pdf = json.load(f)
        with open('read_txt.json', 'r', encoding='utf-8') as f:
            data_read = json.load(f)
        for i in range(len(data_check)):  #opening data_check storaging chack.json
            for key in data_check[i]:
                if key=='serial_number_decimal':
                    serial_number_decimal_check = data_check[i][key]
                elif key=='serial_number_hex':
                    serial_number_hex = data_check[i][key]
                elif key=='Фамилия':
                    surname_check = data_check[i][key]
                elif key=='Имя':
                    name = data_check[i][key]
                elif key=='Отчество':
                    mid_name = data_check[i][key]
                elif key=='ДатаРождения':
                    birth = data_check[i][key]
                elif key=='ДатаФормирования':
                    date_creation = data_check[i][key]
                elif key=='ДатаВремя':
                    date = data_check[i][key]
                elif key=='SignatureMethod':
                    sig_method = data_check[i][key]
                elif key=='DigestMethod':
                    digest_method = data_check[i][key]
        for key in data_sig:
            if key=="Serial Number":
                serial_number_decimal_sig = data_sig[key].replace(":", "")
            elif key=="publisher":
                publisher = data_sig[key]
            elif key=="since":
                date_temp = data_sig[key]
                temp = date_temp.split("/")
                date_since = f"{temp[0]}.{temp[1].zfill(2)}.{temp[2]}"
            elif key=="before":
                date_temp = data_sig[key]
                temp = date_temp.split("/")
                date_since = f"{temp[0]}.{temp[1].zfill(2)}.{temp[2]}"
            elif key=="subj":
                subj = data_sig[key]
        for key in data_pdf:
            if "Сведения о" in key:
                surname_pdf = data_pdf[key]
            elif key=="Имя":
                name_pdf = data_pdf[key]
            elif key=="Отчество":
                mid_name_pdf = data_pdf[key]
            elif key=="Дата Рождения":
                temp = data_pdf[key].split('/')
                birth_pdf = f"{temp[2]}/{temp[1]}/{temp[0]}"
            elif key=="Организация":
                subj_pdf = data_pdf[key]
            elif key=="Сертификат":
                serial_number_cert = data_pdf[key]
            elif key=="Издатель":
                publisher_pdf = data_pdf[key]
            elif key=="Действителен":
                time = data_pdf[key].split('/')
                date_before_pdf = time[0]
                date_after_pdf = time[1]
        for i in range(len(data_read)):
            for key in data_read[i]:
                if key=="Организация: ФОНД ПЕНСИОННОГО И СОЦИАЛЬНОГО":
                    temp = data_read[i][key].split(' ')
                    subj_read = temp[1:]
                elif "Сертификат" in key:
                    temp = data_read[i][key].split(' ')
                    serial_number_read = temp[1:]
                elif "Действителе" in key:
                    temp = data_read[i][key].split(' ')
                    date_before_read = temp[2]
                    date_after_read = temp[4]
        flag = True
        if str(serial_number_hex) == str(serial_number_read) == str(serial_number_cert) ==str(serial_number_decimal_sig):
            if name_pdf == name:
                if surname_check == surname_pdf:
                    if mid_name == mid_name_pdf:
                        if birth_pdf == birth:
                            if date_before_read == date_before_pdf == date_since:
                                if date_after_read == date_after_pdf == date_after:
                                    flag = True
                            else:
                                flag = False
                        else:
                            flag = False
                    else:
                        flag = False
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False
        certificate = get_finally_cert(get_cert)
        if flag==True:
            message1 = "Signature valid"
            message2 = "Chain OK"
            stamp = "timestamp valid"
        else:
            message1= "Signature not valid"
            message2 = "Chain Fail"
            stamp = "timestamp not valid"
        return {"message1": message1,"message2": message2,"flag": flag,"certificate": certificate,
            "subj": subj,"publisher": publisher,"serial_number_decimal_sig": serial_number_decimal_sig,
            "sig_method": sig_method,"digest_method": digest_method,"date": date,"stamp": stamp}

    except Exception as e:
        print(f"Error while dealing with verify function in verify.py: {e}")
        sys.exit(1)

if __name__=="__main__":
    list_json = ['check.json','get_sig.json', 'get_pdf.json', 'read_txt.json']
    get_cert = sys.argv[1]
    ans = verify(list_json,get_cert)
    if ans is None:
        print(f"Error: list is empty (verify.py)")
        sys.exit(1)
    else:
        script_name = os.path.basename(__file__).replace('.py', '')
        output_file = f"{script_name}.json"
        combined_data = {
            "Message": ans["message1"],
            "Result": ans["flag"],
            "SignerCertificateInfo": {
                "Subject": ans["subj"],
                "Issuer": ans["publisher"],
                "SerialNumber": ans["serial_number_decimal_sig"]
            },
            "SignatureInfo": {
                "Algorithm": ans["sig_method"],
                "Digest": ans["digest_method"],
                "SigningTime": ans["date"]
            },
            "Details": {
                "SignatureResult": {
                    "Result": ans["flag"],
                    "Error": "null" 
                },
                "CertificateResult": {
                    "Result": ans["flag"],
                    "Error": []
                }
            },
            "AdditionalCertificateResult": [
                {"Result": ans["flag"], "Message": ans["message2"]}
            ],
            "AdditionalCertificatesInfo": [
                {"Subject": ans["subj"]},
                {"Subject": ans["publisher"]}
            ],
            "AdditionalInfo": [
                ans["stamp"]
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)

        print(f"Data written to {output_file}")
        sys.exit(0)

