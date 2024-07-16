from dataclasses import dataclass
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from scraping.models import Restaurant


def init_driver():
    user_info = (
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_experimental_option("detach", True)  # Keep browser open
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking', 'enable-automation'])  # Disable popup
    options.add_argument("window-size=1200,800")  # Set window size larger
    options.add_argument("incognito")  # Incognito mode
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")  # Disable sandboxing
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    options.add_argument("--mute-audio")  # Mute audio
    options.add_argument(f"user-agent={user_info}")

    driver = webdriver.Chrome(options=options, service=service)
    return driver


def scroll(driver) -> None:
    """
    스크롤을 반복하여 모든 요소가 로드되도록 하는 함수
    https://uipath.tistory.com/136
    + ChatGPT
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            get_more_button = driver.find_elements(By.CSS_SELECTOR, 'div.search_result_place_body a.link_more')[-1]
            driver.execute_script("arguments[0].scrollIntoView(true);", get_more_button)
            action = ActionChains(driver).move_to_element(get_more_button)
            action.perform()
            get_more_button.click()
            print("스크롤중...")

            # 클릭 후 로딩을 위해 잠시 대기
            time.sleep(2)

            # 새로운 높이를 계산하여 끝에 도달했는지 확인
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("##############더 이상 스크롤 할 수 없습니다.##############")
                break
            last_height = new_height

        except IndexError:
            print("##############더 이상 '더보기' 버튼이 없습니다.##############")
            break
        except ElementClickInterceptedException:
            print("##############다른 요소가 클릭을 방해하고 있습니다. 다시 시도합니다.##############")
            driver.execute_script("arguments[0].scrollIntoView(true);", get_more_button)
            time.sleep(1)
            continue
        except Exception as e:
            print(f"##############예기치 않은 오류 발생##############: {e}")
            break

    print("##############스크롤 완료##############")


@dataclass
class RestaurantFields:
    restaurant_name = None
    restaurant_address = None
    review_count = None
    category = None
    star_rate = None
    thumbnail_image = None
    current_state = None
    phone_number = None


class KakaoMapScraper:

    def __init__(self):
        self.driver = init_driver()

    def save_html(self, html: str):
        with open("kakao_scraped.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Successfully saved html")

    def scrap(self, query: str):
        restaurant_fields = RestaurantFields()

        Restaurant.objects.all().delete()

        url = "https://m.map.kakao.com/"
        self.driver.get(url)
        print("##############페이지 로딩 대기##############")
        time.sleep(5)

        self.driver.find_element(By.ID, "innerQuery").send_keys(f"{query}")
        time.sleep(1)
        self.driver.find_element(By.ID, "innerQuery").send_keys(Keys.ENTER)
        print(f"##############{query}을 검색했습니다.##############")
        time.sleep(6)

        scroll(driver=self.driver)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.save_html(soup.prettify())
        restaurant_container = soup.find_all("li", class_="search_item")

        print(f"##############{len(restaurant_container)}##############")

        # Iterate through each restaurant item
        for index, restaurant in enumerate(restaurant_container):
            try:
                if restaurant.find(class_="tit_g"):
                    restaurant_fields.restaurant_name = restaurant.find(class_="tit_g").text.strip()

                if restaurant.find(class_="txt_g"):
                    restaurant_fields.restaurant_address = restaurant.find(class_="txt_g").text.strip()

                if restaurant.find(class_="txt_num"):
                    review_text = restaurant.find(class_="txt_num").text.replace('(', '').replace(')', '').strip()
                    restaurant_fields.review_count = int(review_text) if review_text.isdigit() else 0

                if restaurant.find(class_="txt_ginfo"):
                    restaurant_fields.category = restaurant.find(class_="txt_ginfo").text.strip()

                if restaurant.find(class_="num_rate"):
                    rate_text = restaurant.find(class_="num_rate").text.strip()
                    restaurant_fields.star_rate = float(rate_text) if rate_text.replace('.', '', 1).isdigit() else 0.00

                if restaurant.find(class_="img_result"):
                    restaurant_fields.thumbnail_image = restaurant.find(class_="img_result").get("src")

                if restaurant.find(class_="tag_openoff"):
                    restaurant_fields.current_state = restaurant.find(class_="tag_openoff").text.strip()

                if restaurant.get("data-phone"):
                    restaurant_fields.phone_number = restaurant.get("data-phone").strip()

                data = Restaurant.objects.create(
                    restaurant_name=restaurant_fields.restaurant_name,
                    restaurant_address=restaurant_fields.restaurant_address,
                    review_count=restaurant_fields.review_count,
                    category=restaurant_fields.category,
                    star_rate=restaurant_fields.star_rate,
                    thumbnail_image=restaurant_fields.thumbnail_image,
                    current_state=restaurant_fields.current_state,
                    phone_number=restaurant_fields.phone_number,
                )
                data.save()
                print(f"{index + 1}번째 식당 저장 성공: {restaurant_fields.restaurant_name}")

            except NoSuchElementException as e:
                print(f"{index + 1}번째 식당에서 요소를 찾을 수 없음: {e}")
            except TimeoutException as e:
                print(f"{index + 1}번째 식당에서 타임아웃 발생: {e}")
            except Exception as e:
                print(f"{index + 1}번째 식당에서 예기치 않은 오류 발생: {e}")

        self.driver.quit()


class Command(BaseCommand):
    help = 'Run the KakaoMapScraper to scrape data'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query for KakaoMap')

    def handle(self, *args, **kwargs):
        query = kwargs['query']
        scraper = KakaoMapScraper()
        scraper.scrap(query)
        self.stdout.write(self.style.SUCCESS('Successfully ran the scraper'))
