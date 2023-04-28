import hashlib
import os
import uuid
from flask import Flask, jsonify, request
import json

from api.support import get_user_data,clear_key_cache


app = Flask(__name__, static_folder='static')

# 从文件中读取用户数据并存储到 lru_cache 中（最多存储 128 条数据，过期时间为 300 秒）

# 将用户数据写入文件中
def write_user_data(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@app.before_request
def before_request():
    authorization = request.headers.get('Authorization')
    if request.url.find("static") > 0:
        return
    value = os.environ.get('CHAT_GPT_MANGER_KEY')
    if value != '' and authorization != value:
        return {'error': '你输入秘钥或者输入的秘钥不正确'}, 200


# 查询所有用户
@app.route('/users', methods=['GET'])
def get_users():
    users = get_user_data()
    page_index = int(request.args.get('page_index')) # type: ignore
    page_size = int(request.args.get('page_size')) # type: ignore
    if page_size == 0 or page_size is None:
        page_size = 10
  # 计算用户列表的起始位置和终止位置
    if page_index < 0:
        page_index = 1
    start_idx = (page_index - 1) * page_size # type: ignore
    end_idx = start_idx + page_size
    # 对用户列表进行倒序排序，并取出指定范围内的数据
    paged_users = users[::-1][start_idx:end_idx]
    return jsonify(paged_users)

# 根据 ID 查询单个用户
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    users = get_user_data()
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({'error': 'User not found'})



# 添加新用户
@app.route('/users', methods=['POST'])
def add_user():
    users = get_user_data()
    new_user: dict = request.json # type: ignore
    if 'key' not in new_user:
        return jsonify({'error': 'key is required'})
    for user in users:
        if user['key'] == str(new_user['key']):
            return jsonify({'error': 'User key already exists'})
    new_user['id'] = str(uuid.uuid1())
    users.append(new_user)
    write_user_data(users)  # 将修改后的用户数据写入文件
    get_user_data.cache_clear()  # 清空缓存
    return jsonify(users)

# 修改用户
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    users = get_user_data()
    for user in users:
        if str(user['id']) == str(user_id):
            new_user : dict = request.json # type: ignore
            user.update(new_user)
            write_user_data(users)  # 将修改后的用户数据写入文件
            get_user_data.cache_clear()  # 清空缓存
            return jsonify(user)
    return jsonify({'error': 'User not found'})

# 删除用户
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = get_user_data()
    for i, user in enumerate(users):
        if str(user['id']) == str(user_id):
            del users[i]
            write_user_data(users)  # 将修改后的用户数据写入文件
            get_user_data.cache_clear()  # 清空缓存
            hash_object = hashlib.md5(user['key'].encode())
            key = hash_object.hexdigest()
            clear_key_cache(key)
            return jsonify(users)
    return jsonify({'error': 'User not found'})


if __name__ == '__main__':
    user_port = os.environ.get('GPT_PORT')
    if user_port == '' :
       app.run() # type: ignore
    else :
       app.run(host='0.0.0.0',port = int(str(user_port))) # type: ignore

