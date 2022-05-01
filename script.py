# seleniumの読み込み
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome() # WebDriverのインスタンスを作成
# スクレイピングを行いたいURL
search_link = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&rn=0573&ek=057321520&ek=057341280&ek=057305600&ek=057332110&ae=05731&cb=8.0&ct=11.0&mb=0&mt=9999999&md=05&md=06&md=07&et=10&cn=9999999&co=1&tc=0400601&tc=0400301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50'

driver.get(search_link) # URLを指定してブラウザを開く
time.sleep(2)
search_title = driver.find_element_by_tag_name('h1').text
search_title_text = search_title.split('の賃貸')

#メイン
buildingList = [["物件名", "立地", "家賃", "敷金", "礼金", "階数", "間取り", "リンク"]]

def getBuildingInfo(building_item):
    # 物件のタイトル
    building_title = building_item.find_element(By.CLASS_NAME, 'cassetteitem_content-title').text
    # 立地
    ricchi_desc = building_item.find_element(By.CLASS_NAME, 'cassetteitem_detail-col2').text
    ricchi = ricchi_desc.replace('\n', '・')

    # 賃料/管理費
    yachin_text = building_item.find_element(By.CLASS_NAME, 'cassetteitem_other-emphasis').text
    if yachin_text == '-':
        yachin = 0
    else:
        yachin_sep = yachin_text.split('万円')
        yachin = int(float(yachin_sep[0]) * 10000)

    kanri_text = building_item.find_element(By.CLASS_NAME, 'cassetteitem_price--administration').text
    if kanri_text == '-':
        kanri = 0
    else:
        kanri_sep = kanri_text.split('円')
        kanri = int(kanri_sep[0])

    fixed_cost = yachin + kanri

    # 敷金・礼金
    shiki_text = building_item.find_element(By.CLASS_NAME, 'cassetteitem_price--deposit').text
    if shiki_text == '-':
        shiki = 0
    else:
        shiki_sep = shiki_text.split('万円')
        shiki = int(float(shiki_sep[0]) * 10000)

    rei_text = building_item.find_element(By.CLASS_NAME, 'cassetteitem_price--gratuity').text
    if rei_text == '-':
        rei = 0
    else:
        rei_sep = rei_text.split('万円')
        rei = int(float(rei_sep[0]) * 10000)

    # 間取り
    madori = building_item.find_element(By.CLASS_NAME, 'cassetteitem_madori').text

    # 階
    kai_list = building_item.find_elements(By.CSS_SELECTOR, 'tr.js-cassette_link > td')
    kai = kai_list[2].text
    # 詳細リンク
    link_details = building_item.find_element(By.CLASS_NAME, 'js-cassette_link_href').get_attribute("href")

    buildingList.append([building_title, ricchi, fixed_cost, shiki, rei, kai, madori, link_details])


def getBuildings():
    building_container = driver.find_elements(By.XPATH, "//div[@id='js-bukkenList']/ul[@class='l-cassetteitem']")
    for buildings_list in building_container:
        items = buildings_list.find_elements(By.CSS_SELECTOR, "ul.l-cassetteitem > li")
        for building_item in items:
            getBuildingInfo(building_item)

getBuildings()
time.sleep(2)
driver.quit()

with open('chintai-01.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(buildingList)
