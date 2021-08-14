from instagram_scraping.objects.post import Post

POST_IMAGE_INDEX = 1


class PostsManager:
    def __init__(self, driver, max_posts):
        self.driver = driver
        self.max_posts = max_posts

    def get_posts_urls(self):
        hrefs_in_view = self.driver.find_elements_by_tag_name('a')
        # finding relevant hrefs
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                         if '.com/p/' in elem.get_attribute('href')]

        return hrefs_in_view

    def get_post_image_url(self):
        images = self.driver.find_elements_by_tag_name('img')
        images_urls = []  # image.get_attribute('src') for image in images
        for image in images:
            try:
                images_urls.append(image.get_attribute('src'))
            except:
                continue
        return images_urls

    def run_posts_flow(self):
        posts_urls = self.get_posts_urls()
        num_posts_to_scrap = self.max_posts
        if num_posts_to_scrap > len(posts_urls):
            num_posts_to_scrap = len(posts_urls)
        posts_list = []
        for i in range(num_posts_to_scrap):
            try:
                self.driver.get(posts_urls[i])
                likes = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span').text
                post_desc = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
                images_urls = self.get_post_image_url()
                post_image_url = images_urls[POST_IMAGE_INDEX]
                posts_list.append(Post(likes_num=likes, description=post_desc, img_url=post_image_url))
            except:
                # The post is a video
                continue

        return posts_list
