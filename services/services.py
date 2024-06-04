from config.config import *
from config.token_utils import checkToken
from helpers_def.defs import returns, validate, search_employee, error_base, check_token_access, for_test_token, request_type_check, general_training, \
    read_training, sync_employee, get_user_fullname_from_id, get_user_obj_id_from_id, get_user_from_pin, check_auth, \
    percent_count, get_user_object_id_by_pin, monthly_percent_statistics, monthly_statistics, pin_not_pin_monthly_percent_count, \
    detect_and_train, read_people_training, selected_face_recognition, face_recognition_deep_face, face_verify_deep_face, obj_date_to_str_date, ip_validation, \
    update_token_session, internal_token, get_employee_work_log_statistics, director_user
from config.db import mongo, mongo_emotion_base

# insert====================================================================


insert = Blueprint('insert', __name__)


@insert.route('/insert', methods=['POST'])
# @checkToken("/insert", "POST")
def insert_function():
    # db
    users = mongo.db.users
    # vars
    name_user = request.form['nameUser']
    last_name_user = request.form['lastNameUser']
    profile_image = request.files['profileImage']
    encoded_image = base64.b64encode(profile_image.read()).decode('ascii')

    img_schema = {
        'image': encoded_image,
        'contentType': profile_image.content_type
    }
    schema_insert = {
        'firstName': name_user,
        'lastName': last_name_user,
        'imageList': [img_schema]
    }
    # process
    # mongo.save_file(profile_image.filename, profile_image)
    result_insert_id = users.insert(schema_insert)
    if result_insert_id is None:
        return """
        <h1>User not inserted</h1>
        <a href='/register'>Go back</a>
        """
    else:
        return render_template("user.html", result=True, user_id=result_insert_id, user_name=name_user, user_last_name=last_name_user,
                               picture=[img_schema])


# insert====================================================================


push = Blueprint('push', __name__)


@push.route('/push', methods=['POST', 'GET'])
# @checkToken("/push", "POST")
def push_function():
    # db
    users = mongo.db.users
    ram_user = mongo.db.ramUser
    if request.method == 'POST' and request.files['profileImage']:
        # vars
        id_user = request.form['userId']
        profile_image = request.files['profileImage']
        encoded_image = base64.b64encode(profile_image.read()).decode('ascii')

        search = {
            '_id': ObjectId(id_user)
        }
        img_schema = {
            'image': encoded_image,
            'contentType': profile_image.content_type
        }
        update_schema = {
            "$push": {
                "imageList": img_schema
            }
        }
        # process
        # mongo.save_file(profile_image.filename, profile_image)
        result_update_id = users.update_one(search, update_schema)
        find_user = users.find_one(search)
        if result_update_id.modified_count == 0 or find_user is None:
            return """
            <h1>User not found</h1>
            <a href='/index'>Go back</a>
            """
        else:
            ram_user.insert_one({"id": id_user})
            name_user = find_user['firstName']
            last_name_user = find_user['lastName']
            image_list = find_user['imageList']
            return render_template("push.html", result=True, user_id=id_user, user_name=name_user, user_last_name=last_name_user, picture=image_list)
    else:
        id_user = request.args.get("id")
        find_user = users.find_one({"_id": ObjectId(id_user)})
        if find_user is None:
            return """
                    <h1>User not found</h1>
                    <a href='/index'>Go back</a>
                    """
        else:
            name_user = find_user['firstName']
            last_name_user = find_user['lastName']
            image_list = find_user['imageList']
            return render_template("push.html", result=True, user_id=id_user, user_name=name_user, user_last_name=last_name_user, picture=image_list)


# training====================================================================


training = Blueprint('training', __name__)


@training.route('/training', methods=['GET'])
# @checkToken("/training", "GET")
def training_function():
    # var
    mini = request.args.get('mini')
    true = ['True', 'true', 'Ok', 'ok']
    mini = False if mini not in true else True
    # process
    result = general_training(mini)
    if result is True:
        read_training()
    return jsonify({"result": result})


# sync users====================================================================


sync_users = Blueprint('syncUsers', __name__)


@sync_users.route('/syncUsers', methods=['GET'])
# @checkToken("/syncUsers", "GET")
def sync_users_function():
    # process
    result = sync_employee()
    status_code = 200
    status = 'success'
    output = None
    if result is False:
        status_code = 1051
        status = 'error'
    else:
        result = general_training(mini=True)
        if result is True:
            read_training()
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# find employee====================================================================
find_base_employee = Blueprint('findEmployee', __name__)


@find_base_employee.route('/findBaseEmployee', methods=['POST'])
# @checkToken("/findBaseEmployee", "POST")
def find_base_employee_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'fullName': 1408}
    status = 'success'
    output = None

    result_token = check_token_access(token_schema=token_schema)
    if result_token is None:
        status_code = 403
    else:
        status = "success"
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # vars
            fullname_req = str(data_request['fullName']).split(" ")
            fullname = []
            for indexes in range(3):
                try:
                    if fullname_req[indexes] != '':
                        fullname.append(fullname_req[indexes])
                    else:
                        fullname.append(None)
                except IndexError:
                    fullname.append(None)
            result_search = search_employee(first_name=fullname[0], last_name=fullname[1], patronymic=fullname[2])
            output = result_search['data']
            status_code = result_search['code']
        else:
            output = result['data']
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output)


