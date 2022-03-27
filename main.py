from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1602144106:AAH1pIF5VqQemLTuaIyt9PduMS4lqkJokCU'
logging.basicConfig(level=logging.INFO)
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

knife_ak47 = input('название оружия: ')

driver = webdriver.Chrome()
driver.get("https://steamcommunity.com/market/search?appid=730")
time.sleep(1)
driver.maximize_window()
element = driver.find_element(By.XPATH, '//*[@id="market_search_advanced_show"]/div')  # выбор элемента html
element.click()
start = driver.find_element(By.XPATH, '//*[@id="tag_730_Quality_strange"]')
start.click()
input = driver.find_element(By.XPATH, '//*[@id="advancedSearchBox"]')
input.send_keys(knife_ak47)
poisk = driver.find_element(By.XPATH, '//*[@id="advancedSearchSubmit"]')
poisk.click()
prise = driver.find_element(By.XPATH, '//*[@id="searchResultsRows"]/div/div[1]/div[1]')
prise.click()
new_url = driver.current_url  #мой url в данный момент
print(new_url)
time.sleep(2)

# gun_name1 = input()
# skin_name1 = 'Безлюдный космос'
# wear_name1 = 'После полевых испытаний'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6',
}
steam_link = (new_url)
full_page = requests.get(steam_link, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
skins = soup.find_all('a',class_='market_listing_row_link')


def even_only(skins):
    for skin in skins:
        name = skin.find('span', class_='market_listing_item_name').text  # Название скина
        counts = skin.find('span', class_='market_listing_num_listings_qty').text  # Сколько есть в продаже
        price = skin.find('span', class_='sale_price').text.replace('От', '').strip()  # Цена
        print(f'{name}: {counts}- {price}')
        return


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(even_only(skins))




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

