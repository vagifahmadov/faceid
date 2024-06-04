from config.config import app
from services.pages import index, user, register, compare, capture, work_log, default, notfound, employees, compare_user, root_pro, introduce, statistics, admin, \
    login, sign_out, find_user_by_pin, know_user, health, director
from services.services import insert, push, training, sync_users, find_base_employee, employee_info, emotion, find_employee_by_pin, upload_image, \
    employee_photos, remove_image, submit_snapshot, charts, detect_insert_files, face_identicate, ajax_file, ip_list, ip_list_terminal, employee_work_log, \
    employee_work_log_list, get_work_log_img, change_password, set_remove_admin, director_employee_list, set_remove_director


# job()
# CORS(app)
# services
app.register_blueprint(push)
app.register_blueprint(insert)
app.register_blueprint(training)
app.register_blueprint(sync_users)
app.register_blueprint(find_base_employee)
app.register_blueprint(employee_info)
app.register_blueprint(find_employee_by_pin)
app.register_blueprint(employee_photos)
# app.register_blueprint(know_me)
app.register_blueprint(upload_image)
app.register_blueprint(remove_image)
app.register_blueprint(submit_snapshot)
app.register_blueprint(charts)
app.register_blueprint(ajax_file)
app.register_blueprint(ip_list)
app.register_blueprint(ip_list_terminal)
app.register_blueprint(employee_work_log)
app.register_blueprint(employee_work_log_list)
app.register_blueprint(get_work_log_img)
# emotion project
app.register_blueprint(emotion)
app.register_blueprint(detect_insert_files)
app.register_blueprint(face_identicate)
# pages
app.register_blueprint(index)
app.register_blueprint(user)
app.register_blueprint(register)
app.register_blueprint(compare)
app.register_blueprint(capture)
app.register_blueprint(work_log)
app.register_blueprint(default)
app.register_blueprint(notfound)
app.register_blueprint(compare_user)
app.register_blueprint(root_pro)
app.register_blueprint(introduce)
app.register_blueprint(statistics)
app.register_blueprint(employees)
app.register_blueprint(admin)
app.register_blueprint(login)
app.register_blueprint(sign_out)
app.register_blueprint(find_user_by_pin)
app.register_blueprint(know_user)
app.register_blueprint(change_password)
app.register_blueprint(set_remove_admin)
app.register_blueprint(director)
app.register_blueprint(director_employee_list)
app.register_blueprint(set_remove_director)
# health
app.register_blueprint(health)


if __name__ == '__main__':
    # app.run(debug=True, port=80, host='10.9.20.20')  # server
    # app.run(debug=False, port=1080, host='192.168.35.39')  # work
    # app.run(debug=True, port=80, host='192.168.1.72')  # home -b
    app.run(debug=True, port=9999, host='localhost')  # home -vpn
    # app.run(ssl_context='adhoc', debug=True, port=443, host='192.168.35.39')  # WORK SSL
    # app.run(debug=True, port=9999, host='localhost')  # WORK SSL
    # app.run(debug=True, host='localhost', ssl_context=('/etc/nginx/ssl/qeydiyyat.crt', '/etc/nginx/ssl/qeydiyyat.key'), port=443)
    # app.run(ssl_context='adhoc', debug=True, port=443, host='192.168.1.107')  # HOME SSL
    # app.run(ssl_context='adhoc', debug=True, port=443, host='192.168.0.102')  # HOME SSL
    # app.run(ssl_context='adhoc', debug=True, port=443, host='192.168.100.70')  # HOME SSL
