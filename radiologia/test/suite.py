import unittest
import radiologia 
from radiologia import db, app
import threading
import requests
import tempfile
import os
import json
from radiologia import models
from radiologia.radiologia import create_test_app
from radiologia.config import TestingConfig
import io


testfile = "zombie.mp3"

class TestGetMethods(unittest.TestCase):

    #def setUp(self):
        #self.server = threading.Thread(target=app.run, args=["127.0.0.1"])

    def setUp(self):
        #app = create_test_app()
        app.config.from_object(TestingConfig)
        #app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        #app.config['DEBUG'] = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            #os.path.join(app.config['BASEDIR'], 'test_db.db')
        db.init_app(app)
        app.app_context().push() # this does the binding
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        #mail.init_app(app)
        self.assertEqual(app.debug, False)
        """self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        #with app.app.app_context():
            #app.init_db()"""

    def tearDown(self):
        pass
        #os.close(self.db_fd)
        #os.unlink(app.app.config['DATABASE'])

    def test_getaudio(self):
        data = [
            {
                'name':'promises.mp3',
                'md5':'5c4a2544e338e1fa1ace39fbebbfa778'
            },
            {
                'name':'banana.mp3',
                'md5':'cacca'
            }
        ]
        res = self.app.get("/audio_md5", data=json.dumps(data), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_database(self):
        exams = models.Exam.query.all()
        self.assertEqual(len(exams), 0)
        res = self.app.post("/update_exams", data=json.dumps([{'name':'esame1test', 'steps':[{'language':"it",'description':"descrizione"}]}]), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        exams = models.Exam.query.all()
        self.assertEqual(len(exams), 1)
        res = self.app.post("/update_exams", data=json.dumps([{'name':'esame1test', 'steps':[{'language':"it",'description':"descrizione"}]}]), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        exams = models.Exam.query.all()
        self.assertEqual(len(exams), 1)


    def test_upload(self):
        with open(testfile, 'rb') as f:
            response = self.app.post('upload_audio', buffered=True,
                            content_type='multipart/form-data',
                            data={ 'file' : (io.BytesIO(f.read()), testfile)})
            print(response.data)
        


if __name__ == '__main__':
    unittest.main()