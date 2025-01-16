from func_pac import *

class Snapshot:
    def __init__(self, terms):
        self.terms = terms
        self.posts=make_snapshot(terms)
        

    def print_posts(self):
        for post in self.posts:
            print(post)

    def search_keyword(self, keyword):
        """
        changes structure of object posts
        by filtering out posts that do not contain keyword
        useful to combine with find_pop
        can be used multiple times to progressively filter posts
        """
        keyword = keyword.lower()
        matching_posts = [post for post in self.posts if keyword in post["content"].lower()]
        self.posts=matching_posts
    
    def find_pop(self):
        find_top_words(self.posts)
        find_pop_words(self.posts)

