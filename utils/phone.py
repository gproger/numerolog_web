import re



def get_phone(phone):
    regex = re.compile('[+?\d+]')
    res = ''
    res = res.join(regex.findall(phone))
    return res
