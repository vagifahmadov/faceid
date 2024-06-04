import copy, time
import random
import string
import schedule
import pymongo
from config.config import *
from config.db import mongo, mongo_config, pyodbc, mongo_emotion_base
import glob, socket


# main methods
def request_key_check(request_keys, regulations, array):
    error = False
    for keyreq in request_keys:
        for key_req, val_req in keyreq.items():
            if key_req == 'name':
                if keyreq[key_req] not in regulations:
                    array.append({"key": keyreq[key_req], "type": keyreq['type']})
                    error = True
    return error


def returns(message, status, data):
    json_return_schema = {
        "status": status,
        "message": message,
        "data": data
    }
    return json_return_schema


def validate(request_data, validation):
    validation_list = []
    request_keys = []
    result = []
    valid_sub_key = []
    main_keys_only = []
    status_code = 200
    error = False
    for key, value in validation.items():
        validation_list.append(key)  # to load given validation key
    if request_data is not None:
        for key, value in request_data.items():
            if key not in validation_list:
                main_keys_only.append(key)
            request_keys.append(key)  # to load request keys
            if type(value) is dict:
                for k, v in value.items():
                    if k not in validation_list:
                        valid_sub_key.append(key + "." + k)
                    request_keys.append(k)  # to load request sub keys

        keys_difference = list(set(validation_list) - set(request_keys))  # find difference

        if keys_difference:
            # if keys is valid
            status_code = 404.24
            if type(main_keys_only) != bool and not main_keys_only:  # if request is empty
                main_keys_only = "No such keys"
            if valid_sub_key:
                if len(valid_sub_key) == len(keys_difference) and len(valid_sub_key) == 1:
                    output = {"request": valid_sub_key[0],
                              'actually': str(valid_sub_key[0]).split(".")[0] + "." + keys_difference[0]}
                elif len(valid_sub_key) == len(keys_difference):
                    output = {"request": valid_sub_key, 'actuallySubKeys': keys_difference}
                else:
                    output = {"request": {"mainKeys": main_keys_only, "subKeys": valid_sub_key},
                              "actually": keys_difference}
                    # output=keys_difference+valid_sub_key
            else:
                if main_keys_only == "No such keys":
                    output = {"warning": main_keys_only, "actually": keys_difference}
                else:
                    if len(keys_difference) == 1:
                        output = {"request": main_keys_only[0], "actually": keys_difference[0]}
                    else:
                        output = {"request": {"mainKeys": main_keys_only}, "actually": keys_difference}
        else:
            # if key is valid and no values
            for k_v, v_v in request_data.items():
                if type(v_v) is dict:
                    for k, v in v_v.items():
                        if type(v_v[k]) != bool and not v_v[k]:  # chek value is empty or not boolean
                            result.append(k_v + "." + k)
                            status_code = validation[k]
                            break
                if type(request_data[k_v]) != bool and not request_data[k_v]:
                    result.append(k_v)
                    status_code = validation[k_v]
            output = result
        if status_code != 200:
            error = True
    else:
        output = 'Invalid request: You sent null data inside object data'
        error = True
        status_code = 500
    return {'error': error, 'data': output, 'code': status_code}


def validate_url_get(url, validation):
    status_code = 200
    error = False
    # param = '?'
    # c = 0
    wanted_param = []
    not_wanted_param = []
    all_param_and_values = []
    full_param_dict = {}
    data = {}
    validation_keys = []
    full_param_keys = []

    parsed = urlparse.urlparse(url)
    # result_parsed = urlparse.parse_qs(parsed.query)
    result_parsed = parsed.query
    pars_and_symbol = str(result_parsed).split("&")
    for all_params in pars_and_symbol:
        all_param_and_values.append(all_params)

    for make_param_dict in all_param_and_values:
        if make_param_dict != '':
            full_param = make_param_dict.split("=")
            full_param_dict[full_param[0]] = full_param[1]

    for key, value in validation.items():
        validation_keys.append(key)
    for key, value in full_param_dict.items():
        full_param_keys.append(key)
    difference = list(list_difference(list1=full_param_keys, list2=validation_keys))
    for diff in difference:
        if diff in validation_keys and diff not in full_param_keys:
            wanted_param.append(diff)
            error = True
        elif diff not in validation_keys and diff in full_param_keys:
            not_wanted_param.append(diff)
            error = True
    if len(not_wanted_param) > 0:
        data.update({"notWantedParameters": not_wanted_param})
    if len(wanted_param) > 0:
        data.update({"wantedParameters": wanted_param})
    # create status
    if len(wanted_param) > 0 and len(not_wanted_param) > 0:
        status_code = 1406.99
    elif len(wanted_param) > 0 and len(not_wanted_param) == 0:
        status_code = 1404.9
    elif len(wanted_param) == 0 and len(not_wanted_param) > 0:
        status_code = 1406.98

    return {'error': error, 'code': status_code, 'data': data}


def validate_list_elements(list_value, type_elements, key_lists=None):
    """
    validate elements of list
    :param list_value:
    :param type_elements:
    :param key_lists:
    :return:
    """
    status_code = 1252
    if type_elements is dict and key_lists is not None:
        filtered_list = list(filter(lambda v: type(v) is dict and all(item in key_lists for item in list(v.keys())) is True, list_value))
        filtered_list = list(filter(lambda it: all(it[k] not in ["", None] for k in list(it.keys())) is True, filtered_list))
    else:
        filtered_list = list(filter(lambda v: type(v) is type_elements, list_value))
    if len(filtered_list) == len(list_value):
        status_code = 200
    return status_code


def error_base_method(code, method, message=None):
    status = True
    errors_base = mongo.db.errorBase
    if method:
        # messaging
        message_part2 = " daxil edin"
        if method == "update":
            message_part1 = "Yeni mesajı"
        elif method == "insert":
            message_part1 = "Mesajı"
        else:
            message_part1 = ""

        # body
        if code:
            if method == "insert":
                # insert
                if message:
                    check_code = errors_base.find({"code": code})
                    if check_code.explain()['executionStats']['nReturned'] == 0:
                        error_schema = {
                            "code": code,
                            "message": message
                        }
                        insert = errors_base.insert_one(error_schema)
                        if str(ObjectId(insert.inserted_id)):
                            output = "Xəta mesajı daxil olundu"
                        else:
                            status = False
                            output = "Xəta mesajı daxil olunmadı"
                    else:
                        output = "Bu kodla başqa xəta mesajı artıq qeydiyyatdan keçib."
                else:
                    status = False
                    output = message_part1 + message_part2
            elif method == "update":
                # update
                if message:
                    search_param = {"code": code}
                    update_param = {"code": code, "message": message}
                    update = errors_base.update_one(search_param, {"$set": update_param})
                    if update.modified_count > 0:
                        output = "Uğurla dəyişdirildi"
                    else:
                        status = False
                        output = "Redaktə olunmadı"
                else:
                    status = False
                    output = message_part1 + message_part2
            elif method == "delete":
                # delete
                if code:
                    search_param = {"code": code, "DELETE": {'$exists': False}}
                    delete_param = {"DELETE": True}
                    delete = errors_base.update_one(search_param, {"$set": delete_param})
                    if delete.modified_count > 0:
                        output = "Uğurla silndi"
                    else:
                        status = False
                        output = "Silinmədi"
                else:
                    status = False
                    output = 'Kodu daxil edin'
            elif method == "undelete":
                if code:
                    search_param = {"code": code, "DELETE": True}
                    delete_param = {"DELETE": True}
                    undelete = errors_base.update_one(search_param, {"$unset": delete_param})
                    if undelete.modified_count > 0:
                        output = "Uğurla bərpa olundu"
                    else:
                        status = False
                        output = "Bərpa olunmadı"
                else:
                    status = False
                    output = 'Kodu daxil edin'
            else:
                status = False
                output = "Metod düzgün seçilməyib"
        else:
            if message or method == "delete" or method == "undelete":
                output = "Kodu daxil edin"
                status = False
            else:
                status = False
                output = "Kodu və " + message_part1 + message_part2
    else:
        output = "Metodu daxil edin"

    return {"status": status, "data": output}


