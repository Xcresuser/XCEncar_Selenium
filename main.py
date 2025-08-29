import time
from logger import logger
from helpers import init_driver, click_element, load_page_with_retry
from locators import LOCATORS


def run_script():
    start_time = time.time()
    driver = init_driver()

    try:
        # Загрузка страницы с повторными попытками
        if not load_page_with_retry(driver, "https://www.encar.com"):
            logger.error("Не удалось загрузить страницу. Прерывание выполнения.")
            return
        # Правильный порядок аргументов: driver, xpath, description, timeout
        click_element(driver, LOCATORS["manufact"], "Выбор производителя")
        click_element(driver, LOCATORS["brand"], "Выбор бренда")
        click_element(driver, LOCATORS["model"], "Выбор модели")
        click_element(driver, LOCATORS["year"], "Выбор года")
        click_element(driver, LOCATORS["search_button"], "Кнопка поиска")
        

        time.sleep(20)  # оставить, чтобы проверить результат

    except Exception as e:
        logger.error(f"Ошибка во время выполнения скрипта: {str(e)}")
        # Сохраняем скриншот для отладки
        try:
            driver.save_screenshot("error.png")
            logger.info("Скриншот ошибки сохранен как error.png")
        except:
            logger.error("Не удалось сохранить скриншот ошибки")
    finally:
        try:
            driver.quit()
            logger.info("Браузер закрыт")
        except:
            logger.warning("Не удалось корректно закрыть браузер")
        
        logger.info(f"Общее время выполнения: {time.time() - start_time:.2f} сек")


if __name__ == "__main__":
    run_script()