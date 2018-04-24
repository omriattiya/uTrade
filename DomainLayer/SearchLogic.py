from DatabaseLayer import Items, Shops
from pattern.en import spelling

def search_by_name(item_name):
    if item_name is not None:
        return Items.search_items_by_name(item_name)
    else:
        return False


def search_shop(shop_name):
    if shop_name is not None:
        return Shops.search_shop(shop_name)


def search_item_in_shop(shop_name, item_name):
    if item_name is not None:
        if shop_name is not None:
            return Items.search_item_in_shop(shop_name, item_name)
    else:
        return False


def search_items_in_shop(shop_name):
    if shop_name is not None:
        return Items.search_items_in_shop(shop_name)
    else:
        return False


def search_by_category(item_category):
    if item_category is not None:
        return Items.search_items_by_category(item_category)


def search_by_keywords(item_keywords):
    if item_keywords is not None:
        keywords_array = item_keywords.replace(';', ' ')
        return Items.search_items_by_keywords(keywords_array)



def signature(s):
    """Returns the signature of this string, which is a string
    that contains all of the letters in order.
    """
    t = list(s)
    t.sort()
    t = ''.join(t)
    return t


def all_anagrams(filename):
    """Finds all anagrams in a list of words.

    filename: string filename of the word list

    Returns: a map from each word to a list of its anagrams.
    """
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)

        if t not in d:
            d[t] = [word]
        else:
            d[t].append(word)
    return d




def metathesis_pairs(d):
    """Print all pairs of words that differ by swapping two letters.

    d: map from word to list of anagrams
    """
    for anagrams in d.values():
        for word1 in anagrams:
            for word2 in anagrams:
                if word1 < word2 and word_distance(word1, word2) == 2:
                    print(word1, word2)

def word_distance(word1, word2):
    """Computes the number of differences between two words.

    word1, word2: strings

    Returns: integer
    """
    assert len(word1) == len(word2)

    count = 0
    for c1, c2 in zip(word1, word2):
        if c1 != c2:
            count += 1

    return count


def get_similar_words(word):
    sets = all_anagrams(word)
    metathesis_pairs(sets)
