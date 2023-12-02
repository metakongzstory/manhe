import os
import openai
import streamlit as st
import time

# Fetch the API key from the environment variable
api_key = os.environ.get('OPENAI_API_KEY')

# Check if the API key is available
if not api_key:
    st.error("OpenAI API key is not set in the environment variables.")
    st.stop()

# Initialize the OpenAI client with the API key
openai.api_key = api_key

# #thread id를 하나로 관리하기 위함
# if 'thread_id' not in st.session_state:
#     thread = openai.Thread.create()
#     st.session_state.thread_id = thread.id

# #thread_id, assistant_id 설정
# thread_id = st.session_state.thread_id

#미리 만들어 둔 Assistant

thread_id = "thread_fIdmyhU4U5qQHdV2HNGtVoJ7"
assistant_id = "asst_KC8f7CVoJAdma43Wi0YiFM3q"

#메세지 모두 불러오기
thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

#페이지 제목
st.header("만해 한용운 님과의 대화")

#메세지 역순으로 가져와서 UI에 뿌려주기
for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)

#입력창에 입력을 받아서 입력된 내용으로 메세지 생성
prompt = st.chat_input("만해 한용운 님과 대화를 시작해 보세요.")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    #입력한 메세지 UI에 표시
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    #RUN을 돌리는 과정
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="당신은 대한민국의 자랑스러운 독립운동가이자 승려인 만해 한용운입니다."
    )

    with st.spinner('응답 기다리는 중...'):
        #RUN이 completed 되었나 1초마다 체크
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    #while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    #마지막 메세지 UI에 추가하기
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
