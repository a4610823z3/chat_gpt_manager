FROM python:3.8.16-slim
RUN pip install tornado
RUN pip install flask
RUN pip install lru_cache
RUN mkdir chat_gpt_manager_api
WORKDIR /chat_gpt_manager_api
ADD ./chat_gpt_manager.tar.gz ./
ADD ./start.sh ./
RUN chmod -R 777 start.sh
RUN ls
EXPOSE 7799
CMD ["sh","start.sh"]