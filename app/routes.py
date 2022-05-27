import requests
from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from datetime import datetime
from app.models import City, FuncCity, db
from config import Config


main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


def get_time(data: dict):
    timezone = int(data.get('timezone'))
    timestamp = int(data.get('dt')) + timezone
    return int(datetime.utcfromtimestamp(timestamp).strftime('%H'))


def get_parts_day(data: dict):
    time = get_time(data=data)
    if 5 <= time < 12:
        return 'morning'
    elif 12 <= time < 18:
        return 'day'
    elif 18 <= time < 23:
        return 'evening'
    else:
        return 'night'


def get_weather_data(city_name: str):
    if city_name:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={Config.API_KEY}'
        param = {
            'units': 'metric'
        }
        response = requests.get(url=url, params=param)
        data = response.json()
        return process_data(data=data)


def process_data(data: dict):
        try:
            weather_data = {
                'city': data['name'].upper(),
                'state': data['weather'][0]['main'],
                'state_icon': data['weather'][0]['icon'],
                'temp': round(data['main']['temp']),
                'pressure': round(data['main']['pressure'] * 0.75),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed']),
                'date': datetime.now().strftime('%d.%m.%Y'),
                'part_of_day': get_parts_day(data=data)
            }
        except KeyError:
            return None
        return weather_data


def load_weather(city_name: str):
    if city_name:
        city = db.session.query(City).filter(City.name == city_name).first()
        if city:
            weather = {
                'id': city.id,
                'city': city.name.upper(),
                'state': city.state,
                'state_icon': city.state_icon,
                'temp': city.temp,
                'pressure': city.pressure,
                'humidity': city.humidity,
                'wind_speed': city.wind_speed,
                'date': city.date,
                'part_of_day': city.part_of_day
            }
        else:
            weather = None
        return weather


@main_bp.route('/', methods=['GET'])
def render_main():
    weather_list = []
    cities = FuncCity.get_cities()
    if cities:
        for city in cities:
            weather = load_weather(city.name)
            weather_list.append(weather)

    return render_template('index.html', weather_list=weather_list)


@main_bp.route('/add', methods=['POST'])
def render_add():
    if request.method == 'POST':
        city_name = request.form.get('city_name').lower()
        if not City.query.filter_by(name=city_name).first():
            weather = get_weather_data(city_name)
            if weather:
                if len(City.query.all()) < 6:
                    FuncCity.add_city(city_name, weather)
                else:
                    flash('You can add only 6 cities!')
            else:
                flash('The city doesn\'t exist!')
        else:
            flash('The city has already been added to the list!')
        return redirect(url_for('main_bp.render_main'))


@main_bp.route('/delete/<int:city_id>', methods=['POST'])
def render_delete(city_id):
    if request.method == 'POST':
        FuncCity.delete_city(city_id)
        return redirect(url_for('main_bp.render_main'))


@main_bp.route('/update/<int:city_id>', methods=['POST'])
def render_update(city_id):
    if request.method == 'POST':
        city_name = FuncCity.get_city_name(city_id=city_id)
        FuncCity.update_city(city_id=city_id, weather=get_weather_data(city_name=city_name))

        return redirect(url_for('main_bp.render_main'))