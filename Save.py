import string, random
def ranletter():
    return random.sample(string.ascii_lowercase,1)[0]
def save(wnum):
    tosave=""
    for _ in range(3):
        tosave+=ranletter()
    tosave+=str(wnum)
    tosave+="0"
    tosave+=str(random.randint(0,9))
    tosave+=ranletter()
    tosave+=str(10-wnum)
    tosave+=ranletter()
    return tosave
def load(s):
    if len(s)!=9:
        return False
    if not all([char in string.ascii_lowercase for char in s[:3]+s[6]+s[8]]):
        return False
    try:
        wnum=int(s[3])
        int(s[5])
        if int(s[7])!=10-wnum:
            return False
    except ValueError:
        return False
    if s[4]!="0":
        return False
    return wnum
