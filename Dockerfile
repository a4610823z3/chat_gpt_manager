FROM python:3.8.16-slim
RUN pip install flask
RUN pip install tornado
RUN pip install requests
RUN pip install lru_cache
RUN mkdir chat_gpt_manager
WORKDIR /chat_gpt_manager
COPY . .
RUN chmod -R 777 start.sh
EXPOSE 7788
CMD ["sh","start.sh"]