# employee info====================================================================


employee_info = Blueprint('employeeInfo', __name__)


@employee_info.route('/employeeInfo', methods=['POST'])
# @checkToken("/employeeInfo", "POST")
def employee_info_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'employeeId': 1404}
    type_validation = {'employeeId': [str]}
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None

    if result_token is None:
        status_code = 403
    else:
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                # var
                employee_id = data_request['employeeId']
                _id = get_user_obj_id_from_id(employee_id)
                output = None if _id is None else get_user_fullname_from_id(_id=_id, full=True)
        else:
            output = result['data']
            status = 'error'
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# find employee by pin====================================================================


find_employee_by_pin = Blueprint('findEmployeeByPin', __name__)


@find_employee_by_pin.route('/findEmployeeByPin', methods=['POST'])
# @checkToken("/findEmployeeByPin", "POST")
def find_employee_by_pin_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'pin': 1555}
    type_validation = {'pin': [str]}
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None

    if result_token is None:
        status_code = 403
    else:
        user_pin = token_schema['userPIN']
        organisation_pin = token_schema['organisationPin']
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
    if status_code != 200:
        status = 'error'
    data_result = False if type(output) is not tuple else output[1]
    output = returns(message=error_base(status_code), status=status, data=output if type(output) is not tuple else output[0])
    return jsonify(output, status_code, data_result)


# know me====================================================================


# know_me = Blueprint('knowMe', __name__)
#
#
# @know_me.route('/knowMe', methods=['POST'])
# def know_me_function(token_schema=None):
#     # for test mod
#     token_schema = for_test_token() if token_schema is None else token_schema
#     # for test mod
#     data_request = request.json
#     validation = {'ImgB64': 404, 'userPin': 1404}
#     type_validation = {'ImgB64': [str], 'userPin': [str]}
#     result_token = check_token_access(token_schema=token_schema)
#     status = 'success'
#     output = None
#
#     if result_token is None:
#         status_code = 403
#     else:
#         result = validate(request_data=data_request, validation=validation)
#         status_code = result['code']
#         if not result['error']:
#             # check request validation
#             status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
#             if status_code == 200:
#                 b64image = request.json['ImgB64']
#                 b64image = b64image.replace("data:image/jpeg;base64,", "")
#                 img_name = random_string_code_generator(32)
#                 img_name = img_name + '.jpeg'
#                 full_path = 'temp/' + img_name
#                 base64_string_to_folder(base64_string=b64image, file_path=img_name, folder_name="temp")
#                 image_file = open(full_path, 'rb')
#                 files = {"captureImage": image_file}
#                 data = {"capture": True}
#                 # url = "https://192.168.35.39:443/compare"
#                 url = "http://localhost:9999/compare"
#                 # url = "https://qeydiyyat.asan.org:443/compare"
#                 resp = requests.post(url, files=files, data=data, verify=False)
#                 # return resp
#                 response_data = resp.text
#                 response_data = json.loads(response_data)
#                 user_id = response_data['foundId']
#                 found_pin = user_id if user_id is None else get_user_pin_from_id(user_id)
#                 result = True if found_pin == data_request['userPin'] else False
#                 full_name = "Sistem sizi düzgün tanımadı. Sistemin sizi bənzətdiyi şəxs: " + str(response_data['person']) if result is False and user_id is not None else response_data['person']
#                 output = {'result': result, 'fullName': full_name}
#         else:
#             output = result['data']
#             status = 'error'
#     if status_code != 200:
#         status = 'error'
#     output = returns(message=error_base(status_code), status=status, data=output)
#     return jsonify(output, status_code)


# upload picture====================================================================


upload_image = Blueprint('admin/uploadImage', __name__)


@upload_image.route('/admin/uploadImage', methods=['GET', 'POST'])
@internal_token
def upload_image_function(internal_token_schema=None):
    # db
    ram_user = mongo.db.ramUser
    users = mongo.db.users
    # vars
    status_code = 200
    output = None
    status = 'success'

    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        if request.method == 'POST' and 'file' in request.files:
            files = request.files.getlist('file')
            # process
            if files is not None and len(files) > 0:
                # vars
                user_pin = dict(request.form)['pin']
                search = {
                    'pin': user_pin
                }
                img_schema_list = list(map(lambda im: {'image': base64.b64encode(im.read()).decode('ascii'), 'contentType': im.content_type}, files))

                update_schema = {
                    "$push": {
                        "imageList": {"$each": img_schema_list}
                    }
                }
                # process
                # list(map(lambda img: mongo.save_file(img.filename, img), files))
                result_update_id = users.update_one(search, update_schema)
                if result_update_id is None:
                    status_code = 1200
                else:
                    id_user = get_user_object_id_by_pin(user_pin)
                    ram_user.update({"id": id_user}, {"id": id_user}, upsert=True)
                    # training
                    result = general_training(mini=True)
                    if result is True:
                        read_training()
    else:
        status_code = internal_token_schema['code']
        output = internal_token_schema['message']
    if status_code != 200:
        status = "error"
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# submit snapshot====================================================================


submit_snapshot = Blueprint('admin/submitSnapshot', __name__)


