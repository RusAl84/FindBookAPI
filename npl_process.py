import os
import json
import nltk
import pymorphy3


db_fileName_data = "./data.txt"
db_fileName = "./data.json"


def remove_digit(data):
    str2 = ''
    for c in data:
        if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '«', '»', '–', "\""):
            str2 = str2 + c
    data = str2
    return data


def remove_punctuation(data):
    str2 = ''
    import string
    pattern = string.punctuation
    for c in data:
        if c not in pattern:
            str2 = str2 + c
        else:
            str2 = str2 + ""
    data = str2
    return data


def remove_stopwords(data):
    str2 = ''
    from nltk.corpus import stopwords
    russian_stopwords = stopwords.words("russian")
    for word in data.split():
        if word not in (russian_stopwords):
            str2 = str2 + " " + word
    data = str2
    return data


def remove_short_words(data, length=1):
    str2 = ''
    for line in data.split("\n"):
        str3 = ""
        for word in line.split():
            if len(word) > length:
                str3 += " " + word
        str2 = str2 + "\n" + str3
    data = str2
    return data


def remove_paragraf_to_lower(data):
    data = data.lower()
    data = data.replace('\n', ' ')
    return data


def remove_all(data):
    data = remove_digit(data)
    data = remove_punctuation(data)
    data = remove_stopwords(data)
    data = remove_short_words(data, length=3)
    data = remove_paragraf_to_lower(data)
    return data

def get_normal_form_mas(words):
    morph = pymorphy3.MorphAnalyzer()
    result = []
    for word in words.split():
        p = morph.parse(word)[0]
        result.append(p.normal_form)
    return result


def get_normal_form(words):
    morph = pymorphy3.MorphAnalyzer()
    p = morph.parse(words)[0]
    return p.normal_form

def remove_paragraf_and_toLower(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    text = ' '.join([k for k in text.split(" ") if k])
    return text


def get_keywords(data):
    data=remove_all(data)
    mas=[]
    morph = pymorphy3.MorphAnalyzer()
    for word in data.split():
        p = morph.parse(word)[0]
        mas.append(p.normal_form)
    return mas

def nltk_download():
    nltk.download('stopwords')
    nltk.download('punkt')
    
    
def calc_intersection_list(list1, list2):
    count = 0
    for item1 in list1:
        for item2 in list2:
            count += calc_intersection_text(item1, item2)
    return count

def calc_intersection_text(text1, text2):
    count = 0
    text1 = str(text1)
    text2 = str(text2)
    for item1 in text1.split():
        for item2 in text2.split():
            if item1 == item2:
                count += 1
    return count


def load_db():
    import pathlib
    path = pathlib.Path(db_fileName)
    if path.exists():
        with open(db_fileName, "r", encoding="UTF8") as file:
            jsoncontent = file.read()
        content = json.loads(jsoncontent)
        return content
    else:
        return [{}]

def find_book(text):
    data_cl = load_db()
    kw1 = get_keywords(text)
    counts=3 # минимальное количество ключевых слов в тексте для нахождения нужной книги
    find_data = []
    for item in data_cl:
        intersects = calc_intersection_list(kw1,item['keywords'])
        item['intersects'] = intersects
        find_data.append(item)
    jsonstring = json.dumps(find_data, ensure_ascii=False)
    with open("./find_data.json", "w", encoding="UTF8") as file:
        file.write(jsonstring)
    find_count_set=set()
    for item in find_data:
        find_count_set.add(item['intersects'])
    # find_count_set=sorted(find_count_set, reverse=True)
    find_max = max(find_count_set)
    find_books = []
    for item in find_data:
        if item['intersects'] == find_max:
            find_books.append(item)
    jsonstring = json.dumps(find_books, ensure_ascii=False)
    with open("./find_books.json", "w", encoding="UTF8") as file:
        file.write(jsonstring)
    return find_books    
        
if __name__ == '__main__':
    # nltk_download()
    str1="Роман-антиутопия рассказывает нам о том, как к 1984 году, в результате войн и политических кризисов на планете Земля, образовались три тоталитарных сверхдержавы: Океания, Евразия и Остазия – которые непрерывно воюют друг с другом. Действие происходит в будущем тоталитарном обществе, где правительство во главе с Большим Братом полностью контролирует все аспекты жизни граждан. Главный герой работает в Министерстве правды и начинает восставать против деспотичного режима правительства, но в итоге сталкивается с серьёзными последствиями своих действий."
    data = get_keywords(str1)
    print(data)
    
    data = find_book(str1)
    print(data)
