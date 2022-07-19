# Blog
## Installation

- mysql
- database for mysql with script to CREATE TABLE provided [create_blog.sql](./create_blog.sql)
- flask and python required packages (Tải pycharm và tải các thư viện cần thiết)

```shell
git clone https://github.com/minh-trancong/Blog.git
```

```shell
python3 -m venv Blog
cd Blog
source bin/activate
pip3 install flask
```

```shell
pip3 install -r requirements.txt
```

```shell
flask run
```

## API

```python
'/api/login', methods=['GET', 'POST']
'/api/register', methods=['GET', 'POST']
'/api/update/users/<int:userid>', methods=['PUT']
'/api/users', methods=['GET'] -> Get all users
'/api/users/<int:userid>', methods=['GET'] -> Get specific user information by his/her id
```

```python
'/api/google/login' [GET, POST]
'/api/google/register' [GET, POST]
'/api/google/<int:userid>/occupation' [GET, POST]
'/api/google/checkmail'
'/api/google/callback'
```

```python
'/api/posts/<int:id>' [GET, DELETE]
'/api/users/<int:id>/posts' [GET]
'/api/users/<int:id>/posts/create' [POST]
```

```python
'/api/reacts' [GET]
'/api/reacts/posts/<int:postid>' [GET]
'/api/reacts/posts/<int:postid>/likes' [GET]
'/api/reacts/users/<int:userid>/posts/<int:postid>' [GET, POST, DELETE]
```

## INTERACT WITH WEB

- Go to http://127.0.0.1:5000 and experience some features.

| ![image-20220719084707341](pic/image-20220719084707341.png) | ![image-20220719084700084](pic/image-20220719084700084.png) |
| ----------------------------------------------------------- | ----------------------------------------------------------- |

