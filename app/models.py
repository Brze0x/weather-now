from app import db


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    state_icon = db.Column(db.String(10), nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(30), nullable=False)
    part_of_day = db.Column(db.String(30), nullable=False)


class FuncCity:
    @staticmethod
    def get_cities():
        cities = db.session.query(City).all()
        return cities


    @staticmethod
    def get_city_name(city_id: int):
        city = City.query.filter_by(id=city_id).first()
        return city.name


    @staticmethod
    def add_city(city_name: str, weather: dict):
        city = City(
            name=city_name, 
            state=weather['state'],
            state_icon=weather['state_icon'], 
            temp=weather['temp'], 
            pressure=weather['pressure'],
            humidity=weather['humidity'],
            wind_speed=weather['wind_speed'],
            date=weather['date'],
            part_of_day=weather['part_of_day']
            )
            
        if city_name not in [city.name for city in FuncCity.get_cities()]:
            db.session.add(city)
            db.session.commit()


    @staticmethod
    def update_city(city_id: int, weather: dict):
        city = City.query.filter_by(id=city_id).first()
        city.state = weather['state']
        city.state_icon = weather['state_icon']
        city.temp = weather['temp']
        city.pressure = weather['pressure']
        city.humidity = weather['humidity']
        city.wind_speed = weather['wind_speed']
        city.date = weather['date']
        city.part_of_day = weather['part_of_day']
        db.session.commit()


    @staticmethod
    def delete_city(city_id: int):
        city = City.query.filter_by(id=city_id).first()
        db.session.delete(city)
        db.session.commit()