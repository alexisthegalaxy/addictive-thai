from all import All


def get_city_words(al: All):
    return {
        "คน": {
            "map": al.mas.chaiyaphum,
            "x": 800,
            "y": 711,
        },
        "ดี": {
            "map": al.mas.chumphae,
            "x": 818,
            "y": 622,
        },
        "ดู": {
            "map": al.mas.lomsak,
            "x": 818,
            "y": 622,
        },
        "ใจ": {
            "map": al.mas.lomsak,
            "x": 669,
            "y": 618,
        },
        "ยิน": {
            "map": al.mas.kasetsombum,
            "x": 790,
            "y": 655,
        },
    }


AGGREGATES = [
    {
        "english": "good person/darling, honey",
        "thai": "คน_ดี",
        "words": ["คน", "ดี"],
    },
    {
        "english": "audience, spectator, onlooker",
        "thai": "คน_ดู",
        "words": ["คน", "ดู"],
    },
    {
        "english": "to look good",
        "thai": "ดู_ดี",
        "words": ["ดู", "ดี"],
    },
    {
        "english": "to be nice",
        "thai": "ใจ_ดี",
        "words": ["ใจ", "ดี"],
    },
    {
        "english": "to be glad",
        "thai": "ยิน_ดี",
        "words": ["ยิน", "ดี"],
    },
]


def get_links_from_city_word(current_word: str, al: All):
    city_words = get_city_words(al)
    near_city_words = []
    for aggregate in AGGREGATES:
        if current_word in aggregate["words"]:
            for word in aggregate["words"]:
                if word != current_word:
                    near_city_words.append({
                        "english": aggregate["english"],
                        "thai": aggregate["thai"],
                        "words": aggregate["words"],
                        "city": city_words[word],
                    })
    # al.aggregates = near_city_words
    for near_city_word in near_city_words:
        print(near_city_word)
