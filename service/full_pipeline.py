import os
from catboost import CatBoostClassifier
import pandas as pd

from audio2text import audio2text, convert_video_to_audio
from bert import getPredictBert
from xclip_extractor import myFeatureExtractor


def is_audio_file(filepath):
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']
    _, ext = os.path.splitext(filepath)
    return ext.lower() in audio_extensions


def is_video_file(filepath):
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mpeg', '.mpg', '.wbm']
    _, ext = os.path.splitext(filepath)
    return ext.lower() in video_extensions


id2label = {0: 'Промо/Нет/Нет',
            1: 'Имидж/Нет/Нет',
            2: 'Имидж/Нет/Да',
            3: 'Промо/Доставка/Нет',
            4: 'Промо/Нет/Да',
            5: 'Имидж/Доставка/Нет',
            7: 'Имидж',
            8: 'Кредитование',
            9: 'Range',
            10: 'Дебетовые карты',
            11: 'Услуги бизнесу',
            12: 'Кредитные карты',
            13: 'Инвестиционные продукты',
            14: 'Экосистемные сервисы',
            15: 'Музыка',
            16: 'Колонки+Голосовой помощник',
            17: 'Клипы',
            18: 'Соц сети'}


cb_model = CatBoostClassifier()
cb_model.load_model('service/cb')


def full_pipeline(file):
    if is_audio_file(file):
        extracted_text = audio2text(file)
        num_class = getPredictBert(extracted_text)
        pred = id2label[num_class]
        return pred
    elif is_video_file(file):
        audio = convert_video_to_audio(file)
        extracted_text = audio2text(audio)
        if 'субтитры' in extracted_text.lower() or 'динамичная' in extracted_text.lower() or len(extracted_text) < 3:
            features = myFeatureExtractor(file).cpu().flatten().numpy()
            names = [f'array_feature_{i}' for i in range(512)]
            df = pd.Series(features, names)
            num_class = cb_model.predict(df)[0]
            pred = id2label[num_class]
            return pred
        else:
            num_class = getPredictBert(extracted_text)
            pred = id2label[num_class]
            return pred
    else:
        return None
