# Django example

## Prerequisites

* Xcode Command Line Tools

    ```
    # Download from (https://developer.apple.com/xcode/download/)
    xcode-select --install
    ```

* Python >=3.5.0

    ```
    # Install pyenv with Homebrew (https://github.com/yyuu/pyenv#homebrew-on-mac-os-x)
    brew install pyenv
    # Install Python 3 with pyenv
    cd zero-django
    pyenv install
    ```

## Installation

    cd zero-django
    pip install -r requirements.txt

## Running the example

    ./manage.py runserver

Visit http://localhost:8000/graphiql


## Query String

    query {
      person(id:"1") {
        id
        firstName
        lastName
        email
        friends {
          firstName
          email
        }
      }
    }
    
## 导出 Schema
安装之后

    INSTALLED_APPS += ('graphene_django')

可以使用如下命令导出 Schema

    ./manage.py graphql_schema --schema zero_django.schema.schema --out schema.json
    
更多参考[这里](http://docs.graphene-python.org/projects/django/en/latest/introspection/)
   
## create app

    django-admin.py startapp ingredients
    
    
## loadata

    python manage.py loaddata ingredients/ingredients.json
    
## reference

- <https://www.youtube.com/embed/UBGzsb2UkeY>