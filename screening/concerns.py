import re


PROBLEM_LIST = [

    (
        "milestones",
        "Delayed milestones",
        "The child is slow to learn skills like holding the head up, "
        "sitting, crawling, standing or walking."
    ),

    (
        "speech",
        "Speech delay or unclear speech",
        "The child speaks late, says few words, or is hard to "
        "understand for their age."
    ),

    (
        "attention",
        "Poor attention",
        "The child is easily distracted and cannot stay with one "
        "activity for long."
    ),

    (
        "balance",
        "Poor balance or posture",
        "The child is unsteady, falls easily, slumps, or finds it "
        "hard to keep the body upright."
    ),

    (
        "finemotor",
        "Poor hand and finger skills",
        "The child finds it hard to hold a spoon, crayon or small "
        "objects, or to use both hands together."
    ),

    (
        "hyper",
        "Very active or restless",
        "The child cannot sit still and is always moving, running "
        "or climbing."
    ),

    (
        "lowtone",
        "Floppy or weak body",
        "The child's body feels loose or soft, and the child tires "
        "easily."
    ),

    (
        "eye",
        "Poor eye contact",
        "The child rarely looks at your face or eyes when you talk "
        "or play."
    ),

    (
        "hightone",
        "Stiff body",
        "The child's arms or legs feel tight or stiff and are hard "
        "to move or bend."
    ),

    (
        "social",
        "Difficulty playing or mixing with others",
        "The child does not play with, or respond to, other "
        "children or people."
    ),

    (
        "adl",
        "Needs a lot of help with daily tasks",
        "The child needs more help than expected with eating, "
        "dressing, toileting or washing."
    ),

    (
        "drool",
        "Drooling",
        "Saliva often runs out of the mouth, more than expected "
        "for the child's age."
    ),

    (
        "weak",
        "Weak arms or legs",
        "The child's arms or legs seem weak, or one side is used "
        "less than the other."
    ),

    (
        "tantrum",
        "Frequent tantrums",
        "Strong outbursts of crying, screaming or anger that are "
        "hard to calm."
    ),

    (
        "tactile",
        "Strong reaction to touch",
        "The child dislikes certain clothes, textures, messy play "
        "or being touched."
    ),

    (
        "repetitive",
        "Repeated movements or sounds",
        "The child repeats actions such as hand flapping, rocking, "
        "spinning or repeats words again and again."
    ),

    (
        "tiptoe",
        "Walking on tiptoes",
        "The child often walks on the toes instead of the whole foot."
    ),

    (
        "impuls",
        "Acts without thinking",
        "The child acts very quickly, interrupts, or finds it hard "
        "to wait."
    ),

    (
        "regress",
        "Lost skills",
        "The child could do something before, like say a word or "
        "make a movement, but has stopped doing it."
    ),

    (
        "feeding",
        "Feeding difficulty",
        "The child has trouble chewing, swallowing or accepting "
        "some foods."
    ),

    (
        "sound",
        "Strong reaction to sounds",
        "The child covers the ears, gets upset by noise, or does "
        "not seem to respond to sounds."
    ),

    (
        "sleep",
        "Poor sleep",
        "The child has trouble falling asleep or staying asleep."
    ),

    (
        "fits",
        "Fits (convulsions)",
        "Sudden shaking of the body, sometimes with loss of "
        "awareness."
    )
]


PROBLEM_NAMES = {
    key: name
    for key, name, meaning in PROBLEM_LIST
}


PROBLEM_KEYWORDS = {

    "milestones":
        r"milestone|ddm|developmental delay|delayed (in )?walking|not (yet )?(sitting|crawling|walking|standing)|head control",

    "speech":
        r"speech|speak|talk|words|language|articulat|non.?verbal|babbl",

    "attention":
        r"attention|concentrat|distract|focus",

    "balance":
        r"balance|postur|trunk|unsteady|falls|coordination",

    "finemotor":
        r"fine motor|hand function|grasp|writing|holding",

    "hyper":
        r"hyperactiv|restless",

    "lowtone":
        r"low (muscle )?tone|floppy|hypotoni",

    "eye":
        r"eye contact",

    "hightone":
        r"high (muscle )?tone|stiff|spastic|hypertoni",

    "social":
        r"social|interact|play with",

    "adl":
        r"adl|potty|toilet|dressing|bathing|self.?care",

    "drool":
        r"drool|drull|saliva",

    "weak":
        r"weak",

    "tantrum":
        r"tantrum|aggress|meltdown",

    "tactile":
        r"tactile|touch|texture|defensive",

    "repetitive":
        r"mannerism|stimming|flapping|rocking|head banging|echolalia|spinning",

    "tiptoe":
        r"tip.?toe|toe walking",

    "impuls":
        r"impulsiv",

    "regress":
        r"regress|lost (a )?skill|stopped (talking|walking|speaking)",

    "feeding":
        r"feeding|chew|swallow|picky",

    "sound":
        r"auditory|noise|loud sound",

    "sleep":
        r"sleep",

    "fits":
        r"convuls|seizure|\bfits?\b|epilep"
}


def match_problem_keywords(text):

    text = str(text).lower()

    return {
        key
        for key, pattern in PROBLEM_KEYWORDS.items()
        if re.search(pattern, text)
    }


PROBLEM_SCORE_NEEDED = 2


PROBLEM_SUPPORT = {

    "speech": {
        "Speech Delay": 2
    },

    "milestones": {
        "Developmental Delay": 2
    },

    "hightone": {
        "CP": 2
    },

    "drool": {
        "CP": 1
    },

    "weak": {
        "CP": 1,
        "Developmental Delay": 1
    },

    "balance": {
        "CP": 1,
        "Developmental Delay": 1
    },

    "tiptoe": {
        "CP": 1,
        "ASD": 1
    },

    "lowtone": {
        "Developmental Delay": 1
    },

    "finemotor": {
        "Developmental Delay": 1
    },

    "adl": {
        "Developmental Delay": 1
    },

    "feeding": {
        "Developmental Delay": 1
    },

    "hyper": {
        "ADHD": 1
    },

    "attention": {
        "ADHD": 1
    },

    "impuls": {
        "ADHD": 1
    },

    "eye": {
        "ASD": 1
    },

    "social": {
        "ASD": 1
    },

    "repetitive": {
        "ASD": 1
    },

    "tantrum": {
        "ASD": 1
    },

    "tactile": {
        "ASD": 1
    },

    "sound": {
        "ASD": 1
    },

    "sleep": {
        "ASD": 1
    }
}


PROBLEM_IMPRESSION_NAMES = {

    "CP":
        "Cerebral Palsy",

    "ASD":
        "Autism Spectrum Disorder",

    "ADHD":
        "Attention-Deficit/Hyperactivity Disorder",

    "Speech Delay":
        "Delayed Speech",

    "Developmental Delay":
        "Developmental Delay",

    "Hemiplegia":
        "Hemiplegia",

    "Down Syndrome":
        "Down Syndrome"
}
