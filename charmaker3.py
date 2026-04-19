import random
import os, platform
import csv

characterName="GenericName"

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def section_header(title):
    line = "=" * 70
    return f"{line}\n{title.upper():^70}\n{line}\n"

def subsection_header(title):
    line = "-" * 50
    return f"\n{title}\n{line}\n"

def indent(text, spaces=4):
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() != "" else "" for line in text.split("\n"))

def load_csv_options(filepath):
    options = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            text = row[0].strip()
            weight = int(row[1]) if len(row) > 1 and row[1].isdigit() else 1
            options.extend([text] * weight)
    return options

def print_header(headerName):
    print("\n" + "=" * 60)
    print(headerName)
    print("=" * 60)

def load_csv_options_filtered(filepath, key):
    options = []
    key = key.strip().lower()

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not any(cell.strip() for cell in row):
                continue

            row_key = row[0].strip().lower()

            if row_key != key:
                continue

            text = row[1].strip()
            weight = int(row[2]) if len(row) > 2 and row[2].isdigit() else 1
            options.extend([text] * weight)

    return options

def load_csv_rows(filepath):
    rows = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # skip empty or whitespace-only rows
            if not row or not any(cell.strip() for cell in row):
                continue

            rows.append(tuple(cell.strip() for cell in row))
    return rows

def build_section(
    title,
    *,
    csv_file=None,
    key=None,
    options=None,
    header_type="section",
    pre_text=None,

    # behavior
    pick_fn=None,          # how to generate result
    format_fn=None,        # how to display result
    reroll_fn=None,        # how to reroll

    # defaults
    allow_duplicates=True
):
    global QUICK_MODE

    # load options
    if options is None:
        if csv_file:
            if key:
                options = load_csv_options_filtered(csv_file, key)
            else:
                options = load_csv_options(csv_file)
        elif pick_fn is None:
            raise ValueError("Must provide csv_file, options, or pick_fn")

    # default picker
    if pick_fn is None:
        pick_fn = lambda: choose_n(options, 1, allow_duplicates, True)[0]

    # default formatter
    if format_fn is None:
        format_fn = lambda x: x

    # initial build
    result = pick_fn()
    display = format_fn(result)

    if not QUICK_MODE:
        print_header(title)
        while True:
            print(display)
            user_input = input("Press Enter to accept, or type anything to reroll: ").strip()

            if user_input == "":
                break
            else:
                if reroll_fn:
                    result = reroll_fn()
                else:
                    result = pick_fn()

                display = format_fn(result)

    output = []

    if header_type == "section":
        output.append(section_header(title))
    else:
        output.append(subsection_header(title))

    if pre_text:
        output.append(indent(pre_text))
        output.append("")

    output.append(indent(display))
    output.append("")

    return "\n".join(output)


def choose_n(options, n, allow_duplicates=False, quick_mode=False):
    """
    Randomly choose n items from a list, optionally prompting the user to accept or reroll.

    Parameters:
    - options (list): List of items to choose from.
    - n (int): Number of items to choose.
    - allow_duplicates (bool): Whether duplicates are allowed.
    - quick_mode (bool): If True, skip user prompts and return random result immediately.
    """

    rejected_items = set()
    pool = options.copy()

    def pick_items():
        nonlocal pool, rejected_items

        if not allow_duplicates:
            # Reset if not enough items remain
            if len(pool) < n:
                pool = options.copy()
                rejected_items.clear()

            available = [item for item in pool if item not in rejected_items]

            if len(available) < n:
                rejected_items.clear()
                available = pool.copy()

            return random.sample(available, n)

        else:
            return [random.choice(pool) for _ in range(n)]

    # QUICK MODE: no prompts, just pick once
    if quick_mode:
        chosen = pick_items()
        return chosen

    # INTERACTIVE MODE
    while True:
        chosen = pick_items()

        print(f"Chosen items: {chosen}")
        accept = input("Accept these? (y/n): ").strip().lower()

        if accept == 'y':
            return chosen
        else:
            if not allow_duplicates:
                rejected_items.update(chosen)
            print("Rerolling...\n")


# ==========================================================
# CHARACTER NAME
# ==========================================================

