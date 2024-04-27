### Django Tree menu
#### Запуск в PyCharm:
- Скопируйте репозиторий на локальную машину: `git clone https://github.com/Giriraj-das/Django-tree-menu`
- Откройте склонированный репозиторий в PyCharm
- Если PyCharm не предложит сам:
  - Создайте виртуальное окружение
  - Установите зависимости: `pip install -r requirements.txt`
#### Запуск API в Docker (ARM архитектура):
- Из корня репозитория скачать yml-файл: https://github.com/Giriraj-das/Django-tree-menu/blob/main/docker-compose.yml
- В терминале из директории, где лежит yml-файл запустить: `docker-compose up -d`

#### Вход в админку:
- username: Admin
- password: tree-menu
