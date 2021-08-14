class Post:
    def __init__(self, likes_num, description, img_url):
        self.likes_num = likes_num
        self.description = description
        self.img_url = img_url

    def get_as_map(self):
        data_map = {"likes_num": self.likes_num, "description": self.description, "img_url": self.img_url}
        return data_map
