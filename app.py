from flask import Flask, render_template, request
from sentiment_analizer import Model
from amazon_api import Amazon

app = Flask(__name__)

model = Model()

positive_reviews = []
negative_reviews = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        amazon = Amazon(url)
        reviews = amazon.get_reviews()
        for i in reviews["reviews"]:
            result = model.predict_text(i)
            if result == 1:
                positive_reviews.append(result)
            else:
                negative_reviews.append(result)
        pos_percentage = (len(positive_reviews) / len(reviews)) * 100
        neg_percentage = (len(negative_reviews) / len(reviews)) * 100
        percentage_difference = abs(pos_percentage - neg_percentage)
        price = amazon.get_price()
        title = amazon.get_title()
        image = amazon.get_image()
        print(len(reviews))
        if percentage_difference > 20:
            if pos_percentage > neg_percentage:
                result=f"The reviews tell us that this product is received as relatively positive. Roughly {round(pos_percentage)}% \
of customers had a good experience with this product and {round(neg_percentage)}% found cavaets with it."
                return render_template("index.html", result=result, image=image, price=price, title=title, url=url)
            else:
                result=f"Most customers were unsatisfied with this product. About {round(neg_percentage)}% \
of customers had a negative experience, with {round(pos_percentage)}% of customers relatively content with their purchace"
                return render_template("index.html", result=result, image=image, price=price, title=title, url=url)
        else:
            result=f"The ratio of positive to negative oppinions aren't that far apart. {round(neg_percentage)}% \
of users found cavaets with this product and {round(pos_percentage)}% of users has positive things to say about their purchace"
            return render_template("index.html", result=result, image=image, price=price, title=title, url=url)
    else:
        return render_template("index.html")

if  __name__ == "__main__":
    app.run(debug=True)
