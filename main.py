

import sys
import time
import uuid

from PyQt6 import uic
from PyQt6.QtWidgets import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import translate
import googletrans

translator = googletrans.Translator()
translatorNG = translate.Translator(from_lang='en', to_lang='ru')


def parserAmazon(href):
    driver = webdriver.Chrome()
    driver.get(href)
    time.sleep(4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    allResult = soup.findAll('a',
                             class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

    allres = []
    print(len(allResult))
    for i in allResult:
        if len(allResult) == 1:
            break

        try:
            driver.get(f'https://www.amazon.com{i["href"]}')
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            price = soup.find('span',
                              attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})

            try:
                size = soup.findAll('span', attrs={
                    'class': 'a-button a-button-toggle text-swatch-button'
                })

                size = [
                    i.find('span', attrs={'class': 'a-size-base swatch-title-text-display swatch-title-text'}).text
                    for i in size]
            except:
                try:
                    size = soup.findAll('span', attrs={
                        'class': 'a-button a-button-toggle text-swatch-button'
                    })

                    size = [
                        i.find('span',
                               attrs={'class': 'a-size-base swatch-title-text-display swatch-title-text'}).text
                        for i in size]
                except:
                    break

            if price is None:
                try:
                    price = \
                        soup.findAll('span', attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'})[
                            0].text
                    if price is None:
                        price = None
                except:
                    price = None
            else:
                price = price.text

            desc = str('; '.join(
                [i.text for i in soup.findAll('span', {'class': 'a-list-item a-size-base a-color-base'})]).strip())
            try:
                image_item = soup.find('image', {'class': 'a-dynamic-image a-stretch-vertical'})['src']
            except:
                image_item = soup.find('image', {'class': 'a-dynamic-image a-stretch-horizontal'})['src']
            try:
                color = translator.translate(
                    soup.find('span', {'id': 'inline-twister-expanded-dimension-text-color_name'}).text.strip(),
                    src='en', dest='ru').text
            except:
                color = ' '

            art = str(uuid.uuid4())[:8]
            try:
                descipt = translator.translate(desc, src='en', dest='ru').text
            except:
                descipt = desc
            if len(size) > 1:
                for el in enumerate(size):
                    res = {
                        'art': art,
                        'art-m': art + '-' + str(el[0] + 1),
                        'link': f'https://www.amazon.com{i["href"]}',
                        'name': translator.translate(soup.find('span', {'id': 'productTitle'}).text.strip(),
                                                     src='en',
                                                     dest='ru').text,
                        'color': color,
                        'price': float(price.split('$')[1]) if price else 0,
                        'desc': descipt,
                        'size': el[1],
                        'image': image_item
                    }

                    allres.append(res)
            else:
                res = {
                    'art': art,
                    'art-m': art,
                    'link': f'https://www.amazon.com{i["href"]}',
                    'name': translator.translate(soup.find('span', {'id': 'productTitle'}).text.strip(), src='en',
                                                 dest='ru').text,
                    'color': color,
                    'price': float(price.split('$')[1]) if price else 0,
                    'desc': descipt,
                    'size': '',
                    'image': image_item
                }

                allres.append(res)
        except Exception as ex:
            print(ex)
            try:
                driver.get(f'https://www.amazon.com{i["href"]}')
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                price = soup.find('span',
                                  attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})

                try:
                    size = soup.findAll('span', attrs={
                        'class': 'a-button a-button-toggle text-swatch-button'
                    })

                    size = [
                        i.find('span', attrs={'class': 'a-size-base swatch-title-text-display swatch-title-text'}).text
                        for i in size]
                except:
                    try:
                        size = soup.findAll('span', attrs={
                            'class': 'a-button a-button-toggle text-swatch-button'
                        })

                        size = [
                            i.find('span',
                                   attrs={'class': 'a-size-base swatch-title-text-display swatch-title-text'}).text
                            for i in size]
                    except:
                        break

                if price is None:
                    try:
                        price = \
                            soup.findAll('span', attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'})[
                                0].text
                        if price is None:
                            price = None
                    except:
                        price = None
                else:
                    price = price.text

                desc = str('; '.join(
                    [i.text for i in soup.findAll('span', {'class': 'a-list-item a-size-base a-color-base'})]).strip())
                try:
                    image_item = soup.find('image', {'class': 'a-dynamic-image a-stretch-vertical'})['src']
                except:
                    image_item = soup.find('image', {'class': 'a-dynamic-image a-stretch-horizontal'})['src']
                try:
                    color = translator.translate(
                        soup.find('span', {'id': 'inline-twister-expanded-dimension-text-color_name'}).text.strip(),
                        src='en', dest='ru').text
                except:
                    color = ' '

                art = str(uuid.uuid4())[:8]
                try:
                    descipt = translator.translate(desc, src='en', dest='ru').text
                except:
                    descipt = desc
                if len(size) > 1:
                    for el in enumerate(size):
                        res = {
                            'art': art,
                            'art-m': art + '-' + str(el[0] + 1),
                            'link': f'https://www.amazon.com{i["href"]}',
                            'brand': translator.translate(soup.find('span', {'id': 'productTitle'}).text.strip(),
                                                         src='en',
                                                         dest='ru').text,
                            'name': translator.translate(soup.find('span', {'id': 'productTitle'}).text.strip(),
                                                         src='en',
                                                         dest='ru').text,
                            'color': color,
                            'price': float(price.split('$')[1]) if price else 0,
                            'desc': descipt,
                            'size': el[1],
                            'image': image_item
                        }

                        allres.append(res)
                else:
                    res = {
                        'art': art,
                        'art-m': art,
                        'link': f'https://www.amazon.com{i["href"]}',
                        'name': translator.translate(soup.find('span', {'id': 'productTitle'}).text.strip(), src='en',
                                                     dest='ru').text,
                        'color': color,
                        'price': float(price.split('$')[1]) if price else 0,
                        'desc': descipt,
                        'size': '',
                        'image': image_item
                    }

                    allres.append(res)
            except Exception as ex:
                print(ex)
                allres.append(None)

    driver.quit()
    return allres


