# ==========================================================
# TEMPLATE FOR NEW SECTION - REMEMBER TO ADD character.append(template_function_name()) to main
# ==========================================================
def template_function_name():
    return weighted_section("TEMPLATE_FUNCTION_NAME", [
        ("OPTION 1", 1), #WEIGHT of 1
        ("OPTION 2", 3), #WEIGHT of 3
        ("OPTION 3", 3) #last line has NO COMMA
    ])
# ==============END OF TEMPLATE SECTION====================


import random
import os, platform

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



# ==========================================================
# SELF-CONTAINED UNIVERSAL WEIGHTED SECTION
# ==========================================================
def weighted_section(section_name, weighted_options, pre_text=None, header_type="section"):

    base_pool = []
    for text, weight in weighted_options:
        base_pool.extend([text] * weight)

    pool = list(base_pool)

    def generator():
        nonlocal pool
        if not pool:
            pool = list(base_pool)
        choice = random.choice(pool)
        pool.remove(choice)
        return choice

    if QUICK_MODE:
        result = generator()
    else:
        while True:
            result = generator()

            print("\n" + "=" * 60)
            print(section_name)
            print("=" * 60)

            if pre_text:
                print(pre_text + "\n")

            print(result)
            print()

            choice = input("Press Enter to accept, or type anything to reroll: ").strip()
            if choice == "":
                break

    output = []

    # HEADER CONTROL
    if header_type == "section":
        output.append(section_header(section_name))
    elif header_type == "subsection":
        output.append(subsection_header(section_name))
    # if "none" → print nothing

    if pre_text:
        output.append(indent(pre_text))
        output.append("")

    output.append(indent(result))
    output.append("")

    return "\n".join(output)


# ==========================================================
# CHARACTER NAME
# ==========================================================

def character_name():

    first_halves = [
        ("Al", 1), ("Be", 1), ("Gi", 1), ("Her", 1), ("Ni", 1), ("Nor", 1),
        ("O", 1), ("Ra", 1), ("Sam", 1), ("Ta", 1), ("Theo", 1), ("Vas", 1),

        ("Ari", 1), ("Chrisi", 1), ("Emi", 1), ("Er", 1), ("Hel", 1), ("Joh", 1),
        ("Ly", 1), ("Mari", 1), ("Mel", 1), ("Ren", 1), ("Sy", 1), ("Yve", 1)
    ]

    second_halves = [
        ("forr", 1), ("khal", 1), ("lon", 1), ("mer", 1), ("mund", 1), ("nard", 1),
        ("ote", 1), ("ramos", 1), ("ric", 1), ("shak", 1), ("sius", 1), ("well", 1),

        ("ana", 1), ("bell", 1), ("ette", 1), ("eva", 1), ("fri", 1), ("lia", 1),
        ("lody", 1), ("mys", 1), ("orie", 1), ("quin", 1), ("sil", 1), ("till", 1)
    ]

    first = weighted_section("FIRST HALF", first_halves, header_type="none").strip()
    second = weighted_section("SECOND HALF", second_halves, header_type="none").strip()

    full_name = first + second

    output = []
    output.append(section_header("CHARACTER NAME"))
    output.append(indent(full_name))
    output.append("")

    return "\n".join(output)


# ==========================================================
# PIETY
# ==========================================================
def piety():
    return weighted_section("PIETY", [
        ("Believes that gods do not exist", 1),
        ("Believes in their god but does not care", 3),
        ("Has worshipped before", 3),
        ("Worships intermittently, but may attend regularly", 7),
        ("Worships regularly", 3),
        ("Worships fluently", 2),
        ("Worships Fanatically, willing to die for god", 1)
    ])

# ==========================================================
# DISPOSITION DIMENSION
# ==========================================================

def disposition_dimension(section_name, ethical_traits, descriptions):

    morality_map = {
        "Misaligned": "Misaligned: generally displeased or suffers from these feelings / actions.",
        "Neutral": "Neutral: neither pleased nor displeased. Does not suffer or benefit from these feelings / actions.",
        "Aligned": "Aligned: generally pleased or benefits from these feelings / actions."
    }

    weighted_options = []

    for ethicality, traits in ethical_traits.items():
        for trait in traits:
            for morality_key, morality_text in morality_map.items():

                if ethicality == "Neutral" or morality_key == "Neutral":
                    weight = 1
                else:
                    weight = 2

                formatted = (
                    f"Ethicality: {ethicality}\n"
                    f"{trait}: {descriptions.get(trait, '')}\n"
                    f"Morality: {morality_text}"
                )

                weighted_options.append((formatted, weight))

    return weighted_section(section_name, weighted_options, header_type="subsection")


# ==========================================================
# DISPOSITION – INTRAPERSONAL
# ==========================================================

def disposition_intrapersonal():

    ethical_traits = {
        "Ethical": ["Conformity", "Patterned"],
        "Unethical": ["Individuality", "Randomness"],
        "Neutral": ["Neutral Stance"]
    }

    descriptions = {
        "Conformity": "Tends to consider groups more important than individuals, or at least succumb to their norms. Likely to avoid dressing or talking differently, deviating from customs, etc.",
        "Patterned": "Prefers to seek patterns in things as a means to understanding. Tend to carefully weigh decisions instead of utilizing randomness.",
        "Individuality": "Values individuals over groups, or at least what distinguishes themselves from others. Tend to dress differently, enjoy customizing expressions, and see themselves as different than others.",
        "Randomness": "Suggests a lack of a definite aim, direction, rule, or method with no specific goal or purpose. Prefer to make decisions by the flip of a coin or pure chance."
    }

    return disposition_dimension(
        "DISPOSITION – INTRA-PERSONAL",
        ethical_traits,
        descriptions
    )

# ==========================================================
# DISPOSITION – FAMILY
# ==========================================================

