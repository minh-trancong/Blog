# Blog
## Các tính năng
### Login
- Login with Facebook
- Login with Google
### Register
### Logout


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

