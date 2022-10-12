from flask import Flask, render_template
from datetime import date
import models
from models import *
app = Flask(__name__)
session = Session()


@app.route("/api/v1/hello-world-<int:id>")
def hello(id):
    hello = "Hello World " + str(id)
    return render_template("index.html", hello=hello)


def test():
    #test1 = User(id_user = 1, username = 'test', first_name = 'test', last_name = 'test', age = 18, email = 'test@gmail.com', password = '12345', phone_number = '888333', userstatus= "user" )
    #test2 = Category(id_category = 1, category_name= 'test', description= 'test')
    #test3 = Medicine(id_medicine = 1, medicine_name = "test", manufacturer = "test", medicine_description = 'test', category_id = 1, price = 10, medicine_status= "available", demand=False)
    #test4 = Order(id_order = 1, user_id = 1, address = "test", date_of_purchase = "2022-10-05 18:32:54", shipData=date.today(), order_status="placed", complete = False)
    #test5 = Order_details.insert().values(order_id = 1, medicine_id=1, count=8)
    #session.add(test1)
    #session.commit()
    #session.add(test2)
    #session.commit()
    #session.add(test3)
    #session.commit()
    #session.add(test4)
    #session.commit()
    #session.execute(test5)
    #session.commit()
    #sql1 = delete(User).where(User.id_user == 1)
    #session.execute(sql1)
    #session.commit()
    #session.close()
    #waitress-serve --port=8080 --url-scheme=http main:app
test()
if __name__ == '__main__':
    app.run(debug=True)