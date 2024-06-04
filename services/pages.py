from config.config import *
from config.db import mongo
import json
from helpers_def.defs import base64_string_to_folder, random_string_code_generator, get_user_image_from_id, index_pagination, returns, \
    open_file, current_str_date, current_str_time, get_user_fullname_from_id, read_training, query_maker, validate, get_user_from_pin, request_type_check, error_base, \
    get_user_pin_from_id, current_full_sql_date, run_sql_with_transaction, current_full_obj_date, update_token_session, face_detect, internal_token, check_auth, director_user

# index====================================================================

index = Blueprint('index', __name__)


@index.route('/index', methods=['GET', 'POST'])
def index_function():
    # var
    output = []
    limit = 30
    offset = 0
    # db
    users = mongo.db.users
    user_list = list(users.find().sort('_id', DESCENDING))
    if request.method == "GET":
        # vars
        last_id = user_list[offset]['_id']
        output = index_pagination(collection=users, last_id=last_id, limit=limit)
        return render_template("index.html", user_list=output)
    else:
        # vars
        error = False
        data_request = request.json
        if 'offset' in data_request:
            offset = data_request['offset']
            limit = 15
            last_id = user_list[offset]['_id']
            output = index_pagination(collection=users, last_id=last_id, limit=limit)
        else:
            error = True
        status_code = 200 if error is False else 403
        return jsonify(output, status_code)


# capture====================================================================

work_log = Blueprint('workLog', __name__)


@work_log.route('/workLog', methods=['POST'])
def work_log_function():
    output = {"response": None}
    if request.method == "POST":
        request_data = request.json
        if 'type' in request_data and 'userId' in request_data:
            # db
            users_work_log = mongo.db.usersWorkLog
            # vars
            error = False
            message = "Ok."
            user_data = get_user_fullname_from_id(request_data['userId'])
            current_time_log = current_str_time()
            by_fin = request_data['byFin']
            # test
            fac_d = True if by_fin is False else face_detect(b64_img=request_data['image'])
            print('\n\n---------------------\nface detect:\t', fac_d, '\n---------------------\n\n')
            if fac_d:
                # sql
                sql_insert_schema = {
                    "pin": get_user_pin_from_id(request_data['userId']),
                    "datetime": "datetime",
                }
                print(current_full_sql_date())

                key_list = list(sql_insert_schema.keys())
                query_schema = []

                sql_table = "acc_face"
                list(map(lambda qs: query_schema.append({qs: sql_insert_schema[qs]}), key_list))
                query = query_maker(table=sql_table, values_and_rows=query_schema, type_query="insert", date_fields=True, date_elements=['datetime'])
                print('\n\n\n---------------\n\n\n', query, '\n\n\n---------------\n\n\n')
                result = run_sql_with_transaction(sql_query_list=[query], date_element=True, replace_with='GETDATE()')
                # sql
                if result['error'] is False:
                    # mongo

                    mdb_insert_schema = {
                        "fullDate": current_full_obj_date(),
                        "date": current_str_date(),
                        "time": current_time_log,
                        "userId": request_data['userId'],
                        "type": request_data['type'],
                        "byFin": by_fin
                    }

                    if by_fin is True and 'image' in request_data:
                        mdb_insert_schema.update({'image': request_data['image']})

                    insert_result = users_work_log.insert_one(mdb_insert_schema)
                    if insert_result is None:
                        error = True
                        message = "Not inserted"

                    # mongo
            else:
                message = 'faceDetectProblem'
                error = True
            output = {
                "response": {
                    "error": error,
                    "message": message,
                    "data": {
                        "user": user_data,
                        "time": current_time_log
                    }
                }
            }
    return jsonify(output)


# capture====================================================================

capture = Blueprint('capture', __name__)


@capture.route('/capture', methods=['GET', 'POST'])
def capture_function():
    response_data = False
    if request.method == "POST":
        b64image = request.json['b64image']
        b64image = b64image.replace("data:image/jpeg;base64,", "")
        img_name = random_string_code_generator(32)
        img_name = img_name + '.jpeg'
        full_path = 'temp/' + img_name
        base64_string_to_folder(base64_string=b64image, file_path=img_name, folder_name="temp")
        image_file = open(full_path, 'rb')
        files = {"captureImage": image_file}
        data = {"capture": True}
        # url = "https://qeydiyyat.asan.org:443/compare"
        # url = "https://192.168.35.39:443/compare"
        url = "http://localhost:9999/compare"
        resp = requests.post(url, files=files, data=data, verify=False)
        # return resp
        response_data = resp.text
        response_data = json.loads(response_data)
        response_data.update({"eventTime": current_str_time()})
        return jsonify(response_data)
    else:
        return render_template("capture.html", data_response=response_data)


