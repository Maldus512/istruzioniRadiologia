from radiologia import app
from flask import render_template, request
from radiologia import babel, db
from radiologia.config import BaseConfig
from flask import jsonify
from flask import session
from radiologia import db, models
import json
import datetime
import os
from radiologia.utils import filemd5

@babel.localeselector
def get_locale():
    if not 'lang' in session:
        session['lang'] = request.accept_languages.best_match(BaseConfig.LANGUAGES.keys())
    return session['lang']


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    if not 'step' in session:
        session['step'] = 1
    if not 'lang' in session:
        session['lang'] = request.accept_languages.best_match(BaseConfig.LANGUAGES.keys())

    if request.method =='POST':
        if request.form and 'lang' in request.form:
            session['lang'] = request.form['lang']
            if session['step'] == 1:
                session['step'] = 2
        if request.form and 'exam' in request.form:
            session['exam'] = request.form['exam']
            if session['step'] == 2:
                session['step'] = 3

    if session['step'] == 1:
        return render_template("index.html", user="Maldus", title = "tesi patti",
                        languages=BaseConfig.LANGUAGES_LIST, locale=session['lang'])
    elif session['step'] == 2:
        exams = models.Exam.query.all()
        return render_template("index.html", user="Maldus", title = "tesi patti",
                        languages=BaseConfig.LANGUAGES_LIST, exams=exams, locale=session['lang'])
    elif session['step'] == 3:
        exams = models.Exam.query.all()
        translations = []
        if len(exams) > 0:
            exam = models.Exam.query.filter_by(id=session['exam']).first()
            steps = exam.steps.filter_by(language=session['lang']).first().description.split('\n\n')
            for s in steps:
                content = s.split('\n')
                translations.append(content)

        audio = "static/audio/promises.mp3"

        return render_template("index.html", user="Maldus", title = "tesi patti", exam=exam, audio=audio,
                        languages=BaseConfig.LANGUAGES_LIST, exams=exams, steps=translations, locale=session['lang'])

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/index/language', methods=['POST'])
def change_language():
    if request.form and 'lang' in request.form:
        session['lang'] = request.form['lang']
        session['step'] = 2
        return jsonify({'result':'success'})
    else:
        return jsonify({'result':'failure'})


@app.route('/update_exams', methods=['POST'])
def update_database():
    data = request.get_json()
    if data:
        models.clear_data(db.session)
        for exam in data:
            e = models.Exam(name=exam['name'])
            db.session.add(e)
            for desc in exam["steps"]:
                d = models.Description(language=desc['language'], description=desc['description'], exam=e)
                db.session.add(d)

        db.session.commit()
        #with open("/tmp/{}.json".format(datetime.datetime.now(), "w")) as f:
            #json.dump(data, f, indent=4)

        return jsonify({'result':'success'})
    else:
        return jsonify({'result':'failure', 'data':data})

@app.route('/audio_md5', methods=['GET'])
def get_audio_md5():
    data = request.get_json()
    response = []
    if data:
        for el in data:
            filename = os.path.join(app.config["AUDIODIR"], el["name"])
            if os.path.isfile(filename):
                local = filemd5(filename)
                remote = el["md5"]

                if local != remote:
                    el["servermd5"] = local
                    response.append(el)
            else:
                response.append(el)

        return jsonify({'result':'success', 'data':response})
    else:
        return jsonify({'result':'failure'})