def disposition_family():

    ethical_traits = {
        "Ethical": ["Loyalty", "Distinction"],
        "Unethical": ["Betrayal", "Ambiguity"],
        "Neutral": ["Neutral Stance"]
    }

    descriptions = {
        "Loyalty": "Devoted to their family.",
        "Distinction": "Prefer to recognize a distinction between family and non-family, usually feeling repulsed at the implications of familial ambiguity.",
        "Betrayal": "Likely to cheat on their spouse and bad-mouth their family when not in their presence. Generally either disgruntled with their families or taking them for granted, not valuing them.",
        "Ambiguity": "To be societally unaware of a character’s own family and to draw no distinctions thereof. Believes that that familial ambiguity and uncertainty will minimize bias, placing more emphasis on the society and its problems."
    }

    return disposition_dimension(
        "DISPOSITION – FAMILY",
        ethical_traits,
        descriptions
    )

# ==========================================================
# DISPOSITION – COMMUNITY
# ==========================================================

def disposition_community():

    ethical_traits = {
        "Ethical": ["Interdependence", "Lawfulness"],
        "Unethical": ["Independence", "Criminality"],
        "Neutral": ["Neutral Stance"]
    }

    descriptions = {
        "Interdependence": "Enjoy the mutual dependence between themselves and their community, usually valuing social contact and participating in public events.",
        "Lawfulness": "Obeys laws, though this obedience may be the result of respect or fear of punishment.",
        "Independence": "Prefers to avoid the community, minimizing interaction when possible, and thus being independent of it. Likely to avoid socializing, value the privacy of their home and/or distance themselves from others by living rurally, etc.",
        "Criminality": "Do not respect the local laws, feeling as though they are an imposition or a hindrance. Likely to disregard established laws."
    }

    return disposition_dimension(
        "DISPOSITION – COMMUNITY",
        ethical_traits,
        descriptions
    )

# ==========================================================
# DISPOSITION – STATE
# ==========================================================

def disposition_state():

    ethical_traits = {
        "Ethical": ["Bureaucracy", "Patriotism"],
        "Unethical": ["Anarchy", "Treacherousness"],
        "Neutral": ["Neutral Stance"]
    }

    descriptions = {
        "Bureaucracy": "Prefer to be governed by a structure of abundance, which, while it may adapt and move slowly, results in a highly structured society with classes, rank, hierarchy, and organization.",
        "Patriotism": "Prefer their state, nation, land, etc, to others.",
        "Anarchy": "Preference for a lack of government, an abolishment of social distinctions.",
        "Treacherousness": "Prefers other states, nations, laws, and lands to their own, disliking the government that presides over them."
    }

    return disposition_dimension(
        "DISPOSITION – STATE",
        ethical_traits,
        descriptions
    )
# ==========================================================
# DISPOSITION – UNIVERSE
# ==========================================================

def disposition_universe():

    ethical_traits = {
        "Ethical": ["Necessity", "Meaningfulness"],
        "Unethical": ["Chance", "Meaninglessness"],
        "Neutral": ["Neutral Stance"]
    }

    descriptions = {
        "Necessity": "Believes that all events are the results of causes, and chance plays no part in bringing about events. Believes that when events seem the result of chance, they are merely the result of unknown causes; chance does not exist. This does not presuppose that all events are planned, pre-destined, or forced to occur to fulfill a decreed purpose. Instead, necessity asserts simply that all events are predetermined, the result of infinitely long causal chains.",
        "Meaningfulness": "Asserts that there is an objective reality. Resultant from this objective reality, these characters tend to discover purpose in their lives or purpose to the universe. Tend to be more active in making choices than those who do not find purpose in the universe.",
        "Chance": "Believes that events are NOT merely the result of causal chains, predetermined beyond our power. Instead, chance emphasizes the power of choice, the freedom to take the universe in a new direction with every chosen action. Sometimes, things just happen.",
        "Meaninglessness": "Results from the perceived subjectivity of reality, the refusal to accept a singular objective reality. Characters with this view tend to question reality and dismiss notions of the universe progressing purposively. These characters believe that life is short and choices made do not affect anything with significance."
    }

    return disposition_dimension(
        "DISPOSITION – UNIVERSE",
        ethical_traits,
        descriptions
    )


def disposition():
    output = []
    output.append(section_header("DISPOSITION"))
    output.append(disposition_intrapersonal())
    output.append(disposition_family())
    output.append(disposition_community())
    output.append(disposition_state())
    output.append(disposition_universe())
    return "\n".join(output)



# ==========================================================
# VIRTUES & VICES
# ==========================================================