# user====================================================================


user = Blueprint('user', __name__)


@user.route('/user/<user_id>', methods=['GET'])
def user_function(user_id):
    # db
    users = mongo.db.users
    # process & vars
    try:
        find_result = users.find_one({"_id": ObjectId(user_id)})
    except (bson.errors.InvalidId, ValueError):
        find_result = None
    if find_result is not None:
        name_user = find_result['firstName']
        last_name = find_result['lastName']
        image = find_result['imageList']
    else:
        return """
        <h1>User not found</h1><br>
        <a href='/index'>Go back</a>
        """
    return render_template("user.html", result=None, user_id=user_id, user_name=name_user, user_last_name=last_name,
                           picture=image)


# register====================================================================


register = Blueprint('register', __name__)


@register.route('/register', methods=['GET'])
def register_function():
    return render_template("register.html")
    # return redirect(url_for('/register'))


# notfound====================================================================


notfound = Blueprint('notfound', __name__)


@notfound.route('/notfound', methods=['GET'])
def notfound_function():
    return render_template("notfound.html")
    # return redirect(url_for('/register'))


# default====================================================================


default = Blueprint('default', __name__)


@default.route('/default', methods=['GET'])
def default_function():
    return render_template("default.html")
    # return redirect(url_for('/register'))


# root_pro====================================================================


root_pro = Blueprint('', __name__)


@root_pro.route('/', methods=['GET'])
def default_function():
    return render_template("default.html")
    # return redirect(url_for('/register'))


# compare====================================================================


compare = Blueprint('compare', __name__)


@compare.route('/compare', methods=['GET', 'POST'])
def compare_function():
    data_page = None
    if request.method == 'POST' and 'profileImage' in request.files and request.files['profileImage'] or request.method == 'POST' and 'captureImage' in request.files and request.files['captureImage']:
        # face recognition & vars
        file_key = 'captureImage' if 'captureImage' in request.files else 'profileImage' if 'profileImage' in request.files else None
        file = None if file_key is None else request.files[file_key]
        if file is not None:
            # train_faces(known_face_names=known_face_names, known_face_encodings=known_face_encodings)
            result_training = read_training()
            known_face_encodings = result_training["knownFaceEncoding"]
            known_face_names = result_training["knownFaceNames"]
            data_page = open_file(file=file, known_face_encodings=known_face_encodings, known_face_names=known_face_names)
            if data_page['foundId'] is not None:
                data_page['foundImage'] = get_user_image_from_id(data_page['foundId'])
    if 'profileImage' not in request.files and 'captureImage' in request.files:
        return jsonify(data_page)
    else:
        return render_template("compare.html", data_page=data_page)


# admin====================================================================


employees = Blueprint('admin/users', __name__)


@employees.route('/admin/users', methods=['GET'])
@internal_token
def employees_function():
    # var
    if session['userData'] is not None and session['userData']['authorityType'] in [2, 3]: return redirect('/admin/introduce', code=303)
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")

    output = []
    limit = 30
    offset = 0
    # db
    users = mongo.db.users
    user_list = list(users.find().sort('_id', DESCENDING))
    if request.method == "GET":
        # vars
        last_id = user_list[offset]['_id']
        output = index_pagination(collection=users, last_id=last_id, limit=limit)
        return render_template("admin/users.html", user_list=output, user_data=session['userData'])
    else:
        # vars
        error = False
        data_request = request.json
        if 'offset' in data_request:
            offset = data_request['offset']
            limit = 15
            last_id = user_list[offset]['_id']
            output = index_pagination(collection=users, last_id=last_id, limit=limit)
        else:
            error = True
        status_code = 200 if error is False else 403
        return jsonify(output, status_code)


# compare====================================================================


compare_user = Blueprint('admin/compare', __name__)


