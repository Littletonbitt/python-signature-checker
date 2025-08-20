import sys
import os
import json

def get_month(string):
    dict_month = {"Jan": 1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
    return dict_month.get(string, -1)

def get_initials(path_open):
    dict_initials = {}
    try:
        with open(path_open, "r") as f:
            text = f.read()
        lines = text.split('\n')
        list_inf = [line.strip() for line in lines if line.strip()]
        for i in range(len(list_inf)):
            if "Serial Number" in list_inf[i] and (i+1)<len(list_inf):
                dict_initials["Serial Number"] = list_inf[i+1]
            elif "Issuer:" in list_inf[i] and "email" in list_inf[i]:
                dict_initials["publisher"] = list_inf[i]
            elif "Not" in list_inf[i] and "Before" in list_inf[i]:
                temp = list_inf[i].split()
                day, month, year = "?", "?", "?"
                for part in temp:
                    if len(part)==3:
                        try_month = get_month(part)
                        if try_month>0:
                            month = try_month
                    elif len(part)==2:
                        day = part
                    elif len(part)==4:
                        year = part
                dict_initials["since"] = f"{day}/{month}/{year}"
            elif "Not After" in list_inf[i]:
                temp = list_inf[i].split()
                day, month, year = "?", "?", "?"
                for part in temp:
                    if len(part)==3:
                        try_month = get_month(part)
                        if try_month>0:
                            month = try_month
                    elif len(part)==2 and part.isdigit()==True:
                        day = part
                    elif len(part)==4 and part.isdigit()==True:
                        year = part
                dict_initials["before"] = f"{day}/{month}/{year}"
            elif "Subject:" in list_inf[i] and "C=RU" in list_inf[i]:
                dict_initials['subj'] = list_inf[i]
        return dict_initials
    except Exception as e:
        print(f"Error processing {path_open}: {e}")
        import traceback
        traceback.print_exc()
        return {}

if __name__=="__main__":
    path_open = sys.argv[1]
    result = get_initials(path_open)
    if not result:
        print("No information extracted")
        sys.exit(1)
    else:
        script_name = os.path.basename(__file__).replace('.py', '')
        output_file = f"{script_name}.json"
    
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
        print(f"Data written to {output_file}")
        sys.exit(0)