def virtues_and_vices():

    axes = [
        ("Fearful", "Courageous", "Reckless"),
        ("Complacent", "Assertive", "Combative"),
        ("Callous", "Empathetic", "Anxious"),
        ("Distrusting", "Trusting", "Gullible"),
        ("Bondless", "Loyal", "Fanatic"),
        ("Impulsive", "Patient", "Dilatory"),
        ("Apathetic", "Determined", "Zealous"),
        ("Coddling", "Honest", "Surly"),
        ("Aimless", "Ambitious", "Perfectionist"),
        ("Cynical", "Open-minded", "Traditionalist"),
        ("Prideful", "Humble", "Self-deprecating"),
        ("Aloof", "Curious", "Intrusive"),
        ("Subordinate", "Independent", "Isolated"),
        ("Insecure", "Self-Valuing", "Entitled"),
        ("Prejudiced", "Tolerant", "Pandering"),
        ("Offensive", "Discrete", "Ambiguous"),
        ("Shameless", "Modest", "Bashful"),
        ("Ascetic", "Temperate", "Hedonistic"),
        ("Miserly", "Magnificent", "Garishly Opulent"),
        ("Inirascible", "Tempered", "Irascible")
    ]

    virtue_vice_descriptions = {
        "Dilatory": "Slow to act; procrastinator; causes delay",
        "Coddling": "Sheltering; withholds information and actions that would cause others pain",
        "Surly": "Unfriendly and rude; cares not if their words or actions cause others pain.",
        "Insecure": "You do not feel that you deserve anything.",
        "Self-Valuing": "You believe you deserve what you have earned and that some others do not (because they haven't earned them, etc).",
        "Entitled": "You strongly believe you are due more than you have, and more than others.",
        "Ascetic": "The practice of severe self-discipline and abstention from all forms of indulgence.",
        "Temperate": "Not pained at the absence of what is pleasant and at their abstinence from it. Avoid excessive pleasure. Rarely feel pain or craving when these pleasures are absent.",
        "Hedonistic": "Self-indulgent; gives in to pleasure constantly and often; pains desperately when it is missing.",
        "Miserly": "Hoards wealth and spends as little money as possible.",
        "Magnificent": "While staying within means, spending of large sums on things and events that benefit numerous persons besides the spender.",
        "Inirascible": "Unable to be angered; unlikely to defend oneself; weathers insults and does not intervene when their friends are insulted",
        "Tempered": "Angered over the 'proper' things; not easily provoked or goaded",
        "Irascible": "Easily angered; hot-headed and easily provoked",
        "Empathetic": "Able to understand and share the feelings of others.",
        "Loyal": "Faithful to commitments or obligations.",
        "Patient": "Able to endure delay or suffering without becoming annoyed.",
        "Determined": "Purposeful and unwilling to give up.",
        "Honest": "Upright, sincere, and truthful.",
        "Ambitious": "Driven to achieve or improve.",
        "Open-minded": "Willing to consider different ideas and perspectives.",
        "Humble": "Modest and respectful of others.",
        "Curious": "Eager to learn and explore.",
        "Independent": "Self-reliant and capable of acting without support.",
        "Tolerant": "Accepting of different views or behaviors.",
        "Temperate": "Moderate and self-restrained.",
        "Magnificent": "Generous, grand, or impressive in character.",
        "Trusting": "Willing to rely on others with confidence.",
        "Modest": "Not boastful; moderate in estimation of one's abilities.",
        "Discrete": "Careful in speech or action, especially to avoid offense."
    }

    weighted_choices = [
        ("Deficiency", 3),
        ("Virtue", 2),
        ("Excess", 3)
    ]

    def pick_kind():
        base = []
        for text, weight in weighted_choices:
            base.extend([text] * weight)
        return random.choice(base)

    selected = []

    for deficiency, virtue, excess in axes:

        while True:

            kind = pick_kind()

            if kind == "Deficiency":
                trait = deficiency
                label = f"Deficiency of {virtue}: {trait}"
            elif kind == "Virtue":
                trait = virtue
                label = f"Virtue: {trait}"
            else:
                trait = excess
                label = f"Excess of {virtue}: {trait}"

            description = virtue_vice_descriptions.get(trait, "")

            # Build preview block
            preview = []
            preview.append(label)
            if description.strip():
                preview.append(description)

            preview_text = "\n".join(preview)

            if QUICK_MODE:
                break

            print("\n" + "=" * 60)
            print("TRAIT")
            print("=" * 60)
            print(preview_text)
            print()

            choice = input("Press Enter to accept, or type anything to reroll: ").strip()
            if choice == "":
                break

        selected.append((label, description))

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

