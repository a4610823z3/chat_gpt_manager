import hashlib
import os
import random
import string
import uuid
from flask import Flask, jsonify, request
import json

from api.support import get_user_data,clear_key_cache,write_user_data,had_user_key


app = Flask(__name__, static_folder='static')

# 从文件中读取用户数据并存储到 lru_cache 中（最多存储 128 条数据，过期时间为 300 秒）

# 将用户数据写入文件中
@app.before_request
def before_request():
    authorization = request.headers.get('Authorization')
    if request.url.find("static") > 0:
        return
    if request.url.find("/users/keys") > 0:
        return
    value = os.environ.get('CHAT_GPT_MANGER_KEY')
    if value is None:
        return
    if value != '' and authorization != value:
        return jsonify({'error': '你输入秘钥或者输入的秘钥不正确'}), 200


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

@app.route('/users/keys/<string:key>', methods=['GET'])
def validate_by_key(key):
    result = had_user_key(key)
    response_json = {
        "code" : 0,
        "data" : result
    }
    print(response_json)
    return jsonify(response_json)


# 添加新用户
@app.route('/users', methods=['POST'])
def add_user():
    users = get_user_data()
    new_user: dict = request.json # type: ignore
    new_user['id'] = str(uuid.uuid1())
    length = 4
    chars = string.ascii_letters + string.digits
    key = ''.join(random.choice(chars) for _ in range(length))
    new_user['key'] = key
    for db_user in users:
        if db_user['key'] == key:
           return jsonify({'error': '用户秘钥已存在'})
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
    if user_port == '' or user_port is None:
       app.run() # type: ignore
    else :
       app.run(host='0.0.0.0',port = int(user_port)) # type: ignore

