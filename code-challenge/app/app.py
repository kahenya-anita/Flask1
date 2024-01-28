from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import db, Hero, Power, HeroPower

app = Flask(__name__,
            static_url_path='',
            static_folder='../client/build',
            template_folder='../client/build'
            )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)



@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_one_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_all_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_one_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    description = data.get('description')

    if not description or len(description) < 20:
        return jsonify({'errors': ['validation errors']}), 400

    power.description = description
    try:
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or strength not in ['Strong', 'Weak', 'Average'] or not power_id or not hero_id:
        return jsonify({'errors': ['validation errors']}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'errors': ['validation errors']}), 400

    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    try:
        db.session.add(hero_power)
        db.session.commit()
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    app.run(port=5555)