def error_base(error_code):
    # coding=utf-8
    errors_base = mongo.db.errorBase
    output = "Error not in base"
    list_error = errors_base.find_one({'code': error_code, "DELETE": {'$exists': False}})
    if list_error:
        output = list_error['message']
    return output


def hash_encrypt(string_name):
    sha_signature = sha256(string_name.encode()).hexdigest()
    return sha_signature


def list_difference(list1, list2):
    return {*list1} ^ {*list2}


def filter_symbol(simple_text):
    base_replace = "$#?/-.,;:\|\"*+@!%^()=~\n"
    double_space = "  "
    for sym in base_replace:
        if sym in simple_text:
            simple_text = simple_text.replace(sym, " ")
        if double_space in simple_text:
            simple_text = simple_text.replace(double_space, " ")
    if simple_text[-1] == " ":
        simple_text = simple_text[:-1]
    return simple_text


def check_token_access(token_schema):
    # variables
    authorities = mongo_config.db.authorities
    authorities_list = []
    token_auth_list = []
    authorities_dict = {}
    result = None

    # authorities list
    find_authorities = list(authorities.find())
    if len(find_authorities) > 0:
        for auth in find_authorities:
            authorities_list.append(auth['name'])
            authorities_dict.update({auth['name']: auth['root']})
        # token authorities
        for auth_token in token_schema['userGroupType']:
            token_auth_list.append(auth_token['name'])
        # check token auth
        for token_user_auth in token_auth_list:
            if token_user_auth in authorities_list and authorities_dict[token_user_auth] == 0:
                result = 0
                break
            elif token_user_auth in authorities_list and authorities_dict[token_user_auth] > 0:
                result = authorities_dict[token_user_auth]
    return result


def for_test_token():
    result = {
        'userPIN': 'C0D5B93D-A373-4EDF-B5A7-4A58C6EC8C88',
        'organisationPin': 'C64FA776-1C42-44DA-9F30-66CC725FEFC0',
        'userGroupType': [
            {
                'name': 'Administrator',
                'id': 3
            }
        ]
    }
    return result


def request_type_check(type_request_validation, request_data):
    """
    This method check type of all request field types.
    :param type_request_validation:
    :param request_data:
    :return:
    """
    status_code = 200
    for k, v in type_request_validation.items():
        if k in request_data and type(request_data[k]) not in v:
            status_code = 1201
            break
        elif k not in request_data:
            status_code = 1202
            break
    return status_code


def random_string_code_generator(length):
    result = ''
    letters = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    for i in range(0, length):
        result += random.choice(letters)
    return result


def current_full_str_date():
    return strftime("%d.%m.%Y %H:%M:%S", localtime())


def current_str_date():
    today = date.today()
    return today.strftime("%d.%m.%Y")


def current_str_time():
    format_time = "%H:%M"
    return datetime.now().time().strftime(format_time)


def current_full_obj_date():
    full_format_date = "%d.%m.%Y %H:%M:%S"
    return datetime.today().strptime(current_full_str_date(), full_format_date)


def current_full_sql_date():
    # full_format_date = "%Y-%m-%d %H:%M:%S"
    # result_date = datetime.today().strptime(strftime(full_format_date, localtime()), full_format_date)
    result_date = datetime.now()
    return result_date


def sorting(sorting_obj, sorting_param):
    sorted_obj = sorted(sorting_obj, key=lambda k: k[sorting_param])  # sorting array by parameters
    return sorted_obj


def desc_sorting(sorting_obj, sorting_param):
    sorted_obj = sorted(sorting_obj, key=lambda k: k[sorting_param],
                        reverse=True)  # DESC sorting oby by sorting parameters
    return sorted_obj


def date_day_difference(date1, date2):
    date_format = "%d.%m.%Y"
    date_1 = datetime.strptime(date1, date_format)
    date_2 = datetime.strptime(date2, date_format)
    difference = date_1 - date_2
    return difference.days


def str_to_obj_time(str_time):
    return datetime.strptime(str_time, '%H:%M').time()


def obj_date_to_str_date(obj_date):
    return datetime.strftime(obj_date, "%d.%m.%Y %H:%M")


# convert aze names to eng START
def aze_to_english_letter_replacement(input_text):
    if input_text is not None:
        aze_specific_letter_base = {
            "ə": "a",
            "Ə": "A",
            "i": "i",
            "İ": "I",
            "ı": "i",
            "I": "I",
            "ö": "o",
            "Ö": "O",
            "ü": "u",
            "Ü": "U",
            "ç": "ch",
            "Ç": "Ch",
            "ş": "sh",
            "Ş": "Sh",
            "ğ": "g",
            "Ğ": "G",
            "q": 'g',
            "Q": "G",
            "x": 'kh',
            "X": 'Kh'
        }
        keys = list(aze_specific_letter_base.keys())
        input_text = list(map(lambda t: t if t not in keys else aze_specific_letter_base[t], input_text))
        input_text = list(''.join(input_text))
        text_for_index_define = list(copy.deepcopy(input_text))
        define_upper_case_index = list(map(lambda i: replace_character_save_index(i, text_for_index_define) if i.isupper() else None, text_for_index_define))
        define_upper_case_index = list(filter(lambda f: f is not None, define_upper_case_index))
        input_text = ''.join(list(
            map(lambda t: replace_character_return_upper(t, input_text) if t.islower() and input_text.index(t) + 1 in define_upper_case_index else t,
                input_text)))
    return input_text


def replace_character_save_index(letter, full_txt):
    idx = full_txt.index(letter)
    full_txt[idx] = '_'
    return idx


def replace_character_return_upper(letter, full_list):
    idx = full_list.index(letter)
    full_list[idx] = '_'
    return letter.upper()


# convert aze names to eng END


def current_obj_time():
    return str_to_obj_time(current_str_time())


def obj_date_to_str_time(obj_date):
    return str(obj_date.hour) + ":" + str(obj_date.minute)


def current_obj_date():
    return datetime.now().date()


def index_pagination(collection, last_id, limit):
    result_list = list(collection.find({'_id': {'$lte': last_id}}).sort('_id', DESCENDING).limit(limit))
    list(map(lambda u: u.update({'employeeId': str(u['id']), 'id': str(u['_id'])}), result_list))
    list(map(lambda u: u.pop('_id'), result_list))
    return result_list


