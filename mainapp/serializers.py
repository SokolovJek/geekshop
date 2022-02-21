from rest_framework import serializers


"""Сложный объект (набор записей из Django-модели) нужно превратить в более простую структуру,
 в нашем случае в список словарей. Понадобится сериалайзер."""
"""Сериалайзер поможет достать данные из нужных атрибутов (полей) записи и сформировать упорядоченный 
python-словарь — объект класса OrderedDict. Отмечу, что в Python с версии 3.7 и «обычные» словари стали сохранять 
порядок вставки пар «ключ — значение».
Для сериалайзера нужно описать поля: каждое поле будет отвечать за извлечение и представление данных из 
корреспондирующего поля табличной записи."""


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    category = serializers.CharField(source='category.name', max_length=200)
    description = serializers.CharField(max_length=200)

