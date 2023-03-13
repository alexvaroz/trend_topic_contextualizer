import openai
import streamlit as st
from captura_tweets import list_trend_topics, list_tweets_by_trend_topic, stopwords, prepare_tweets
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

response = False
prompt = ""

openai.api_key = st.secrets["pass"]


def make_request(question_input: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", "content": f"{question_input},"
            }
        ]
    )
    return response


st.set_page_config(page_title="Trend Topic Contextualizer", layout="wide")
st.sidebar.markdown("## Sobre o TrendTopicContextualizer")
st.sidebar.write("""
                Trata-se de um exercício para a aplicação prática de recursos do ChatGPT.\n
                Nesse caso, a lista dos assuntos mais comentados no Twiiter, no Brasil, é
                 capturada e à API do ChatGPT, solicitando que sejam extraídos os tópicos 
                 de 80 tweets relacionados a aquele assunto .\n 
                
                Para complementar a análise, é apresentada uma nuvem de palavras com o texto dos tweets
                capturados.
                """)

st.sidebar.info("Meu nome é Alexandre Vaz Roriz e disponibilizo alguns "
                "trabalhos [aqui](https://alexvaroz.github.io/Portfolio/). "
                "Estou sempre a disposição "
                "para [contatos](https://www.linkedin.com/in/alexandre-vaz-roriz-07880724/).", icon="ℹ️")

st.write("# Twitter Trend Topic Contextualizer")
st.write("##### Dada a lista dos tópicos mais quentes do Twitter no momento, no Brasil, "
             "selecione um deles para obter uma contextualização, com a ajuda do ChatGPT.")

trend_topics = list_trend_topics().values

trend_topics_formatada = "\n".join([f"-  {topic}" for topic in trend_topics])
st.markdown(f"{trend_topics_formatada}")

topic = st.selectbox(label='Selecione o tópico:', options=trend_topics)
tweets_list = prepare_tweets(list_tweets_by_trend_topic(topic))

prompt = "vou te encaminhar uma lista com 100 tweets e quero que você explique em português o que está " \
         f"acontecendo com base nas postagens:  {tweets_list}"

run_buton = st.button("Pesquisar")


if run_buton:
    response = make_request(prompt)
    if response:
        st.write(response["choices"][0]["message"]["content"])
    # Display the generated image:
    wc = WordCloud(stopwords=stopwords, collocations=False, max_font_size=55,
                   max_words=80, background_color="black")
    wc.generate(' '.join(tweets_list))
    plt.figure(figsize=(10, 12))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot()
else:
    pass
