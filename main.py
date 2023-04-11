from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    print(bool("True"))
    return render_template("index.html")
    


## HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = choice(all_cafes)
    random_cafe_data = random_cafe.to_dict()
    return jsonify(random_cafe_data)


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    all_cafes_data = [cafe.to_dict() for cafe in all_cafes]
    return all_cafes_data

@app.route(f"/search")
def locate_cafe():
    cafe = Cafe.query.filter_by(location=request.args.get("loc")).first()
    if cafe is None:
        message = {
            "error": {
                "not found": "Sorry, we could not find a cafe in the specified location"
            }
        }
        return jsonify(message)
    return(jsonify(cafe.to_dict()))

## HTTP POST - Create Record
@app.route("/addcafe", methods=["POST"])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name = request.form["name"],
            map_url = request.form["map_url"],
            img_url = request.form["img_url"],
            location = request.form["location"],
            seats = request.form["seats"],
            has_toilet = bool(request.form["has_toilet"]),
            has_wifi = bool(request.form["has_wifi"]),
            has_sockets = bool(request.form["has_sockets"]),
            can_take_calls = bool(request.form["can_take_calls"]),
            coffee_price = request.form["coffee_price"]
        )
        db.session.add(new_cafe)
        db.session.commit()
        message = {
            "success": {
                "message": "cafe added now"
            }
        }
        return jsonify(message)

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