@submit_snapshot.route('/admin/submitSnapshot', methods=['POST'])
@internal_token
def submit_snapshot_function(internal_token_schema=None):
    result_session_token = update_token_session(session['userData']['authorityType'])
    print(result_session_token)
    if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

    # db
    ram_user = mongo.db.ramUser
    users = mongo.db.users
    # vars
    status_code = 200
    output = None
    status = 'success'
    data_request = request.json
    img_schema_list = data_request['imageList']
    user_pin = data_request['pin']
    search = {
        'pin': user_pin
    }
    list(map(lambda im: print(str(str(im).split("base64,")[0]).split('data:')[1][:-1]), img_schema_list))
    img_schema_list = list(map(lambda im: {'image': str(im).split("base64,")[1], 'contentType': str(str(im).split("base64,")[0]).split('data:')[1][:-1]}, img_schema_list))
    update_schema = {
        "$push": {
            "imageList": {"$each": img_schema_list}
        }
    }
    # process
    # list(map(lambda img: mongo.save_file(img.filename, img), files))
    result_update_id = users.update_one(search, update_schema)
    if result_update_id is None:
        status_code = 1200
    else:
        id_user = get_user_object_id_by_pin(user_pin)
        ram_user.update({"id": id_user}, {"id": id_user}, upsert=True)
        # training
        result = general_training(mini=True)
        if result is True:
            read_training()
    if status_code != 200:
        status = "error"
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# remove image====================================================================


remove_image = Blueprint('admin/removeImage', __name__)


@remove_image.route('/admin/removeImage', methods=['POST'])
@internal_token
def remove_image_user_function(internal_token_schema=None):
    result_session_token = update_token_session(session['userData']['authorityType'])
    if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

    # db
    ram_user = mongo.db.ramUser
    users = mongo.db.users
    # vars
    status_code = 200
    output = None
    status = 'success'
    # data_request = dict(request.form)
    data_request = request.json
    pin = data_request['pin']
    photo = str(data_request['photo']).split("base64,")[1]
    search = {
        'pin': pin
    }
    pull = {
        '$pull': {'imageList': {'image': photo}}
    }
    # process
    remove_photo = users.update_one(search, pull)
    if remove_photo.modified_count == 0:
        status_code = 1200
    else:
        id_user = get_user_object_id_by_pin(pin)
        ram_user.update({"id": id_user}, {"id": id_user}, upsert=True)
        # training
        result = general_training(mini=True)
        if result is True:
            read_training()
    if status_code != 200:
        status = "error"
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# employee photos====================================================================


employee_photos = Blueprint('employeePhotos', __name__)


@employee_photos.route('/admin/employeePhotos', methods=['GET'])
@internal_token
def employee_photos_function(internal_token_schema=None):
    # var
    pin = request.args.get('pin')
    status_code = 200
    photos = []

    if internal_token_schema is not None and internal_token_schema['error'] is False:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        if pin is not None:
            # db
            users = mongo.db.users
            # vars
            search = {
                'pin': pin
            }
            # process
            find = users.find_one(search)
            if find is None:
                status_code = 404
            else:
                photos = list(map(lambda im: "data:"+im['contentType']+";base64,"+im['image'], find['imageList']))
    else:
        status_code = 1102 if internal_token_schema['code'] == 403 else internal_token_schema['code']
    if status_code == 200:
        status = "success"
    else:
        status = "error"
    output = returns(message=error_base(status_code), status=status, data=photos)
    return jsonify(output, status_code)


# charts====================================================================


charts = Blueprint('charts', __name__)