def temperament():
    temperament_descriptions = {
        "Sanguine": "This temperament is associated with extroverts, talkative characters, and optimists. These characters have appealing personalities and are the life of any party. They have good senses of humor and are usually gifted at Storytelling. Sanguine characters are enthusiastic, expressive, and emotional. Wide-eyed, innocent, and curious, these characters live in the present and are always sincere at heart. Sanguine characters manage to find the humor in disasters, are always cheery, and are liked by others. Creative and colorful, these characters look great on the surface and have energy and enthusiasm in all that they do. Thriving on compliments, sanguine characters make friends easily and love others. These characters seek to prevent dull moments by providing excitement, and they never hold grudges. Sanguine characters are compulsive talkers with loud voices. Remembering names is difficult for these characters, and they are prone to complaining. It is possible these characters appear too happy to others and, seeming fake, scare them away. Driven by their inner child, sanguine characters are naïve and easily get angry. Sanguine characters are disorganized and would rather talk than act. Further, they often forget obligations, have fading confidence, and are undisciplined. Many decisions are based upon feelings. Hating to be alone and needing attention, these characters seek center stage by dominating conversations and energetically interrupting others. These characters often make excuses and have a tendency to repeat stories.",
        "Choleric": "This temperament is associated with extroverts, doers, and optimists. Born leaders, choleric characters are active and have a compulsive need for change. Driven to correct wrongs, they are not discouraged easily and may be unemotional. These characters exude confidence, are strong-willed, and decisive. This temperament causes characters to be organized and task-oriented. Insisting on the productivity of others, these characters seek practical solutions to problems and move quickly to action. Thriving on opposition, these characters have little need for friends or groups and excel during emergencies. Unfortunately, choleric characters may be bossy, impatient, quick-tempered, unable to relax, and refuse to give up even when clearly losing. These characters are too intense, come on too strong, and are inflexible and uncomplimentary. Choleric characters dislike tears and emotions, and are generally unsympathetic. These characters give answers too quickly, dominate more than is good, and are often too busy for their families. Also, choleric characters are impatient with poor performance and have little tolerance for mistakes. Choleric characters are often rude, tactless, and manipulate others. Though these characters may often be right, which they always insist upon, this also makes them unpopular with others.",
        "Melancholic": "This temperament is associated with the introvert, thinker, and pessimist. Melancholic characters tend to be deep, thoughtful, and analytical. They are serious, purposeful, and prone to genius. Often, they are talented and creative, with an artistic or musical inclination. Melancholic characters may be philosophical, poetic, and appreciate beauty. Sensitive to others, they may be self-sacrificing, conscientious, or idealistic. This temperament causes characters to set high standards and want everything done right. Their homes are orderly, and otherwise they are persistent, thorough, orderly, organized, and always neat and tidy. This powerful drive is often characterized negatively by others, but melancholic characters often solve problems and surprise others with creativity. Melancholic characters need to finish what they start. Socially, this temperament causes characters to make friends cautiously and stay in the background to avoid attention. These characters are faithful, devoted, and listen well to complaints. Unfortunately, they can be moody and depressed, often remembering or emphasizing the negative. Further, they are self-centered, often in another world, and may have a low opinion of themselves. Melancholic characters are not people-oriented, and prefer to deal with things rather than people. Also, these characters prefer analysis to work. Having a deep need for approval, these characters are hard to please and often set standards too high. Often withdrawn and remote, melancholic characters are critical of others and withhold affection. In characters, this temperament can cause them to be antagonistic and vengeful because they are suspicious of others and dislike those in opposition. This temperament causes characters to be unforgiving and skeptical of compliments.",
        "Phlegmatic": "This temperament is associated with introverts, watchers, and pessimists. Having low-key personalities, phlegmatic characters are relaxed, calm, cool, and easy-going. Their lives are balanced and consistent. They are quiet but witty, sympathetic, and kind. Good parents, phlegmatic characters are able to take the bad with the good, keep their emotions hidden, and are never in a hurry. Phlegmatic characters are competent, steady, agreeable, and good under pressure, though they often seek the easiest way to get things done. These characters are easy to get along with, pleasant, and inoffensive. However, since they are unenthusiastic, they may be feared or others may worry about them, especially since they are indecisive and avoid responsibility. This temperament causes characters to be too shy, compromising, and self-righteous. Phlegmatic characters are lax on discipline, lack motivation, and are not goal-oriented. They can be lazy, careless, and discouraging to others. These characters would rather watch than become involved. While they watch, however, they are judgmental, sarcastic, and resistant to change."
    }

    temperament_strengths = {
        "Sanguine": [
            "Appealing personality", "Talkative", "Good Sense of Humor", "Enthusiastic", "Cheerful",
            "Curious", "Sincere", "Turns disaster into humor", "Volunteers for jobs", "Creative and colorful",
            "Easily inspires others", "Easily makes friends", "Loves characters", "Thrives on compliments",
            "Envied by others", "Doesn't hold grudges", "Apologizes quickly", "Spontaneous"
        ],
        "Choleric": [
            "Born leader", "Dynamic & active", "Compulsive need to change", "Must correct wrongs",
            "Strong-willed", "Decisive", "Unemotional", "Not easily discouraged", "Independent",
            "Self-sufficient", "Confident", "Can run anything", "Goal-oriented", "Sees the whole picture",
            "Organizes well", "Seeks practical solutions", "Moves quickly to action", "Delegates work",
            "Insists on production", "Stimulates activity", "Thrives on opposition", "Has little need for friends",
            "Will lead and organize", "Is usually right", "Excels in emergencies"
        ],
        "Melancholic": [
            "Thoughtful", "Analytical", "Serious and purposeful", "Prone to genius", "Talented and creative",
            "Artistic or musical", "Philosophical or poetic", "Appreciates beauty", "Sensitive to others",
            "Self-sacrificing", "Conscientious", "Idealistic", "Perfectionist", "Schedule-oriented",
            "Conscious of details", "Persistent", "Orderly and organized", "Economical", "Sees the problems",
            "Finds creative solutions", "Avoids causing attention", "Faithful and devoted", "Compassionate"
        ],
        "Phlegmatic": [
            "Low key", "Easy going", "Relaxed", "Cool calm and collected", "Patient", "Quiet, but witty",
            "Keeps emotions hidden", "Good parent", "Not in a hurry", "Can take the good with the bad",
            "Doesn’t get upset", "Competent and steady", "Peaceful and agreeable", "Mediated problems",
            "Avoids conflicts", "Good under pressure", "Finds the easy way", "Good listener",
            "Has many friends", "Inoffensive", "Dry sense of humor", "Compassion and concern"
        ]
    }

    temperament_weaknesses = {
        "Sanguine": [
            "Compulsive talker", "Exaggerates", "Elaborates", "Dwells on trivia", "Cannot remember names",
            "Scares others away", "Too happy for some", "Restless energy", "Egotistical", "Complains",
            "Controlled by circumstances", "Seems phony", "Never matures", "Doesn't follow through",
            "Undisciplined", "Decides by feelings", "Easily distracted", "Hates to be alone",
            "Needs center stage", "Wants to be popular", "Dominates conversations", "Interrupts", "Doesn’t listen"
        ],
        "Choleric": [
            "Bossy", "Impatient", "Cannot relax", "Enjoys controversy", "Argumentative", "Won’t give up if losing",
            "Comes on too strong", "Inflexible", "Dislikes emotions", "Little tolerance for mistakes",
            "Unsympathetic", "May be rude", "Manipulates others", "Demanding of others", "Workaholic",
            "Can do everything better", "Knows everything", "Decides for others", "Possessive",
            "Cannot say 'I'm sorry'",
            "Might be right but unpopular"
        ],
        "Melancholic": [
            "Moody / depressed", "False humility", "Off in another world", "Remembers negatives",
            "Low self-image", "Selective hearing", "Too introspective", "Guilty feelings", "Persecution complex",
            "Bothered by imperfection", "Hesitant to start projects", "Plans too much", "Prefers analysis to work",
            "Hard to please", "Standards too high", "Deep need for approval", "Socially insecure",
            "Critical of others", "Antagonistic", "Unforgiving", "Skeptical of compliments"
        ],
        "Phlegmatic": [
            "Unenthusiastic", "Fearful", "Worried", "Indecisive", "Avoids responsibilities", "Selfish",
            "Too shy", "Too compromising", "Self-righteous", "Lacks self-motivation", "Hard to get moving",
            "Resents being pushed", "Lazy and careless", "Discourages others", "Would rather watch",
            "Dampens enthusiasm", "Stays uninvolved", "Indifferent to plans", "Judges others",
            "Sarcastic and teasing", "Resists change"
        ]
    }

    temps = ["Sanguine", "Choleric", "Melancholic", "Phlegmatic"]

    def pick_traits(temp, num_strengths, num_weaknesses):
        strengths = random.sample(temperament_strengths[temp], num_strengths)
        weaknesses = random.sample(temperament_weaknesses[temp], num_weaknesses)
        return strengths, weaknesses

    def build_block(title, temp, num_strengths, num_weaknesses):
        strengths, weaknesses = pick_traits(temp, num_strengths, num_weaknesses)

        block = []
        block.append(subsection_header(title))
        block.append(indent(temp))
        block.append(indent(temperament_descriptions[temp]))
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
            temp = random.choice(pool)
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

    # PRIMARY
    primary, primary_block = confirm_temp(
        "PRIMARY TEMPERAMENT",
        temps,
        5,
        3
    )

    # SECONDARY (exclude primary)
    secondary_pool = [t for t in temps if t != primary]

    secondary, secondary_block = confirm_temp(
        "SECONDARY TEMPERAMENT",
        secondary_pool,
        2,
        1
    )

    output = []
    output.append(section_header("TEMPERAMENT"))
    output.append(primary_block)
    output.append(secondary_block)

    return "\n".join(output)

