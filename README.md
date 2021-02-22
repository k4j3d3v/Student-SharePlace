# Student-SharePlace
Web application for sharing course notes and other university related things.
This WebApp is developed for Web Technologies exam for Computer Science BS at University of Modena.

## Installation
For use this webapp need to have installed python (tested from 3.8+).
I suggest to use a virtualenv (or other equivalent), if you don't have it, you can install it with your package manager.
For me on Manjaro with bash, it will be something like that:
```bash
sudo pacman -S virtualenv
```
Now you can create a virtualenv:
```bash
virtualenv <your_env_name>
```
After that you need ```active``` it:
```bash
source <your_env_name>/bin/activate
```
Now, you can use ```pip``` for installing packages needed for use this project:

```bash
(<your_env_name>) pip install -r requirements.txt
```

If everything is gone in the right way, you'll be able to use the project in debug mode:
```bash
(<your_env_name>) python manage.py runserver
```
### Note
For use it without having errors during registration you need to create some object instances, this is due for respecting referential integrity relationship (```ForeignKey```, ```ManytoMany```, etc...).
You can add it from admin panel, accessing from your browser: ```http://127.0.0.1:8000/admin```.
In registration form you must specify your ```Degree```, so you first need to create an instance of that.
