import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import os
from logger import logger
from locators import LOCATORS


def init_driver():
    """Инициализация Chrome WebDriver с улучшенными настройками"""
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Дополнительные опции для стабильности
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-notifications')
    
    # Опции для ускорения загрузки
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # Блокировать изображения для ускорения
            'javascript': 1,  # Разрешить JavaScript
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)

    service = Service(executable_path="chromedriver.exe", log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)  # Увеличиваем таймаут до 60 секунд
    return driver


def load_page_with_retry(driver, url, max_attempts=3):
    """Загрузка страницы с повторными попытками"""
    for attempt in range(max_attempts):
        try:
            logger.info(f"Попытка {attempt+1} загрузки страницы: {url}")
            driver.get(url)
            logger.info("Страница успешно загружена")
            return True
        except TimeoutException:
            if attempt == max_attempts - 1:
                logger.error(f"Все {max_attempts} попытки загрузки страницы завершились таймаутом")
                return False
            logger.warning(f"Таймаут при загрузке страницы. Попытка {attempt+2} через 5 секунд...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Ошибка при загрузке страницы: {str(e)}")
            return False
    return False


def click_element(driver, xpath: str, description: str, timeout: int = 8):

    """Кликает по элементу с ожиданием"""
    start = time.time()
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(("xpath", xpath))
        ).click()
        logger.info(f"{description} найден и кликнут за {time.time() - start:.2f} сек")
        return True
    except TimeoutException:
        logger.error(f"Таймаут: {description} ({xpath})")
        return False
    except NoSuchElementException:
        logger.error(f"Элемент не найден: {description} ({xpath})")
        return False
    except WebDriverException as e:
        logger.error(f"Ошибка WebDriver при клике {description}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при клике {description}: {str(e)}")
        return False
def parse_car_row(row):
    """Парсит строку с данными о машине"""
    car_data = {
        "car_id": row.get_attribute("data-carid") or "",
        "brand": get_text_safe(row, LOCATORS["brand"]),
        "model": get_text_safe(row, LOCATORS["model"]),
        "engine": get_text_safe(row, LOCATORS["engine"]),
        "trim": get_text_safe(row, LOCATORS["trim"]),
        "registration_date": get_text_safe(row, LOCATORS["registration_date"]).replace("식", ""),
        "mileage": get_text_safe(row, LOCATORS["mileage"]).replace("km", "").replace(",", "").strip(),
        "fuel_type": get_text_safe(row, LOCATORS["fuel_type"]),
        "location": get_text_safe(row, LOCATORS["location"]),
        "price": get_text_safe(row, LOCATORS["price"]).replace(",", "").replace("만원", "").strip(),
        "url": get_attr_safe(row, LOCATORS["url"], "href"),
        "image_url": get_attr_safe(row, LOCATORS["image_url"], "src"),
    }
    return car_data



def get_text_safe(row, xpath):
    """Возвращает текст элемента по XPath или пустую строку"""
    try:
        return row.find_element("xpath", xpath).text.strip()
    except NoSuchElementException:
        return ""

def get_attr_safe(row, xpath, attr):
    """Возвращает атрибут элемента по XPath или пустую строку"""
    try:
        return row.find_element("xpath", xpath).get_attribute(attr)
    except NoSuchElementException:
        return ""