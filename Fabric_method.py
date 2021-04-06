"""
Паттерн "Фабричный метод".
    1. Реализовать класс SimpleFileBuilder для построения драйвера SimpleFileDriver
    2. В блоке __main__ убедиться в построении драйверов JsonFileDriver и SimpleFileDriver
    3. В паттерне "Стратегия" использовать фабрику для получение драйверов в getter свойства driver.
        Getter должен возвращать драйвер, если его нет, то вызывать фабрику для получения драйвера.
"""

from abc import ABC, abstractmethod
from typing import Sequence
import json
import pickle


class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        ...


class IStructureDriver(ABC):

    @abstractmethod
    def read(self) -> Sequence:
        """
        Считывает информацию из драйвера и возвращает её для объекта, использующего этот драйвер
        :return Последовательность элементов, считанная драйвером, для объекта
        """
        pass

    @abstractmethod
    def write(self, data: Sequence) -> None:
        """
        Получает информацию из объекта, использующего этот драйвер, и записывает её в драйвер
        :param data Последовательность элементов, полученная от объекта, для записи драйвером
        """
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename: str):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename) as file:
            return json.load(file)

    def write(self, data: Sequence) -> None:
        with open(self._filename, "w") as file:
            json.dump(data, file)


class PicleFileDriver(IStructureDriver):
    def __init__(self, filename: str):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename, "rb") as file:
            return pickle.load(file)

    def write(self, data: Sequence) -> None:
        with open(self._filename, "wb") as file:
            pickle.dump(data, file)


class JsonFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.json'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название json файла: (.json)').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.json'):
            filename = f'{filename}.json'

        return JsonFileDriver(filename)


class PicleFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.bin'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название picle файла: (.bin)').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.bin'):
            filename = f'{filename}.bin'

        return PicleFileDriver(filename)


class DriverFabric:
    DRIVER_BUILDER = {
        'json_file': JsonFileBuilder, 'picle_file': PicleFileBuilder
    }
    DEFAULT_DRIVER = 'json_file'

    # DEFAULT_DRIVER = 'picle_file'

    @classmethod
    def get_driver(cls):
        driver_name = input("Введите название драйвера: ")
        driver_name = driver_name or cls.DEFAULT_DRIVER

        driver_builder = cls.DRIVER_BUILDER[driver_name]
        return driver_builder.build()


if __name__ == '__main__':
    driver = DriverFabric.get_driver()
    print(driver.read())
