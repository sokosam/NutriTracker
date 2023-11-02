

def onlyNums(s):
    for i in s:
        if not i.isnumeric():
            s = s.replace(i,"")
    return int(s)

def findVals(data, val):
    try:
        i = data.index(val)
    except Exception:
        if val[-2] + val[-1] == "er":
            try:
                val = val[:-2] + "re"
                i = data.index(val)
            except Exception:
                return IndexError
        else:
            return IndexError
    
    def has_numbers(s):
        return any(char.isdigit() for char in s)
    
    while(has_numbers(data[i]) == False):
        i+=1
    return i

def process(data):
    nums = {"carbohydrate" : 0, "fat": 0, "protein": 0, "calcium": 0, "fiber" :0, "sugars":0, "iron":0, "calories" :0}
    textData = data["text"]
    textData = [x.lower() for x in textData]
    for value in nums:
        try:
            nums[value] = onlyNums(textData[findVals(textData, value)])
        except TypeError or IndexError:
            nums[value] = 0
    return nums

