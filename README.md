# Определение скорости объекта в видеопотоке

## Для запуска проекта необходим docker, docker-compose и стабильный доступ в интернет

### Архитектура программного средства

![Image alt](images/Software_architecture.png)

### Для запуска проекта выполните следующие команды
```
- git clone https://github.com/xxxFilosoFxxx/Web_speed_determination
- cd Web_speed_determination
- sudo docker-compose up -d --build
```

После сборки и развертывания откройте ссылку в браузере

```
localhost:8888
```

При выделении фактического расстояния плоскости потребуется расставлять 
точки прямоугольника в определенной последовательности:

```
1 - левый верхний угол
2 - правый верхний угол
3 - левый нижний угол
4 - правый нижний угол
```

Перекрестия размеченных линий **недопустимы**!

Далее, сначала определяем **ширину** прямоугольника,
затем **высоту** прямоугольника (величины рассчитываются в метрах).
