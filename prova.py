import json
import sys
from app import models, db

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("arguments!")
        exit(1)


    with open(sys.argv[1], 'r') as f:
        clear_data(db.session)
        data = json.load(f)
        e = models.Exam(name=data['name'])
        db.session.add(e)
        for desc in data["steps"]:
            for line in desc['description'].split('\n'):
                d = models.Description(language=desc['language'], description=desc['description'], exam=e)
                db.session.add(d)

        db.session.commit()
