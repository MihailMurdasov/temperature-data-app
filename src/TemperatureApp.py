import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import matplotlib.pyplot as plt
from RedBlackTree import RedBlackTree

class TemperatureApp:
    def __init__(self, root):
        self.trees = []
        self.trees.append((1, RedBlackTree()))

        root.title("Температурные данные")
        root.geometry("400x400")

        self.label = tk.Label(root, text="Введите температуру:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.add_button = tk.Button(root, text="Добавить", command=self.add_temperature)
        self.add_button.pack()

        self.search_button = tk.Button(root, text="Найти количество", command=self.search_temperature)
        self.search_button.pack()

        self.histogram_button = tk.Button(root, text="Построить гистограмму", command=self.show_histogram)
        self.histogram_button.pack()

        self.load_button = tk.Button(root, text="Загрузить данные из файла", command=self.load_temperatures_from_file)
        self.load_button.pack()

        self.load_button = tk.Button(root, text="Следующий день", command=self.next_day)
        self.load_button.pack()

        self.output = tk.Text(root, height=10, width=50)
        self.output.insert(tk.END, f"====================[День {self.trees[-1][0]}]=====================\n")
        print(f"====================[День {self.trees[-1][0]}]=====================")
        self.output.pack()

    def next_day(self):
        self.output.insert(tk.END, f"================[День {self.trees[-1][0]} окончен]=================\n")
        print(f"================[День {self.trees[-1][0]} окончен]=================")
        next_num = self.trees[-1][0] + 1
        self.trees.append((next_num, RedBlackTree()))
        self.output.insert(tk.END, f"====================[День {self.trees[-1][0]}]=====================\n")
        print(f"====================[День {self.trees[-1][0]}]=====================")

    def add_temperature(self):
        try:
            temp = int(self.entry.get())
            self.trees[-1][1].insert(temp)
            self.output.insert(tk.END, f"Добавлена температура: {temp}\n")
            self.output.see(tk.END)
            print(f"Добавлена температура: {temp}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число!")

    def search_temperature(self):
        try:
            temp = int(self.entry.get())
            count = self.trees[-1][1].find_count(temp)
            self.output.insert(tk.END, f"Температура {temp} зафиксирована {count} раз(а).\n")
            self.output.see(tk.END)
            print(f"Температура {temp} зафиксирована {count} раз(а).")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число!")

    def show_histogram(self):
        choice = simpledialog.askstring("Выбор гистограммы",
                                        "Выберите опцию:\n1. За конкретный день\n2. Все дни\n3. За последние <=7 дней\nВведите номер (1-3):")
        if not choice:
            return
        nodes = []
        days_nums = 0
        day = -1

        if choice == "1":
            day = simpledialog.askinteger("Выбор дня", "Введите номер дня:")
            if not day or day <= 0 or day > len(self.trees):
                messagebox.showerror("Ошибка", "Неверный номер дня.")
                return
            nodes = self.trees[day - 1][1].inorder()

        elif choice == "2":
            for tree in self.trees:
                nodes.extend(tree[1].inorder())

        elif choice == "3":
            if len(self.trees) < 7:
                days_nums = -1 * len(self.trees)
            else:
                days_nums = -7
            for tree in self.trees[days_nums:]:
                nodes.extend(tree[1].inorder())

        else:
            messagebox.showerror("Ошибка", "Неверный ввод. Введите 1, 2 или 3.")
            return

        if not nodes:
            self.output.insert(tk.END, "Нет данных для гистограммы.\n")
            self.output.see(tk.END)
            return

        temperatures = [node[0] for node in nodes]

        min_temp = int(min(temperatures)) - 1
        max_temp = int(max(temperatures)) + 1
        num_bins = 5
        step = max((max_temp - min_temp) / num_bins, 1)
        bins = [round(min_temp + step * i) for i in range(num_bins + 1)]

        histogram = [0] * num_bins
        for elem in nodes:
            for i in range(num_bins):
                if (bins[i] <= elem[0] < bins[i + 1]) or (i == num_bins - 1 and bins[i] <= elem[0] <= bins[i + 1]):
                    histogram[i] += elem[1]
                    break

        bin_labels = [f"[{bins[i]}, {bins[i + 1]})" for i in range(num_bins - 1)]
        bin_labels.append(f"[{bins[-2]}, {bins[-1]}]")

        print("Текстовая гистограмма:")
        for i in range(num_bins):
            print(f"{bin_labels[i]}: {'*' * histogram[i]}")

        plt.bar(bin_labels, histogram, color='blue')
        plt.xlabel("Диапазоны температур")
        plt.ylabel("Количество измерений")
        title = "Гистограмма температур"
        if choice == "1":
            title += f" за день {day}"
        elif choice == "2":
            title += " за все дни"
        elif choice == "3":
            title += f" за последние {-days_nums} дней"
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def load_temperatures_from_file(self):
        file_path = filedialog.askopenfilename(title="Выберите файл с температурами",
                                               filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    for line in file:
                        try:
                            temp = int(line.strip())
                            self.trees[-1][1].insert(temp)
                            self.output.insert(tk.END, f"Добавлена температура из файла: {temp}\n")
                            self.output.see(tk.END)
                            print(f"Добавлена температура из файла: {temp}")
                        except ValueError:
                            messagebox.showerror("Ошибка", f"Некорректное значение в файле: {line.strip()}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()