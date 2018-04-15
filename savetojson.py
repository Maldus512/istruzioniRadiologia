import json
import sys
from radiologia import models, db

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("arguments!")
        exit(1)


    with open(sys.argv[1], 'w') as f:
        data = []
        exams = models.Exam.query.all()
        for e in exams:
            print(e)
            steps = []
            for s in e.steps.all():
                print(s)
                steps.append({
                    "language": s.language,
                    "description": s.description
                })

            data.append( {
                "name":e.name,
                "steps": steps
            })

        json.dump(data, f, indent=4)
