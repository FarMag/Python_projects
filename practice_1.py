import os
import psutil
import json
import xml.etree.ElementTree as ET
import zipfile

def display_disk_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Монтирование: {partition.mountpoint}")
            print(f"Устройство: {partition.device}")
            print(f"Метка тома: {partition.opts}")
            print(f"Общий размер: {usage.total // (1024 ** 3)} ГБ")
            print(f"Файловая система: {partition.fstype}")
            print("----------")
        except PermissionError:
            print(f"Нет доступа к разделу: {partition}")


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def validate_filename(self):
        if '.' not in self.filename:
            print("Ошибка: Имя файла должно содержать расширение.")
            return False
        return True

    def create_file(self):
        if self.validate_filename():
            with open(self.filename, 'w') as file:
                print(f"Файл '{self.filename}' создан.")

    def write_to_file(self, content):
        if self.validate_filename() and os.path.exists(self.filename):
            with open(self.filename, 'a') as file:
                file.write(content + '\n')
                print(f"Текст добавлен в файл '{self.filename}'.")
        else:
            print(f"Файл '{self.filename}' не найден.")

    def read_file(self):
        if self.validate_filename() and os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                print(f"Содержимое файла '{self.filename}':")
                print(file.read())
        else:
            print(f"Файл '{self.filename}' не найден.")

    def delete_file(self):
        if self.validate_filename() and os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Файл '{self.filename}' удалён.")
        else:
            print(f"Файл '{self.filename}' не найден.")


