"""
MOLECULAR QUEST: ОТ ДНК ДО БЕЛКА
================================

Учебная игра по молекулярной биологии на Python.
Подходит для JupyterLab и обычного запуска Python 3.

Запуск в JupyterLab:
    %run molecular_quest.py

Игра включает:
1. Комплементарность ДНК.
2. Транскрипцию: матричная ДНК -> иРНК.
3. Трансляцию: кодоны иРНК -> аминокислоты.
4. Финальное задание на весь путь от ДНК до белка.

Используются только стандартные библиотеки Python.
"""

import random
import textwrap


DNA_BASES = "ATGC"

# Таблица генетического кода: кодон иРНК -> аминокислота.
# Названия аминокислот даны по-русски.
GENETIC_CODE = {
    "UUU": "фенилаланин", "UUC": "фенилаланин",
    "UUA": "лейцин", "UUG": "лейцин",
    "UCU": "серин", "UCC": "серин", "UCA": "серин", "UCG": "серин",
    "UAU": "тирозин", "UAC": "тирозин",
    "UAA": "СТОП", "UAG": "СТОП",
    "UGU": "цистеин", "UGC": "цистеин",
    "UGA": "СТОП", "UGG": "триптофан",

    "CUU": "лейцин", "CUC": "лейцин", "CUA": "лейцин", "CUG": "лейцин",
    "CCU": "пролин", "CCC": "пролин", "CCA": "пролин", "CCG": "пролин",
    "CAU": "гистидин", "CAC": "гистидин",
    "CAA": "глутамин", "CAG": "глутамин",
    "CGU": "аргинин", "CGC": "аргинин", "CGA": "аргинин", "CGG": "аргинин",

    "AUU": "изолейцин", "AUC": "изолейцин", "AUA": "изолейцин",
    "AUG": "метионин (СТАРТ)",
    "ACU": "треонин", "ACC": "треонин", "ACA": "треонин", "ACG": "треонин",
    "AAU": "аспарагин", "AAC": "аспарагин",
    "AAA": "лизин", "AAG": "лизин",
    "AGU": "серин", "AGC": "серин",
    "AGA": "аргинин", "AGG": "аргинин",

    "GUU": "валин", "GUC": "валин", "GUA": "валин", "GUG": "валин",
    "GCU": "аланин", "GCC": "аланин", "GCA": "аланин", "GCG": "аланин",
    "GAU": "аспарагиновая кислота", "GAC": "аспарагиновая кислота",
    "GAA": "глутаминовая кислота", "GAG": "глутаминовая кислота",
    "GGU": "глицин", "GGC": "глицин", "GGA": "глицин", "GGG": "глицин",
}


def make_dna(length):
    """Создать случайную последовательность ДНК."""
    return "".join(random.choice(DNA_BASES) for _ in range(length))


def dna_complement(sequence):
    """Построить комплементарную ДНК-цепь."""
    pairs = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return "".join(pairs[base] for base in sequence)


def transcribe(template_dna):
    """
    Построить иРНК по матричной цепи ДНК.
    ДНК A -> РНК U; T -> A; G -> C; C -> G.
    """
    pairs = {"A": "U", "T": "A", "G": "C", "C": "G"}
    return "".join(pairs[base] for base in template_dna)


def translate(mrna):
    """Разбить иРНК на кодоны и перевести их в аминокислоты."""
    amino_acids = []
    codons = [mrna[i:i + 3] for i in range(0, len(mrna), 3)]

    for codon in codons:
        if len(codon) != 3:
            break
        amino_acid = GENETIC_CODE[codon]
        if amino_acid == "СТОП":
            break
        amino_acids.append(amino_acid)

    return codons, amino_acids


def normalize_sequence(answer):
    """Убрать пробелы и привести последовательность к верхнему регистру."""
    return "".join(answer.upper().split())


def ask_sequence(prompt, allowed_letters):
    """Попросить пользователя ввести последовательность и проверить символы."""
    while True:
        answer = normalize_sequence(input(prompt))
        if answer and all(letter in allowed_letters for letter in answer):
            return answer
        print("Проверь ввод: используй только буквы", ", ".join(allowed_letters))


