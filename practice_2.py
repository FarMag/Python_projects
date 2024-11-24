import hashlib
import itertools
import time
import concurrent.futures

def generate_hash(password: str, hash_type: str) -> str:
    if hash_type == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    return ""

def detect_hash_type(hash_value: str) -> str:
    if len(hash_value) == 32:
        return "md5"
    elif len(hash_value) == 64:
        return "sha256"
    else:
        raise ValueError("Некорректное хэш-значение. Оно должно быть длиной 32 (MD5) или 64 (SHA-256) символа.")

def brute_force_multi(hash_value: str, hash_type: str, num_threads: int) -> str:
    start_time = time.time()

    # Функция для потоков
    def worker(start_index, step):
        for i, combination in enumerate(itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=5)):
            if i % step == start_index: 
                password = ''.join(combination)
                if generate_hash(password, hash_type) == hash_value:
                    return password
        return None

    # Запуск потоков
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(worker, range(num_threads), [num_threads] * num_threads))

    # Проверка результатов
    for result in results:
        if result is not None:
            duration = time.time() - start_time
            print(f"Найден пароль '{result}' для хэша {hash_value} за {duration:.2f} секунд")
            return result

    print(f"Пароль для хэша {hash_value} не найден.")
    return None

def brute_force_single(hash_value: str, hash_type: str) -> str:
    start_time = time.time()
    for combination in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=5):
        password = ''.join(combination)
        if generate_hash(password, hash_type) == hash_value:
            duration = time.time() - start_time
            print(f"Найден пароль '{password}' для хэша {hash_value} за {duration:.2f} секунд")
            return password
    print(f"Пароль для хэша {hash_value} не найден.")
    return None

def main():
    hash_value = input("Введите хэш-значение: ").strip()
    try:
        hash_type = detect_hash_type(hash_value)
        print(f"Определен тип хэша: {hash_type.upper()}")
    except ValueError as e:
        print(e)
        return

    mode = input("Выберите режим (1 - однопоточный, 2 - многопоточный): ").strip()
    if mode == "2":
        num_threads = int(input("Введите количество потоков: "))
        brute_force_multi(hash_value, hash_type, num_threads)
    else:
        brute_force_single(hash_value, hash_type)

if __name__ == "__main__":
    main()
