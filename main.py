import os
import time
from logger import logger
from helpers import init_driver, click_element, load_page_with_retry, parse_car_row
from locators import LOCATORS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver.common.by import By
from helpers import init_driver



def run_script():
    start_time = time.time()
    driver = init_driver()
    cars = []

    try:
        if not load_page_with_retry(driver, "https://www.encar.com"):
            logger.error("Не удалось загрузить страницу. Прерывание выполнения.")
            return

        # Кликаем по фильтрам
        for step in ["manufact", "brand1", "series", "year", "search_button"]:
            click_element(driver, LOCATORS[step], f"Клик: {step}", 10)

        # Ждем таблицу с машинами
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[data-impression]")))

        rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-impression]")
        logger.info(f"Найдено {len(rows)} автомобилей")

        for row in rows:
            car_data = parse_car_row(row)
            if car_data:
                cars.append(car_data)

        if cars:
            keys = cars[0].keys()
            file_exists = os.path.isfile("cars.csv")

            with open("cars.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(cars)

            logger.info(f"✅ Данные сохранены ({len(cars)} записей)")

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()
        logger.info(f"Время работы: {time.time() - start_time:.2f} сек")

if __name__ == "__main__":
    run_script()