@charts.route('/admin/charts', methods=['GET'])
@internal_token
def charts_function(internal_token_schema=None):
    status_code = 200
    status = 'success'
    output = None

    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # db
        users = mongo.db.users
        users_work_log = mongo.db.usersWorkLog
        # vars
        total_employees = users.find().count()
        total_using_employees = users_work_log.distinct("userId")
        total_not_using_employees = total_employees - len(total_using_employees)
        using_percent = percent_count(total_not_using_employees, len(total_using_employees))
        total_using_percent = list(filter(lambda f: f is not None, list(map(lambda tu: tu if len(total_using_employees) in tu else None, using_percent))))[0][len(total_using_employees)]
        total_not_using_percent = 100 - total_using_percent
        date_range = list(map(lambda m: "01."+str(m)+"."+str(datetime.now().year) if m > 9 else "01.0"+str(m)+"."+str(datetime.now().year), range(1, 13)))
        using_data_range = list(map(lambda dr: monthly_statistics(dr), date_range))
        not_using_data_range = deepcopy(using_data_range)
        total_with_pin_result = list(set(list(map(lambda wp: wp['userId'], list(users_work_log.find({"byFin": True}, {'_id': 0, 'userId': 1}))))))
        total_without_pin_result = list(set(list(map(lambda wp: wp['userId'], list(users_work_log.find({"byFin": False}, {'_id': 0, 'userId': 1}))))))
        total_with_pin = len(total_with_pin_result)
        total_without_pin = len(total_without_pin_result)
        never_pin = len(list(filter(lambda f1: f1 not in total_with_pin_result, total_without_pin_result)))
        never_face = len(list(filter(lambda f2: f2 not in total_without_pin_result, total_with_pin_result)))
        both_fin_face_using = len(total_using_employees) - never_face - never_pin
        list(map(lambda nu: nu.update({list(nu.keys())[0]: total_employees-list(nu.values())[0]}), not_using_data_range))
        using_data_percent = monthly_percent_statistics(using_data_range, not_using_data_range)
        not_using_data_percent = monthly_percent_statistics(using_data_range, not_using_data_range, 2)

        pin_using_employee_range = list(map(lambda dr: monthly_statistics(dr, {'byFin': True}), date_range))
        pin_not_using_employee_range = list(map(lambda dr: monthly_statistics(dr, {'byFin': False}), date_range))
        pin_using_percent_range = pin_not_pin_monthly_percent_count(pin_using_employee_range, pin_not_using_employee_range)
        pin_not_using_percent_range = pin_not_pin_monthly_percent_count(pin_using_employee_range, pin_not_using_employee_range, 2)

        # round percents
        using_data_percent = list(map(lambda udp: round(udp, 2), using_data_percent))
        not_using_data_percent = list(map(lambda ndp: round(ndp, 2), not_using_data_percent))
        pin_using_percent_range = list(map(lambda pup: round(pup, 2), pin_using_percent_range))
        pin_not_using_percent_range = list(map(lambda pnu: round(pnu, 2), pin_not_using_percent_range))

        output = {
            # "totalEmployees": total_employees,
            # "totalUsingEmployees": len(total_using_employees),
            # "totalNotUsingEmployees": total_not_using_employees,
            # 'usingDataRange': list(map(lambda us: list(us.values())[0], using_data_range)),
            # 'notUsingDataRange': list(map(lambda nu: list(nu.values())[0], not_using_data_range)),
            'usingDataPercent': using_data_percent,
            'notUsingDataPercent': not_using_data_percent,
            'barChartPercentPinReg': pin_using_percent_range,
            'barChartPercentFaceReg': pin_not_using_percent_range,
            # 'totalUsingPercent': total_using_percent,
            # 'totalNotUsingPercent': total_not_using_percent,
            # "neverPinEmployees": never_pin,
            # "neverFaceEmployees": never_face,
            # "bothFacePinEmployees": both_fin_face_using,
            # "totalWithPin": total_with_pin,
            # "totalWithoutPin": total_without_pin,
            "months": ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'iyun', 'İyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr'],
            "pieUsingLabels": ['sistemdən istifadə etməyənlər', 'yalnız FİN-dən istifadə edənlər', 'yalnız üztanımadan istifadə edənlər', 'eynizamanda FİN və üztanımadan istifadə edənlər'],
            "pieBgColors": ['#d2d6de', '#f56954', '#00a65a', '#00BBE9'],
            "pieUsingData": [total_not_using_employees, never_face, never_pin, both_fin_face_using],
            "donutPinFaceLabels": ['Qeydiyyatlarda üztanımalardan istifadə edənlər', 'Qeydiyyatlarda FİN-dən istifadə edənlər'],
            "areaChartLabels": ['sistemdən istifadə etməyənlər', 'sistemdən istifadə edənlər'],
            "donutPinFaceData": [total_without_pin, total_with_pin],
            "donutBgColors":  ['#00c0ef', '#f39c12']
        }
    else:
        status_code = 1102 if internal_token_schema['code'] == 403 else internal_token_schema['code']
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)

# noname====================================================================


noname = Blueprint('noname', __name__)


@noname.route('/noname', methods=['POST'])
@checkToken("/noname", "POST")
def noname_function(token_schema):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'orgPin': 1002}
    type_validation = {'orgPin': [str]}
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None

    if result_token is None:
        status_code = 403
    else:
        user_pin = token_schema['userPIN']
        organisation_pin = token_schema['organisationPin']
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                # db
                pass
        else:
            output = result['data']
            status = 'error'
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# ip list====================================================================
ip_list = Blueprint('ipList', __name__)


@ip_list.route('/ipList', methods=['GET'])
@internal_token
def ip_list_function(internal_token_schema=None):
    print('\n\n\n-----------------------\ntoken-->\t', internal_token_schema, '\n-----------------------\n\n\n')
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] in [0, 2]:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # db
        terminal_list = mongo.db.terminals
        # process
        output = list(map(lambda tl: tl['ip'], list(terminal_list.find())))
    else:
        if request.args.get('defaultToken') == 'DEFAULT':
            # db
            terminal_list = mongo.db.terminals
            # process
            output = list(map(lambda tl: tl['ip'], list(terminal_list.find())))
        else:
            output = {'message': internal_token_schema['message']}
    return jsonify(output)


# sub employee list====================================================================
director_employee_list = Blueprint('directorEmployeeList', __name__)


@director_employee_list.route('/directorEmployeeList', methods=['GET'])
@internal_token
def director_employee_list_function(internal_token_schema=None):
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 2:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)
        if 'error' in result_session_token and result_session_token['error'] is True: return render_template("admin/login.html")
        user_data = director_user(user_pin=session['userData']['userName'], user_type=session['userData']['authorityType'])
        output = user_data['employeeList']
    else:
        output = {'message': internal_token_schema['message']}
    return jsonify(output)


# ajax file====================================================================
ajax_file = Blueprint('ajaxFile', __name__)


