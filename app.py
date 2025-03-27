import streamlit as st
import anthropic

# API 키 불러오기
client = anthropic.Anthropic(api_key=st.secrets["anthropic_api_key"])

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}]

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    # 사용자 메시지 출력 및 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Claude 응답 받기 (스트리밍)
    with st.chat_message("assistant"):
        full_response = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
