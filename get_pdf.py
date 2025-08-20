import sys
import os
import json

def get_month(string):
    dict_months = {"янв":1, "фев":2, "мар": 3, "апр": 4, "май": 5, "июн": 6, "июл": 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12}
    string_lower = string.lower()
    for key in dict_months:
        if key in string_lower:
            return dict_months[key]
    return 0

def get_day(string):
    digits = ''.join(filter(str.isdigit, string))
    return int(digits) if digits else 1

def get_initials(to_open):
    try:
        list_inf = []
        dict_initials = {}
        with open(to_open, "r") as f:
            text = f.read()
            text = text.replace("&#160;", " ")
            temp = text.split('\n')
            for i in temp:
                i = i.replace("&#160;", " ").strip()
                if i:
                    list_inf.append(i)
        for i in range(len(list_inf)):
            current_line = list_inf[i]
            if (('Имя' in current_line) or ('Отчество' in current_line) or ('Фамилия' in current_line)) and i + 1 < len(list_inf):
                dict_initials[current_line] = list_inf[i + 1].replace("&#160;", " ").strip()
                i += 2
                continue
            elif current_line== 'Дата Рождения' and i + 1 < len(list_inf):
                birth_line = list_inf[i + 1].replace("&#160;", " ").replace("34","")
                temp = birth_line.split()
                if len(temp) >= 3:
                    day = get_day(temp[0])
                    month = get_month(temp[1])
                    year = temp[2]
                    dict_initials[current_line] = f"{day:02d}/{month:02d}/{year}"
                i += 2
                continue
            elif 'Сертификат' in current_line:
                temp = current_line.split()
                cert = temp[-1]
                dict_initials['Сертификат'] = cert
                continue
            elif 'Издатель' in current_line:
                temp = current_line.split()
                string = ""
                for i in range(len(temp)):
                    if i > 0:
                        string += temp[i] + ';'
                dict_initials['Издатель'] = string
                continue
            elif 'Организаци' in current_line:
                temp = current_line.split()
                string = ""
                for i in range(len(temp)):
                    if i > 0:
                        string += temp[i] + " "
                dict_initials['Организация'] = string
                continue
            elif 'Действи' in current_line:
                temp = current_line.split("&#160;")
                line = "".join(temp)
                tempp = line.split(' ')
                dict_initials['Действителен'] = f"{tempp[2]}/{tempp[4]}"
                continue
        return dict_initials
    except Exception as e:
        print(f"Error reading file {to_open}: {e}")
        import traceback
        traceback.print_exc()
        return {}

if __name__=="__main__":
    to_open = sys.argv[1]
    dict_temp = get_initials(to_open)
    if not dict_temp:
        print(f"ERROR: {to_open} returns empty dictionary!")
        sys.exit(1)
    else:
        script_name = os.path.basename(__file__).replace('.py', '')
        output_file = f"{script_name}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dict_temp, f, ensure_ascii=False, indent=2)
        print(f"Data written to {output_file}")
        sys.exit(0)