def character_name():
    global QUICK_MODE

    first_options = load_csv_options("charNameFirst.csv")
    second_options = load_csv_options("charNameSecond.csv")
    first = choose_n(first_options, 1, True, True)[0]
    second = choose_n(second_options, 1, True, True)[0]
    full_name = first + second

    if not QUICK_MODE:
        print_header("CHARACTER NAME")
        while True:
            first = choose_n(first_options, 1, allow_duplicates=True, quick_mode=QUICK_MODE)[0]
            second = choose_n(second_options, 1, allow_duplicates=True, quick_mode=QUICK_MODE)[0]
            full_name = first + second
            print(full_name)

            user_input = input("Press Enter to accept, r to reroll, or type a custom name: ").strip()

            if user_input == "":
                break
            elif user_input == "r":
                continue
            else:
                full_name = user_input
                break

    output = []
    output.append(section_header("CHARACTER NAME"))
    output.append(indent(full_name))
    global characterName
    characterName = full_name
    output.append("")

    return "\n".join(output)


# ==========================================================
# DISPOSITION DIMENSION
# ==========================================================

morality_map = {
        "Misaligned": "Misaligned: generally displeased or suffers from these feelings / actions.",
        "Neutral": "Neutral: neither pleased nor displeased. Does not suffer or benefit from these feelings / actions.",
        "Aligned": "Aligned: generally pleased or benefits from these feelings / actions."
    }


# ==========================================================
# DISPOSITION
# ==========================================================

def disposition_section(title, csv_file):
    options = load_csv_rows(csv_file)

    def pick():
        row = choose_n(options, 1, True, True)[0]
        trait = row[0]
        desc = row[1] if len(row) > 1 else ""
        morality_key = choose_n(list(morality_map.keys()), 1, True, True)[0]
        return (trait, desc, morality_key)

    def format_fn(data):
        trait, desc, morality_key = data
        return f"{trait}: {desc}\nMorality: {morality_map[morality_key]}"

    return build_section(
        title,
        options=options,
        pick_fn=pick,
        format_fn=format_fn,
        header_type="subsection"
    )


# ==========================================================
# VIRTUES & VICES
# ==========================================================

def virtues_and_vices():
    global QUICK_MODE

    rows = load_csv_rows("virtues_and_vices.csv")
    # rows: [(axis, kind, trait, desc), ...]

    # group by axis
    axes = {}
    for row in rows:
        axis = row[0]
        center = row[1]  # virtue anchor
        kind = row[2]
        trait = row[3]
        desc = row[4] if len(row) > 4 else ""

        axes.setdefault(axis, []).append((center, kind, trait, desc))

    selected = []

    for axis, options in axes.items():

        rejected = set()

        def pick():
            nonlocal rejected

            available = [opt for opt in options if opt not in rejected]

            if not available:
                rejected.clear()
                available = options.copy()

            choice = random.choice(available)
            return choice

        center, kind, trait, desc = pick()
        virtue_name = center

        def build_label(center, kind, trait, desc):
            if kind == "Deficiency":
                label = f"Deficiency of {center}: {trait}"
            elif kind == "Virtue":
                label = f"Virtue: {trait}"
            else:
                label = f"Excess of {center}: {trait}"

            preview = [label]
            if desc.strip():
                preview.append(desc)

            return label, "\n".join(preview)

        label, preview_text = build_label(center, kind, trait, desc)

        if not QUICK_MODE:
            print_header("VIRTUES AND VICES")
            while True:
                print("\n" + "=" * 60)
                print("TRAIT")
                print("=" * 60)
                print(preview_text)
                print()

                choice = input("Press Enter to accept, or type anything to reroll: ").strip()

                if choice == "":
                    break

                rejected.add((center, kind, trait, desc))
                center, kind, trait, desc = pick()
                label, preview_text = build_label(center, kind, trait, desc)

        selected.append((label, desc))

    virtues = sorted([x for x in selected if x[0].startswith("Virtue")])
    deficiencies = sorted([x for x in selected if x[0].startswith("Deficiency")])
    excesses = sorted([x for x in selected if x[0].startswith("Excess")])

    output = []
    output.append(section_header("VIRTUES & VICES"))

    output.append(subsection_header("VIRTUES"))
    for label, desc in virtues:
        output.append(indent(label))
        if desc.strip():
            output.append(indent(desc))
        output.append("")

    output.append(subsection_header("VICES"))

    if deficiencies:
        output.append(indent("DEFICIENCIES"))
        output.append(indent("-" * 30))
        for label, desc in deficiencies:
            output.append(indent(label, 8))
            if desc.strip():
                output.append(indent(desc, 12))
            output.append("")

    if excesses:
        output.append(indent("EXCESSES"))
        output.append(indent("-" * 30))
        for label, desc in excesses:
            output.append(indent(label, 8))
            if desc.strip():
                output.append(indent(desc, 12))
            output.append("")

    return "\n".join(output)

