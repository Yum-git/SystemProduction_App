from flask import Flask, render_template, request, redirect, url_for
import crossplane
import pprint
import subprocess
# import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/flask/")
def index():
    status_all = nginx_parser()

    print(status_all)
    for key in range(len(status_all)):
        if status_all[key][1] == '2':
            status_all[key][1] = 'very_hard'
        elif status_all[key][1] == '4':
            status_all[key][1] = 'hard'
        elif status_all[key][1] == '8':
            status_all[key][1] = 'soft'
        elif status_all[key][1] == '16':
            status_all[key][1] = 'very_soft'
        else:
            status_all[key][1] = 'custom'
    logs = []
    # logs = ['20201123 : saoshoahsoa' for i in range(100)]
    with open('/var/log/naxsi.log', 'r', encoding='utf-8') as f:
        logs = [s.strip() for s in f.readlines()]
        logs = [value for value in logs if 'error' in value]

    date_list = [value.split()[0] for value in logs]
    date_list.sort()
    date_ = []
    co_ = []
    
    tmp = 1
    for idx in range(len(date_list) - 1):
        if date_list[idx] != date_list[idx + 1]:
            date_.append(date_list[idx])
            co_.append(tmp)

            tmp = 1
        elif idx == len(date_list) - 2:
            date_.append(date_list[idx])
            co_.append(tmp + 1)
        else:
            tmp += 1
    # print(date_)
    # print(co_)
    
    # fig = plt.figure()
    # plt.plot(co_, date_)
    # fig.saveshow('test.png')

    logs.reverse()
    return render_template("index.html", logs=logs, status_all=status_all)


@app.route("/flask/api", methods=['POST'])
def api():
    print(request.get_data().decode())
    request_data = list(request.get_data().decode().split('='))
    if request_data[1] == 'very_hard':
        str_insert = '$' + request_data[0].upper() + ' >= 2'
    elif request_data[1] == 'hard':
        str_insert = '$' + request_data[0].upper() + ' >= 4'
    elif request_data[1] == 'soft':
        str_insert = '$' + request_data[0].upper() + ' >= 8'
    elif request_data[1] == 'very_soft':
        str_insert = '$' + request_data[0].upper() + ' >= 16'

    str_test = str_insert
    nginx_conf = crossplane.parse('/usr/local/nginx/conf/nginx.conf')

    for idx_http, value_first in enumerate(nginx_conf['config'][0]['parsed']):
        if value_first['directive'] == 'http':
            for idx_server, value_second in enumerate(value_first['block']):
                if value_second['directive'] == 'server':
                    for idx_location, value_third in enumerate(value_second['block']):
                        if value_third['directive'] == 'location':
                            # pprint.pprint(value_third)
                            for idx_args, value_forth in enumerate(value_third['block']):
                                # pprint.pprint(value_forth)
                                try:
                                    print(request_data[0], value_forth['args'][0].lower())
                                    if value_forth['directive'] == 'CheckRule' and request_data[0] in value_forth['args'][0].lower():
                                        nginx_conf['config'][0]['parsed'][idx_http]['block'][idx_server]['block'][idx_location]['block'][idx_args]['args'][0] = str_test
                                        pprint.pprint(nginx_conf['config'][0]['parsed'][idx_http]['block'][idx_server]['block'][idx_location]['block'])
                                except Exception as e:
                                    print('List Error!')
    # pprint.pprint(nginx_conf['config'][0]['parsed'])
    config = crossplane.build(nginx_conf['config'][0]['parsed'])

    with open('/usr/local/nginx/conf/nginx.conf', 'w') as f:
        f.write(config)

    subprocess.call(["service nginx reload"], shell=True)
    return redirect(url_for('index'))


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


def nginx_parser():
    setting_list = []

    nginx_conf = crossplane.parse('/usr/local/nginx/conf/nginx.conf')

    for value_1 in nginx_conf['config'][0]['parsed']:
        if value_1['directive'] == 'http':
            for value_2 in value_1['block']:
                if value_2['directive'] == 'server':
                    for value_3 in value_2['block']:
                        if value_3['directive'] == 'location' and value_3['args'] == ['~*', '\\.cgi$']:
                            for value_4 in value_3['block']:
                                if value_4['directive'] == 'CheckRule':
                                    value_result = value_4['args'][0].split()
                                    print(value_result)
                                    setting_list.append([value_result[0][1:], value_result[2]])

    return setting_list

def picture_update(data:list):
    print()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
