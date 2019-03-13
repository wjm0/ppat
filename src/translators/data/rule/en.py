from big_phoney import PredictionModel, PhoneticDictionary


pred_model = PredictionModel()
phonetic_dict = PhoneticDictionary()


def predict(word):
    """
    Transform an english word into phonetics as the ARPAbet classified.
    Using big_phoney.PredictionModel
    :param word:
    :return:
    """
    result = pred_model.predict(word)
    if result is not None:
        return result
    return ''


def lookup(word):
    """
    Lookup an english word's phonetics using big_phoney.
    :param word:
    :return:
    """
    result = phonetic_dict.lookup(word)
    if result is not None:
        return result
    return ''
