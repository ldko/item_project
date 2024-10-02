# Favorite Item App

This is a Django app that allows users to save and annotate their favorite items (or items
relevant to their work) from the [Brown Digital Repository](https://repository.library.brown.edu/studio/).
After registering, users may save items to their account by entering a BDR ID. They also designate
if they want the item to be shown publicly on their profile page (not yet implemented), and can add
notes about the item.

--- 

# Installation

```bash

## setup directories
$ mkdir ./item_project_stuff
$ cd ./item_project_stuff/
$ mkdir ./logs
$ mkdir ./DBs

## get the project-code
$ git clone https://github.com/ldko/item_project.git

## setup the envar-settings
$ cd ./item_project/
$ cp ./config/dotenv_example_file.txt ../.env

## setup the virtual-environment
$ python3 -m venv ../venv
$ source ../venv/bin/activate
(venv) $ pip install pip-tools
(venv) $ pip-compile ./config/requirements/requirements_base.in
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python3 ./manage.py makemigrations item_app
(venv) $ python3 ./manage.py migrate
(venv) $ python3 ./manage.py runserver
```

---


# Usage

- To get started, open a browser to <http://127.0.0.1:8000/register/>, and create an account.

- To favorite an item from BDR, enter the BDR identifier, choose to make it public or private, and optionally, add some notes.

# API

- Retrieve all items that have been favorited in the system: <http://127.0.0.1:8000/api/items/>

- Retrieve data about a single item that has been favorited in the system: <http://127.0.0.1:8000/api/items/[ bdr id ]/>
  - example: <http://127.0.0.1:8000/api/items/bdr:16423/>

- An authenticated user can retrieve their favorite items: <http://127.0.0.1:8000/home/?format=json>

# Testing
- Run tests via `(venv) $ python ./manage.py test`.

- Check out the logs (`item_project_stuff/logs/`). The envar log-level is `DEBUG`, easily changed. On the servers that should be `INFO` or higher, and remember to rotate them, not via python's log-rotate -- but by the server's log-rotate.

---


# nice features/practices

- Nothing private is in the project-repo; avoids using the `.gitignore` for security.
- Shows pattern to keep `views.py` functions short-ish, to act as manager functions (eg `views.version()`).
- Shows pattern to expose the data used by the page via adding `?format=json` (eg `views.info()`). Useful for developing the front-end and troubleshooting.
- Log-formatting shows useful stuff.
- Git branch/commit url is constructed in a way that avoids the new git `dubious ownership` error.
- Includes a couple of client-get tests that respond differentially to dev and prod settings.
- Includes a dev-only error-check url (enables confirmation that email-admins-on-error is set up correctly).
- Uses python-dotenv.
- Uses tilde-comparators in the `.in` requirements files for stable upgrades.
- Uses layered `base.in` and `server.in` requirements files which will produce `.txt` files -- for clarity re what's really in the venv. 
- Specifies compatible package versions for reliable staging and prod deployment.
- Shows one possible pattern to make async calls (`app/lib/version_helper.manage_git_calls()`) and gather together the results.
- This webapp doesn't access the db much, but if it did, and you wanted to inspect the sql generated by the ORM, uncomment out the `django.db.backends` logger in `settings.py`.