@ajax_file.route('/admin/ajaxFile', methods=['POST', "GET"])
@internal_token
def ajax_file_function(internal_token_schema=None):
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # db
        users_work_log = mongo.db.usersWorkLog
        users = mongo.db.users
        data_log = {}
        if request.method == 'POST':
            draw = request.form['draw']
            # row = int(request.form['start'])  # limit
            row = int(request.form['start'])  # limit
            row_per_page = int(request.form['length'])  # length
            search_value = request.form["search[value]"]
            columns = ['userId', 'type', 'time', 'fullDate', 'byFin']
            ordered_column_index = int(request.form['order[0][column]'])
            sort_types = {'asc': 1, 'desc': -1}
            sort_by = sort_types[request.form['order[0][dir]']]
            order_by = columns[ordered_column_index]
            search_users = {'$or': [{'firstName': {'$regex': search_value}}, {'lastName': {'$regex': search_value}}]} if search_value != '' else {}
            user_ids = list(map(lambda uid: str(uid['_id']), list(users.find(search_users, {'_id': 1}))))

            search = {'$or': [{'userId': {'$in': user_ids}}, {'type': {'$regex': search_value}}, {'time': {'$regex': search_value}}, {'fullDate': {'$regex': search_value}}]} if search_value != '' else {}

            start_id = list(users_work_log.find(search))[row]['_id']
            total_records = users_work_log.find(search, {"_id": 0}).count()
            search.update({'_id': {'$gte': start_id}})
            user_id = users_work_log.find_one({'_id': start_id}, {'_id': 0, 'userId': 1})['userId']
            print('\n\n\n**********************\nman:\t', get_user_fullname_from_id(_id=user_id), '\n**********************\n\n\n')
            data_log = list(users_work_log.find(search, {'_id': 0}).sort(order_by, sort_by).limit(int(row_per_page)))

            print('------------------\n\n\nrow:\t', row, '\nrow_per_page:\t', row_per_page, '\nsearch_value:\t', search_value,
                  '\nsearch_users:\t', search_users, '\ntotal_records:\t', total_records, '\norder_by:\t', order_by,
                  '\nuser_ids:\t', user_ids, '\nsearch:\t', search, '\ndraw:\t', draw, '\n------------------\n\n\n')

            list(map(lambda us: us.update({'fullName': get_user_fullname_from_id(us['userId']), 'type': '<div id="type_reg" style="border: 3px solid rgb(103, 182, 0); color: rgb(103, 182, 0);">Giriş</div>' if us['type'] == 'in' else '<div id="type_reg" style="border: 3px solid rgb(255, 193, 7); color: rgb(255, 193, 7);">Çıxış</div>', 'time': us['time'], 'fullDate': obj_date_to_str_date(us['fullDate']), 'byFin': """<div id="byFINtd"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill text-success" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                      </svg></div>""" if us['byFin'] is True else """<div id="byFINtd"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill text-danger" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                                      </svg></div>"""}), data_log))
            data_log = {
                'draw': draw,
                'iTotalRecords': total_records,
                'iTotalDisplayRecords': total_records,
                'aaData': data_log,

            }
    else:
        data_log = {}
    return jsonify(data_log)


# ip list terminal====================================================================
ip_list_terminal = Blueprint('ipListTerminal', __name__)


@ip_list_terminal.route('/admin/ipListTerminal', methods=["POST", "GET", "PUT", "DELETE"])
@internal_token
def ip_list_terminal_function(internal_token_schema=None):
    print('token schema:\t', internal_token_schema)
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] in [0, 2]:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # db
        ip_list_terminal_coll = mongo.db.terminals
        # vars
        search = {}

        if request.method == 'GET':
            ip = request.args.get('ip')
            description = request.args.get('description')
            if description is not '': search.update({'description': {'$regex': description}})
            if ip is not '': search.update({'ip': {'$regex': ip}})

        if request.method == 'POST':
            ip = request.form['ip']
            description = request.form['description']
            if ip_validation(ip):
                insert_schema = {'ip': ip, 'description': description}
                ip_list_terminal_coll.insert_one(insert_schema)

        if request.method == 'PUT':
            ip = request.form['ip']
            description = request.form['description']
            _id = request.form['_id']
            if ip_validation(ip):
                search_schema = {
                    '_id': ObjectId(_id)
                }
                update_schema = {
                    '$set': {'ip': ip, 'description': description}
                }
                ip_list_terminal_coll.update_one(search_schema, update_schema)

        if request.method == 'DELETE':
            _id = request.form['_id']
            search_schema = {'_id': ObjectId(_id)}
            ip_list_terminal_coll.remove(search_schema)
        ip_list_ter = list(ip_list_terminal_coll.find(search).sort('_id', -1))
        list(map(lambda ipl: ipl.update({'_id': str(ipl['_id'])}), ip_list_ter))
    else:
        ip_list_ter = []
    return jsonify(ip_list_ter)


# employee work log====================================================================


employee_work_log = Blueprint('employeeWorkLog', __name__)


