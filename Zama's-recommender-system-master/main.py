from flask import Flask, render_template, request
import pandas as pd
import numpy as np

with open('popular.pkl', 'rb') as f:
    popular_df = pd.read_pickle(f)

with open('pt.pkl', 'rb') as f:
    pt = pd.read_pickle(f)

with open('books.pkl', 'rb') as f:
    books = pd.read_pickle(f)

with open('similarity_scores.pkl', 'rb') as f:
    similarity_scores = pd.read_pickle(f)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(
                               popular_df['avg_rating'].values.round()),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


#
# class recommend_books(index):
#     user_input = index("data", validators=[index(), similarity_scores()])


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    data = []

    user_input = request.form['user_input']
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Image-URL-M'].values))

            data.append(item)

            print(data)

    # index = books.index(user_input)
    except:
        error_message = f"Book '{user_input}' not found in dataset, Please try searching for some known book. For e.g. Beloved"
        print(error_message)
        return render_template('recommend.html', error=error_message)

    return render_template('recommend.html', data=data)

@app.route('/about')
def about_ui():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
