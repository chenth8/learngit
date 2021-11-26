#!/usr/bin/python3
import argparse
import json
import requests
import urllib3
import uuid


MASTER_URL = 'http://cloudsim.xiaopeng.link'
QUERY_URL = 'http://cloudsim.xiaopeng.link'
PROD_URL = 'http://cloud-simulation.front-client.c611fa09849b14d06a7d4f6889ade9e1b.cn-shanghai.alicontainer.com'



def get_scenario_ids_from_name(name):
    payload, content_type = urllib3.encode_multipart_formdata({
            "page": 1, 
            "size": 100,
            'status': -1,
            'search_labels': 'cngp_log',
            'scenarioName': name
        }
    )
    try:
        scenario_ids_response = requests.post(QUERY_URL + '/simulation/scenario/paginate_query_aio/', data=payload, headers={'Content-Type': content_type}).json()
        scenario_list = scenario_ids_response['data']
        #print(scenario_ids_response)
        
        for scenario in scenario_list:
            scenario_ids = scenario['id']
        return scenario_ids
    except:
        print("Query metrics based on labels has failed!")

def get_job_id(job_name):
    data = {"page": 1, "size": 10, "job_name": job_name}
    req = requests.post(QUERY_URL + '/simulation/simjob/paginate_query_job_name/', data).json()
    return req['data'][0]['id']
def send_request(binary_id, user,jobname):

    job_name = jobname

    out = {
        'scenario_ids': json.dumps(payload),
        'binary_id': binary_id,
        'job_name': job_name,
        'is_async': 1,
        'cluster_name': 'main',
        'invoke_user':  user,
        'upload_output': 1
    }

    req = requests.post(MASTER_URL + '/simulation/master/schedule_module_tasks/', data=out).json()
    print('master res: {}'.format(json.dumps(req, indent=2)))

    job_id = get_job_id(job_name)
    print('This job link is {}{}'.format(PROD_URL + '/#/job/', job_id))


ids = []

##### 在这里填想要测试的scenario名称,注意如果有三位数的老case会搜索出错
names = [4338,4336,4334,4230,4244,4231,4183,3984,3976,4304,4297,4296,4292]
new_names = [] #如果是BP或者PRED直接填进这个list
for name in names:
    name = 'LDRIV-{}'.format(name)
    new_names.append(name)

for name in new_names:
    ids.append(get_scenario_ids_from_name(name))    

print('scenario names are ', new_names)     
print('scenario ids are ',ids)

logsim_scenario_ids = ids
worldsim_scenario_ids = []

payload = [{'scenario_id': e, 'modules': ['MODULE_TYPE_CHIEF', 'MODULE_TYPE_DDS_SCENARIO_PLAYER']} for e in logsim_scenario_ids]

payload += [{'scenario_id': e, 'modules': ['MODULE_TYPE_CHIEF']} for e in worldsim_scenario_ids]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--id',
                        required=True,
                        help='Binary ID')
    
    
    parser.add_argument('-n',
                        required=True,
                        help='jobname')
    
    args = parser.parse_args()
    send_request(args.id, 'chenth@xiaopeng.com', args.n) 

# 1124 must pass: 4338,4336,4334,4230,4244,4231,4183,3984,3976,4304,4297,4296,4292

# 1124case:4338,4337,4336,4335,4334,4333,4331,4330
# 1123case: 4304,4303,4302,4301,4300,4298,4297,4296,4295,4294,4293,4292
# 1122 must pass: 4189,4188,4187,4182,4181,4180,4179,4175,4173,4172,4171,4139,4136,4133,4127,4125
# 1122: 4252,4251,4250,4247,4246,4244,4243,4231,4230,4228
# binary 1122: 19216 1124:19665
# 1119: 4190,4189,4188,4187,4185,4184,4183,4182,4181,4180,4179,4178,4176,4175,4174,4173,4172,4171,4170

# 1118: 4139,4138,4137,4136,4135,4134,4133,4132,4131,4130,4129,4128,4127,4126,4125

# 1117: 4068,4069,4070,4071,4072,4073,4074,4075,4076,4077,4078,4079,4080,4081,4082,4083,4084

# 1116: 4044,4043,4041,4040,4039,4038,4037,4036,4035,4033 binary 18315

# 1115: 3997,3996,3995,3994,3993,3992,3991,3990,3989,3988,3987,3986,3985,3984,3983,3982

# 1112: 3973,3974,3975,3976,3977,3978,3980
# 1111: 3929,3930,3931,3932,3936 
# 1110: 3898,3899,3900,3901,3903,3904,3905,3906,3908,3909,3910,3911 binary 17195
# 1108: 3804,3805,3806,3808,3809,3812,3814,3815,3816,3818,3819,3820
# 1109: 3858,3859,3860,3861,3862
# last week 3699,3702,3709,3727,3733,3638,3694,3698,3704,3708,3710,3729,3725,3706,3662,3731,3732,3739,3741


# Navigation not right : 4331,4301,


