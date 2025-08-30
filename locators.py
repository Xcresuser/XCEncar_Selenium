#locators.py
# Все XPath вынесены в словарь
LOCATORS = {
    "manufact": "//*[@id='manufact']/a",
    "brand1": "//*[@id='manufactListText']/ul[1]/li[3]/a",
    "series": "//*[@id='seriesItemList']/li[9]/a",
    "year": "//*[@id='mdlItemList']/li[2]/a",
    "search_button": "//*[@id='indexSch1']/div[1]/a",
    "rows" : "//*[@id='sr_normal']",
    "car_list": "//*[@id='sr_normal']/tr[@data-impression]",
    "brand": ".//span[@class='cls']/strong",
    "model": ".//span[@class='cls']/em",
    "engine": ".//span[@class='dtl']/strong",
    "trim": ".//span[@class='dtl']/em",
    "registration_date": ".//span[@class='yer']",
    "mileage": ".//span[@class='km']",
    "fuel_type": ".//span[@class='fue']",
    "location": ".//span[@class='lo']",
    "price": ".//strong[@class='prc']",
    "url": ".//a[contains(@class,'newLink') and contains(@class,'_link')]",
    "image_url": ".//img[contains(@class,'thumb')]",
}