# ==========================================================
# SIBLINGS
# ==========================================================

def siblings():
    return weighted_section("SIBLINGS", [

        ("Only child", 1),
        ("1 brother", 1),
        ("1 sister", 1),
        ("1 brother and 1 sister", 1),
        ("2 brothers", 1),
        ("2 sisters", 1),
        ("2 brothers and 1 sister", 1),
        ("1 brother and 2 sisters", 1),
        ("3 brothers", 1),
        ("3 sisters", 1),
        ("3 brothers and 1 sister", 1),
        ("1 brother and 3 sisters", 1),
        ("2 brothers and 2 sisters", 1),
        ("3 brothers and 2 sisters", 1),
        ("2 brothers and 3 sisters", 1),
        ("3 brothers and 3 sisters", 1),
        ("More than 3 brothers and/or sisters", 1)
    ])

# ==========================================================
# CHARACTER ARC – THE GHOST
# ==========================================================
def ghost():
    return weighted_section(
        "THE GHOST",
        [
            ("The loss of a protector or friend", 1),
            ("Survivor's guilt", 1),
            ("Betrayed by an ally", 1),
            ("Past failure", 1),
            ("Dark Secret", 1),
            ("Exiled from community", 1),
            ("Veteran of a great struggle", 1),
            ("Orphan upbringing", 1),
            ("Witnessed something traumatic", 1),
            ("Living Under a Curse", 1)
        ],
        pre_text="The ghost is a formative event in your character's backstory. It does not need to be negative.", header_type="subsection"
    )


# ==========================================================
# CHARACTER ARC – THE LIE
# ==========================================================

def lie():
    return weighted_section(
        "THE LIE",
        [
            ("Inherent unworthiness", 1),
            ("Trust is weakness", 1),
            ("Power = safety", 1),
            ("Happiness is unattainable", 1),
            ("Must go it alone", 1),
            ("Change is dangerous", 1),
            ("Emotions are a liability", 1),
            ("Self-sacrifice is noble", 1),
            ("Must uphold tradition", 1),
            ("Life is a trap", 1)
        ],
        pre_text="This is a misconception the character has formed about themselves or the world.", header_type="subsection"
    )

# ==========================================================
# CHARACTER ARC – THE WANT
# ==========================================================

def want():

    axis1 = [
        ("Revenge", 1),
        ("Power", 1),
        ("Love", 1),
        ("Knowledge", 1),
        ("Freedom", 1),
        ("Redemption", 1),
        ("Survival", 1),
        ("Justice", 1),
        ("Adventure", 1)
    ]

    axis2 = [
        ("Person", 1),
        ("Place", 1),
        ("Thing", 1),
        ("State of Mind", 1),
        ("Ability or Power", 1),
        ("Status or Role", 1),
        ("Belief or Ideology", 1),
        ("Legacy", 1)
    ]

    def pick_axis(options):
        base = []
        for text, weight in options:
            base.extend([text] * weight)
        return random.choice(base)

    header = (
        "This is the thing the character initially believes that they want "
        "or that will make them whole / happy. This is a misguided, incorrect "
        "assumption based on their lie, and pursuing their want STRENGTHENS their lie."
    )

    main_plot = f"{pick_axis(axis1)} towards a {pick_axis(axis2)}"
    subplot1 = f"{pick_axis(axis1)} towards a {pick_axis(axis2)}"
    subplot2 = f"{pick_axis(axis1)} towards a {pick_axis(axis2)}"

    output = []
    output.append(subsection_header("THE WANT"))
    output.append(indent(header))
    output.append("")
    output.append(indent("MAIN PLOT:", 4))
    output.append(indent(main_plot, 8))
    output.append("")
    output.append(indent("SUBPLOT 1:", 4))
    output.append(indent(subplot1, 8))
    output.append("")
    output.append(indent("SUBPLOT 2:", 4))
    output.append(indent(subplot2, 8))
    output.append("")

    return "\n".join(output)

# ==========================================================
# CHARACTER ARC – THE NEED
# ==========================================================

def need():
    return weighted_section(
        "THE NEED",
        [
            ("Accepting of Self", 1),
            ("Trust in others", 1),
            ("Vulnerability as Strength", 1),
            ("Embracing Change", 1),
            ("Emotional Honesty", 1),
            ("Personal Happiness", 1),
            ("Balance between self and others", 1),
            ("Challenge tradition", 1),
            ("Openness to love", 1),
            ("Self-validation", 1)
        ],
        pre_text="What the character actually requires to be complete. Provides a 'personalized anecdote' to their lie. Usually a key realization. Comes later in the story / arc after they pursue the want, achieve it, and realize that they still feel empty. Challenges the status quo of the world.", header_type="subsection"
    )