def parserZalando(href):
    driver = webdriver.Chrome()
    driver.get(href)
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    allProducts = soup.findAll('div',
                               class_='_5qdMrS w8MdNG cYylcv BaerYO _75qWlu iOzucJ JT3_zV _Qe9k6')
    result = []
    for i in allProducts:
        link = i.find_next('a').attrs['href']

        if 'en.zalando.de/' in link:
            try:
                driver.get(link)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Фото товара
                imgList = soup.find_all('li', class_='LiPgRT DlJ4rT Zhr-fS')

                img = []
                for el in imgList:
                    img.append(el.find_next('img')['src'].replace('?imwidth=156', '').replace('&filter=packshot', ''))

                img = ', '.join(img)

                # Артикул
                art = str(uuid.uuid4())[:8]

                # Берём имя товара
                brandName = soup.find('h3', class_='FtrEr_ QdlUSH FxZV-M HlZ_Tf _5Yd-hZ').text.strip()
                productType = soup.find('span', class_='EKabf7 R_QwOV').text.strip().replace(' - ', ' ')

                # Берём цену товара в разных типах отображения
                try:
                    dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y')
                    if dirtPrice:
                        dirtPrice = dirtPrice.text
                    else:
                        dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y _65i7kZ').text
                    price = ''
                    for el in dirtPrice:
                        if el.isdigit():
                            price += el
                except:
                    dirtPrice = soup.find(class_='sDq_FX _4sa1cA FxZV-M HlZ_Tf')
                    if dirtPrice:
                        dirtPrice = dirtPrice.text
                    else:
                        dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y _65i7kZ')
                        if dirtPrice:
                            dirtPrice = dirtPrice.text
                    price = ''
                    for el in dirtPrice:
                        if el.isdigit():
                            price += el

                color = soup.find('span', class_='sDq_FX lystZ1 dgII7d HlZ_Tf zN9KaA').text.strip()

                # Описание
                desc = soup.find('div', class_='Z1Xqqm sb1S7G sKmkSN pMa0tB')
                dsup = BeautifulSoup(str(desc), 'html.parser')
                rdes = []
                for el in dsup.findAll('div')[0].find_all_next('div'):
                    rdes.append(el.text)

                time.sleep(1)
                # Соглашаемся только с важными Cookie
                try:
                    driver.find_element(By.ID, """uc-btn-deny-banner""").click()
                except:
                    print('No cookie attention')

                # Нажимаем кнопку разворота размеров
                pressSizeBtn = driver.find_element(By.ID, """picker-trigger""")

                try:
                    pressColorBtn = driver.find_element(By.XPATH,
                                                        """//*[@id="main-content"]/div[1]/div[1]/div[2]/x-wrapper-re-1-4[
                                                        1]/div[3]/div[2]/div[2]/ul[1]/li[6]/button[1]""")
                except:
                    pressColorBtn = None

                time.sleep(1)
                try:
                    driver.find_element(By.ID, """uc-btn-deny-banner""").click()
                except:
                    print('No cookie attention')

                pressSizeBtn.click()
                if pressColorBtn:
                    pressColorBtn.click()

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Вытягиваем все размеры
                allSize = soup.findAll('div', class_='KnR7WS _0xLoFW JT3_zV FCIprz LyRfpJ')
                sizes = []
                for el in allSize:
                    sup = BeautifulSoup(str(el), 'html.parser')
                    sizes.append(sup.findAll('span')[0].find_all_next('span')[0].text)
                # Вытягиваем цвет
                allColor = soup.findAll('li', class_='pl0w2g _5qdMrS _2ZBgf')
                allColorList = []

                for el in allColor:
                    if 'https://en.zalando.de/' in el.find_next('a').attrs['href']:
                        allColorList.append(el.find_next('a').attrs['href'])

                if len(sizes) > 1 and price != '':
                    productInfo = {
                        'art': art,
                        'art-m': art + '-1',
                        'link': link,
                        'brand': brandName,
                        'name': f'{brandName} - {productType}',
                        'price': float(price.replace(',', '.')) / 100,
                        'color': color.encode("utf-8"),
                        'size': sizes[0],
                        'desc': ' '.join(rdes[0:-1]).replace('\xa0', ' ').encode("utf-8"),
                        'image': img
                    }
                    sizes.pop(0)
                    result.append(productInfo)
                    for prod in enumerate(sizes):
                        driver.get(prod[1])

                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')

                        # Фото товара
                        imgList = soup.find_all('li', class_='LiPgRT DlJ4rT Zhr-fS')

                        img = []
                        for el in imgList:
                            img.append(
                                el.find_next('img')['src'].replace('?imwidth=156', '').replace('&filter=packshot', ''))

                        img = ', '.join(img)

                        # Берём имя товара
                        brandName = soup.find('h3', class_='FtrEr_ QdlUSH FxZV-M HlZ_Tf _5Yd-hZ').text.strip()
                        productType = soup.find('span', class_='EKabf7 R_QwOV').text.strip().replace(' - ', ' ')

                        # Берём цену товара в разных типах отображения
                        try:
                            dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y')
                            if dirtPrice:
                                dirtPrice = dirtPrice.text
                            else:
                                dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y _65i7kZ')
                                if dirtPrice:
                                    dirtPrice = dirtPrice.text

                            price = ''
                            for el in dirtPrice:
                                if el.isdigit():
                                    price += el
                        except:
                            dirtPrice = soup.find(class_='sDq_FX _4sa1cA FxZV-M HlZ_Tf')
                            if dirtPrice:
                                dirtPrice = dirtPrice.text
                            else:
                                dirtPrice = soup.find(class_='sDq_FX _4sa1cA dgII7d Km7l2y _65i7kZ')
                                if dirtPrice:
                                    dirtPrice = dirtPrice.text
                            price = ''
                            for el in dirtPrice:
                                if el.isdigit():
                                    price += el

                        color = soup.find('span', class_='sDq_FX lystZ1 dgII7d HlZ_Tf zN9KaA').text.strip()

                        # Описание
                        desc = soup.find('div', class_='Z1Xqqm sb1S7G sKmkSN pMa0tB')
                        dsup = BeautifulSoup(str(desc), 'html.parser')
                        rdes = []
                        for el in dsup.findAll('div')[0].find_all_next('div'):
                            rdes.append(el.text)

                        time.sleep(1)
                        # Соглашаемся только с важными Cookie
                        try:
                            driver.find_element(By.ID, """uc-btn-deny-banner""").click()
                        except:
                            print('No cookie attention')

                        # Нажимаем кнопку разворота размеров
                        pressSizeBtn = driver.find_element(By.ID, """picker-trigger""")

                        time.sleep(1)
                        try:
                            driver.find_element(By.ID, """uc-btn-deny-banner""").click()
                        except:
                            print('No cookie attention')

                        pressSizeBtn.click()
                        if price != '':
                            productInfo = {
                                'art': art,
                                'art-m': art + '-' + str(prod[0] + 2),
                                'link': link,
                                'brand': brandName,
                                'name': f'{brandName} - {productType}',
                                'price': float(price.replace(',', '.')) / 100,
                                'color': color.encode("utf-8"),
                                'size': sizes,
                                'desc': ' '.join(rdes[0:-1]).replace('\xa0', ' ').encode("utf-8"),
                                'image': img
                            }
                            result.append(productInfo)
                            print(productInfo)

                else:
                    if price != '':
                        productInfo = {
                            'art': art,
                            'art-m': art,
                            'link': link,
                            'brand': brandName,
                            'name': f'{brandName} - {productType}',
                            'price': float(price.replace(',', '.')) / 100,
                            'color': color.encode("utf-8"),
                            'size': sizes[0],
                            'desc': ' '.join(rdes[0:-1]).replace('\xa0', ' ').encode("utf-8"),
                            'image': img
                        }
                        result.append(productInfo)
                        print(productInfo)
            except Exception as ex:
                print('fail')

    print('1')
    print(result)
    return result


