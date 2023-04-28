## 启动流程 
### 1.打包
sh build.sh

### 2.部署管理界面
#### 2.1 cd manager 切换至manager目录
```bash
    1.打包镜像
    docker build -t chat_gpt_manager:latest .
    2.运行镜像
    docker run -d -v /root/static-file/data:/chat_gpt_manager/data  -p 9001:7788 -e GPT_PORT=7788 -e CHAT_GPT_MANGER_KEY=xxx -e GPT_DATA_DIR=/chat_gpt_manager/data chat_gpt_manager:latest > /root/static-file/logs/chat_gpt_manager.log 2>&1 &
    3.其中
        a.GPT_PORT是服务端口
        b.CHAT_GPT_MANGER_KEY是秘钥
        c./root/static-file/data是宿主机目录
```

### 3.部署对外的api
#### 3.1 cd gateway 切换至gateway目录
```bash
    1.打包镜像
    docker build -t chat_gpt_manager_api:latest .
    2.运行镜像
    docker run -d -v /root/static-file/data:/chat_gpt_manager_api/data  -p 9002:7799 -e GPT_PORT=7799 -e CHAT_GPT_MANGER_KEY=xxx -e GPT_DATA_DIR=/chat_gpt_manager_api/data chat_gpt_manager_api:latest > /root/static-file/logs/chat_gpt_manager_api.log 2>&1 &
    3.其中
        a.GPT_PORT是服务端口
        b.CHAT_GPT_MANGER_KEY是秘钥
        c./root/static-file/data是宿主机目录
```