@compare_user.route('/admin/compare', methods=['GET', 'POST'])
@internal_token
def compare_user_function():
    if session['userData'] is not None and session['userData']['authorityType'] in [2, 3]: return redirect('/admin/introduce', code=303)
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")

    if request.method == 'POST' and 'file' in request.files:
        # vars
        result = {}
        files = request.files.getlist('file')
        # process
        if files is not None and len(files) > 0:
            result_training = read_training()
            known_face_encodings = result_training["knownFaceEncoding"]
            known_face_names = result_training["knownFaceNames"]
            found = list(map(lambda fi: open_file(file=fi, known_face_encodings=known_face_encodings, known_face_names=known_face_names), files))
            not_found = list(filter(lambda f: f['foundId'] is None, found))
            found = list(filter(lambda im: im['foundId'] is not None, found))
            list(map(lambda imn: imn.update(
                {'foundImage': get_user_image_from_id(imn['foundId']), 'parenStructure': get_user_fullname_from_id(imn['foundId'], True)['parenStructure']}),
                     found))
            result = {"foundEmployee": found, "notFoundEmployee": not_found}
            # returns 'person' 'tempFile' 'foundId' 'foundImage'
        return jsonify(result)
    else:
        return render_template("admin/compare.html", user_data=session['userData'])


# introduce====================================================================

introduce = Blueprint('/admin/introduce', __name__)


@introduce.route('/admin/introduce', methods=['GET'])
@internal_token
def introduce_function():
    # var
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")
    return render_template("admin/introduce.html", user_data=session['userData'])


# statistics====================================================================

statistics = Blueprint('statistics', __name__)


@statistics.route('/admin/statistics', methods=['GET'])
@internal_token
def statistics_function():
    # db
    if session['userData'] is not None and session['userData']['authorityType'] in [2, 3]: return redirect('/admin/introduce', code=303)
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")

    # users_work_log = mongo.db.usersWorkLog
    # # process
    # data_log = list(users_work_log.find({}, {"_id": 0}))
    # list(map(lambda us: us.update({'fullName': get_user_fullname_from_id(us['userId'])}), data_log))
    # return render_template("admin/statistics.html", workLogs=data_log)
    return render_template("admin/statistics.html", user_data=session['userData'])


# admin====================================================================

admin = Blueprint('admin/', __name__)


@admin.route('/admin/', methods=['GET'])
@internal_token
def admin_function():
    # var
    if session['userData'] is not None and session['userData']['authorityType'] in [2, 3]: return redirect('/admin/introduce', code=303)
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")

    return render_template("admin/users.html", user_data=session['userData'])


# admin====================================================================


director = Blueprint('director', __name__)


@director.route('/admin/director/', methods=['GET'])
@internal_token
def director_function(internal_token_schema=None):
    # var
    if session['userData'] is None or (session['userData'] is not None and session['userData']['authorityType'] not in [2, 3]): return redirect('/admin/', code=303)
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")
    user_data = director_user(user_pin=session['userData']['userName'], user_type=session['userData']['authorityType'], employee_list_add=False)
    user_data.update(session['userData'])
    return render_template("admin/director.html", user_data=user_data)


# login and create jwt=================================================================

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def login_func():
    warning = "" if session.get('signOut') else "İstifadəçi adı və ya şifrə daxil olunmayıb."
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username = request.form['username'].upper()
            password = request.form['password']
            password = password.upper() if password.upper() == username else password
            result = check_auth(user_name=username, password=password)
            if result is None:
                warning = "İstifadəçi tapılmadı."
            else:
                # auth = request.authorization
                token = jwt.encode({'user': username, 'authorityType': result['authorityType'], 'exp': datetime.utcnow() + timedelta(minutes=10)}, app.config['SECRET_KEY'])
                session['token'] = token
                session['logged'] = True
                session['userData'] = result
                session['signOut'] = False
                return redirect("/admin", code=303)
    else:
        if session.get('logged'):
            return redirect("/admin", code=303)
    # return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required."'})
    return render_template("admin/login.html", warning=warning)


# sign out====================================================================

sign_out = Blueprint('signOut/', __name__)


@sign_out.route('/signOut/', methods=['GET'])
@internal_token
def sign_out_function(internal_token_schema=None):
    # var
    session['token'] = None
    session['logged'] = False
    session['userData'] = None
    session['signOut'] = True
    return redirect('/login', code=303)


# find user by pin====================================================================


find_user_by_pin = Blueprint('findUserByPin', __name__)


