from radiologia import db

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    steps = db.relationship('Description', backref='exam', lazy='dynamic')
    #pictures = db.Column(db.String(160), nullable=True)

    def __repr__(self):
        return '<Exam %r>' % (self.name)


#cut off this
"""class Step(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    num = db.Column(db.Integer, nullable=False)
    translations = db.relationship('Description', backref='step', lazy='dynamic')

    def __repr__(self):
        return '<Step %r>' % (self.num)
        """

class Description(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    language = db.Column(db.String(8), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    audio = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Description in %r of %r>' % (self.language, self.exam)

    #TODO: fai dei modelli seri e comincia con una test suite.