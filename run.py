from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from helpers import init_driver
import time

# Инициализация драйвера
driver = init_driver()

def parse_car_row(row):
    """
    Парсит строку <tr> с данными о машине и возвращает словарь с данными.
    Использует точные CSS-селекторы для извлечения данных.
    """
    try:
        # Извлекаем данные из атрибута data-impression
        impression = row.get_attribute("data-impression") or ""
        impression_parts = impression.split("|")
        
        # Базовые данные из data-impression
        car_data = {
            "car_id": impression_parts[0] if len(impression_parts) > 0 else "",
            "price_impression": impression_parts[1] if len(impression_parts) > 1 else "",
        }
        
        # 1. Извлекаем бренд и модель
        try:
            brand_elem = row.find_element(By.CSS_SELECTOR, "span.cls strong")
            car_data["brand"] = brand_elem.text.strip()
        except NoSuchElementException:
            car_data["brand"] = ""
        
        try:
            model_elem = row.find_element(By.CSS_SELECTOR, "span.cls em")
            car_data["model"] = model_elem.text.strip()
        except NoSuchElementException:
            car_data["model"] = ""
        
        # 2. Извлекаем детали двигателя и комплектации
        try:
            engine_elem = row.find_element(By.CSS_SELECTOR, "span.dtl strong")
            car_data["engine"] = engine_elem.text.strip()
        except NoSuchElementException:
            car_data["engine"] = ""
        
        try:
            trim_elem = row.find_element(By.CSS_SELECTOR, "span.dtl em")
            car_data["trim"] = trim_elem.text.strip()
        except NoSuchElementException:
            car_data["trim"] = ""
        
        # 3. Извлекаем ДАТУ РЕГИСТРАЦИИ (23/01식)
        try:
            registration_elem = row.find_element(By.CSS_SELECTOR, "span.yer")
            car_data["registration_date"] = registration_elem.text.replace("식", "").strip()
        except NoSuchElementException:
            car_data["registration_date"] = ""
        
        # 4. Извлекаем ПРОБЕГ (26,933km)
        try:
            mileage_elem = row.find_element(By.CSS_SELECTOR, "span.km")
            mileage_text = mileage_elem.text.replace("·", "").replace("km", "").replace(",", "").strip()
            car_data["mileage"] = mileage_text
        except NoSuchElementException:
            car_data["mileage"] = ""
        
        # 5. Извлекаем ТИП ТОПЛИВА (가솔린 - бензин)
        try:
            fuel_elem = row.find_element(By.CSS_SELECTOR, "span.fue")
            fuel_text = fuel_elem.text.replace("·", "").strip()
            car_data["fuel_type"] = fuel_text
        except NoSuchElementException:
            car_data["fuel_type"] = ""
        
        # 6. Извлекаем МЕСТОПОЛОЖЕНИЕ (경기 - провинция Кёнги)
        try:
            location_elem = row.find_element(By.CSS_SELECTOR, "span.lo")
            location_text = location_elem.text.replace("·", "").strip()
            car_data["location"] = location_text
        except NoSuchElementException:
            car_data["location"] = ""
        
        # 7. Извлекаем ЦЕНУ (1,790만원)
        try:
            price_elem = row.find_element(By.CSS_SELECTOR, "strong.prc")
            price_text = price_elem.text.replace(",", "").replace("만원", "").strip()
            car_data["price"] = price_text
        except NoSuchElementException:
            car_data["price"] = car_data.get("price_impression", "")
        
        # 8. Извлекаем ССЫЛКУ на страницу автомобиля
        try:
            link_elem = row.find_element(By.CSS_SELECTOR, "a.newLink._link")
            car_data["url"] = link_elem.get_attribute("href")
        except NoSuchElementException:
            car_data["url"] = ""
        
        # 9. Извлекаем ссылку на ИЗОБРАЖЕНИЕ
        try:
            img_elem = row.find_element(By.CSS_SELECTOR, "img.thumb")
            car_data["image_url"] = img_elem.get_attribute("src")
        except NoSuchElementException:
            car_data["image_url"] = ""
        
        return car_data
        
    except Exception as e:
        print(f"Ошибка при парсинге карточки автомобиля: {e}")
        return None
       

# Основной код
# Основной код
try:
    # Переходим на страницу с автомобилями
    driver.get("https://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.K3._.Model.%EB%8D%94%20%EB%89%B4%20K3%202%EC%84%B8%EB%8C%80.))))%22%7D")
    
    # Ждем загрузки страницы
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-impression]")))
    
    time.sleep(3)
    
    # Находим все строки с данными об автомобилях
    car_rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-impression]")
    
    print(f"Найдено {len(car_rows)} автомобилей")
    
    # Парсим каждую строку
    for i, row in enumerate(car_rows):
        print(f"Обрабатываем автомобиль {i+1} из {len(car_rows)}")
        car_data = parse_car_row(row)
        if car_data:
            print(f"ID: {car_data.get('car_id', 'N/A')}")
            print(f"Бренд: {car_data.get('brand', 'N/A')}")
            print(f"Модель: {car_data.get('model', 'N/A')}")
            print(f"Двигатель: {car_data.get('engine', 'N/A')}")
            print(f"Комплектация: {car_data.get('trim', 'N/A')}")
            print(f"Дата регистрации: {car_data.get('registration_date', 'N/A')}")
            print(f"Пробег: {car_data.get('mileage', 'N/A')} km")
            print(f"Топливо: {car_data.get('fuel_type', 'N/A')}")
            print(f"Местоположение: {car_data.get('location', 'N/A')}")
            print(f"Цена: {car_data.get('price', 'N/A')} млн вон")
            print(f"URL: {car_data.get('url', 'N/A')}")
            print("---")
    
    input("Нажмите Enter для закрытия браузера...")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
finally:
    driver.quit()