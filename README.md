Install virtualenv 
```
$ sudo apt install virtualenv

```
Setup virtural environment
```
$ virtualenv -p python3 touchless_env

```
Change environment
```
$ cd touchless_env
$ source bin/activate

```
Install dependencies
```
(touchless_env)$ pip3 install -r requirements.txt
```
Run the code
```
(touchless_env)$ python test.py
```
Deactivate environment
```
touchless_env)$ deactivate
```