def writesv(dicti, file, percent, course):
    if dicti:

        f = open(file, 'w', encoding="utf-8")

        f.write('Артикул;Артикул модификации;Наименование;Цена;Закупочная цена;Количество;Размер;Цвет;Фото '
                'модификации;Вес в кг;Размеры в мм;URL адрес;Категория: 1;Категория: 2;Включен;Валюта;Фото '
                'товара;Свойство: Ткань;Свойство: Фасон;Ед. изм.;Скидка в процентах;Числовая скидка в валюте '
                'товара;Цена'
                'доставки;Краткое описание;Описание;SEO Titile;SEO Meta Keywords;SEO Meta Description;SEO H1;Артикулы '
                'связанных товаров;Артикулы альтернативных товаров;Видео;Новинка;Хит '
                'продаж;Рекомендованный;Распродажа;Ручной рейтинг товара;Производитель;Под заказ;Дополнительные '
                'опции;Теги;Подарки;Минимальное количество;Максимальное количество;Кратность '
                'количества;Штрихкод;Налог;Предмет расчета;Способ расчета;Товар для взрослых;Гарантия '
                'производителя;Яндекс.Маркет: Заметки для продажи;Яндекс.Маркет: Префикс;Яндекс.Маркет: Название '
                'товара;Яндекс.Маркет: Модель;Яндекс.Маркет: Обозначения размерных сеток;Яндекс.Маркет: Ставка для '
                'карточки модели;Яндекс.Маркет: Уцененный товар;Яндекс.Маркет: Состояние товара;Яндекс.Маркет: Причина '
                'уценки;Google Merchant: GTIN;Google Merchant: Категория товара;Авито: Свойства товара;Комплект '
                'товаров;Скидка на комплект товаров;тест\n')

        for data in dicti:
            if data:
                if 'cock' in data['color'].decode():
                    data['color'] = 'Черный'

                if data['desc'].decode() == '':
                    destcr = 'No info'
                else:
                    destcr = data['desc'].decode()

                f.write(
                    f"{data['art']};{data['art-m']};{translator.translate(data['name'], dest='ru').text};{data['price'] * percent * course};"
                    f"{data['price'] * course};1;{data['size']};{data['color'].decode()};;0;;{data['link']};Каталог >> Категория 1;;;RUB;"
                    f"{data['image']};;;;;;;;{translator.translate(destcr.replace(';', ' . '), dest='ru').text};;;;;;;;;;;;;{data['brand']};;;;;;1"
                    f";;;Без НДС;Товар;Полная предоплата;-;-;;;;;;0;-;;;;;;;;\n")

        f.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle('Parser')
        self.setFixedSize(550, 338)
        self.pushButton.clicked.connect(self.goparse)

        self.persent = float(f'1.{self.precentSpinBox.text()}')
        self.course = int(self.courseSpinBox.text())

    def goparse(self):
        hrf = self.lineEdit.text()
        if 'en.zalando.de' in hrf:
            res = parserZalando(hrf)
        else:
            res = parserAmazon(hrf)
        print('3')
        file = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".") + '/res.csv'

        try:
            writesv(res, file, self.persent, self.course)
            QMessageBox.information(self, "Успешно", "Результат в файле res.csv")
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Ошибка ", "Ошибка")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_app = MainWindow()
    main_app.show()

    sys.exit(app.exec())
