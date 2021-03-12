from flask import Flask, render_template, request, redirect, url_for, send_file
app = Flask(__name__)
from cookbook import CookBook

@app.route('/')
def home(): return render_template('search.html',cookbook=CookBook.pd.sort_values(by=['title','date']),searched=0)


@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'GET': return redirect(url_for('home'))
    query = request.form['query']
    if not query: return redirect(url_for('home'))
    hits = CookBook.search(query)
    return render_template('search.html',cookbook=hits,searched=1)


@app.route('/image/<index>')
def image(index):
    return send_file(CookBook.locate_image(index),mimetype='image/gif')


@app.route('/recipe/<index>')
def view_recipe(index):
    recipe = CookBook.locate_html(index)
    title = CookBook.locate_title(index)
    main_image = '/image/'+index
    tags = CookBook.locate_tags(index)
    return render_template('recipe_view.html',cookbook=None,
                                              recipe=recipe,
                                              title=title,
                                              main_image=main_image,
                                              tags=tags,
                                              open=open)

if __name__ == '__main__':
    app.run(debug=1)
