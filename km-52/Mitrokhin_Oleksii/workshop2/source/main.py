"""
Тут написати умову до завдання
"""
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/api/<action>, methods = [ 'GET'])
def api_get(action):
    if action = "user_product":
        return render_template("user_product.html", user_product=user_product_dictionary)
    elif action = "available_product":
        return render_template("available_product.html", available_product=available_product_dictionary)
    elif action = "all":
        return render_template("all.html")
    else:
        return render_template("404.html")


@app.route('/api', methods=['POST'])
def api_post():
    if request.form["action"] == "user_product_update":
        user_product_dictionary["product_id"] = request.form["product_id"]
        return redirect(url_for('api_get', action="all"))


if __name__ == '__main__':

    user_product_dictionary = {
        "product_id": "1",
        "purchase_date": "19.11.2018",
        "user_product_price": "0.76",
        "product_count": "10",
        "product_prioity": "Medium"
    }

    available_product_dictionary ={
        "product_name": "Prod1",
        "product_average_price": "0.79"
    }

    app.run()



if __name__ == "__main__":
    #TODO
