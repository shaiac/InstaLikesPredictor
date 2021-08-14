
class InfluencerData:

    def __init__(self, username, following, followers, num_of_posts, profile_description, profile_image_url, posts):
        self.username = username
        self.following = following
        self.followers = followers
        self.num_of_posts = num_of_posts
        self.profile_description = profile_description
        self.profile_image_url = profile_image_url
        self.posts = posts

    def get_as_map(self):
        data_map = {"username": self.username, "following": self.following, "followers": self.followers,
                    "num_of_posts": self.num_of_posts, "profile_description": self.profile_description,
                    "profile_image_url": self.profile_image_url}
        posts_lst = []
        for post in self.posts:
            posts_lst.append(post.get_as_map())
        data_map["posts"] = posts_lst
        return data_map

