# python_labs

### To install and boot this service you would need the following:
 > Python 3.7.* 
 
### Pull the dependencies using the following command
```commandline
pip install -r requirements.txt      
```

### Boot it via waitress-serve with the command below
```commandline
waitress-serve --port=8080 --url-scheme=http main:app
```
