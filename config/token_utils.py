from functools import wraps
from config.config import *
from helpers_def.defs import returns, error_base


#
# development: http://192.168.20.245:8080/csec/
# production: http://wscs.prod/csec/
#

def checkToken(service_name, service_type):
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            url = 'http://wscs.prod/csec/Token/checkToken?serviceName=' + str(
                service_name) + '&serviceType=' + str(service_type)

            token = request.headers.get('Authorization')
            ugTypeId = request.headers.get('UserGroupTypeId')

            # reqHeaders={
            #   'Authorization': 'Basic '+token,
            #    'Content-Type':'application / json',
            #    'UserGroupTypeId': ugTypeId
            # }

            reqHeaders = {
                "RequestNumber": "aaaaaaaaa",
                "Accept-Language": "az",
                "Accept": "application/json",
                "IpAddress": "10.9.20.21",
                "AppName": "ITHelp",
                "Content-Type": "application/json;charset=UTF-8",
                "Authorization": token,
                "UserGroupTypeId": ugTypeId
            }

            r = requests.get(url=url, headers=reqHeaders)
            global data
            data = json.loads(r.content)
            if str(data["error"]) != "None":
                data = returns(status='error', message=error_base(int(data['error']['code'])), data=None)
                return Response(json.dumps(data), 200, {'Content-Type': 'application/json'})

            # property check
            return_data = data['data']
            user_group_type = return_data['userGroupType']
            user_data = return_data['user']
            user_pin = user_data['id']
            organisation_pin = return_data['structure']['rootStructureId']
            token_schema = {
                "userData": user_data,
                "userPIN": user_pin,
                "organisationPin": organisation_pin,
                "userGroupType": user_group_type,
                "apiToken": str(token).split(" ")[1]
            }
            return f(token_schema, *args, **kwargs)

        return decorated

    return requires_auth
