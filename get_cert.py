import re
import os
import sys

def write_to_file(name, ans):
    try:
        with open(name, "w") as f:
            for i in range(len(ans)):
                f.write(ans[i] + "\n")
        size = os.path.getsize(name)
        return True
    except Exception as e:
        print(f"Counld proccess {name}")
        return False


def get_cert(to_open, to_write):
    try:
        list_inf = []
        split_char = r"[<\n>]"
        ans = ['-----BEGIN CERTIFICATE-----']
        with open(to_open, "r") as f:
            text = f.read()
        list_inf = re.split(split_char, text)
        check = False
        for i in range(len(list_inf)):
            if check==True:
                if list_inf[i]!='/X509Certificate':
                    ans.append(list_inf[i])
                else:
                    check=False
                    break
            if list_inf[i]=='X509Certificate':
                check=True
        ans.append('-----END CERTIFICATE-----')
    
        write_to_file(to_write, ans)
        return True
    except FileNotFoundError:
        print(f"Error: File {to_open} not found")
        return False
    except Exception as e:
        print(f"Error processing {to_open}: {e}")
        return False

if __name__=="__main__":
    to_open = sys.argv[1]
    to_write = sys.argv[2]
    success = get_cert(to_open, to_write)
    sys.exit(0 if success==True else 1)
