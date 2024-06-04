from config import config, db
# from helpers_def.defs import *


# EMOTION PROJECT - schedule --------------------------------------------------------------------------------------------------------------------------------
# def schedule_task():
#     """Run scheduled job."""
#     print('Schedule started: \t', current_str_time(), '\n************************')
#     # var & process
#     file_dir = "D:\\images\\"
#     inside_folder = list(os.listdir(file_dir))
#     output = list(map(lambda rl: {'folder': rl, 'insertedCount': detect_and_train(file_dir + str(rl) + "\\")}, inside_folder))
#     all_events = get_all_events()
#     output = {"detectNewFaces": output, "DateEventCounts": all_events}
#     print('Done: \t', output, '\n-----------------------------------------------------\n\n')
#
#
# schedule.every(50).seconds.do(schedule_task)
#
# while True:
#     schedule.run_pending()
#     time.sleep(0.5)

user_work_log = db.mongo.db.usersWorkLog
users = db.mongo.db.users

find_wl = list(user_work_log.find({}, {'_id': 0, 'userId': 1}))
find_wl = list(map(lambda wl: config.ObjectId(wl['userId']), find_wl))
search = {'posName': None, 'posNameId': None, 'structureName': None, 'parentStructureName': None, '_id': {'$in': find_wl}}
fu = users.find(search)
find_usr = list(fu)
print(fu.count())
