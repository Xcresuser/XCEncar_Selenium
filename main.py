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
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def run_script():
    start_time = time.time()
    driver = init_driver()
    cars = []

    try:
        logger.info("Запуск скрипта парсинга Encart")
        
        if not load_page_with_retry(driver, "https://www.encar.com"):
            logger.error("Не удалось загрузить страницу. Прерывание выполнения.")
            return

        logger.info("Страница успешно загружена")
        

        # Кликаем по фильтрам
        for step in ["manufact", "brand1", "series", "year", "search_button"]:
            if not click_element(driver, LOCATORS[step], f"Клик: {step}", 10):
                logger.error(f"Не удалось кликнуть на элемент: {step}")
                driver.save_screenshot(f"error_{step}.png")
                return
            time.sleep(1)  # Краткая пауза между кликами

        # Даем время на загрузку результатов
        logger.info("Ожидание загрузки результатов поиска...")
        time.sleep(3)
        
        # Проверяем загрузилась ли таблица
        logger.info(f"Текущий URL: {driver.current_url}")
       

        # Проверяем наличие модальных окон и закрываем их
        try:
            close_buttons = driver.find_elements(By.CSS_SELECTOR, ".modal-close, .btn-close, .popup-close")
            for close_button in close_buttons:
                if close_button.is_displayed():
                    close_button.click()
                    logger.info("Закрыто модальное окно")
                    time.sleep(1)
        except:
            pass  # Если нет модальных окон, продолжаем

        # Ждем таблицу с машинами
        wait = WebDriverWait(driver, 20)
        logger.info("Ожидание появления результатов...")
        
        try:
            # Проверяем наличие таблицы
            wait.until(EC.presence_of_element_located(("id", "sr_normal")))
            logger.info("Таблица с результатами найдена")
            
            # Ждем появления хотя бы одной строки с данными
            rows = wait.until(EC.presence_of_all_elements_located(("xpath", LOCATORS["car_list"])))
            logger.info(f"Найдено {len(rows)} автомобилей")
            
            # Парсим данные
            for i, row in enumerate(rows):
                logger.info(f"Обработка автомобиля {i+1}/{len(rows)}")
                car_data = parse_car_row(row)
                if car_data:
                    cars.append(car_data)
                # Делаем скриншот каждого 5-го автомобиля для отладки
                

        except TimeoutException:
            logger.error("Таблица с машинами не загрузилась в течение 20 секунд")
            driver.save_screenshot("timeout_error.png")
            return

        # Сохраняем данные в CSV
        if cars:
            keys = cars[0].keys()
            file_exists = os.path.isfile("cars.csv")

            with open("cars.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(cars)

            logger.info(f"✅ Данные сохранены в cars.csv ({len(cars)} записей)")
        else:
            logger.warning("Не найдено данных для сохранения")

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        import traceback
        logger.error(traceback.format_exc())
        driver.save_screenshot("critical_error.png")
    finally:
        driver.quit()
        logger.info(f"Время работы скрипта: {time.time() - start_time:.2f} сек")

if __name__ == "__main__":
    run_script()