import pandas as pd, re, csv, os, time, pathlib, re, requests
# still need some modules installed: lxml, html5lib, bs4


def anime():
    for times in range(1):
        time.sleep(0.05)
        print('\n')


def getInput(str):
    while True:
        anime()
        user_input = input(str)
        if user_input.isnumeric() == True:
            return user_input
        else:
            anime()
            print('Nice try.')


def delNameChar(line):
    try:
        str_list = list(line[2])
        str_list.pop()
        line[2] = ''.join(str_list)
        return line
    except:
        return line


def DataSpliter(data):
    index = re.findall(r'\d{1,3},', data)
    data = data.replace('\n', '')
    data = data.lstrip(index[0])
    data = data.replace(',,,', '')
    data = data.split(',')
    return data


def CrownGiver(line):
    global crown_id
    try:
        if line[3] == crown_list[crown_id]:
            line.append('True')
            crown_id = crown_id + 1
        else:
            pass
        return line
    except:
        return line


def WhoStay(line, department):
    global selector_list
    if 'True' in line and department == line[3]:
        selector_list.append(line[1])
    return line


def ContentFetcher(year, department_id):
    url = 'https://freshman.tw/cross/%(year)s/%(department)s' % {
        'year': year,
        'department': department_id
    }

    #確認學年資料夾存在，若不存在則創建
    pathlib.Path(year).mkdir(exist_ok=True)

    #讀取網頁表格
    header = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With":
        "XMLHttpRequest"
    }
    try:
        r = requests.get(url, headers=header)
        table = pd.read_html(r.text)[0]
    except:
        return
    table.to_csv('meta.csv', encoding='utf_8_sig')
    r_text = r.text
    r_text = r_text.replace('<a href="#">', '')

    #讀取系級名稱
    department = re.findall(r'國立東華大學 [^<\s]{3,19}', r_text)
    department[0] = department[0].replace('國立東華大學 ', '')
    department_name = '國立東華大學 ' + department[0]
    department_name_short = department[0]
    print('%s\n' % department[0])

    #取得網頁內容
    meta = open('meta.csv', 'rt', encoding='utf_8_sig')

    #取得選擇科系
    crown = re.findall(
        r'<span class="crown"></span>[^<\s]{2,20}大學 [^<\s]{3,19}</a>', r_text)
    for choice in crown:
        global crown_list
        choice = choice.replace('<span class="crown"></span>', '')
        choice = choice.replace('</a>', '')
        crown_list.append(choice)

    #開始處理資料
    title = meta.readline()
    data_list = meta.readlines()
    new_list = []
    i = 0
    for a in data_list:
        line = DataSpliter(data_list[i])
        if i == 0:
            delNameChar(line)
        else:
            if len(line) == 2:
                line2 = new_list[i - 1]
                line = line2[:3] + line
            elif len(line) == 5:
                delNameChar(line)
            elif len(line) == 4:
                line.insert(0, '')
                delNameChar(line)
            else:
                pass
        #刪除非正備取的資料
        if line[0] == '':
            continue
        else:
            pass
        line.append(year)
        line.append(department_name_short)
        line = CrownGiver(line)
        line = WhoStay(line, department_name)
        try:
            split_str = line[3].split(' ')
            line = line[:3] + split_str + line[4:]
        except:
            pass
        new_list.append(line)
        i = i + 1

    #找出選擇東華的同學
    new_new_list = []
    global selector_list
    for b in new_list:
        try:
            if b[1] in selector_list:
                new_new_list.append(b)
        except:
            pass

    #將結果輸出成'/學年/學年_系名.csv'
    output = open(
        '%s/%s_%s.csv' % (year, year, department[0]),
        'w',
        newline='',
        encoding='utf_8_sig')
    output_writer = csv.writer(output, delimiter=',')
    output_writer.writerow([
        '東華_系正備取', '准考證號碼', '考生姓名', '報考學校', '報考科系', '正備取', '申請年', '東華_系', '錄取碼'
    ])
    output_writer.writerows(new_list)

    #寫入all檔案
    file_all = open(
        'All/%s.csv' % year, 'a+', newline='', encoding='utf_8_sig')
    file_all_writer = csv.writer(file_all, delimiter=',')
    file_all_writer.writerows(new_list)
    file_all.close()

    #寫入ndhu檔案
    file_ndhu = open(
        'All_ndhu/%s_ndhu.csv' % year, 'a+', newline='', encoding='utf_8_sig')
    file_ndhu_writer = csv.writer(file_ndhu, delimiter=',')
    file_ndhu_writer.writerows(new_new_list)
    file_ndhu.close()

    #清除暫存資料
    crown_id = 0
    data_list.clear()
    new_list.clear()
    new_new_list.clear()
    crown_list.clear()
    selector_list.clear()
    meta.close()
    output.close()
    os.remove('meta.csv')


if __name__ == '__main__':

    #使用介面(輸入年份)
    start = getInput('Start with: ')
    anime()
    end = getInput('End with: ')
    title = [
        '東華_系正備取', '准考證號碼', '考生姓名', '報考學校', '報考科系', '正備取', '申請年', '東華_系', '錄取碼'
    ]
    anime()
    print('Processing...')
    anime()

    for year in range(int(start), int(end)+1):
        year = str(year)
        #建立all檔案
        pathlib.Path('All').mkdir(exist_ok=True)
        file_all = open(
            'All/%s.csv' % year, 'a+', newline='', encoding='utf_8_sig')
        title_writer = csv.writer(file_all, delimiter=',')
        title_writer.writerow(title)
        file_all.close()

        #建立ndhu檔案
        pathlib.Path('All_ndhu').mkdir(exist_ok=True)
        file_ndhu = open(
            'All_ndhu/%s_ndhu.csv' % year, 'wt', newline='', encoding='utf_8_sig')
        title_ndhu_writer = csv.writer(file_ndhu, delimiter=',')
        title_ndhu_writer.writerow(title)
        file_ndhu.close()

        #建立non_ndhu檔案
        pathlib.Path('All_non_ndhu').mkdir(exist_ok=True)
        file_non_ndhu = open(
            'All_non_ndhu/%s_non_ndhu.csv' % year, 'wt', newline='', encoding='utf_8_sig')
        title_non_ndhu_writer = csv.writer(file_non_ndhu, delimiter=',')
        title_non_ndhu_writer.writerow(title)
        file_non_ndhu.close()
        #迴圈處理整年度資料
        id = 34012
        for i in range(42):
            crown_list = []
            crown_id = 0
            selector_list = []
            idstr = str(id)
            print('%s-0%s' % (year ,idstr))
            ContentFetcher(year, '0%s' % idstr)
            id = id + 10

        #寫入non_ndhu檔案
        file_all = open('All/%s.csv' % year, 'rt', encoding='utf_8_sig')
        set_all = set(file_all.readlines())
        file_ndhu = open('All_ndhu/%s_ndhu.csv' % year, 'rt', encoding='utf_8_sig')
        set_ndhu = set(file_ndhu.readlines())
        list_non_ndhu = list(set_all - set_ndhu)
        file_non_ndhu = open(
            'All_non_ndhu/%s_non_ndhu.csv' % year, 'a+', encoding='utf_8_sig')
        file_non_ndhu_writer = csv.writer(file_non_ndhu)
        ix = 0
        for data in list_non_ndhu:
            data = data.replace('\n', '')
            list_non_ndhu[ix] = data.split(',')
            ix = ix + 1
        file_non_ndhu_writer.writerows(list_non_ndhu)
        file_non_ndhu.close()
    print('\nProcess Complete!\n\n')