# ==========================================================
# CHARACTER ARC – THE TRUTH
# ==========================================================

def truth():
    return weighted_section(
        "THE TRUTH",
        [
            ("Worthiness is intrinsic", 1),
            ("Trust builds strength", 1),
            ("Power does not guarantee safety", 1),
            ("Happiness is within reach", 1),
            ("Strength in community", 1),
            ("Change is growth", 1),
            ("Emotions are human", 1),
            ("Self-care is necessary", 1),
            ("Tradition can evolve", 1),
            ("Love is strength", 1)
        ],
        pre_text="Antidote to the lie. The character struggles to accept this. At the climax, the character accepts the truth and vanquishes the lie. This makes the character complete.", header_type="subsection"
    )

def character_arc():
    output = []
    output.append(section_header("CHARACTER ARC"))
    output.append(ghost())
    output.append(lie())
    output.append(want())
    output.append(need())
    output.append(truth())
    return "\n".join(output)




# ==========================================================
# ROOTING INTEREST
# ==========================================================

def rooting_interest():
    return weighted_section(
        "ROOTING INTEREST",
        [
            ("Sympathy: Show how that character has been unjustly punished by the world.", 1),
            ("Skill: Describe what they're excellent at and why it's impressive.", 1),
            ("Personality: Your character has a unique voice, wit, or special way of seeing the world.", 1),
            ("Progression: The character is going to master and learn a skill or craft.", 1),
            ("Worthy Cause: Character is striving for a hard-to-reach ideal.", 1)
        ],
        pre_text="Why the audience roots for the character or stays invested in their journey."
    )

# ==========================================================
# RACE
# ==========================================================

def race():
    return weighted_section("RACE", [

        ("Human", 20),
        ("Orc", 5),
        ("Elf", 7),
        ("Dwarf", 7),
        ("Halfling", 5),
        ("Tiefling", 4),
        ("Gnome", 6),
        ("Half-elf", 4),
        ("Half-orc", 3),
        ("Goblin", 4),
        ("Kenku", 3),
        ("Drow", 4),
        ("Dragonborn", 5),
        ("Doppelganger", 2),
        ("Bugbear", 4),
        ("Goliath", 4),
        ("Ghost", 2),
        ("Sentient Object", 1),
        ("Hag in disguise", 1),
        ("Dragon in disguise", 3),
        ("Demon in disguise", 2)

    ])

# ==========================================================
# AGE & SEX
# ==========================================================

def age_and_sex():
    return weighted_section("AGE & SEX", [

        ("Male child", 1),
        ("Female child", 1),
        ("Male teenager", 1),
        ("Female teenager", 1),
        ("Male adult", 1),
        ("Female adult", 1),
        ("Middle-aged man", 1),
        ("Middle-aged woman", 1),
        ("Old man", 1),
        ("Old woman", 1)

    ])

# ==========================================================
# UNIQUE LOOK
# ==========================================================

def unique_look():
    return weighted_section("UNIQUE LOOK", [

        ("Bad posture", 1),
        ("Bald", 1),
        ("Beautiful", 1),
        ("Big nose or ears", 1),
        ("Cross-eyed", 1),
        ("Pale", 1),
        ("Short", 1),
        ("Tall", 1),
        ("Unique armor", 1),
        ("Unique clothing", 1),
        ("Unique jewelry", 1),
        ("Unique emblem or symbol", 1),
        ("Unusual eye color", 1),
        ("Unusual hair color", 1),
        ("Unusual hair or beard style", 1),
        ("Scar or tattoo", 1),
        ("Multiple scars or tattoos", 1),
        ("Rare item or weapon", 1),
        ("Paralyzed part", 1),
        ("Mechanical part", 1)

    ])

# ==========================================================
# TALENT
# ==========================================================

def talent():
    return weighted_section("TALENT", [

        ("Master of lies", 1),
        ("Appears more clever than he/she is", 1),
        ("Can hide in plain sight", 1),
        ("Can eat enormous amounts of food", 1),
        ("Can outdrink everyone at the table", 1),
        ("Great at creating distractions", 1),
        ("Great memory", 1),
        ("Great at predictions", 1),
        ("Great with animals", 1),
        ("Great at inspiring and motivating people", 1),
        ("Great at hiding his emotions", 1),
        ("Great improvisation skills", 1),
        ("Great with riddles and puzzles", 1),
        ("Great with athletics", 1),
        ("Great at throwing stuff with precision", 1),
        ("Expert salesman", 1),
        ("Expert performer", 1),
        ("Expert painter", 1),
        ("Expert cartographer", 1),
        ("Expert on woodcrafts", 1)

    ])

# ==========================================================
# OCCUPATION
# ==========================================================

def occupation():
    return weighted_section("OCCUPATION", [

        ("Apothecary", 1), ("Armorer", 1), ("Architect", 1),
        ("Apprentice", 1), ("Baker", 1), ("Bandit", 1),
        ("Beggar", 1), ("Blacksmith", 1), ("Brewer", 1),
        ("Busker (Street Performer / Musician)", 1), ("Butcher", 1), ("Camp Follower", 1),
        ("Carpenter", 1), ("Carter (cart and horse to transport goods)", 1),
        ("Cheesemaker", 1), ("Cartographer", 1),
        ("Cook", 1), ("Cobbler", 1),
        ("Costermonger (sells goods, especially fruit and vegetables, from a handcart in the street)", 1),
        ("Court Jester", 1), ("Diplomat", 1), ("Falconer", 1),
        ("Farmer", 1), ("Fishmonger", 1), ("Fletcher", 1), ("Gardener", 1), ("Gravedigger", 1),
        ("Stable Boy", 1), ("Innkeeper", 1),
        ("Jeweler", 1), ("Locksmith", 1), ("Mason", 1),
        ("Merchant", 1), ("Miller", 1), ("Minstrel", 1),
        ("Outlaw", 1),
        ("Page (runs errands and carries messages for high ranking officials)", 1),
        ("Poison Tester", 1),
        ("Peasant", 1), ("Pig farmer", 1), ("Painter", 1),
        ("Ropemaker", 1), ("Sailor", 1), ("Scribe", 1),
        ("Servant", 1), ("Shepherd", 1), ("Skinner", 1),
        ("Soldier", 1), ("Spy", 1),
        ("Squire", 1), ("Storyteller", 1), ("Summoner", 1),
        ("Tailor", 1), ("Tanner", 1), ("Tax collector", 1),
        ("Trader", 1), ("Guard", 1), ("Weaponsmith", 1), ("Winemaker", 1)

    ])