@employee_work_log.route('/employeeWorkLog', methods=['POST'])
# @checkToken("/employeeWorkLog", "POST")
def employee_work_log_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'employeeId': 1404}
    type_validation = {'employeeId': [str]}
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None

    if result_token is None:
        status_code = 403
    else:
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                # var
                employee_id = data_request['employeeId']
                _id = get_user_obj_id_from_id(employee_id)
                emp_inf = get_user_fullname_from_id(_id=_id, full=True)
                if emp_inf is not None:
                    emp_inf = {
                        'firstName': emp_inf['firstName'],
                        'lastName': emp_inf['lastName'],
                        'patronymic': emp_inf['patronymic'],
                        'posName': emp_inf['posName'],
                        'imgURL': emp_inf['imageList'][0]['image'],
                        'imgContentType': emp_inf['imageList'][0]['contentType']
                    }
                else:
                    emp_inf = None
                # all_log_by_fin = [] if _id is None else get_user_work_log_from_id(user_id=_id, by_fin=True)
                # output = {'allWorkLogByFin': all_log_by_fin, 'employeeWorkLogPercents': get_employee_work_log_statistics(user_id=_id), 'employeeInfo': emp_inf}
                output = {'employeeWorkLogPercents': get_employee_work_log_statistics(user_id=_id), 'employeeInfo': emp_inf, '_id': _id}
        else:
            output = result['data']
            status = 'error'
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# employee work log list====================================================================

employee_work_log_list = Blueprint('employeeWorkLogList', __name__)


@employee_work_log_list.route('/admin/employeeWorkLogList', methods=['POST', "GET"])
@internal_token
def employee_work_log_list_function(internal_token_schema=None):
    # db
    users_work_log = mongo.db.usersWorkLog
    data_log = {}
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] in [0, 2]:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

    if request.method == 'POST':
            draw = request.form['draw']
            _id = request.form['_id']
            # row = int(request.form['start'])  # limit
            row = int(request.form['start'])  # limit
            row_per_page = int(request.form['length'])  # length
            # search_value = request.form["search[value]"]
            columns = ['type', 'fullDate']
            # ordered_column_index = int(request.form['order[0][column]'])
            ordered_column_index = 0
            sort_types = {'asc': 1, 'desc': -1}
            # sort_by = sort_types[request.form['order[0][dir]']]
            sort_by = 1
            order_by = columns[ordered_column_index]
            # search_users = {'$or': [{'firstName': {'$regex': search_value}}, {'lastName': {'$regex': search_value}}]} if search_value != '' else {}
            # user_ids = list(map(lambda uid: str(uid['_id']), list(users.find(search_users, {'_id': 1}))))

            # search = {'$or': [{'userId': {'$in': user_ids}}, {'type': {'$regex': search_value}}, {'time': {'$regex': search_value}}, {'fullDate': {'$regex': search_value}}]} if search_value != '' else {}
            # all_log_by_fin = [] if _id is None else get_user_work_log_from_id(user_id=_id, by_fin=True)
            search = {'userId': _id, 'byFin': True}
            total_records = users_work_log.find(search, {'date': 0, 'time': 0, 'userId': 0, 'byFin': 0, 'image': 0}).count()
            start_id = None if total_records == 0 else list(users_work_log.find(search).sort(order_by, sort_by))[row]['_id']
            if start_id is not None: search.update({'_id': {'$gte': start_id}})
            # user_id = users_work_log.find_one({'_id': start_id}, {'date': 0, 'time': 0, 'userId': 0, 'byFin': 0})['userId']
            # print('\n\n\n**********************\nman:\t', get_user_fullname_from_id(_id=user_id), '\n**********************\n\n\n')
            data_log = list(users_work_log.find(search, {'date': 0, 'time': 0, 'userId': 0, 'byFin': 0, 'image': 0}).sort(order_by, sort_by).limit(int(row_per_page)))

            # print('------------------\n\n\nrow:\t', row, '\nrow_per_page:\t', row_per_page, '\ntotal_records:\t',
            #       total_records, '\norder_by:\t', order_by, '\nsearch:\t', search, '\ndraw:\t', draw, '\n------------------\n\n\n')

            list(map(lambda us: us.update({'type': '<div id="type_reg" style="border: 3px solid rgb(103, 182, 0); color: rgb(103, 182, 0);">Giriş</div>' if us['type'] == 'in' else '<div id="type_reg" style="border: 3px solid rgb(255, 193, 7); color: rgb(255, 193, 7);">Çıxış</div>', 'fullDate': '<a id=\'ewl\'  href="javascript:employeeWorkLogIMG(\''+str(us['_id'])+'\')">'+obj_date_to_str_date(us['fullDate'])+'</a>'}), data_log))
            list(map(lambda us: us.pop('_id'), data_log))
            data_log = {
                'draw': draw,
                'iTotalRecords': total_records,
                'iTotalDisplayRecords': total_records,
                'aaData': data_log,

            }
    return jsonify(data_log)


# change password====================================================================
change_password = Blueprint('changePassword', __name__)


@change_password.route('/admin/changePassword', methods=['POST'])
@internal_token
def change_password_function(internal_token_schema=None):
    error = False
    message = 'Şifrə dəyişdirildi, artıq yeni şifrədən istifadə edin.'
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # vars
        request_data = request.json
        validation = {'oldPassword': 404, 'newPassword': 404, 'reNewPassword': 404, 'userName': 404}
        type_validation = {'oldPassword': [str], 'newPassword': [str], 'reNewPassword': [str], 'userName': [str]}
        # db
        authority_users = mongo.db.authorityUsers
        # process
        result = validate(request_data=request_data, validation=validation)

        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=request_data)
            if status_code == 200:
                user_name = request_data['userName']
                old_password = request_data['oldPassword']
                new_password = request_data['newPassword']
                re_new_password = request_data['reNewPassword']

                result = check_auth(user_name=user_name, password=old_password)
                if result is None:
                    message = "İstifadəçi tapılmadı."
                    error = True
                else:
                    if new_password == re_new_password:
                        update_user_password_schema = {
                            'password': md5(new_password.encode('utf-8')).hexdigest()
                        }
                        search_user = {
                            'id': result['id']
                        }
                        result_update = authority_users.update_one(search_user, {'$set': update_user_password_schema})
                        if result_update.modified_count != 1:
                            message = "Şifrə dəyişdirilə bilmədi"
                            error = True
                    else:
                        message = "Yeni şifrə və təkrarı arasında uyğunsuzluq var"
                        error = True
        else:
            message = "Parametrlər düz göndərilməyib"
            error = True
    else:
        error = True
        message = internal_token_schema['message']

    output = {'message': message, 'error': error}
    return jsonify(output)

