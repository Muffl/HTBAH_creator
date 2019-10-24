from flask import render_template, redirect, url_for
from app import db
from app.models import *
from app.main import bp

@bp.route('/init_system', methods=['GET', 'POST'])
def init_system():
    ### create Abilities_cat
    categorylist = ['Wissen','Soziales', 'Sportliches','Aktionen','Handwerk', 'Kampf']
    for item in categorylist:
        if db.session.query(Abilities_cat).filter(Abilities_cat.name==item).count() == 0:
            new_ac=Abilities_cat(name=item)
            db.session.add(new_ac)
            db.session.commit()

    ### create STas List
    statlist = ['KK','AU','GE','IN','CH','MB','ATN','PA','ATD','INI','LE','GG','--']
    for item in statlist:
        if db.session.query(stats_templates).filter(stats_templates.Stat==item).count() == 0:
            new_ac=stats_templates(Stat=item)
            db.session.add(new_ac)
            db.session.commit()

    ### create Abilites_tempalte
    abilitlist = [
    ('Chemie','IN','IN','MB', 'Wissen'),
    ('Physik','IN','IN','MB', 'Wissen'),
    ('Biologie','IN','IN','MB', 'Wissen'),
    ('Medizin','IN','IN','MB', 'Wissen'),
    ('Mathematik','IN','IN','MB', 'Wissen'),
    ('Meterologie','IN','MB','IN', 'Wissen'),
    ('Botanik','IN','IN','MB', 'Wissen'),
    ('Literatur','IN','IN','IN', 'Wissen'),
    ('Überlebenstechnik','IN','MB','MB', 'Wissen'),
    ('Urbanes Wissen','IN','MB','MB', 'Wissen'),
    ('Ländliches Wissen','IN','MB','MB', 'Wissen'),
    ('Beruhigen','CH','CH','IN', 'Soziales'),
    ('Manipulieren','CH','IN','IN', 'Soziales'),
    ('Bedrohen','CH','MB','MB', 'Soziales'),
    ('Überreden','IN','CH','CH', 'Soziales'),
    ('Betöhren','GE','IN','MB', 'Soziales'),
    ('Feilschen','CH','CH','CH', 'Soziales'),
    ('Lügen','CH','IN','IN', 'Soziales'),
    ('Menschenkenntnis','IN','IN','MB', 'Soziales'),
    ('Begeistern/Führen','CH','CH','MB', 'Soziales'),
    ('Laufen','AU','KK','AU', 'Sportliches'),
    ('Klettern','KK','AU','KK', 'Sportliches'),
    ('Schwimmen','KK','AU','AU', 'Sportliches'),
    ('Springen','KK','GE','AU', 'Sportliches'),
    ('Werfen','KK','KK','GE', 'Sportliches'),
    ('Balancieren','GE','GE','AU', 'Sportliches'),
    ('Erste Hilfe','IN','GE','GE', 'Aktionen'),
    ('Fahren','GE','GE','MB', 'Aktionen'),
    ('Reiten','GE','GE','AU', 'Aktionen'),
    ('Spurenlesen','IN','MB','MB', 'Aktionen'),
    ('Fliegen','MB','GE','GE', 'Aktionen'),
    ('Tiere Zähmen','CH','IN','MB', 'Aktionen'),
    ('Schlösser Knacken','GE','GE','IN', 'Aktionen'),
    ('Schleichen','GE','GE','AU', 'Aktionen'),
    ('Bogenbau','GE','GE','IN', 'Handwerk'),
    ('Schmieden','GE','KK','GE', 'Handwerk'),
    ('Tischlern','GE','GE','KK', 'Handwerk'),
    ('Maurern','KK','KK','GE', 'Handwerk'),
    ('Zeichnen','IN','IN','MB', 'Handwerk'),
    ('Mechanik','GE','IN','IN', 'Handwerk'),
    ('Nahkampfwaffe Spitz','--','--','--', 'Kampf'),
    ('Nahkampfwaffe Scharf','--','--','--', 'Kampf'),
    ('Nahkampfwaffe Stumpf','--','--','--', 'Kampf'),
    ('Wurfwaffen','--','--','--', 'Kampf'),
    ('Faustfeuerwaffen','--','--','--', 'Kampf'),
    ('Langwaffen','--','--','--', 'Kampf'),
    ('Spezialwaffen','--','--','--', 'Kampf'),
    ('Bogenschiessen','--','--','--', 'Kampf'),
    ('Faustkampf / Kampfkunst','--','--','--', 'Kampf'),
    ]
    for item in abilitlist:
        if db.session.query(Abilities_templates).filter(Abilities_templates.Name==item[0]).count() == 0:
            new_ac=Abilities_templates(Name=item[0],
                                 test01=db.session.query(stats_templates).filter(stats_templates.Stat==item[1]).first().id,
                                 test02=db.session.query(stats_templates).filter(stats_templates.Stat==item[2]).first().id,
                                 test03=db.session.query(stats_templates).filter(stats_templates.Stat==item[3]).first().id,
                                 category=db.session.query(Abilities_cat).filter(Abilities_cat.name==item[4]).first().id
            )
            db.session.add(new_ac)
            db.session.commit()

    return redirect(url_for('creator.creator_index'))
