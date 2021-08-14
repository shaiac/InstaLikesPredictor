import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from posts_manager import PostsManager
from instagram_scraping.objects.influencer_data import InfluencerData

PROFILE_IMAGE_INDEX = 0


class InstaScrape:

    def __init__(self):
        self.driver = webdriver.Chrome('C:/Tools/Chrome Driver/chromedriver.exe')
        self.influencers = []
        self.bpreform_login = True
        self.posts_manager = PostsManager(driver=self.driver, max_posts=10)
        self.get_influencers_lst()

    def get_influencers_lst(self):
        with open("top_influencers.txt", "r") as file:
            content = file.read()
            self.influencers = content.split("\n")
        file.close()

    def iterate_all_influencer(self):
        for influencer_username in self.influencers:
            try:
                self.scrape(influencer_username=influencer_username)
            except:
                print(f"Error in reading {influencer_username} data")
                continue

    @staticmethod
    def write_to_json_file(influencer: InfluencerData):
        json_string = json.dumps(influencer.get_as_map())
        with open(f"influencer_data/{influencer.username}.json", 'w+') as file:
            # file.write(json_string)
            json.dump(influencer.get_as_map(), file, indent=4)
            file.close()

    def preform_login(self):
        self.driver.get("https://www.instagram.com/")

        # Login
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        password.clear()
        username.send_keys("ronr94440@gmail.com")
        password.send_keys("Roniron123")
        log_in = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),"
                                                                                             " 'Not Now')]"))).click()

    def scrape(self, influencer_username):
        if self.bpreform_login:
            self.preform_login()
            self.bpreform_login = False
        # Searching instagram user
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        search_box.clear()

        search_box.send_keys(influencer_username)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.ENTER)

        # Letting the page load
        time.sleep(4)

        # Geting number of followers
        followers = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
        print(followers)

        # Getting number of posts
        num_of_posts = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text
        print(num_of_posts)

        # Getting number of following
        following = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        print(following)

        # Getting profile description
        profile_description = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/div[2]').text
        print(profile_description)

        # Getting profile image url
        images = self.driver.find_elements_by_tag_name('img')
        profile_image_url = images[PROFILE_IMAGE_INDEX].get_attribute('src')

        # Posts
        posts_list = self.posts_manager.run_posts_flow()

        influencer_data = InfluencerData(username=influencer_username, following=following, followers=followers,
                                         num_of_posts=num_of_posts, profile_description=profile_description,
                                         profile_image_url=profile_image_url, posts=posts_list)

        self.write_to_json_file(influencer=influencer_data)



