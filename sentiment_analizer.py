import pickle

class Model:
    def __init__(self) -> None:
        model_file_name = "C:\\Users\\Kevin Igweh\Documents\\AI Project\\AI project\\sentiment_analyzer"
        self.model = pickle.load(open(model_file_name, 'rb'))

    
    def predict_text(self, text):
        prediction = self.model.predict([text])[0]
        return prediction
        

class ObjModel:
    def __init__(self) -> None:
        obj_model_file_name = "C:\\Users\\Kevin Igweh\\Documents\\AI Project\\AI project\\objectivity_analyzer"
        self.model_objectivity = pickle.load(open(obj_model_file_name, 'rb'))

    def predict(self, text):
        prediction = self.model_objectivity.predict([text])[0]
        return prediction
