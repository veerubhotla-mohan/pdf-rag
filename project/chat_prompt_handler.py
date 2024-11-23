from langchain.chat_models.bedrock import BedrockChat
def get_query_response(query, docs):
    context= "".join(doc.page_content + "\n" for doc in docs)
    bedrock_llm = BedrockChat(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")
    messages = [
        (
            "system",
            f"""You are a helpful assistant who can answers user's query with reference to some given context. The user's data is given below:
            <data>
            {context}
            </data>
            
            With reference to the above data, now answer the user's query. Be politeful and do not make any assumptions. Do not add any prefixes like "Based on the given data" or "Based on given context" or any similar prefixes. Start answering the user's query directly without any additional text or information. Do not mention anything about your source of data or the context.
            """,
        ),
        ("human", query),
    ]
    response = bedrock_llm.invoke(messages)
    return response.content