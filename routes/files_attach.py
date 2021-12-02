from flask import request
import random, string
import pathlib
from models import *
import json
from main import app
import os


@app.route('/insert/request/request', methods=['POST', 'GET'])
def sys_config_table():
    try:
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            check_token = auth_user_key.AuthUsersKeys().search({'token':str(access_token)})
            if check_token:
                current_dir = pathlib.Path().absolute()
                upload_files_path = str(current_dir) + '/uploaded_file'
                # check the if the path is a directory
                if not os.path.isdir(upload_files_path):
                    os.makedirs(upload_files_path)
                app.config['UPLOAD_FOLDER'] = upload_files_path
                if 'filename' in request.files:
                    uploaded_file = request.files['filename']
                    file_name = uploaded_file.filename
                    if uploaded_file:
                        full_uploaded_file_path = upload_files_path + '/' + str(file_name)
                        if os.path.isfile(full_uploaded_file_path):
                            # Set Current File with different name
                            new_str = ''.join(
                                random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in
                                range(10))
                            filename, ext = os.path.splitext(file_name)
                            if filename and ext:
                                full_uploaded_file_path = upload_files_path + '/' + str(filename) + '-' + new_str + str(ext)
                                uploaded_file.save(dst=full_uploaded_file_path)
                        else:
                            uploaded_file.save(dst=full_uploaded_file_path)
                default_value = False
                imd = request.form
                dict_form_data = imd.to_dict(flat=False)
                list_values = {}
                if bool(dict_form_data) and 'data' in dict_form_data and bool(dict_form_data['data']):
                    data_vals = dict_form_data['data'][0]
                    json_dump = json.loads(str(data_vals))
                    if 'rev_pld_var' in json_dump:
                        list_values['rev_pld_var'] = json_dump['rev_pld_var']
                    if 'src_port' in json_dump:
                        list_values['src_port'] = json_dump['src_port']

                    if 'pld_distinct' in json_dump:
                        list_values['pld_distinct'] = json_dump['pld_distinct']

                    if 'rev_hdr_ccnt' in json_dump:
                        list_values['rev_hdr_ccnt'] = json_dump['rev_hdr_ccnt']

                    if 'bytes_out' in json_dump:
                        list_values['bytes_out'] = json_dump['bytes_out']

                    if 'hdr_mean' in json_dump:
                        list_values['hdr_mean'] = json_dump['hdr_mean']

                if bool(list_values):
                    metric = android.Android().create(list_values)

                message = {'success': True}
                return {'code': 200, 'message': message}
            return {'code': 403, 'message': 'Access Denied' }
    except Exception as e:
        print(e)