@find_user_by_pin.route('/findUserByPin', methods=['POST'])
@internal_token
def find_user_by_pin_function(internal_token_schema=None):
    data_request = request.json
    validation = {'pin': 1555}
    type_validation = {'pin': [str]}
    output = None
    status = 'success'

    if internal_token_schema is not None and internal_token_schema['error'] is False:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)
        
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                # vars
                pin = data_request['pin']
                output = get_user_from_pin(pin)
                # print('***************\n\n\n', output, '\n\n\n***************')
        else:
            output = result['data']
            status = 'error'
        data_result = False if type(output) is not tuple else output[1]
    else:
        status_code = internal_token_schema['code']
        output = internal_token_schema['message']
        data_result = False if type(output) is not tuple else output[1]

    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output if type(output) is not tuple else output[0])
    return jsonify(output, status_code, data_result)


# know me====================================================================


know_user = Blueprint('knowUser', __name__)


@know_user.route('/knowUser', methods=['POST'])
@internal_token
def know_user_function(internal_token_schema=None):
    # var
    data_request = request.json
    validation = {'ImgB64': 404, 'userPin': 1404}
    type_validation = {'ImgB64': [str], 'userPin': [str]}
    status = 'success'
    output = None

    if internal_token_schema is not None and internal_token_schema['error'] is False:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                b64image = request.json['ImgB64']
                b64image = b64image.replace("data:image/jpeg;base64,", "")
                img_name = random_string_code_generator(32)
                img_name = img_name + '.jpeg'
                full_path = 'temp/' + img_name
                base64_string_to_folder(base64_string=b64image, file_path=img_name, folder_name="temp")
                image_file = open(full_path, 'rb')
                files = {"captureImage": image_file}
                data = {"capture": True}
                url = "https://192.168.35.39:443/compare"
                # url = "http://localhost:9999/compare"
                # url = "https://qeydiyyat.asan.org:443/compare"
                resp = requests.post(url, files=files, data=data, verify=False)
                # return resp
                response_data = resp.text
                response_data = json.loads(response_data)
                user_id = response_data['foundId']
                found_pin = user_id if user_id is None else get_user_pin_from_id(user_id)
                result = True if found_pin == data_request['userPin'] else False
                full_name = "Sistem sizi düzgün tanımadı. Sistemin sizi bənzətdiyi şəxs: " + str(response_data['person']) if result is False and user_id is not None else response_data['person']
                output = {'result': result, 'fullName': full_name}
            else:
                output = result['data']
                status = 'error'
    else:
        status_code = internal_token_schema['code']
        output = {'result': False, 'fullName': internal_token_schema['message']}
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# health =======================================================================

health = Blueprint('health', __name__)


@health.route('/health', methods=['GET'])
def health_func():
    # check MongoDB
    output = {}
    try:
        # apps.config['MONGO_DBNAME'] = 'offers'
        # apps.config['MONGO_URI'] = 'mongodb://offersAdmin:gHD3UcA3s177rf6A@10.9.20.23:27017/offers?authSource=offers'
        # mongo_db = PyMongo(apps)
        # mongo_db.db.list_collection_names()
        mongo.db.list_collection_names()
        output.update({'ok': 0.0, 'errmsgNOSQL': 'Ok', 'codeNOSQL': None, 'codeName': 'Success', 'error': False, 'style': 'text-success'})
    except pymongo.errors.OperationFailure as e:
        output = e.details
        output['errmsgNOSQL'] = str(output['errmsgNOSQL']).split("to execute command")[0]
        output['error'], output['style'] = True, "text-danger"
        print(type(e), str(e), e.details, sep="\n-------------------------------\n")
    except pymongo.errors.ServerSelectionTimeoutError as e:
        output = output.update({'errmsgNOSQL': str(e).split(", ")[0], 'error': True, 'style': "text-danger", "codeNOSQL": None})
        print(type(e), str(e), sep="\n-------------------------------\n")
    # check MsSQL
    try:
        conn = pyodbc.connect('DRIVER=SQL Server;SERVER=ITS-NB-047;PORT=1433;DATABASE=test;UID=sa;PWD=Aze1234567')
        cursor = conn.cursor()
        query = "SELECT pin FROM acc_face WHERE pin=?;"
        pin = '16KF91G'
        result = cursor.execute(query, pin)
        result = list(result.fetchone())[0]
        if result == pin:
            output.update({"errmsgSQL": "Ok", 'codeSQL': None})
        else:
            output.update({"errmsgSQL": list(set(result))[0], 'codeSQL': None})
    except pyodbc.Error as e:
        output.update({"errmsgSQL": e, 'codeSQL': None})
    return render_template("health/health.html", table_data=output)
