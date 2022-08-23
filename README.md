## Установка ПО
    sudo apt install docker.io
    sudo apt install docker-compose-plugin
    sudo chown $USER /var/run/docker.sock && sudo usermod -a -G docker $USER
    sudo -- sh -c "echo '127.0.0.1 lismart.loc' >> /etc/hosts"

## Деплой heroku
    heroku maintenance:on
    git push heroku master
    heroku run flask deploy
    heroku restart
    heroku maintenance:off