# ==========================================================
# TEMPERAMENT
# ==========================================================

def load_temperament_csv(filepath):
    data = {}
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            temp = row[0].strip()
            typ = row[1].strip()
            text = row[2].strip()
            data.setdefault(temp, {"description": "", "strength": [], "weakness": []})
            if typ == "description":
                data[temp]["description"] = text
            else:
                data[temp][typ].append(text)
    return data

def temperament():
    global QUICK_MODE

    data = load_temperament_csv("temperament.csv")
    temps = list(data.keys())

    def build_block(title, temp, num_strengths, num_weaknesses):
        strengths = choose_n(data[temp]["strength"], num_strengths, allow_duplicates=False, quick_mode=True)
        weaknesses = choose_n(data[temp]["weakness"], num_weaknesses, allow_duplicates=False, quick_mode=True)

        block = []
        block.append(subsection_header(title))
        block.append(indent(temp))
        block.append(indent(data[temp]["description"]))
        block.append("")
        block.append(indent("Strengths:", 4))
        for s in strengths:
            block.append(indent(f"- {s}", 8))
        block.append("")
        block.append(indent("Weaknesses:", 4))
        for w in weaknesses:
            block.append(indent(f"- {w}", 8))
        block.append("")

        return "\n".join(block)

    def confirm_temp(title, pool, num_strengths, num_weaknesses):
        while True:
            temp = choose_n(pool, 1, allow_duplicates=False, quick_mode=True)[0]
            block_text = build_block(title, temp, num_strengths, num_weaknesses)

            if QUICK_MODE:
                return temp, block_text

            print("\n" + "=" * 60)
            print(title)
            print("=" * 60)
            print(block_text)

            choice = input("Press Enter to accept, or type anything to reroll: ").strip()
            if choice == "":
                return temp, block_text

    primary, primary_block = confirm_temp("PRIMARY TEMPERAMENT", temps, 5, 3)

    secondary_pool = [t for t in temps if t != primary]

    secondary, secondary_block = confirm_temp("SECONDARY TEMPERAMENT", secondary_pool, 2, 1)

    output = []
    output.append(section_header("TEMPERAMENT"))
    output.append(primary_block)
    output.append(secondary_block)

    return "\n".join(output)


# ==========================================================
# CHARACTER ARC – THE GHOST
# ==========================================================

def ghost():
    return build_section(
        "THE GHOST",
        csv_file="character_arc.csv",
        key="ghost",
        header_type="subsection",
        pre_text="The ghost is a formative event in your character's backstory. It does not need to be negative."
    )


# ==========================================================
# CHARACTER ARC – THE LIE
# ==========================================================
def lie():
    return build_section(
        "THE LIE",
        csv_file="character_arc.csv",
        key="lie",
        header_type="subsection",
        pre_text="This is a misconception the character has formed about themselves or the world."
    )

# ==========================================================
# CHARACTER ARC – THE WANT
# ==========================================================

def want():
    axis1 = load_csv_options_filtered("character_arc.csv", "want_axis1")
    axis2 = load_csv_options_filtered("character_arc.csv", "want_axis2")

    def pick():
        # ensure unique targets
        targets = choose_n(axis2, 3, allow_duplicates=False, quick_mode=True)

        def one(target):
            return f"{choose_n(axis1, 1, True, True)[0]} towards a {target}"

        return (
            one(targets[0]),
            one(targets[1]),
            one(targets[2])
        )

    def format_fn(data):
        main, sub1, sub2 = data
        return (
            f"MAIN PLOT:\n{main}\n\n"
            f"SUBPLOT 1:\n{sub1}\n\n"
            f"SUBPLOT 2:\n{sub2}"
        )

    return build_section(
        "THE WANT",
        options=[None],
        pick_fn=pick,
        format_fn=format_fn,
        header_type="subsection",
        pre_text="This is the thing the character initially believes that they want or that will make them whole / happy. This is a misguided, incorrect assumption based on their lie, and pursuing their want STRENGTHENS their lie."
    )

