import json


def load_livers():
    f = open("./json/streamers.json", 'r', encoding="utf-8_sig")
    data = json.load(f)
    f.close()

    return data


def write_livers(data:dict):
    f = open("./json/streamers.json", 'w', encoding="utf-8_sig")
    json.dump(data, f, indent=3, ensure_ascii=False)
    f.close


def getindex_by_id(id:int):
    livers = load_livers()
    ret = None

    for i, liver in enumerate(livers):
        if liver["id"] == id:
            ret = i
            break
    
    return ret


def getdict_by_id(id:int):
    js = load_livers()
    idx = getindex_by_id(id)

    if idx is None:
        return None
    else:
        return js[idx]


def mod_by_id(id:int, data:dict):
    js = load_livers()
    idx = getindex_by_id(id)
    
    if idx is None:
        js.append(data)
    else:
        js[idx] = data
    
    write_livers(js)
    

if __name__ == "__main__":
    dic = getdict_by_id(810)
    dic["id"]=893
    mod_by_id(810, dic)
