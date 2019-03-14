from string import digits

from big_phoney import PredictionModel, PhoneticDictionary

pred_model = PredictionModel()
phonetic_dict = PhoneticDictionary()
remove_digits = str.maketrans('', '', digits)  # Remove digits from big_phoney's results


def lookup_or_predict(word):
    """
    Lookup an english word's phonetics using big_phoney.
    If not found, predict the phonetics as the ARPAbet classified
     using big_phoney.PredictionModel
    :param word:
    :return:
    """
    result = phonetic_dict.lookup(word)
    if result is not None:
        return result.translate(remove_digits).split(' ')
    result = pred_model.predict(word)
    return result.translate(remove_digits).split(' ')
