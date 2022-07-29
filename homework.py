from dataclasses import dataclass, asdict
from typing import Union, List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_MESSAGE: str = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration:.3f} ч.; '
                             'Дистанция: {distance:.3f} км; '
                             'Ср. скорость: {speed:.3f} км/ч; '
                             'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.TRAINING_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    SIXTY_MINUTES: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(type(self).__name__,
                self.duration,
                self.get_distance(),
                self.get_mean_speed(),
                self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLICATOR: float = 18
    COEFF_CALORIE: float = 20

    def get_spent_calories(self) -> float:
        return ((self.SPEED_MULTIPLICATOR * self.get_mean_speed()
                - self.COEFF_CALORIE) * self.weight / self.M_IN_KM
                * (self.duration * self.SIXTY_MINUTES))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_1 = 0.035
    CALORIE_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.CALORIE_2 * self.weight)
                * (self.duration * self.SIXTY_MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    PLUS_COEF_SPEED: float = 1.1
    MULTIPLICATOR_OF_WEIGHT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        return (((self.get_mean_speed()) + self.PLUS_COEF_SPEED)
                * self.MULTIPLICATOR_OF_WEIGHT * self.weight)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


TYPES_OF_WORKOUT_CLASSES: Dict[str, float] = {"SWM": Swimming,
                                              "RUN": Running,
                                              "WLK": SportsWalking}


def read_package(workout_type: str,
                 data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in TYPES_OF_WORKOUT_CLASSES:
        return TYPES_OF_WORKOUT_CLASSES[workout_type](*data)
    raise AttributeError('Неизвестный тип тренировки'
                         ' доступны - Swimming, Running, SportsWalking')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))