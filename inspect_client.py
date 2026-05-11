import inspect
from pageindex import PageIndexClient

client = PageIndexClient(api_key=None)
with open("pi_methods.txt", "a") as f:
    f.write("\n\nSignature of submit_document:\n")
    f.write(str(inspect.signature(client.submit_document)))
    f.write("\n\nSignature of get_tree:\n")
    f.write(str(inspect.signature(client.get_tree)))
    f.write("\n\nSignature of chat_completions:\n")
    f.write(str(inspect.signature(client.chat_completions)))
