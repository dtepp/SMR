import tagui as r
import pandas as pd

Major_name = 'Not Found'
Uni_name = 'Not Found'
Apply_req = 'Not Found'
Lang_req = 'Not Found'
Fee = 'Not Found'

def click_next_page(num):
    for n in range(1, num + 1):
        if r.read(f'(//div[@class="ym_bj zydb_ym"]/a/span)[{n}]') == "下一页":
            r.click(f'(//div[@class="ym_bj zydb_ym"]/a/span)[{n}]')
            break
        else:
            continue


def store_data(num, data):
    global Major_name
    global Uni_name
    global Apply_req
    global Lang_req
    global Fee
    Major_name = r.read("//table[@class='zylb1_xxnr']/tbody/tr[2]/td[2]")
    Uni_name = r.read("//table[@class='zylb1_xxnr']/tbody/tr[3]/td[2]")
    for i in range(5, 8):
        if r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[1]") == "申请要求":
            Apply_req = r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[2]")
            break
    for i in range(6, 9):
        if r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[1]") == "语言要求":
            Lang_req = r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[2]")
            break
    for i in range(10, num + 1):
        if r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[1]") == "预估费用":
            Fee = r.read(f"//table[@class='zylb1_xxnr']/tbody/tr[{i}]/td[2]")
            break
    data.append({'Major Name': Major_name, 'Uni Name': Uni_name, 'Apply req': Apply_req, 'Lang req': Lang_req, 'Fee': Fee})
    Major_name = 'Not Found'
    Uni_name = 'Not Found'
    Apply_req = 'Not Found'
    Lang_req = 'Not Found'
    Fee = 'Not Found'


data = []
r.init()
r.url('https://www.nanxingjiaoyu.com/xxzy/')
r.wait(3)
total_page = 2500
linknumber = r.count('//div[@class="ym_bj zydb_ym"]/a')
for j in range(1, total_page + 1):
    print(j)
    current_page_num = r.count('//div[@class="zydb_zy"]')
    r.wait(1)
    for i in range(1, current_page_num + 1):
        r.click(f'(//div[@class="zydb_zy"]//span)[{i}]')
        r.wait(2)
        table_num = r.count("//table[@class='zylb1_xxnr']/tbody/tr/td/b")
        r.wait(3)
        print(table_num)
        store_data(table_num, data)
        print('success')
        if j == 1:
            r.url('https://www.nanxingjiaoyu.com/xxzy/')
        else:
            r.url(f'https://www.nanxingjiaoyu.com/xxzy/index_{j}.html')
    click_next_page(linknumber)

r.close()

df = pd.DataFrame(data)
df.to_excel("file.xlsx", index=False)