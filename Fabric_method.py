"""
Паттерн "Фабричный метод".
    1. Реализовать класс SimpleFileBuilder для построения драйвера SimpleFileDriver
    2. В блоке __main__ убедиться в построении драйверов JsonFileDriver и SimpleFileDriver
    3. В паттерне "Стратегия" использовать фабрику для получение драйверов в getter свойства driver.
        Getter должен возвращать драйвер, если его нет, то вызывать фабрику для получения драйвера.
"""

from abc import ABC, abstractmethod

from Patterns import IStructureDriver, JsonFileDriver, PicleFileDriver

class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        ...


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


