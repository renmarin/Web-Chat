# Web-Chat
Service for discussing topics in chats

# Prerequisites
On your machine should be installed Docker and  to create application's work environment. You can use Docker Desktop on Mac and Windows, for Linux you need to install Docker Engine and Docker Compose. Guide how to install it:
https://docs.docker.com/get-started/#download-and-install-docker .

# How to run it

## Create a Django project

1. Change to the root of your project directory.

2. Create the Django project by running the **docker-compose run** command as follows.

    `sudo docker-compose run web django-admin startproject webapp .`      

3. After the docker-compose command completes, list the contents of your project. If you are running Docker on Linux, the files **django-admin** created are owned by root. This happens because the container runs as the root user. Change the ownership of the new files.

      `sudo chown -R $USER:$USER .`

## Configure the settings

1. In your project directory, edit the **webapp/settings.py** file.
2. Replace the DATABASES = ... with the following:

      ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'BorisDoes',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'db',
                'PORT': 5432,
            }
        }

These settings are determined by the postgres Docker image specified in **docker-compose.yml**.

3. Add CHANNEL_LAYERS:

      ```
         CHANNEL_LAYERS = {
             'default': {
                 'BACKEND': 'channels_redis.core.RedisChannelLayer',
                 'CONFIG': {
                     "hosts": [('redis', 6379)],
                 },
             },
         }

4. Add apps to the INSTALLED_APPS:

      ```
         INSTALLED_APPS = [
             ...
             'rest_framework',
             'rest_framework.authtoken',     # Optional, in case token authentication is needed
             'channels',
             'web_chat.apps.WebChatConfig',
         ]

5. Add ASGI setting for running app as asynchronous:

      `ASGI_APPLICATION = 'webapp.asgi.application'`

6. Change date and time settings:

      ```
         TIME_ZONE = 'Europe/Kiev'
         USE_L10N = False
         TIME_INPUT_FORMATS = "%H:%M:%S"
         DATETIME_FORMAT = "d b Y - H:i:s"

7. Add Django Rest Framework Authentication:

      ```
         REST_FRAMEWORK = {
             'DEFAULT_AUTHENTICATION_CLASSES': [
             'rest_framework.authentication.TokenAuthentication',
             'rest_framework.authentication.SessionAuthentication',
             ],
         }

8. Run the `sudo docker-compose up` command from the top level directory for your project.

At this point, your Django app should be running at port 8000 on your Docker host. On Docker Desktop for Mac and Docker Desktop for Windows, go to http://localhost:8000


## Set up Django app

1. Include the Web Chat URLconf in your project **urls.py** like this:
    ```
    from django.urls import include
    urlpatterns = [
        ...
        path('api-auth/', include('rest_framework.urls')),
        path('', include('web_chat.urls')),
    ]

2. Add imports and change application variable in **webapp.asgi.py**:
    ```
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import web_chat.routing
    
    application = ProtocolTypeRouter({
      "http": get_asgi_application(),
      "websocket": AuthMiddlewareStack(
            URLRouter(
                web_chat.routing.websocket_urlpatterns
            )
        ),
    })
3. Use `sudo docker exec -ti [your_container_id] bash` to connect to container's terminal. To see your container id use `docker ps` command.  You'll need id of project_name_web image.
4.  Run "python manage.py migrate" to create the Web Chat models.
5.  Visit http://127.0.0.1:8000
