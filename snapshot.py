from func_pac import *
from bs4 import BeautifulSoup

class Snapshot:
    def __init__(self, terms):
        self.terms = terms
        self.posts=make_snapshot(terms)
        

    def print_posts(self):
        for post in self.posts:
            print(post)

    def search_keyword(self, keyword):
        """
        Search for a keyword in the list of posts.

        :param posts: List of formatted posts
        :param keyword: Keyword to search for
        :return: List of posts containing the keyword
        """
        keyword = keyword.lower()
        matching_posts = [post for post in self.posts if keyword in post["content"].lower()]
        self.posts=matching_posts
    
    def find_pop(self):
        find_top_words(self.posts)
        find_pop_words(self.posts)

