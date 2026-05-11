import inspect
try:
    from pageindex import PageIndexClient
    sig = inspect.signature(PageIndexClient.__init__)
    print(f"Signature: {sig}")
except Exception as e:
    print(f"Error: {e}")
