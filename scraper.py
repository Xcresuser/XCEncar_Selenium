import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ---------- ИНИЦИАЛИЗАЦИЯ ----------
chrome_options = Options()

chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.K3._.Model.%EB%8D%94%20%EB%89%B4%20K3%202%EC%84%B8%EB%8C%80.))))%22%7D")  # сюда можно поставить готовый URL с фильтрами

wait = WebDriverWait(driver, 10)
IMPRESSION_MAP = {

    "car_id": 0,
    "price": 1,
    "mileage": 2,
    "year": 3,
    "fuel": 4,
    "transmission": 5,
    "engine": 6,
    "region": 7,
    "color": 8,
    "registration": 9,
    "options": 10,
    "seller_type": 11,
    "seller_id": 12,
    "certified": 13,
    "accident": 14,
    "imported": 15,
    "auction_grade": 16,
    "auction_deductible": 17,
    "auction_note": 18,
}
rows = driver.find_elements(By.XPATH, "//tr[@data-impression]")
for row in rows:
    impression = row.get_attribute("data-impression")
    car_id = impression.split("|")[0] 

impression = row.get_attribute("data-impression").split("|")
car_info = {key: impression[idx] for key, idx in IMPRESSION_MAP.items()}

print(car_info["car_id"], car_info["price"])
# # ---------- ФАЙЛ ДЛЯ СОХРАНЕНИЯ ----------
# with open("cars.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Title", "Price", "Image", "Link"])  # заголовки CSV

    # page = 1
    # while True:
    #     print(f"Парсим страницу {page}...")

    #     # Ждём карточки
    #     try:
    #         wait.until(EC.presence_of_all_elements_located(("xpath", "//*[@id='rySch_result']/div[1]/div[6]/div[2]/table//*[@id='sr_normal']")))
    #     except TimeoutException:
    #         print("Карточки не найдены, выходим")
    #         break

    #     cars = driver.find_elements("xpath", "//*[@id='rySch_result']/div[1]/div[6]/div[2]/table//*[@id='sr_normal']")

    #     for car in cars:
    #         try:
    #             title = car.find_element("xpath", "//*[@id='sr_normal']/tr").text
    #             # price = car.find_element("xpath", ".//span[contains(@class,'pay')]").text
    #             # image = car.find_element("xpath", ".//img").get_attribute("src")
    #             # link = car.find_element("xpath", ".//a").get_attribute("href")

    #             writer.writerow([title, """ price, image, link """])
    #         except Exception as e:
    #             print("Ошибка парсинга карточки:", e)

        # ---------- ПРОВЕРКА НА СЛЕДУЮЩУЮ ----------
        # try:
        #     next_btn = driver.find_element(By.XPATH, "//a[@class='btn_next']")
        #     if "disabled" in next_btn.get_attribute("class"):
        #         print("Дальше страниц нет")
        #         break
        #     else:
        #         next_btn.click()
        #         page += 1
        #         time.sleep(2)
        # except NoSuchElementException:
        #     print("Кнопка 'следующая' не найдена")
        #     break

driver.quit()
