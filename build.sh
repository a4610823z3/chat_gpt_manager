rm chat_gpt_manager.tar.gz
rm manager/chat_gpt_manager.tar.gz
rm gateway/chat_gpt_manager.tar.gz
tar --exclude='*.tar.gz' -czvf chat_gpt_manager.tar.gz *
cp chat_gpt_manager.tar.gz gateway/chat_gpt_manager.tar.gz
cp chat_gpt_manager.tar.gz manager/chat_gpt_manager.tar.gz
