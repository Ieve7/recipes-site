import pandas as pd
import pathlib
import sys,os
sys.path = sys.path + [os.path.abspath(os.path.dirname(__file__))]
RECIPES_PATH = r'recipes'
MAX_TITLE_LENGTH = 99

class cookbook:
    def __init__(self):
        self.pd = self.load()
        print('---------------------------------------------------------------------')
        print('---------------------------------------------------------------------')
        print(self.pd.index)

    def load(self):
        dict_recipes = {'date':[],'.html':[],'title':[],'tags':[],'image':[], 'hits':[]}
        index = []
        for item in pathlib.Path(RECIPES_PATH).iterdir():
            _,file = os.path.split(item)
            date,_ = file.split('_')[:2]
            dict_recipes['date'].append(date)
            index.append(file)
            dict_recipes['.html'].append(os.path.join(item,'recipe.html'))
            with open(os.path.join(item,'title.txt')) as fp:
                dict_recipes['title'].append(fp.read()[:MAX_TITLE_LENGTH])
            with open(os.path.join(item,'tags.txt')) as fp:
                dict_recipes['tags'].append(fp.read().lower().split(','))

            image_url = list(pathlib.Path(os.path.join(item,'image')).iterdir())[0]
            print(image_url)
            dict_recipes['image'].append(image_url)
            dict_recipes['hits'].append(0)
        return pd.DataFrame(dict_recipes,index=index)

    def locate_html(self,index):
        return str(self.pd.loc[index]['.html'])

    def locate_title(self,index):
        return str(self.pd.loc[index]['title'])

    def locate_image(self,index):
        return str(self.pd.loc[index]['image'])
    def locate_tags(self,index):
        return str(self.pd.loc[index]['tags'])

    def search(self,query):
        print(self.pd)
        array_hits = []
        for i in self.pd.index:
            hits = 0
            for search in query.lower().split():
                for tag in self.pd.loc[i]['tags'] + self.pd.loc[i]['title'].lower().split():
                    if search in tag:
                        hits += 1
                        break
            array_hits.append(hits)
        copy_pd = self.pd.copy()
        copy_pd['hits'] = array_hits
        copy_pd = copy_pd.sort_values(by=['hits'], ascending=False)
        copy_pd = copy_pd.reindex()
        print(copy_pd)
        return copy_pd

CookBook = cookbook()