class JSONHandler(FileHandler):
    def write_json(self):
        if self.validate_filename() and self.filename.endswith('.json'):
            data = {}
            print("Добавьте данные для JSON файла (оставьте поле 'ключ' пустым, чтобы завершить ввод).")

            while True:
                key = input("Введите ключ (или оставьте пустым для завершения): ").strip()
                if key == "":
                    break
                value = input(f"Введите значение для ключа '{key}': ").strip()
                data[key] = value

            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print(f"Данные сохранены в JSON файл '{self.filename}'.")

    def read_json(self):
        if self.validate_filename() and self.filename.endswith('.json'):
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    print(f"Содержимое JSON файла '{self.filename}':")
                    print(json.dumps(data, ensure_ascii=False, indent=4))
            else:
                print(f"JSON файл '{self.filename}' не найден.")

    def add_object_to_json(self):
        if self.validate_filename() and self.filename.endswith('.json'):
            if os.path.exists(self.filename):

                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                new_object = {}
                print("Добавьте новый объект в JSON файл (оставьте поле 'ключ' пустым, чтобы завершить ввод).")
                while True:
                    key = input("Введите ключ для нового объекта (или оставьте пустым для завершения): ").strip()
                    if key == "":
                        break
                    value = input(f"Введите значение для ключа '{key}': ").strip()
                    new_object[key] = value


                data.update(new_object)
                with open(self.filename, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                print(f"Новый объект добавлен в JSON файл '{self.filename}'.")
            else:
                print(f"JSON файл '{self.filename}' не найден.")


class XMLHandler(FileHandler):
    def write_xml(self, root_tag, content=None):
        if self.validate_filename() and self.filename.endswith('.xml'):
            root = ET.Element(root_tag)
            if content:
                child = ET.SubElement(root, "Content")
                child.text = content
            tree = ET.ElementTree(root)
            tree.write(self.filename, encoding="utf-8", xml_declaration=True)
            print(f"XML файл '{self.filename}' создан.")

    def read_xml(self):
        if self.validate_filename() and self.filename.endswith('.xml') and os.path.exists(self.filename):
            tree = ET.parse(self.filename)
            root = tree.getroot()
            print(f"Содержимое XML файла '{self.filename}':")
            ET.dump(root)
        else:
            print(f"XML файл '{self.filename}' не найден.")

    def add_data_to_xml(self):
        if self.validate_filename() and self.filename.endswith('.xml'):
            if os.path.exists(self.filename):
                tree = ET.parse(self.filename)
                root = tree.getroot()
                element_tag = input("Введите тег для нового элемента: ")
                element_text = input("Введите текст для нового элемента: ")
                new_element = ET.SubElement(root, element_tag)
                new_element.text = element_text
                tree.write(self.filename, encoding="utf-8", xml_declaration=True)
                print(f"Новый элемент добавлен в XML файл '{self.filename}'.")
            else:
                print(f"XML файл '{self.filename}' не найден.")


class ZipHandler:
    def __init__(self, zipname):
        self.zipname = zipname

    def create_empty_zip(self):
        with zipfile.ZipFile(self.zipname, 'w') as zipf:
            print(f"Пустой архив '{self.zipname}' создан.")

    def add_file_to_zip(self, filename):
        if not os.path.exists(self.zipname):
            print(f"Архив '{self.zipname}' не найден.")
            return
        if not os.path.exists(filename):
            print(f"Файл '{filename}' не найден.")
            return

        with zipfile.ZipFile(self.zipname, 'a') as zipf:
            zipf.write(filename)
            print(f"Файл '{filename}' добавлен в архив '{self.zipname}'.")

    def extract_zip(self):
        if os.path.exists(self.zipname):
            with zipfile.ZipFile(self.zipname, 'r') as zipf:
                zipf.extractall()
                print(f"Архив '{self.zipname}' распакован.")
                zipf.printdir()
        else:
            print(f"Архив '{self.zipname}' не найден.")

    def delete_zip(self):
        if os.path.exists(self.zipname):
            os.remove(self.zipname)
            print(f"Архив '{self.zipname}' удалён.")
        else:
            print(f"Архив '{self.zipname}' не найден.")


def main_menu():
    while True:
        print("\nВыберите действие:")
        print("1. Информация о логических дисках")
        print("2. Создать текстовый файл")
        print("3. Записать текст в файл")
        print("4. Прочитать текстовый файл")
        print("5. Удалить текстовый файл")
        print("6. Создать JSON файл")
        print("7. Добавить новый объект в JSON файл")
        print("8. Прочитать JSON файл")
        print("9. Удалить JSON файл")
        print("10. Создать XML файл")
        print("11. Добавить данные в XML файл")
        print("12. Прочитать XML файл")
        print("13. Удалить XML файл")
        print("14. Создать ZIP архив")
        print("15. Добавить файл в ZIP архив")
        print("16. Распаковать ZIP архив")
        print("17. Удалить ZIP архив")
        print("18. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            display_disk_info()

        elif choice == '2':
            filename = input("Введите имя текстового файла: ")
            handler = FileHandler(filename)
            handler.create_file()

        elif choice == '3':
            filename = input("Введите имя файла для записи текста: ")
            content = input("Введите текст для записи: ")
            handler = FileHandler(filename)
            handler.write_to_file(content)

        elif choice == '4':
            filename = input("Введите имя текстового файла: ")
            handler = FileHandler(filename)
            handler.read_file()

        elif choice == '5':
            filename = input("Введите имя текстового файла: ")
            handler = FileHandler(filename)
            handler.delete_file()

        elif choice == '6':
            filename = input("Введите имя JSON файла: ").strip()
            json_handler = JSONHandler(filename)
            json_handler.write_json()

        elif choice == '7':
            filename = input("Введите имя JSON файла для добавления объекта: ")
            handler = JSONHandler(filename)
            handler.add_object_to_json()

        elif choice == '8':
            filename = input("Введите имя JSON файла: ")
            handler = JSONHandler(filename)
            handler.read_json()

        elif choice == '9':
            filename = input("Введите имя JSON файла для удаления: ")
            handler = JSONHandler(filename)
            handler.delete_file()

        elif choice == '10':
            filename = input("Введите имя XML файла: ")
            root_tag = input("Введите имя корневого элемента: ")
            content = input("Введите текст для XML (или оставьте пустым): ")
            handler = XMLHandler(filename)
            handler.write_xml(root_tag, content)

        elif choice == '11':
            filename = input("Введите имя XML файла для добавления данных: ")
            handler = XMLHandler(filename)
            handler.add_data_to_xml()

        elif choice == '12':
            filename = input("Введите имя XML файла: ")
            handler = XMLHandler(filename)
            handler.read_xml()

        elif choice == '13':
            filename = input("Введите имя XML файла для удаления: ")
            handler = XMLHandler(filename)
            handler.delete_file()

        elif choice == '14':
            zipname = input("Введите имя ZIP архива для создания: ")
            handler = ZipHandler(zipname)
            handler.create_empty_zip()

        elif choice == '15':
            zipname = input("Введите имя ZIP архива для добавления файла: ")
            filename = input("Введите имя файла для добавления в архив: ")
            handler = ZipHandler(zipname)
            handler.add_file_to_zip(filename)

        elif choice == '16':
            zipname = input("Введите имя ZIP архива для распаковки: ")
            handler = ZipHandler(zipname)
            handler.extract_zip()

        elif choice == '17':
            zipname = input("Введите имя ZIP архива для удаления: ")
            handler = ZipHandler(zipname)
            handler.delete_zip()

        elif choice == '18':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте снова.")
        print()

if __name__ == "__main__":
    main_menu()