# set admin role====================================================================


set_remove_admin = Blueprint('setRemoveAdmin', __name__)


@set_remove_admin.route('/admin/setRemoveAdmin', methods=['POST'])
@internal_token
def set_remove_admin_function(internal_token_schema=None):
    error = False
    message = 'Səlahiyyət dəyişdirildi.'
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # vars
        request_data = request.json
        validation = {'userPin': 404}
        type_validation = {'userPin': [str]}
        # db
        authority_users = mongo.db.authorityUsers
        # process
        result = validate(request_data=request_data, validation=validation)

        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=request_data)
            if status_code == 200:
                user_name = request_data['userPin']
                result = check_auth(user_name=user_name, only_user_name=True)
                if result is None:
                    message = "İstifadəçi tapılmadı."
                    error = True
                else:
                    update_auth_schema = {
                        'authorityType': 0 if result['authorityType'] != 0 else 3
                    }
                    search_user = {
                        'userName': user_name
                    }
                    result_update = authority_users.update_one(search_user, {'$set': update_auth_schema})
                    if result_update.modified_count != 1:
                        message = "Səlayiyyət verilə bilmədi"
                        error = True
        else:
            message = "Parametrlər düz göndərilməyib"
            error = True
    else:
        error = True
        message = internal_token_schema['message']

    output = {'message': message, 'error': error}
    return jsonify(output)

# set director role====================================================================


set_remove_director = Blueprint('switchDirectorInput', __name__)


@set_remove_director.route('/admin/switchDirectorInput', methods=['POST'])
@internal_token
def set_remove_director_function(internal_token_schema=None):
    error = False
    message = 'Səlahiyyət dəyişdirildi.'
    if internal_token_schema is not None and internal_token_schema['error'] is False and internal_token_schema['data']['authorityType'] == 0:
        result_session_token = update_token_session(session['userData']['authorityType'])
        if 'error' in result_session_token and result_session_token['error'] is True: return jsonify(result_session_token)

        # vars
        request_data = request.json
        validation = {'userPin': 404}
        type_validation = {'userPin': [str]}
        # db
        authority_users = mongo.db.authorityUsers
        # process
        result = validate(request_data=request_data, validation=validation)

        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=request_data)
            if status_code == 200:
                user_name = request_data['userPin']
                result = check_auth(user_name=user_name, only_user_name=True)
                if result is None:
                    message = "İstifadəçi tapılmadı."
                    error = True
                else:
                    update_auth_schema = {
                        'authorityType': 2 if result['authorityType'] != 2 else 3
                    }
                    search_user = {
                        'userName': user_name
                    }
                    result_update = authority_users.update_one(search_user, {'$set': update_auth_schema})
                    if result_update.modified_count != 1:
                        message = "Səlayiyyət verilə bilmədi"
                        error = True
        else:
            message = "Parametrlər düz göndərilməyib"
            error = True
    else:
        error = True
        message = internal_token_schema['message']

    output = {'message': message, 'error': error}
    return jsonify(output)


# noname====================================================================


get_work_log_img = Blueprint('getWorkLogIMG', __name__)


@get_work_log_img.route('/getWorkLogIMG', methods=['POST'])
def get_work_log_img_function():
    # var
    data_request = request.json
    # db
    user_work_log = mongo.db.usersWorkLog
    # process
    _id = data_request['id']
    search = {'_id': ObjectId(_id)}
    show = {'_id': 0, 'image': 1, 'date': 1}
    find_uwl_img = user_work_log.find_one(search, show)
    output = find_uwl_img if find_uwl_img is not None else ''
    return jsonify(output)


# EMOTION PROJECT====================================================================


# emotion PROJECT detection====================================================================

emotion = Blueprint('emotion', __name__)


@emotion.route('/emotion', methods=['POST'])
# @checkToken("/push", "POST")
def emotion_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    status_code = 200
    output = None
    status = "success"
    path = "D:\\photos\\"
    data_request = request.json
    if type(data_request) is list:
        error_code_list = list(map(lambda e: True if 'photo' in e and 'asan' in e else False, data_request))
        if False not in error_code_list:
            result_token = check_token_access(token_schema=token_schema)
            if result_token is None:
                status_code = 403
            else:
                # vars
                actions = ['age', 'gender', 'race', 'emotion']
                path_list = list(map(lambda pl: str(path) + str(pl['asan']) + "\\" + str(pl['photo']), data_request))
                output = list(map(lambda pls: DeepFace.analyze(img_path=pls, actions=actions), path_list))
                # DeepFace.stream(db_path=path + str(data_request[0]['asan']))
        else:
            status_code = 403
    else:
        status_code = 403
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)

