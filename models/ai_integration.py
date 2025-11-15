from .train_and_load import ensure_models_exist
from .fishing_model import predict_fishing
from .disaster_model import predict_disaster

def build_all_if_missing():
    ensure_models_exist()
