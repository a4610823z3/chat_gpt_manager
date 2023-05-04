FROM python:3.8.16-slim
RUN pip install flask
RUN pip install tornado
RUN pip install requests
RUN pip install lru_cache
RUN mkdir chat_gpt_manager
WORKDIR /chat_gpt_manager
ADD chat_gpt_manager.tar.gz ./
ADD start.sh ./
# RUN chmod -R 777 chat_gpt_manager.tar.gz
RUN chmod -R 777 start.sh
RUN ls
EXPOSE 7788
CMD ["sh","start.sh"]