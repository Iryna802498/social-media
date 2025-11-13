# 💬 Social Media Api

Api service for social media management written on DRF.

# Installing using GitHib

```bash
git clone https://github.com/Iryna802498/social-media.git
cd social-media
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
cp .env.sample .env (Do not forget that .env file not commit to your own repository)
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser (create superuser with your credentials)
python manage.py runserver
```

# Run with Docker

Docker should be installed

```bash
docker-compose build
docker-compose up
```

# Getting access

- create user via api/user/register
- get access and refresh token api/user/token
- get logout page use refresh token

# Features

- JWT authenticated
- Admin panel /admin/
- Documentation: api/doc/swagger/ or api/doc/redoc/
- Managing profiles, posts, follows, likes and comments
- Creating profiles or posts with some image
- Seeing your followers and followings via individual endpoints (api/social-media/my-followers/ or api/my-followings/)
- Individual endpoints to follow and unfollow user
- Filtering profiles by username
- Filtering posts by hashtags or username
- Individual endpoint to add your own comment to post (api/social-media/posts/1/add-comment/)
- Individual endpoints to like or unlike some post (api/social-media/posts/1/like/ or api/social-media/posts/1/unlike/)