# face recognition algorithm
def face_recognition_from_picture(cv_frame, full_random_name, known_face_encodings, known_face_names):
    print("---- Recognized Started ----")
    small_frame = cv2.resize(cv_frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    small_rgb_frame = small_frame[:, :, ::-1]

    # get face location
    face_locations = face_recognition.face_locations(small_rgb_frame)
    print("- Face location scan completed")

    face_encodings = face_recognition.face_encodings(small_rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
        # face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        # print('Known percent:', (1-max(face_distance)*100))

        name = "not recognized"  # default name is not recognized

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            # acc = fbeta_score(known_face_encodings[first_match_index], face_encoding)
            # print('\n\n\n++++++++++++++++++++++++++++++++++++\n', acc, '\n++++++++++++++++++++++++++++++++++++\n\n\n')

        face_names.append(name)

    # print("- Face Locations:")
    # print face data
    # print(*face_locations, sep='\n')
    # print(*face_names, sep='\n')
    # print("- Face name searching completed")
    # draw face rectangle and name on current frame
    draw_face_on_image(cv_frame, face_locations, face_names, full_random_name)
    # Label string

    face_names = ''.join(face_names)
    count = str(len(face_locations))
    location = ','.join([str(i) for i in face_locations])
    # return_string = "\nNames: " + face_names + \
    #                 "\nFace Count: " + count + "\nLocations: " + location + "\n"
    user_id = face_names.split(".")
    user_id[0] = check_object_id(user_id[0])
    # print('//////////////////////////////////\n\n\n\n\n', user_id, '\n////////////////////////////////////////\n\n\n')
    if len(user_id) == 1 and "" in user_id or len(user_id) == 1 and "not recognized" in user_id:
        return_string = "Tanınmadı"
        found_id = None
    else:
        return_string = get_user_fullname_from_id(user_id[0])
        found_id = user_id[0]

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n', return_string, '\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # lblTag["text"] = return_string
    print("---- Recognized Completed ----")
    with open(full_random_name, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    result_schema = {
        "person": return_string,
        "tempFile": encoded_image,
        "foundId": found_id,
        'foundImage': None
    }
    return result_schema


def draw_face_on_image(def_frame, face_locations, face_names, temp_name):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(def_frame, (left, top), (right, bottom), (153, 0, 51), 4)

        # Draw a label with a name below the face
        cv2.rectangle(def_frame, (left, top + 35),
                      (right, top), (153, 0, 51), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        name = name if '.' not in name else get_user_fullname_from_id(str(name).split(".")[0])
        name = aze_to_english_letter_replacement(name)
        try:
            name = name if name == 'not recognized' else get_user_fullname_from_id(str(name))
            name = aze_to_english_letter_replacement(name)
        except bson.errors.InvalidId:
            pass
        cv2.putText(def_frame, name, (left + 10, top + 25), font, 1.0, (255, 255, 255), 2)
    # write temp image file for lblimage item
    cv2.imwrite(temp_name, def_frame)


def open_file(file, known_face_encodings, known_face_names):
    camera_is_open = False
    upload_dir = 'temp'
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = upload_dir
    # open file dialog for picture
    # filename = tkinter.filedialog.askopenfilename(initialdir="/", title="Choose Photo")
    # file = request.files['profileImage']
    filename = secure_filename(file.filename)
    full_name = filename.split('.')
    f_name = random_string_code_generator(32)
    filename = f_name + "." + full_name[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # recognize face
    full_random_name = app.config['UPLOAD_FOLDER'] + "/" + filename
    cv_frame = cv2.imread(full_random_name)
    return face_recognition_from_picture(cv_frame, full_random_name, known_face_encodings=known_face_encodings, known_face_names=known_face_names)


# face recognition
def base64_string_to_folder(base64_string, file_path, folder_name):
    # if base64_string is False: print('*******************\nb64:', base64_string, '\n*******************\n')
    img_data = base64.b64decode(base64_string)
    file_path = folder_name + "/" + file_path
    with open(file_path, 'wb') as f:
        f.write(img_data)


def get_user_fullname_from_id(_id, full=False):
    # db
    users = mongo.db.users
    # vars
    _id = check_object_id(_id)

    search = {
        "_id": ObjectId(_id)
    }
    # process
    result = users.find_one(search, {'_id': 0})
    result = result if result is None else str(result['firstName']) + ' ' + str(result['lastName']) if full is False else result
    return result


def get_user_pin_from_id(_id):
    # db
    users = mongo.db.users
    # vars
    _id = check_object_id(_id)

    search = {
        "_id": ObjectId(_id)
    }
    # process
    result = users.find_one(search, {'_id': 0})
    result = result if result is None else result['pin']
    return result


def get_user_from_pin(pin):
    # db
    users = mongo.db.users
    authority_users = mongo.db.authorityUsers
    # vars
    search = {
        "pin": pin
    }
    # process
    result = users.find_one(search)
    authority_type = authority_users.find_one({'userName': pin}, {'_id': 0, 'authorityType': 1})
    result = result if result is None else {'fullName': str(result['firstName']) + ' ' + str(result['lastName']), 'img': result['imageList'][0],
                                            'id': str(result['_id']), 'authorityType': authority_type if authority_type is None else authority_type['authorityType']}
    message_result = error_base(1555) if result is None else result
    return message_result, True if result is not None else False


def get_user_work_logs_from_id(_id):
    # db
    users_work_log = mongo.db.usersWorkLog
    # vars
    search = {'date': current_str_date(), 'userId': _id}
    # vars
    _id = check_object_id(_id)
    work_data = {}
    # process
    work_log = list(users_work_log.find(search, {'_id': 0}))
    list(map(lambda w: work_data.update(w), work_log)) if len(work_log) > 0 else work_data.update({'in': None, 'out': None})
    work_data.update({'in': None}) if 'in' not in work_data and 'out' in work_data else work_data.update(
        {'out': None}) if 'in' in work_data and 'out' not in work_data else None
    return work_data


def get_user_obj_id_from_id(user_id):
    # db
    users = mongo.db.users
    # vars
    search = {'id': user_id}
    result = users.find_one(search)
    _id = result if result is None else str(result['_id'])
    return _id


def get_user_work_log_from_id(user_id, by_fin=None, img=False, type_event=None, count_data=False):
    # db
    user_work_log = mongo.db.usersWorkLog
    # process
    search = {'byFin': by_fin, 'userId': user_id} if by_fin is not None else {'userId': user_id}
    if type_event is not None: search.update({'type': type_event})
    show = {'time': 0, 'date': 0, 'userId': 0, 'byFin': 0} if img is True else {'time': 0, 'image': 0, 'date': 0, 'userId': 0, 'byFin': 0}
    if count_data is False:
        find_work_log = list(user_work_log.find(search, show))
        list(map(lambda wl: wl.update({'fullDate': obj_date_to_str_date(wl['fullDate']), '_id': str(wl['_id'])}), find_work_log))
    else:
        find_work_log = user_work_log.find(search).count()
    return find_work_log


def get_employee_work_log_statistics(user_id):
    face_known = get_user_work_log_from_id(user_id=user_id, by_fin=False, count_data=True)
    face_not_known = get_user_work_log_from_id(user_id=user_id, by_fin=True, count_data=True)
    total_event = face_known + face_not_known
    stats = {'faceKnownPercent': 0, 'countWithFin': face_not_known, 'countWithFace': face_known, 'faceNotKnownPercent': 0, 'totalCount': total_event} if total_event == 0 else {'faceKnownPercent': int(face_known*100/total_event), 'faceNotKnownPercent': int(face_not_known*100/total_event),  'countWithFin': face_not_known, 'countWithFace': face_known, 'totalCount': total_event}
    return stats


def get_user_object_id_by_pin(pin):
    # var
    search = {
        'pin': pin
    }
    # db
    users = mongo.db.users
    # process
    find_user = users.find_one(search)
    return None if find_user is None else str(find_user['_id'])


def check_object_id(_id):
    while "recognized" in _id:
        if ObjectId.is_valid(_id) is False:
            _id = _id.replace("not ", "")
            _id = _id.replace("recognized", "")
    while len(_id) > 24:
        _id = _id[:-1]
    return _id


def get_user_image_from_id(_id):
    # db
    users = mongo.db.users
    # vars
    _id = check_object_id(_id)
    search = {
        "_id": ObjectId(_id)
    }
    result = users.find_one(search, {'_id': 0})
    result = result if result is None else None if len(result['imageList']) == 0 else result['imageList'][-1]['image']
    return result


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def all_image_merge(element):
    # var
    # print('\n\n\n*********************************\n', element, '\n*********************************\n\n\n')
    images = list(map(lambda im: im, element['imageList']))
    index_list = None if 0 < len(images) <= 1 else True if len(images) > 1 else False

    if index_list is True or index_list is None:
        if index_list is True:
            list(map(lambda im: im.update({"url": str(element['_id']) + str("_") + str(images.index(im) + 1) + '.' + str(im['contentType']).split('/')[1]}),
                     images))
        else:
            list(map(lambda im: im.update({"url": str(element['_id']) + '.' + str(im['contentType']).split('/')[1]}), images))
        list(map(lambda im: base64_string_to_folder(base64_string=im['image'], file_path=im['url'], folder_name="faces"), images))


# database and face training
def train_faces(known_face_names, known_face_encodings, document_list=[], mini=False):
    print("---- Training Started ----")
    # db
    users = mongo.db.users
    training_base = mongo.db.training
    ram_user = mongo.db.ramUser
    # process
    all_ram_user = list(ram_user.find({}, {"_id": False}))
    all_ram_image_names = list(map(lambda imn: imn['id'], all_ram_user))  # all wanted image names
    all_ram_user = list(map(lambda ru: ObjectId(ru['id']), all_ram_user))
    all_images = list(users.find()) if mini is False else list(users.find({'_id': {'$in': all_ram_user}}))
    if len(all_images) > 0:
        list(map(lambda im: all_image_merge(im), all_images))
        cond_base = True if mini is True else True if training_base.count() == 0 else False
        if cond_base is True:
            # process
            for root, dirs, files in os.walk("./faces"):
                for filename in files:
                    # print(filename, type(filename))
                    file_result = filename.split("_")
                    known_face_names.append(file_result[0])
                    print('filename: ', filename)
                    image = face_recognition.load_image_file("faces/" + filename)
                    if len(face_recognition.face_encodings(image)) > 0:
                        image_face_encoding = face_recognition.face_encodings(image)[0]
                        known_face_encodings.append(image_face_encoding)
                        image_face_encoding = list(map(lambda s: str(s), image_face_encoding))
                        document_list.append(pymongo.InsertOne(
                            {'knownFaceName': file_result[0], 'knownFaceEncoding': image_face_encoding, 'emp_id': file_result[0].split('.')[0]}))
                        # print("Name: " + file_result[0])

        print("---- Training Completed ----")


def general_training(mini=False):
    # db
    training = mongo.db.training
    ram_user = mongo.db.ramUser
    # vars
    known_face_encodings = []
    known_face_names = []
    document_list = []
    result = True
    if mini is False:
        training.remove()
    train_faces(known_face_names=known_face_names, known_face_encodings=known_face_encodings, document_list=document_list, mini=mini)
    if len(document_list) > 0:
        training.bulk_write(document_list)
        ram_user.remove()
        # remove all files in 'faces' folder
        files = glob.glob('faces/*')
        list(map(lambda f: os.remove(f), files))
    else:
        result = False
    return result


def convert_str_to_numpy(str_list):
    return list(np.asarray(str_list, dtype=np.float32))


def read_training():
    # db
    training = mongo.db.training
    # vars
    known_face_encodings = []
    known_face_names = []
    # result = training.find_one({}, {"_id": False})
    result = list(training.find({}, {"_id": False}))
    if len(result) > 0:
        known_face_names = list(map(lambda r: r['knownFaceName'], result))
        known_face_encodings = list(map(lambda e: e['knownFaceEncoding'], result))
        known_face_encodings = list(map(lambda c: convert_str_to_numpy(c), known_face_encodings))
    # if result is not None:
    #     known_face_names = result['knownFaceNames']
    #     known_face_encodings = result['knownFaceEncoding']
    #     known_face_encodings = list(map(lambda c: convert_str_to_numpy(c), tqdm(known_face_encodings, desc='Make encoding faces progress:')))
    result = {'knownFaceNames': known_face_names, 'knownFaceEncoding': known_face_encodings}
    return result


# synchronise users
def call_employee_service(page_number, page_size, insert_sync_data=True):
    """
    Service using with static token.
    :param insert_sync_data:
    :param page_number:
    :param page_size:
    :return:
    """
    # vars
    error = False
    # service_url = "http://172.23.43.109:8080/hr-1/users/faceRecognition/userList?offset=" + str(offset) + "&max=" + str(max_employee)
    # headers = {
    #     "Authorization": "Basic 30b7f6624d004337a1544176c5f242ae",
    #     "Content-Type": "application/json",
    #     "UserGroupTypeId": "1"
    # }
    service_url = "http://10.97.178.7:5002/User/user-structure-integration?PageNumber=" + str(page_number) + "&PageSize=" + str(page_size)
    headers = {
        "ApiKey": "9bef3b8aaf07a502508d5ceff14e0e5a4b848beb0c3410ed6a1b244b542928e8f215e8f845837276280477c09124541f14106d426642fece82e366e83ede3e11"
    }
    service_response = requests.get(url=service_url, headers=headers)
    service_response = json.loads(service_response.content)
    if type(service_response) is dict:
        if service_response['exception'] is None and service_response['statusCode'] == 200:
            total_page_size = service_response['data']['totalPages']
            result_list = service_response['data']['dataSource']
            # retry
            message = total_page_size
            if insert_sync_data is True:
                print('page num:', page_number)
                insert_employee(employee_list=result_list)
        else:
            # brake
            message = "Service not response the request"
            error = True
    else:
        # break
        message = "Bad response"
        error = True
    return {"message": message, "error": error}


def sync_employee():
    result_employees = call_employee_service(page_number=1, page_size=100, insert_sync_data=False)
    result = result_employees['error']
    if result is False:
        # vars
        page_size = 100
        total_pages = result_employees['message']
        print('-----------------\n\nTOTAL PAGES:', total_pages)
        list(map(lambda c: call_employee_service(page_number=c, page_size=page_size), range(1, total_pages + 1)))
        print('\n\n-----------------\n')
    result = True if result is False else False
    return result


def insert_employee(employee_list):
    # var
    no_avatar = '/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/4QMpaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1LjAtYzA2MCA2MS4xMzQ3NzcsIDIwMTAvMDIvMTItMTc6MzI6MDAgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCBDUzUgV2luZG93cyIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDoyM0UzNkIzM0FFOUUxMUUxQUI0NUNBNEZDNzcyNzczRiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoyM0UzNkIzNEFFOUUxMUUxQUI0NUNBNEZDNzcyNzczRiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjIzRTM2QjMxQUU5RTExRTFBQjQ1Q0E0RkM3NzI3NzNGIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjIzRTM2QjMyQUU5RTExRTFBQjQ1Q0E0RkM3NzI3NzNGIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+/+4ADkFkb2JlAGTAAAAAAf/bAIQAAgICAgICAgICAgMCAgIDBAMCAgME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'
    avatar_exception = ['', None, False, True,  'false', 'NONE', 'null', 'true', 'TRUE', 'FALSE']
    employee_exception = ['4784FD19-FF22-4EC5-AB03-73D7F272C3AD']
    # db
    users_base = mongo.db.users
    ram_users = mongo.db.ramUser
    # process

    list(map(lambda ups: ups.update({'id': str(ups['id']).upper(), 'parentStructureId': str(ups['parentStructureId']).upper(), 'structureId': str(ups['structureId']).upper()}), employee_list))  # ID to upper

    employee_list = list(filter(lambda f: f['id'] not in employee_exception, employee_list))  # if not chairman
    photo_id = list(map(lambda p: {'id': p['id'], 'photo': p['photo'] if p['photo'] not in avatar_exception else no_avatar}, employee_list))
    # photo_id = list(map(lambda p: {'id': p['id'], 'photo': p['photo']}, employee_list))
    list(map(lambda ph: ph.pop('photo'), employee_list))
    # list(map(lambda im: im.update({'imageList': [{'image': list(filter(lambda f: f['id'] == im['id'], photo_id))[0]['photo'], 'contentType': 'image/jpeg'}]}), employee_list))

    query_list = list(map(lambda q: pymongo.UpdateOne({'id': q['id']}, {'$setOnInsert': q, '$addToSet': {'imageList': {'image': list(filter(lambda f: f['id'] == q['id'], photo_id))[0]['photo'], 'contentType': 'image/jpeg'}}}, upsert=True), employee_list))
    # query_list = list(map(lambda q: pymongo.UpdateOne({'id': q['id']}, {'$setOnInsert': q}, upsert=True), employee_list))
    result_insert = users_base.bulk_write(query_list)
    result_count = result_insert.bulk_api_result['nUpserted']
    result_inserted = result_insert.bulk_api_result['upserted']
    print('> COUNT:', result_count)
    if result_count > 0:
        result_inserted = list(map(lambda ins: {'id': str(ObjectId(ins['_id']))}, result_inserted))
        ram_users.insert(result_inserted)
    return result_insert.bulk_api_result['nUpserted']


# find user
def search_employee(first_name=None, last_name=None, patronymic=None):
    # {firstName: /^t/i}
    users = mongo.db.users  # base table
    big_search = {}  # for search
    # make upper********************************************
    if first_name is not None:
        first_name = str(first_name).upper()
    if last_name is not None:
        last_name = str(last_name).upper()
    if patronymic is not None:
        patronymic = str(patronymic).upper()
    # make upper********************************************
    arguments = [{"firstName": first_name}, {"lastName": last_name}, {"patronymic": patronymic}]  # for search
    output = []  # for result
    # parsed_date = date_parsing(date=date)
    error = False
    status_code = 200
    for args in arguments:
        for key, value in args.items():
            if value:
                regx = re.compile("^" + value, re.IGNORECASE)
                big_search.update({key: regx})
    # big_search.update({"DELETE": {'$exists': False}})
    result = list(users.find(big_search, {"_id": False}))
    if len(result) > 0:
        for user in result:
            output.append(user)
    else:
        status_code = 404.37

    if status_code != 200:
        error = True
    return {'error': error, 'data': output, 'code': status_code}


# filename
def random_filename_generator(name_length: int, fullname: str):
    filename, name_p_1 = fullname.split("."), random_string_code_generator(name_length)
    return name_p_1 + "." + filename[1]


# synchnorize sql
def convert_table_data_dict(table):
    table_headers = table.description
    table_headers = list(map(lambda h: h[0], table_headers))

    table_data_helper = table.fetchall()
    table_data = list(map(lambda d: dict(zip(table_headers, d)), table_data_helper))
    # process
    output = None if len(table_data) == 0 else table_data
    return output


def insert_query_helper(values_and_rows: list, type_element: str, date_fields: bool = False, date_elements: list = []):
    """
    This function is helps to make insert query
    :param date_elements:
    :param date_fields:
    :param values_and_rows:
    :param type_element:
    :return:
    """
    query_elements = []
    list(map(lambda u: u.update({str(next(iter(u.keys()))): '\'' + str(next(iter(u.values()))) + '\''}) if type(u[str(next(iter(u.keys())))]) is str else None,
             values_and_rows))
    if type_element == "keys":
        list(map(lambda ql: query_elements.append(str(next(iter(ql.keys()))) + ", "), values_and_rows))
    elif type_element == "values":
        list(map(lambda ql: query_elements.append(
            str(str(next(iter(ql.values()))) + ", ") if date_fields is False else 'GETDATE(), ' if str(next(iter(ql.values()))).replace("''",
                                                                                                                                        "") in date_elements else str(
                str(next(iter(ql.values()))) + ", ")), values_and_rows))
        query_elements = list(map(lambda q: q.replace("''", "'"), query_elements))
    else:
        return None
    query_elements[-1] = query_elements[-1][:-2]
    result = "".join(query_elements)
    return result


def update_query_helper(query: str, values_and_rows: list, statement: str):
    """
    This function is helps to make insert query
    :param statement:
    :param values_and_rows:
    :param query:
    :return:
    """
    query_elements = []
    helper_str_add = ""
    values_and_rows = list(filter(lambda f: str(next(iter(f.keys()))) != statement, values_and_rows))
    list(map(lambda u: u.update({str(next(iter(u.keys()))): "'" + str(next(iter(u.values()))) + "'"}) if type(u[str(next(iter(u.keys())))]) is str else None,
             values_and_rows))
    list(map(lambda q: query_elements.append(str(next(iter(q.keys()))) + "=" + str(next(iter(q.values()))) + ", "), values_and_rows))
    helper_str_add = helper_str_add.join(query_elements)
    query += helper_str_add
    result = query[:-2]
    return result


def query_maker(table: str, values_and_rows: list, type_query: str, statement: str = '', statement_type: str = '', compare_value=None,
                date_fields: bool = False, date_elements: list = []):
    """
    This method modeling the query
    :param date_elements:
    :param date_fields:
    :param compare_value:
    :param statement_type:
    :param statement: <condition> (it works if type_query is update)
    :param type_query: <update> / <insert>
    :param table: <table name>
    :param values_and_rows: {<row>: <value>}
    :return: full sql query
    """
    result = None
    query = ""
    type_query = type_query.lower()
    if type_query in ["update", "insert"]:
        if type_query == "update" and len(statement) > 0 and len(statement_type) > 0 and compare_value is not None:
            query = query + "UPDATE " + str(table) + " SET "
            query = update_query_helper(query=query, values_and_rows=values_and_rows, statement=statement)
            result = query + " WHERE " + str(statement) + statement_type + str(compare_value) + ";"
        elif type_query == "insert":
            query = query + "INSERT INTO " + str(table) + " ("
            helper = insert_query_helper(values_and_rows=values_and_rows, type_element="keys")
            query = None if helper is None else query + helper + ") VALUES ("
            if query is not None:
                helper = insert_query_helper(values_and_rows=values_and_rows, type_element="values", date_fields=date_fields, date_elements=date_elements)
                query = None if helper is None else query + helper + ");"
            result = query
    return result


def run_sql_with_transaction(sql_query_list: list, date_element: bool = False, replace_with: str = ''):
    """
    This function is working with transaction. Using insert and update process only.
    :param replace_with:
    :param date_element:
    :param sql_query_list:
    :return:
    """
    # connection
    conn = pyodbc.connect('DRIVER=SQL Server;SERVER=ITS-NB-047;PORT=1433;DATABASE=test;UID=sa;PWD=Aze1234567')
    # conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.23.45.1;PORT=1433;DATABASE=Central_prod;UID=AppUserFace;PWD=N7?fT4NC!0vu26?3Isg2g+f9Y#p0L32x5!Jz+Xyd')
    # conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.23.45.1;PORT=1433;DATABASE=HR;UID=AppUserFace;PWD=N7?fT4NC!0vu26?3Isg2g+f9Y#p0L32x5!Jz+Xyd')
    # conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=192.168.179.9;PORT=1433;DATABASE=CommonFileUplaod;UID=AppUserFace;PWD=6Av$55n478%Ig!ZZ&b22duQb77R9')  # new
    cursor = conn.cursor()

    # try:
    error = False
    conn.autocommit = True
    new_sql_query = []

    if date_element is True and replace_with != '':
        list(map(lambda qs: new_sql_query.append(str(qs).replace(replace_with, '?')), sql_query_list))
        # list(map(lambda qs: new_sql_query.append(str(qs)), sql_query_list))
        print('\n\n\n>>>>>>>>>>>>>>>>>>>>>\n', new_sql_query, '\n\n\n>>>>>>>>>>>>>>>>>>>>>\n')
        if len(new_sql_query) > 1:
            list(map(lambda sql_query: cursor.execute(sql_query, (current_full_sql_date())), new_sql_query))
        else:
            cursor.execute(new_sql_query[0], (current_full_sql_date()))
            # cursor.execute(new_sql_query[0])
    else:
        list(map(lambda sql_query: cursor.execute(sql_query), sql_query_list))
    cursor.close()
    conn.close()

    output = {'error': error, 'status': 'Connection lost', 'exceptData': pyodbc.Error}
    return output


def percent_count(*args: int):
    total = 0
    zero_div = True
    args = list(args)
    for ar in args:
        total += ar
        if total > 0:
            zero_div = False
    return list(map(lambda ars: {ars: 0}, args)) if zero_div else list(map(lambda ars: {ars: float(ars) * 100 / float(total)}, args))


def str_to_iso_date(str_date: str):
    """
    dd.mm.Y format to ISODate format
    :param str_date:
    :return:
    """
    date_list = str(str_date).split(".")
    d_day = int(date_list[0])
    d_month = int(date_list[1])
    d_year = int(date_list[2])
    try:
        return datetime(d_year, d_month, d_day, 0, 0, 0)
    except ValueError:
        return None


def str_to_datetime_date(str_date: str):
    """
    dd.mm.Y format to ISODate format
    :param str_date:
    :return:
    """
    date_list = str(str_date).split(".")
    d_day = int(date_list[0])
    d_month = int(date_list[1])
    d_year = int(date_list[2])
    try:
        return date(d_year, d_month, d_day)
    except ValueError:
        return None


def datetime_to_iso_date(event_date):
    """
    Y-mm-dd format to ISODate format
    :param event_date:
    :return:"""
    event_date = str(event_date)
    date_list = str(event_date).split("-")
    d_day = int(date_list[2])
    d_month = int(date_list[1])
    d_year = int(date_list[0])
    try:
        return datetime(d_year, d_month, d_day, 0, 0, 0)
    except ValueError:
        return None


def monthly_statistics(str_date: str, additional_param=None):
    # db
    users_work_log = mongo.db.usersWorkLog
    # var
    start_date = str_to_datetime_date(str_date=str_date)
    end_date = start_date + relativedelta(months=1)
    start_date, end_date = datetime_to_iso_date(start_date), datetime_to_iso_date(end_date)
    search = {
        "fullDate": {"$gt": start_date, "$lt": end_date}
    }
    if additional_param is not None:
        search.update(additional_param)
    find_logs = users_work_log.find(search).count()
    return {str(str_date).split('.')[1]: find_logs}


def monthly_percent_statistics(list_data1: list, list_data2: list, return_result=1):
    """
    list_data1 must be same(list length and keys in dict elements of list) as list_data2 and return_result is defines result of function (result by list_data1 or list_data2)
    :param return_result:
    :param list_data1:
    :param list_data2:
    :return:
    """
    result1 = []
    result2 = []
    list(map(lambda pe: list(map(lambda pee: list(map(
        lambda pr: result1.append(pr[list(pe.values())[0]]) if list(pe.values())[0] in pr else None if return_result == 1 else result2.append(
            pr[list(pee.values())[0]]) if list(pee.values())[0] in pr else None, percent_count(list(pe.values())[0], list(pee.values())[0]))) if
    list(pe.keys())[0] == list(pee.keys())[0] else None, list_data2)), list_data1))
    # list(map(lambda pe: list(map(lambda pee: list(map(lambda pr: print(pr[list(pe.values())[0]]) if list(pe.values())[0] in pr else None if return_result == 1 else print(pr[list(pee.values())[0]]) if list(pee.values())[0] in pr else None, percent_count(list(pe.values())[0], list(pee.values())[0]))) if list(pe.keys())[0] == list(pee.keys())[0] else None, list_data2)), list_data1))
    # print('****************\n', result1 if return_result == 1 else result2)
    return result1 if return_result == 1 else result2


def pin_not_pin_monthly_percent_count(list_data1: list, list_data2: list, return_result=1):
    result1 = []
    result2 = []
    compare_list = []
    for l1 in list_data1:
        if return_result == 1:
            compare_list = deepcopy(list_data1)
            list(map(lambda l2: None if list(l1.values())[0] == 0 and list(l2.values())[0] == 0 else result1.append(
                {list(l1.keys())[0]: list(l1.values())[0] * 100 / (list(l1.values())[0] + list(l2.values())[0])}) if list(l1.keys())[0] == list(l2.keys())[
                0] else None, list_data2))
        else:
            compare_list = deepcopy(list_data2)
            list(map(lambda l2: None if list(l1.values())[0] == 0 and list(l2.values())[0] == 0 else result2.append(
                {list(l2.keys())[0]: list(l2.values())[0] * 100 / (list(l1.values())[0] + list(l2.values())[0])}) if list(l1.keys())[0] == list(l2.keys())[
                0] else None, list_data2))
    result_merge = result1 if len(result1) > 0 else result2 if len(result2) > 0 else []
    list(map(
        lambda r: list(map(lambda rr: r.update({list(r.keys())[0]: list(rr.values())[0]}) if list(r.keys())[0] == list(rr.keys())[0] else None, result_merge)),
        compare_list))
    result = list(map(lambda res: list(res.values())[0], compare_list))
    return result


def ip_validation(ip):
    result = False
    len_ip = str(ip).split('.')
    if len(len_ip) == 4:
        try:
            socket.inet_aton(ip)
            result = True
        except socket.error:
            result = False
    return result


# internal token====================================================================================================================
def update_token_session(user_type):
    token = None
    if session['logged']:
        username = session['userData']['userName']
        user_type_check = check_auth(user_name=username, only_user_name=True)
        user_type_check = user_type_check if user_type_check is None else user_type_check['authorityType']
        print(user_type_check, '->', user_type)
        if user_type_check == user_type:
            token = jwt.encode({'user': username, 'authorityType': user_type, 'exp': datetime.utcnow() + timedelta(minutes=10)}, app.config['SECRET_KEY'])
            session['token'] = token
            session['logged'] = True
        else:
            message = "Yalnış token"
            session['token'] = None
            session['logged'] = False
            data = {'error': True, 'message': message, 'data': None, 'code': 404}
            return data
    return token


def internal_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.headers.get('Authorization')
        global response_data
        token = session.get('token')
        page_functions_list = [
            'introduce_function',
            'admin_function',
            'compare_user_function',
            'employees_function',
            'statistics_function',
            'login_func',
        ]
        if not token:
            # return jsonify({'message': 'Token is missing'}), 403
            message = "Token yoxdur"
            if f.__name__ in page_functions_list:
                return render_template("admin/login.html", warning=message)
            else:
                response_data = {'error': True, 'message': message, 'data': None, 'code': 404}
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if f.__name__ not in page_functions_list:
                message = "Sorğu uğurla başa çatdı"
                print(decoded)
                response_data = {'error': False, 'message': message, 'data': {'authorityType': decoded['authorityType']}, 'code': 200}
        except jwt.ExpiredSignatureError:
            session['logged'] = False
            session['userData'] = None
            message = "Sessiyanın vaxtı bitmişdir"
            if f.__name__ in page_functions_list:
                print('\n\npage api and token is expired\n\n')
                return render_template("admin/login.html", warning=message)
            else:
                print('\n\nrestful api and token is expired\n\n')
                # return redirect('/login', code=303)
                response_data = {'error': True, 'message': message, 'data': None, 'code': 403}
                # return jsonify(response_data, 200)
            # return jsonify({'message': 'Token is expired'})
        except jwt.DecodeError:
            # return jsonify({'message': 'Token is invalid'}), 403
            message = "Yalnış token"
            if f.__name__ in page_functions_list:
                return render_template("admin/login.html", warning=message)
            else:
                response_data = {'error': True, 'message': message, 'data': None, 'code': 405}
        if f.__name__ in page_functions_list:
            return f(*args, **kwargs)
        else:
            return f(response_data, *args, **kwargs)
    return decorated

# EMOTION PROJECT===================================================================================================================


def face_detect(b64_img):
    b64image = b64_img
    b64image = b64image.replace("data:image/jpeg;base64,", "")
    img_name = random_string_code_generator(32)
    img_name = img_name + '.jpeg'
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
    base64_string_to_folder(base64_string=b64image, file_path=img_name, folder_name="temp")
    full_path = 'temp/' + img_name
    try:
        DeepFace.detectFace(img_path=full_path, detector_backend=backends[2])
        result_detection = True
    except ValueError:
        result_detection = False
    os.unlink(full_path)
    return result_detection


# EMOTION PROJECT - detect new image and insert trained data
def detect_and_insert_new_files(file_dir):
    # db
    pins = mongo_emotion_base.db.pins
    # vars & process
    file_list = os.listdir(file_dir)
    file_list = list(filter(lambda fl: ".jpg" in fl or ".jpeg" in fl or ".png" in fl or ".bmp" in fl or ".gif" in fl, file_list))
    query_list = list(map(lambda fl: pymongo.UpdateOne({'pin': str(fl).split(".")[0]}, {'$setOnInsert': {'pin': str(fl).split(".")[0], 'date': [current_full_obj_date()]}}, upsert=True), file_list))
    if len(query_list) > 0:
        bulk_insert_pin = pins.bulk_write(query_list)
        result = bulk_insert_pin.bulk_api_result
        inserted = list(map(lambda i: str(i['_id']), result['upserted']))
    else:
        inserted = []
        result = {'nUpserted': [], 'nModified': []}
    # print(inserted, '\n', result)
    return {"newInserted": result['nUpserted'], 'modified': result['nModified'], 'inserted': inserted}


# EMOTION PROJECT - new detected face training
def detected_new_faces_train(known_face_names, known_face_encodings, url_folder, document_list=[], face_reg_list=[]):
    # db
    people = mongo_emotion_base.db.people
    pins_coll = mongo_emotion_base.db.pins
    # var
    output = None
    # process
    if len(face_reg_list) > 0:
        # process
        face_reg_list = list(map(lambda ids: ObjectId(ids), face_reg_list))
        pin_list = list(pins_coll.find({"_id": {"$in": face_reg_list}}))
        pin_list = list(map(lambda pn: pn['pin'], pin_list))
        print("\n---- Training Started ----\n") if len(pin_list) > 0 else None
        for root, dirs, files in os.walk(url_folder):
            for filename in files:
                pin_code = filename.split(".")
                if pin_code[0] in pin_list:
                    # print(filename, type(filename))
                    file_result = filename.split("_")
                    known_face_names.append(file_result[0])
                    print('\tfilename: ', filename)
                    image = face_recognition.load_image_file(str(url_folder) + str(filename))
                    if len(face_recognition.face_encodings(image)) > 0:
                        image_face_encoding = face_recognition.face_encodings(image)[0]
                        known_face_encodings.append(image_face_encoding)
                        image_face_encoding = list(map(lambda s: str(s), image_face_encoding))
                        document_list.append(pymongo.InsertOne(
                            {'knownFaceName': file_result[0], 'knownFaceEncoding': image_face_encoding, 'pin': file_result[0].split(".")[0]}))
                        # print("Name: " + file_result[0])
        print("\n---- Training Completed ----\n") if len(pin_list) > 0 else None
        if len(document_list) > 0:
            result_bw = people.bulk_write(document_list)
            output = result_bw.bulk_api_result['nInserted']
    return output


# EMOTION PROJECT - new detected face process
def detect_and_train(path_dir):
    result_detect = detect_and_insert_new_files(file_dir=path_dir)
    known_face_names = []
    known_face_encodings = []
    document_list = []
    output = detected_new_faces_train(known_face_names=known_face_names, known_face_encodings=known_face_encodings, url_folder=path_dir,
                                      document_list=document_list, face_reg_list=result_detect['inserted'])
    output = output if output is not None else 0
    return output


# EMOTION PROJECT - select all daily events from SQL
# def select_query(table_name: str, statement: str = "", statement_element: str = "", statement_compare_value: str = "", show_rows: list = []):
#     rows_tab = ""
#     for r in show_rows:
#         rows_tab = rows_tab+r+", "
#     query = "select {rows_tab} from {table_name} {ids}"
#     rows_tab = "*" if rows_tab == "" else rows_tab[:-2]
#     # conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=172.23.45.1;PORT=1433;DATABASE=HR;UID=AppUserFace;PWD=N7?fT4NC!0vu26?3Isg2g+f9Y#p0L32x5!Jz+Xyd')
#     conn = pyodbc.connect('DRIVER={SQL Server};SERVER=ITS-NB-047;DATABASE=test;UID=sa;PWD=Aze1234567')
#     cursor = conn.cursor()
#     if statement_element != "" and statement_compare_value != "" and statement != "":
#         statement_compare_value = "'" + statement_compare_value + "'"
#         query = query.format(ids="where " + str(statement_element) + statement + statement_compare_value, table_name=table_name, rows_tab=rows_tab)
#     else:
#         query = query.replace(' {ids}', '')
#         query = query.format(table_name=table_name, rows_tab=rows_tab)
#     print(query)
#     tab = cursor.execute(query)
#     output = convert_table_data_dict(table=tab)
#     cursor.close()
#     conn.close()
#     return output


# EMOTION PROJECT - check pin
def check_people_pin(people_pin):
    people_pin = people_pin if "recognized" not in people_pin and len(people_pin) == 7 else "not recognized"
    return people_pin


# EMOTION PROJECT - get all daily events
# def get_all_events():
#     pins = mongo_emotion_base.db.pins
#     daily_event = select_query(table_name="acc_face")
#     query_list = list(map(lambda ql: pymongo.UpdateOne({"pin": ql['pin']}, {"$addToSet": {'date': ql['date_created']}}), daily_event))
#     event_count = pins.bulk_write(query_list).bulk_api_result['nModified']
#     return event_count


# EMOTION PROJECT - merge function
def selected_face_recognition(photos: list, url_folder: str, known_face_encodings: list, known_face_names:list):
    # process
    result_list = []
    if len(photos) > 0:
        valid_images = [".jpg", ".gif", ".png", ".tga"]
        # image_list = []
        # for f in os.listdir(url_folder):
        #     ext = os.path.splitext(f)[1]
        #     if ext.lower() not in valid_images and os.path.splitext(f) not in photos:
        #         continue
        #     image_list.append(PIL.Image.open(os.path.join(url_folder, f)))
        image_list = list(map(lambda file_im: None if os.path.splitext(file_im)[1].lower() not in valid_images or file_im not in photos else PIL.Image.open(os.path.join(url_folder, file_im)), os.listdir(url_folder)))
        image_list = list(filter(lambda iml: iml is not None, image_list))
        result_list = list(map(lambda im: open_file_emotion(file=im, known_face_encodings=known_face_encodings, known_face_names=known_face_names), image_list))
    return result_list


# EMOTION PROJECT - face recognition
def face_recognition_from_picture_emotion(cv_frame, full_random_name, known_face_encodings, known_face_names):
    print("---- People Recognized Started ----")
    small_frame = cv2.resize(cv_frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    small_rgb_frame = small_frame[:, :, ::-1]

    # get face location
    face_locations = face_recognition.face_locations(small_rgb_frame)
    print("- People Face location scan completed:]\t", face_locations)

    face_encodings = face_recognition.face_encodings(small_rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)

        name = "not recognized"  # default name is not recognized
        print(matches)

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            # acc = fbeta_score(known_face_encodings[first_match_index], face_encoding)
            # print('\n\n\n++++++++++++++++++++++++++++++++++++\n', acc, '\n++++++++++++++++++++++++++++++++++++\n\n\n')

        face_names.append(name)

    draw_face_on_image_emotion(cv_frame, face_locations, face_names, full_random_name)
    # Label string

    face_names = ''.join(face_names)

    count = str(len(face_locations))
    location = ','.join([str(i) for i in face_locations])

    print('count:\t', count, '\tlocation:\t', location)

    people_pin = face_names.split(".")
    people_pin[0] = check_object_id(people_pin[0])
    # print('//////////////////////////////////\n\n\n\n\n', user_id, '\n////////////////////////////////////////\n\n\n')
    if (len(people_pin) == 1 and "" in people_pin or len(people_pin) == 1) or "not recognized" == people_pin:
        return_string = "Tanınmadı"
        found_pin = None
    else:
        return_string = people_pin[0]
        found_pin = people_pin[0]

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n', return_string, '\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # lblTag["text"] = return_string
    print("---- Recognized Completed ----")
    with open(full_random_name, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    result_schema = {
        "SerialNumber": found_pin
    }
    return result_schema


# EMOTION PROJECT - face recognition
def draw_face_on_image_emotion(def_frame, face_locations, face_names, temp_name):
    for (top, right, bottom, left), people_pin in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(def_frame, (left, top), (right, bottom), (153, 0, 51), 4)

        # Draw a label with a name below the face
        cv2.rectangle(def_frame, (left, top + 35),
                      (right, top), (153, 0, 51), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        people_pin = people_pin if '.' not in people_pin else str(people_pin).split(".")[0]
        people_pin = aze_to_english_letter_replacement(people_pin)
        try:
            people_pin = people_pin if people_pin == 'not recognized' else people_pin
            people_pin = aze_to_english_letter_replacement(people_pin)
        except bson.errors.InvalidId:
            pass
        cv2.putText(def_frame, people_pin, (left + 10, top + 25), font, 1.0, (255, 255, 255), 2)
    # write temp image file for lblimage item
    cv2.imwrite(temp_name, def_frame)


# EMOTION PROJECT - face recognition
def open_file_emotion(file, known_face_encodings, known_face_names):
    upload_dir = 'temp'
    app.config['UPLOAD_FOLDER'] = upload_dir
    filename = secure_filename(file.filename)
    full_name = filename.split('.')
    f_name = random_string_code_generator(32)
    filename = f_name + "." + full_name[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # recognize face
    full_random_name = app.config['UPLOAD_FOLDER'] + "/" + filename
    cv_frame = cv2.imread(full_random_name)
    return face_recognition_from_picture_emotion(cv_frame, full_random_name, known_face_encodings=known_face_encodings, known_face_names=known_face_names)


# EMOTION PROJECT - people training
def read_people_training(pin_list):
    # db
    training = mongo_emotion_base.db.people
    # vars
    known_face_encodings = []
    known_face_names = []
    # result = training.find_one({}, {"_id": False})
    result = list(training.find({'pin': {'$in': pin_list}}, {"_id": False}))
    if len(result) > 0:
        known_face_names = list(map(lambda r: r['knownFaceName'], result))
        known_face_encodings = list(map(lambda e: e['knownFaceEncoding'], result))
        known_face_encodings = list(map(lambda c: convert_str_to_numpy(c), known_face_encodings))

    result = {'knownFaceNames': known_face_names, 'knownFaceEncoding': known_face_encodings}
    return result


# EMOTION PROJECT - deep-face recognition
def face_recognition_deep_face(compare_img: str, image_base_path: str):
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    print(image_base_path)
    result = DeepFace.find(img_path=compare_img, db_path=image_base_path, model_name=models[0])
    return result.to_dict()


# EMOTION PROJECT - deep-face verify
def face_verify_deep_face(img1_path: str, img2_path: str, pin: str):
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
    result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name=models[6], detector_backend=backends[4])
    result = result if result['verified'] else None
    if result is not None:
        result.update({'serial': pin})
    print('\n\n\n--------------\n', result)
    return result


# EMOTION PROJECT - schedule --------------------------------------------------------------------------------------------------------------------------------
def erase_emotion_collections(compare_str_time: str):
    # db
    people = mongo_emotion_base.db.people
    pins_coll = mongo_emotion_base.db.pins
    # process
    count_of_peoples = people.find().count()
    count_of_pins_coll = pins_coll.find().count()
    if current_obj_time() > str_to_obj_time(compare_str_time) and count_of_peoples > 0 and count_of_pins_coll > 0:
        people.remove({})
        pins_coll.remove({})


# EMOTION PROJECT - schedule --------------------------------------------------------------------------------------------------------------------------------
def schedule_task():
    """Run scheduled job."""
    compare_str_time = "17:52"
    if current_obj_time() < str_to_obj_time(compare_str_time):
        print('Schedule started: \t', current_str_time(), '\n************************')
        # var & process
        file_dir = "D:\\images\\"
        inside_folder = list(os.listdir(file_dir))
        output = list(map(lambda rl: {'folder': rl, 'insertedCount': detect_and_train(file_dir + str(rl) + "\\")}, inside_folder))
        # all_events = get_all_events()
        # output = {"detectNewFaces": output, "DateEventCounts": all_events}
        output = {"detectNewFaces": output}
        print('Done: \t', output, '\n-----------------------------------------------------\n\n')
    else:
        erase_emotion_collections(compare_str_time="17:52")
        print('Time is:'+current_str_time()+'\nIt is rest time! \nEmotion module will enable tomorrow.')


# user login check
def check_auth(user_name, password='', only_user_name=False):
    # db
    authority_users = mongo.db.authorityUsers
    # process
    search = {'userName': user_name, 'password': md5(password.encode('utf-8')).hexdigest()} if only_user_name is False else {'userName': user_name}
    result = authority_users.find_one(search, {'_id': 0})
    return result


# list director employee

def employee_list_by_str(structure_id, employee_list_add=True):
    # var
    output = {'structureName': None, 'employeeList': []}
    search_str = {'id': structure_id}
    search_emp = {'$or': [{'parenStructureId': structure_id}, {'structureId': structure_id}]}
    # db
    structure_list = mongo.db.structureList
    users = mongo.db.users
    # process
    result = structure_list.find_one(search_str, {'_id': 0, 'name': 1})
    if employee_list_add is True:
        employee_list = list(users.find(search_emp, {'_id': 0, 'firstName': 1, 'lastName': 1, 'pin': 1, 'id': 1}))
        list(map(lambda ids: ids.update({"id": ids['id']}), employee_list))
        output['employeeList'] = employee_list
    output['structureName'] = result if result is None else result['name']
    return output


def get_str_by_pin(user_pin):
    user_id = get_user_object_id_by_pin(pin=user_pin)
    result = get_user_fullname_from_id(_id=user_id, full=True)
    result = result if result is None else result
    root_str_id = 'F13F16AF-49A9-4AEF-9A49-13953FC0AFE8'
    director_jt_id = 'DE47E236-450F-4969-A61E-324C9B1217B9'
    output = None
    if result is not None:
        user_str_id = result['parenStructureId']
        user_post_name_id = result['posNameId']
        if user_str_id == root_str_id and user_post_name_id == director_jt_id:
            output = result['parenStructureId'] if result['parenStructureId'] == root_str_id else result['structureId'] if result['structureId'] == root_str_id else output
            output = output.upper()
    return output


def director_user(user_pin, user_type, employee_list_add=True):
    output = {'structureName': None}
    if user_type == 2:
        str_id = get_str_by_pin(user_pin=user_pin)
        employee_list = employee_list_by_str(structure_id=str_id, employee_list_add=employee_list_add)
        if employee_list_add is True: output['employeeList'] = employee_list['employeeList']
        output['structureName'] = employee_list['structureName']
    return output


# schedule.every(20).seconds.do(schedule_task)
#
# while True:
#     schedule.run_pending()
#     time.sleep(0.5)

