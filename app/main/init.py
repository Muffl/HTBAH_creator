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
    statlist = ['KK','AU','GE','IN','CH','MB','ATN','PA','ATD','INI','LE','GG']
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
    ('Mathematik','IN','IN','MB', 'Wissen')
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
