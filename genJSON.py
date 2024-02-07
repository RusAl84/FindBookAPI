import json
import npl_process

db_fileName_data = "./data.txt"
db_fileName = "./data.json"

def genJson():
    
    import pathlib
    path = pathlib.Path(db_fileName_data)
    lines = []
    if path.exists():
        with open(db_fileName_data, "r", encoding="UTF8") as file:
            lines = file.readlines()
    count_lines = len(lines)
    # print(int(count_lines/4+1))
    books=[]
    for ind in range(int(count_lines/4)):
        line={}
        print(ind)
        line["title"] = lines[ind*4+1]
        line["authors"] = lines[ind*4+2]
        line["descr"] = lines[ind*4+3]
        line["keywords"] = npl_process.get_keywords(line["descr"])
        books.append(line)
    jsonstring = json.dumps(books, ensure_ascii=False)
    with open(db_fileName, "w", encoding="UTF8") as file:
        file.write(jsonstring)

if __name__ == '__main__':
    genJson()