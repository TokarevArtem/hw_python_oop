from dataclasses import dataclass
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP_M: float = 0.65
    SPEED_KMH: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP_M / self.SPEED_KMH

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.action * self.LEN_STEP_M / self.SPEED_KMH) / self.duration

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
    speed_multiplicator: float = 18
    coeff_calorie: float = 20
    sixty_minutes: float = 60

    def get_spent_calories(self) -> float:
        return ((self.speed_multiplicator * self.get_mean_speed()
                - self.coeff_calorie) * self.weight / self.SPEED_KMH
                * (self.duration * self.sixty_minutes))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calorie_1 = 0.035
        calorie_2 = 0.029
        return ((calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * calorie_2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP_M: float = 1.38
    plus_coef_speed: float = 1.1
    multiplicator_of_weight: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return (((self.get_mean_speed()) + self.plus_coef_speed)
                * self.multiplicator_of_weight * self.weight)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.SPEED_KMH / self.duration)


types_of_workout_classes = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking
}


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in types_of_workout_classes:
        return types_of_workout_classes[workout_type](*data)
    raise AttributeError('Неизвестный тип тренировки')


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