# ==========================================================
# MOTIVATION
# ==========================================================

def motivation():

    options = [

        ("Survival of family member(s) or self", 1),
        ("Protecting the weak", 1),
        ("Enjoying the pleasures of life", 1),
        ("Acquiring money for a reason", 1),
        ("Acquiring fame", 1),
        ("Practicing and improving a skill", 1),
        ("Obsession with a project or goal", 1),
        ("Exploration and adventure", 1),
        ("Discovering the truth about a personal matter", 1),
        ("Gathering knowledge", 1),
        ("Doing a favor", 1),
        ("Fulfilling a last wish", 1),
        ("Fulfilling a prophecy", 1),
        ("Staying loyal to a promise or deal", 1),
        ("Love", 1),
        ("Exacting revenge", 1),
        ("Killing a specific person or group", 1),
        ("Enjoying the suffering of others", 1),
        ("Changing the world", 1)

    ]

    first = weighted_section("MOTIVATION", options)

    # 10% chance to add a second motivation
    if random.randint(1, 10) == 10:
        second_pool = [opt for opt in options if opt[0] != first]
        second = weighted_section("SECONDARY MOTIVATION", second_pool)
        result = f"{first} AND {second}"
    else:
        result = first

    output = []
    output.append((result))
    output.append("")

    return "\n".join(output)

# ==========================================================
# SECRET
# ==========================================================

def secret():
    return weighted_section("SECRET", [

        ("Has committed a crime no one knows about", 1),
        ("Has a secret affair", 1),
        ("Has a secret goal", 1),
        ("Has a secret pleasure", 1),
        ("Has a double life", 1),
        ("Has an incurable illness", 1),
        ("Has a special magical power or curse", 1),
        ("Owes a lot of money", 1),
        ("Is a member of an organization", 1),
        ("Is afraid of a certain person or group", 1),
        ("Hates his/her family", 1),
        ("Is jealous of a specific person", 1),
        ("Has a pet no one knows about", 1),
        ("Has a magic item no one knows about", 1),
        ("Has hidden a treasure in his/her house", 1),
        ("Has a patron no one knows about", 1),
        ("Has origins in a noble family", 1),
        ("Uses a fake name", 1),
        ("Has a bounty on his/her head", 1),
        ("Has died in the past", 1)

    ])

# ==========================================================
# FLAW
# ==========================================================

def flaw():
    return weighted_section("FLAW", [

        ("Tries to please everyone", 1),
        ("Has low self-esteem", 1),
        ("Gets anxious in big crowds", 1),
        ("Can easily be manipulated", 1),
        ("Can't hide his/her emotions", 1),
        ("Can't express his/her emotions", 1),
        ("Can't resist good food", 1),
        ("Drinks too much", 1),
        ("Sleeps heavily and too much", 1),
        ("Is obsessed with money/fame", 1),
        ("Is always late", 1),
        ("Gets easily tired with any physical activity", 1),
        ("Gets sick easily", 1),
        ("Has nausea when using any means of transport", 1),
        ("Has a weird phobia", 1),
        ("Has a weird allergy", 1),
        ("Has poor eyesight", 1),
        ("Has poor hearing", 1),
        ("Has trouble sleeping", 1),
        ("Walks in his/her sleep", 1)

    ])

# ==========================================================
# QUIRK
# ==========================================================

def quirk():
    return weighted_section("QUIRK", [

        ("Walks slowly", 1),
        ("Walks fast", 1),
        ("Speaks loudly", 1),
        ("Speaks quietly", 1),
        ("Speaks slowly", 1),
        ("Speaks fast", 1),
        ("Speaks in riddles", 1),
        ("Stutters", 1),
        ("Mumbles to himself/herself", 1),
        ("Has a unique accent", 1),
        ("Uses complex vocabulary", 1),
        ("Dances or sings often", 1),
        ("Stretches often", 1),
        ("Coughs often", 1),
        ("Gets distracted easily", 1),
        ("Falls asleep at inappropriate moments", 1),
        ("Forgets names", 1),
        ("Repeats ideas as his/her own", 1),
        ("Doesn't like a particular member of the group", 1),
        ("Really likes a particular member of the group", 1)

    ])

# ==========================================================
# ATTITUDE
# ==========================================================

def attitude():
    return weighted_section("ATTITUDE", [

        ("Annoyed", 1),
        ("Annoying", 1),
        ("Competitive", 1),
        ("Curious", 1),
        ("Excited", 1),
        ("Friendly", 1),
        ("Generous", 1),
        ("Greedy", 1),
        ("Happy", 1),
        ("Helpful", 1),
        ("Humorous", 1),
        ("Impatient", 1),
        ("Liar", 1),
        ("Nervous", 1),
        ("Patient", 1),
        ("Proud", 1),
        ("Kind", 1),
        ("Rude", 1),
        ("Sad", 1),
        ("Scared", 1),
        ("Serious", 1),
        ("Short-tempered", 1),
        ("Shy", 1),
        ("Stubborn", 1),
        ("Suspicious", 1),
        ("Unhelpful", 1)

    ])

