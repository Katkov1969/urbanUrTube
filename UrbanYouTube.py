import hashlib
import time
from typing import List, Optional

class User:
    def __init__(self, nickname: str, password: str, age: int):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password: str) -> str:
        '''Хэширует пароль с использованием SHA-256.'''
        return hashlib.sha256(password.encode()).hexdigest()

    def __repr__(self):
        return f"User(nickname={self.nickname}, age={self.age})"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.nickname == other.nickname and self.password == other.password
        return False

class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __repr__(self):
        return f"Video(title={self.title}, duration={self.duration}, adult_mode={self.adult_mode})"

    def __eq__(self, other):
        if isinstance(other, Video):
            return self.title == other.title
        return False


class UrTube:
    def __init__(self):
        self.users: List[User] = []
        self.videos: List[Video] = []
        self.current_user: Optional[User] = None

    def log_in(self, nickname: str, password: str) -> None:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                return
        print("Неверный логин или пароль")

    def register(self, nickname: str, password: str, age: int) -> None:
        if any(user.nickname == nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует")
        else:
            new_user = User(nickname, password, age)
            self.users.append(new_user)
            self.current_user = new_user

    def log_out(self) -> None:
        self.current_user = None

    def add(self, *videos: Video) -> None:
        for video in videos:
            if video not in self.videos:
                self.videos.append(video)

    def get_videos(self, search_term: str) -> List[str]:
        search_term = search_term.lower()
        return [video.title for video in self.videos if search_term in video.title.lower()]

    def watch_video(self, title: str) -> None:
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                for second in range(video.time_now, video.duration):
                    print(second + 1, end=' ')
                    time.sleep(1)
                print("Конец видео")
                video.time_now = 0
                return

        print("Видео не найдено")



if __name__ == "__main__":
    ur = UrTube()
    v1 = Video('Лучший язык программирования 2024 года', 200)
    v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

    # Добавление видео
    ur.add(v1, v2)

    # Проверка поиска
    print(ur.get_videos('лучший'))
    print(ur.get_videos('ПРОГ'))

    # Проверка на вход пользователя и возрастное ограничение
    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('vasya_pupkin', 'lolkekcheburek', 13)
    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
    ur.watch_video('Для чего девушкам парень программист?')

    # Проверка входа в другой аккаунт
    ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
    print(ur.current_user)

    # Попытка воспроизведения несуществующего видео
    ur.watch_video('Лучший язык программирования 2024 года!')
