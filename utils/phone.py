import re



def get_phone(phone):
    regex = re.compile('[+?\d+]')
    res = ''
    res = res.join(regex.findall(phone))
    if res[0] == '8':
        res = '+7'+res[1:]
    return res