# ==========================================================
# SUPERPOWER
# ==========================================================

def superpower():
    return weighted_section("SUPERPOWER", [

        ("Can mimic any sound with his/her voice", 1),
        ("Has unbelievable luck", 1),
        ("Can run incredibly fast", 1),
        ("Has superhuman strength", 1),
        ("Has phenomenal perception", 1),
        ("Becomes more powerful when drunk", 1),
        ("Can speak with gods", 1),
        ("Can summon a powerful beast or spirit", 1),
        ("Has immunity to a certain element", 1),
        ("Can manipulate a specific element", 1),
        ("Can control the weather", 1),
        ("His/her sight blocks all magic", 1),
        ("Can pass through walls", 1),
        ("Can't be harmed by normal weapons", 1),
        ("Has great regenerative powers", 1),
        ("Can predict the future", 1),
        ("Can stop time", 1),
        ("Can travel in time", 1),
        ("Can shapeshift into a powerful beast or demon", 1),
        ("Can manipulate and control minds", 1)

    ])

# ==========================================================
# THE FOUR SELVES
# ==========================================================

def social_self():
    return weighted_section("SOCIAL SELF", [
        ("An odd but wealthy person who loves to throw big parties and tell everyone wild tales of past adventures.",1),
        ("A battle-scarred warrior with a fearsome reputation that makes people uneasy around them.",1),
        ("A stern, unforgiving teacher who openly favors some and intimidates others.",1),
        ("A charismatic leader who inspires people with confidence and charm.",1),
        ("A quiet, unremarkable person who blends into the background and doesn't share much about themselves.",1),
        ("A charming trickster with a sly grin, always ready with a joke and a clever comment.",1),
        ("A strict, no-nonsense person who always follows the rules and expects others to do the same.",1),
        ("A friendly, outgoing person who greets everyone like an old friend.",1),
        ("A cold, distant loner who keeps conversations short and avoids getting personal.",1),
        ("A polite, well-mannered individual who always follows proper social rules.",1),
        ("An oddball with weird habits that others find strange but somehow endearing.",1),
        ("A smooth-talking charmer who can get along with anyone, yet reveals almost nothing about their own life.",1),
        ("A carefree jokester who never seems to take anything seriously, always ready with a laugh.",1),
        ("A mysterious stranger who says very little, making everyone curious but giving away no answers.",1)
    ],header_type="subsection")


def personal_self():
    return weighted_section("PERSONAL SELF", [
        ("They are a brave and caring friend who will go to great lengths to protect the people they love.",1),
        ("Relaxed and playful around those they trust, they show a sense of humor and warmth not seen by outsiders.",1),
        ("They can be quick to get angry and brutally honest with close friends, but they are also fiercely loyal to them.",1),
        ("They are gentle and nurturing with family, always putting loved ones' needs first.",1),
        ("Even with friends, they stay quiet and guarded, but occasionally their deep kindness shines through.",1),
        ("They are goofy and lighthearted in private.",1),
        ("They are deeply loyal, willing to sacrifice for those they love.",1),
        ("They are a good listener for their closest friends.",1),
        ("They show more vulnerability with those they care about.",1),
        ("They can be overprotective of their family.",1),
        ("They remain optimistic and encouraging around loved ones.",1),
        ("They are surprisingly gentle with their inner circle.",1),
        ("They share their hopes and fears only with their most trusted friends.",1)
    ],header_type="subsection")

def core_self():
    return weighted_section("CORE SELF", [
        ("Deep down, they feel weary from all they've been through.",1),
        ("They are determined to make up for a terrible mistake in their past.",1),
        ("They believe they are destined for greatness.",1),
        ("They wonder if anything they do really matters.",1),
        ("They see themselves as a monster and can't forgive themselves.",1),
        ("They believe their toughness defines them.",1),
        ("They hold onto a hopeful vision of a better future.",1),
        ("They secretly feel like a fraud.",1),
        ("They seek to understand how the world works.",1),
        ("They define themselves as a protector.",1),
        ("They still ache from a great loss.",1),
        ("They see themselves as a champion of freedom.",1),
        ("They feel completely lost about who they truly are.",1),
        ("They feel cursed by their own abilities or nature.",1)
    ],header_type="subsection")

def hidden_self():
    return weighted_section("HIDDEN SELF", [
        ("They desperately crave approval even though they act independent.",1),
        ("A deep fear influences many of their choices.",1),
        ("In extreme danger, a merciless side takes over.",1),
        ("They possess a hidden talent they haven't discovered.",1),
        ("They suppress a dark urge inside them.",1),
        ("Underneath their exterior is a kind heart they haven't noticed.",1),
        ("An old childhood hurt shapes their fears.",1),
        ("When truly pressed, unexpected courage emerges.",1),
        ("They sabotage their own happiness.",1),
        ("They could become the very thing they fear.",1),
        ("Their family background hides a powerful secret.",1),
        ("They long for something they believe they can never have.",1)
    ],header_type="subsection")



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
    character.append(race())
    character.append(age_and_sex())
    character.append(unique_look())
    character.append(piety())
    character.append(section_header("THE FOUR SELVES"))
    character.append(social_self())
    character.append(personal_self())
    character.append(core_self())
    character.append(hidden_self())


#OTHERS / BACKGROUND
    character.append(siblings())
    character.append(occupation())

#ADDITIONAL TIDBITS
    character.append(talent())
    character.append(flaw())
    character.append(quirk())
    character.append(secret())
    character.append(superpower())

#AS A PERSON
    character.append(attitude())
    character.append(temperament())
    character.append(disposition())
    character.append(virtues_and_vices())

#WHY DO WE CARE
    character.append(motivation())
    character.append(rooting_interest())
    character.append(character_arc())

# Save to file
    filename = "GeneratedCharacter.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for entry in character:
            f.write(entry + "\n")

    print(f"Character saved to {filename}")
# ==========================================================

if __name__ == "__main__":
    main()
