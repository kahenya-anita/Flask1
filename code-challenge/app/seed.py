from app import app, db
from models import Hero, Power, HeroPower


def seed_heroes(heroes_data):
    print("🦸‍♀️ Seeding heroes...")
    for hero_data in heroes_data:
        hero = Hero(**hero_data)
        db.session.add(hero)
        db.session.commit()
    print("Hero seeding completed.")

def seed_powers(powers_data):
    print("🦸‍♀️ Seeding powers...")
    for power_data in powers_data:
        power = Power(**power_data)
        db.session.add(power)
    db.session.commit()
    print("Power seeding completed.")

def seed_hero_powers(hero_power_data ):
    print("🦸‍♀️ Seeding hero_powers...")
    for hero_power_data in heroes_power_data:
        hero_power_data = HeroPower(**hero_power_data)
        db.session.add(hero_power_data)
        db.session.commit()
        print("HeroPower seeding completed.")


if __name__ == '__main__':
  
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"}
        
    ]

    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    heroes_power_data = [
        {'strength': 'Average', 'hero_id': 1, 'power_id': 1},
        {'strength': 'Strong', 'hero_id': 2, 'power_id': 2},
        {'strength': 'Weak', 'hero_id': 3, 'power_id': 3},
        {'strength': 'Average', 'hero_id': 1, 'power_id': 4},
        {'strength': 'Strong', 'hero_id': 2, 'power_id': 5},
        {'strength': 'Weak', 'hero_id': 3, 'power_id': 6}
        # Add more hero power data here
    ]

    with app.app_context():
        seed_heroes(heroes_data)
        seed_powers(powers_data)
        seed_hero_powers(heroes_power_data)