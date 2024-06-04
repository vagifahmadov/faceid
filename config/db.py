from config.config import app, PyMongo, pyodbc

app.config['MONGO_URI'] = 'mongodb://192.168.177.8:27017/face'
# app.config['MONGO_URI'] = 'mongodb://192.168.180.10:27017/face'
# app.config['MONGO_URI'] = 'mongodb://10.9.20.20:27017/face'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/face'
# app.config['MONGO_URI'] = 'mongodb://admin:Aze1234567@ds121495.mlab.com:21495/face'
mongo = PyMongo(app)

# app.config['MONGO_URI'] = 'mongodb://10.9.20.20:27017/helpDesk'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/helpDesk'
mongo_config = PyMongo(app)

# app.config['MONGO_URI'] = 'mongodb://10.9.20.20:27017/emotionBase'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/emotionBase'
mongo_emotion_base = PyMongo(app)

# con_mssql = pyodbc.connect('DRIVER={SQL Server};SERVER=ITS-NB-047;DATABASE=test;UID=sa;PWD=Aze1234567')
# con_mssql = pyodbc.connect('DRIVER={SQL Server};SERVER=172.23.45.1;DATABASE=hr;UID=AppUserFace;PWD=N7?fT4NC!0vu26?3Isg2g+f9Y#p0L32x5!Jz+Xyd')
# con_mssql = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.23.45.1;PORT=1433;DATABASE=HR;UID=AppUserFace;PWD=N7?fT4NC!0vu26?3Isg2g+f9Y#p0L32x5!Jz+Xyd')
# mssql = con_mssql.cursor()
