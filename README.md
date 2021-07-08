# primeuploads-py

> An unoffcial python API wrapper for primeuploads.com 

### Installation
```bash
pip3 install primeuploads-py
```

### Usage example
```python
from prime import PrimeUploads

pu = PrimeUploads()
pu.login(
    key1="AbCDefghiJkLMnoPQrstUVwxYz",  # API keys 
    key2="AbCDefghiJkLMnoPQrstUVwxYz"
)
pu.account_info()
```

### Links:
* [official API docs](https://primeuploads.com/api)