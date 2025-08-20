import sys
import os
import json

def read(to_open):
    try:
        list_inf = []
        with open(to_open, "r") as f:
            for line in f:
                line = line.replace("&#160;", " ").replace("&#34;", " ").replace("\n", "")
                if line.strip():
                    list_inf.append(line.strip())
        return list_inf
    except Exception as e:
        print(f"Error while reading from {to_open}: {e}")
        return None


if __name__=="__main__":
    to_open = sys.argv[1]
    ans = read(to_open)
    if ans is None:
        print(f"Error: got empty list in {to_open}")
        sys.exit(1)
    else:
        script_name = os.path.basename(__file__).replace('.py', '')
        output_file = f"{script_name}.json"
    
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ans, f, ensure_ascii=False, indent=2)
    
        print(f"Data written to {output_file}")
        sys.exit(0)
