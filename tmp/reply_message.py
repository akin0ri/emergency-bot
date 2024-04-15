import os
from langchain_openai import AzureChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

# モデルの設定
load_dotenv(".env")
llm = AzureChatOpenAI(
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT")
)

# 入力された文書をもとに救急に関する返答文を生成する
def reply_message(input_message):
    # 知識の生成
    chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages([
            HumanMessage(content="入力：応急は連鎖します"),
            SystemMessage(content="知識：病気や事故で急変した人を救命し、社会復帰させるために必要な一連の流れを「救命の連鎖」といいます。"),
            HumanMessage(content="入力：突然人が倒れたときは心停止を疑いましょう。"),
            SystemMessage(content="知識：心停止を疑った場合はすぐに119番通報し救急車が来るまで速やかに心肺蘇生などの応急手当を行う必要がある。"),
            HumanMessage(content="入力：危険的な状況ではひどい混乱が生じることがあります。"),
            SystemMessage(content="知識：緊急事態時には認識し次取るべき行動をとることを理解することが重要です。"),
            HumanMessagePromptTemplate.from_template("入力：{input}"),
            AIMessage(content="知識：")
        ])
    )
    knowledge = chain.run(input="救急隊が来るまでに安心させる方法を教えてください")
    
    # 生成された知識をもとに返答文を生成する
    chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template("{bacgroound}"),
            HumanMessagePromptTemplate.from_template("入力：{input}"),
            AIMessagePromptTemplate.from_template("知識：{knowledge}"),
            AIMessage(content="説明と解説：")
        ])
    )
    result = chain.run(input=input_message, knowledge=knowledge, bacgroound="緊急時なので100文字以内で説明してください")

    return result