def print_wrapped(text):
    print(textwrap.fill(text, width=76))


def pause():
    input("\nНажми Enter, чтобы продолжить...")


def stage_intro(number, title, explanation):
    print("\n" + "=" * 68)
    print(f"УРОВЕНЬ {number}. {title.upper()}")
    print("=" * 68)
    print_wrapped(explanation)
    print()


def level_dna(score):
    stage_intro(
        1,
        "Комплементарная ДНК",
        "В ДНК азотистые основания соединяются по принципу "
        "комплементарности: аденин (A) — с тимином (T), "
        "гуанин (G) — с цитозином (C). Построй вторую цепь."
    )

    original = make_dna(8)
    print("Дана цепь ДНК:")
    print("5' —", " ".join(original), "— 3'")

    correct = dna_complement(original)
    answer = ask_sequence(
        "\nВведи комплементарную цепь (можно без пробелов): ",
        DNA_BASES
    )

    if answer == correct:
        print("\nВерно! Все основания подобраны комплементарно.")
        score += 10
    else:
        print("\nПока не совсем верно.")
        print("Правильная цепь:", correct)
        print("Помни: A—T, G—C.")

    print("Обрати внимание: цепи ДНК антипараллельны.")
    print("Если первая записана 5' -> 3', вторая напротив неё идёт 3' -> 5'.")
    return score


def level_transcription(score):
    stage_intro(
        2,
        "Транскрипция",
        "Транскрипция — синтез РНК на матричной цепи ДНК. "
        "При образовании РНК вместо тимина (T) используется урацил (U). "
        "Правила подбора: A ДНК -> U РНК; T -> A; G -> C; C -> G."
    )

    template = make_dna(9)
    correct = transcribe(template)

    print("Матричная цепь ДНК:")
    print("3' —", " ".join(template), "— 5'")
    answer = ask_sequence(
        "\nЗапиши последовательность иРНК: ",
        "AUGC"
    )

    if answer == correct:
        print("\nОтлично! Последовательность иРНК получена правильно.")
        score += 15
    else:
        print("\nЕсть ошибка. Правильная иРНК:")
        print("5' —", " ".join(correct), "— 3'")
        print("Проверь пары: A—U, T—A, G—C, C—G.")

    return score


def level_translation(score):
    stage_intro(
        3,
        "Трансляция",
        "Трансляция — синтез белка на рибосоме по последовательности иРНК. "
        "Три соседних нуклеотида образуют кодон. Каждый кодон задаёт "
        "аминокислоту или сигнал остановки (СТОП). Кодон AUG обычно "
        "служит стартовым и кодирует метионин."
    )

    # Подбираем последовательность с несколькими кодонами и без СТОП внутри.
    possible_codons = [
        "AUG", "GCU", "UUU", "GGU", "CCU", "AAA",
        "UAC", "GAA", "ACU", "UGG", "CAU", "CGU"
    ]
    selected = ["AUG"] + [random.choice(possible_codons[1:]) for _ in range(3)]
    mrna = "".join(selected)
    codons, amino_acids = translate(mrna)

    print("Дана иРНК:")
    print("5' —", " — ".join(selected), "— 3'")
    print("\nИспользуй таблицу генетического кода из задания.")
    print("Введи названия аминокислот по порядку через запятую.")
    print("Например: метионин, аланин, глицин")

    answer = input("\nТвоя последовательность: ").strip().lower()
    user_amino_acids = [
        item.strip() for item in answer.replace(";", ",").split(",") if item.strip()
    ]
    correct = [item.lower() for item in amino_acids]

    if user_amino_acids == correct:
        print("\nПравильно! Ты расшифровала все кодоны.")
        score += 20
    else:
        print("\nСверим результат:")
        for codon, amino_acid in zip(codons, amino_acids):
            print(f"{codon} -> {amino_acid}")
        print("Попробуй запомнить: один кодон состоит из трёх нуклеотидов.")

    print("\nПодсказка: генетический код вырожденный —")
    print("одну и ту же аминокислоту могут кодировать разные кодоны.")
    return score