# emotion people detection and insert====================================================================


detect_insert_files = Blueprint('detectInsertFiles', __name__)


@detect_insert_files.route('/detectInsertFiles', methods=['GET'])
def detect_files_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None
    status_code = 200

    if result_token is None:
        status_code = 403
    else:
        # var & process
        file_dir = "D:\\images\\"
        inside_folder = list(os.listdir(file_dir))
        output = list(map(lambda rl: {'folder': rl, 'insertedCount': detect_and_train(file_dir+str(rl)+"\\")}, inside_folder))
    if status_code != 200:
        status = 'error'
    # all_events = get_all_events()
    # output = {"detectNewFaces": output, "DateEventCounts": all_events}
    output = {"detectNewFaces": output}
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)

# emotion people detection and insert====================================================================


face_identicate = Blueprint('faceIdenticate', __name__)


@face_identicate.route('/faceIdenticate', methods=['POST'])
def detect_files_function(token_schema=None):
    # for test mod
    token_schema = for_test_token() if token_schema is None else token_schema
    # for test mod
    data_request = request.json
    validation = {'photos': 404, 'minDate': 404, 'maxDate': 404, 'faceMatchPercent': 404, "algorithm": 404, "asan": 404}
    type_validation = {'photos': [list], 'minDate': [int], 'maxDate': [int], 'faceMatchPercent': [int], "algorithm": [int], "asan": [str]}
    if 'algorithm' not in data_request:
        data_request['algorithm'] = 1
    if data_request['algorithm'] == 1:
        del validation['asan']
        del type_validation['asan']
    result_token = check_token_access(token_schema=token_schema)
    status = 'success'
    output = None

    if result_token is None:
        status_code = 403
    else:
        result = validate(request_data=data_request, validation=validation)
        status_code = result['code']
        if not result['error']:
            # check request validation
            status_code = request_type_check(type_request_validation=type_validation, request_data=data_request)
            if status_code == 200:
                # vars
                photos = data_request['photos']
                min_date = datetime.fromtimestamp(data_request['minDate'])
                max_date = datetime.fromtimestamp(data_request['maxDate'])
                path = "D:\\photos\\"
                algorithm = data_request['algorithm']
                # db
                pins = mongo_emotion_base.db.pins
                # people = mongo_emotion_base.db.people
                search = {
                    '$match': {
                        'date': {
                            '$elemMatch': {
                                '$gte': min_date,
                                '$lte': max_date
                            }
                        }
                    }
                }
                project = {
                    '$project': {
                        '_id': 0,
                        'pin': 1,
                        'date': {'$arrayElemAt': ['$date', -1]}
                    }
                }
                # process
                print('\n\n\n', min_date, '-', max_date, '\n\n\n')
                result_pins = list(pins.aggregate([search, project]))
                pin_list = list(map(lambda p: p['pin'], result_pins))
                file_extension = ["jpg", "jpeg", "png", "bmp", "gif"]
                sub_path = data_request["asan"]
                image_db_path = "D:\\images\\" + sub_path + "\\"
                print(pin_list)
                if algorithm == 1:
                    people_result = read_people_training(pin_list=pin_list)
                    known_face_encodings = people_result["knownFaceEncoding"]
                    known_face_names = people_result["knownFaceNames"]
                    output = selected_face_recognition(photos=photos, url_folder=path, known_face_names=known_face_names, known_face_encodings=known_face_encodings)
                elif algorithm == 2:
                    # img2_path = image_db_path
                    # file_list = os.listdir(img2_path)
                    # filtered_images = list(filter(lambda fim: str(fim).split(".")[0] in pin_list and str(fim).split(".")[1] in file_extension, file_list))
                    # filtered_images = list(map(lambda oim: PIL.Image.open(os.path.join(image_db_path, oim)), filtered_images))
                    output = list(map(lambda im: face_recognition_deep_face(compare_img=path+str(im), image_base_path=image_db_path), photos))
                elif algorithm == 3:
                    img2_path = image_db_path
                    file_list = os.listdir(img2_path)
                    filtered_images = list(filter(lambda fim: str(fim).split(".")[0] in pin_list and str(fim).split(".")[1] in file_extension, file_list))
                    output = list(map(lambda fm: list(map(lambda im: face_verify_deep_face(img1_path=path+str(im), img2_path=img2_path+str(fm), pin=str(fm).split(".")[0]), photos))[0], filtered_images))
                    output = list(filter(lambda fim: fim is not None, output))
        else:
            output = result['data']
            status = 'error'
    if status_code != 200:
        status = 'error'
    output = returns(message=error_base(status_code), status=status, data=output)
    return jsonify(output, status_code)


# emotion schedule====================================================================

@app.cli.command('run-job')
def scheduled():
    """Run scheduled job."""
    print('Importing feeds...')
    # var & process
    file_dir = "D:\\images\\"
    inside_folder = list(os.listdir(file_dir))
    output = list(map(lambda rl: {'folder': rl, 'insertedCount': detect_and_train(file_dir + str(rl) + "\\")}, inside_folder))
    # all_events = get_all_events()
    # output = {"detectNewFaces": output, "DateEventCounts": all_events}
    output = {"detectNewFaces": output}
    print('Done: \t', output)