# ==========================================================
# CHARACTER ARC – THE NEED
# ==========================================================
def need():
    return build_section(
        "THE NEED",
        csv_file="character_arc.csv",
        key="need",
        header_type="subsection",
        pre_text="What the character actually requires to be complete. Provides a 'personalized anecdote' to their lie. Usually a key realization. Comes later in the story / arc after they pursue the want, achieve it, and realize that they still feel empty. Challenges the status quo of the world."
    )

# ==========================================================
# CHARACTER ARC – THE TRUTH
# ==========================================================
def truth():
    return build_section(
        "THE TRUTH",
        csv_file="character_arc.csv",
        key="truth",
        header_type="subsection",
        pre_text="Antidote to the lie. The character struggles to accept this. At the climax, the character accepts the truth and vanquishes the lie. This makes the character complete."
    )

# ==========================================================
# THE FOUR SELVES
# ==========================================================

def four_self(title, key):
    return build_section(
        title,
        csv_file="four_selves.csv",
        key=key,
        header_type="subsection"
    )

# ==========================================================
# MAIN
# ==========================================================

def main():
    global QUICK_MODE

    choice = input("Quick character? (y/n): ").strip().lower()
    QUICK_MODE = (choice == "y")

    character = []

#APPEARANCE
    character.append(character_name())
    character.append(build_section("RACE", csv_file="race.csv"))
    character.append(build_section("AGE & SEX", csv_file="age_and_sex.csv"))
    character.append(build_section("UNIQUE LOOK", csv_file="unique_look.csv"))
    character.append(build_section("PIETY", csv_file="piety.csv"))
    character.append(section_header("THE FOUR SELVES"))
    character.append(four_self("SOCIAL SELF", "social"))
    character.append(four_self("PERSONAL SELF", "personal"))
    character.append(four_self("CORE SELF", "core"))
    character.append(four_self("HIDDEN SELF", "hidden"))


#OTHERS / BACKGROUND
    character.append(build_section("SIBLINGS", csv_file="siblings.csv"))
    character.append(build_section("OCCUPATION", csv_file="occupation.csv"))

#ADDITIONAL TIDBITS
    character.append(build_section("TALENT", csv_file="talent.csv"))
    character.append(build_section("FLAW", csv_file="flaw.csv"))
    character.append(build_section("QUIRK", csv_file="quirk.csv"))
    character.append(build_section("SECRET", csv_file="secret.csv"))
    character.append(build_section("SUPERPOWER (OPTIONAL)", csv_file="superpower.csv"))

#AS A PERSON
    character.append(build_section("ATTITUDE", csv_file="attitude.csv"))
    character.append(temperament())
    character.append(disposition_section("DISPOSITION – INTRA-PERSONAL", "disposition_intrapersonal.csv"))
    character.append(disposition_section("DISPOSITION – FAMILY", "disposition_family.csv"))
    character.append(disposition_section("DISPOSITION – COMMUNITY", "disposition_community.csv"))
    character.append(disposition_section("DISPOSITION – STATE", "disposition_state.csv"))
    character.append(disposition_section("DISPOSITION – UNIVERSE", "disposition_universe.csv"))
    character.append(virtues_and_vices())

#WHY DO WE CARE
    character.append(build_section("MOTIVATION", csv_file="motivation.csv"))
    character.append(build_section("ROOTING INTEREST", csv_file="rooting_interest.csv"))
    character.append(section_header("CHARACTER ARC"))
    character.append(ghost())
    character.append(lie())
    character.append(want())
    character.append(need())
    character.append(truth())

#VULNERABILITIES (Knife Theory)
    character.append(
        build_section(
            "VULNERABILITIES",
            csv_file="vulnerabilities.csv",
            pick_fn=lambda: choose_n(
                load_csv_options("vulnerabilities.csv"),
                5,
                allow_duplicates=True,
                quick_mode=True
            ),
            format_fn=lambda items: "\n".join(items)
        )
    )

# Save to file
    global characterName
    filename = characterName+".txt"
    with open(filename, "w", encoding="utf-8") as f:
        for entry in character:
            f.write(entry + "\n")

    print(f"Character saved to {filename}")
# ==========================================================

if __name__ == "__main__":
    main()