def final_challenge(score):
    stage_intro(
        4,
        "Финальная миссия: от ДНК до белка",
        "Теперь объедини все этапы. По матричной цепи ДНК построй иРНК, "
        "а затем определи аминокислоты. В этом задании последовательность "
        "содержит три кодона."
    )

    # Подбираем матричную ДНК так, чтобы иРНК начиналась со старт-кодона AUG.
    mrna = "AUG" + random.choice(["GCU", "UUU", "GGU", "CCU", "AAA"])
    # Обратное преобразование: иРНК -> матричная ДНК.
    reverse_pairs = {"U": "A", "A": "T", "G": "C", "C": "G"}
    template = "".join(reverse_pairs[base] for base in mrna)

    print("Матричная цепь ДНК:")
    print("3' —", " — ".join(template[i:i + 3] for i in range(0, 9, 3)), "— 5'")

    answer_rna = ask_sequence("\nШаг 1. Запиши иРНК: ", "AUGC")
    correct_rna = transcribe(template)

    if answer_rna == correct_rna:
        print("Транскрипция выполнена верно!")
        score += 10
    else:
        print("Правильная иРНК:", correct_rna)

    codons, amino_acids = translate(correct_rna)
    print("\nШаг 2. Кодоны иРНК:", " — ".join(codons))
    print("Введи аминокислоты через запятую.")
    answer_protein = input("Твоя последовательность: ").strip().lower()
    user_protein = [
        item.strip() for item in answer_protein.replace(";", ",").split(",")
        if item.strip()
    ]

    if user_protein == [item.lower() for item in amino_acids]:
        print("Верно! Белковая последовательность определена.")
        score += 15
    else:
        print("Правильная последовательность:")
        print(" -> ".join(amino_acids))

    return score


def show_summary(score, maximum=70):
    print("\n" + "*" * 68)
    print("МИССИЯ ЗАВЕРШЕНА!")
    print("*" * 68)
    print(f"Твои очки: {score} из {maximum}")

    if score >= 60:
        print("Ранг: МОЛЕКУЛЯРНЫЙ ЭКСПЕРТ")
    elif score >= 40:
        print("Ранг: ИССЛЕДОВАТЕЛЬ")
    elif score >= 20:
        print("Ранг: МОЛЕКУЛЯРНЫЙ СТАЖЁР")
    else:
        print("Ранг: НАЧИНАЮЩИЙ ИССЛЕДОВАТЕЛЬ")

    print("\nГлавная схема, которую нужно запомнить:")
    print("ДНК --транскрипция--> иРНК --трансляция--> белок")
    print("\nВажно: игра упрощает некоторые детали реальных клеточных процессов.")


def main():
    print("=" * 68)
    print("             MOLECULAR QUEST: ОТ ДНК ДО БЕЛКА")
    print("=" * 68)
    print("Добро пожаловать в лабораторию молекулярной биологии!")
    print("Пройди уровни и собери белок, используя генетическую информацию.")

    while True:
        print("\nГЛАВНОЕ МЕНЮ")
        print("1 — Начать новую игру")
        print("2 — Посмотреть правила и биологическую теорию")
        print("0 — Выйти")

        choice = input("\nТвой выбор: ").strip()

        if choice == "1":
            score = 0
            score = level_dna(score)
            pause()
            score = level_transcription(score)
            pause()
            score = level_translation(score)
            pause()
            score = final_challenge(score)
            show_summary(score)
        elif choice == "2":
            print("\nКРАТКАЯ ТЕОРИЯ")
            print("• ДНК хранит наследственную информацию.")
            print("• Репликация — удвоение ДНК.")
            print("• Транскрипция — синтез РНК на матрице ДНК.")
            print("• Трансляция — синтез белка на рибосоме по иРНК.")
            print("• Кодон — последовательность из трёх нуклеотидов иРНК.")
            print("• Аминокислоты соединяются пептидными связями.")
        elif choice == "0":
            print("До встречи в лаборатории!")
            break
        else:
            print("Пожалуйста, введи 1, 2 или 0.")


if __name__ == "__main__":
    main()
