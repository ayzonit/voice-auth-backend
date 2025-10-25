import torch
import os
from App.models.architectures import SpeakerEmbeddingModel, SpoofDetectionModel
from App.config import SPEAKER_MODEL_PATH, SPOOF_MODEL_PATH
from App.core.logger import logger

def load_models():
    try:
        speaker_model = SpeakerEmbeddingModel(input_dim=59, embedding_dim=128)
        spoof_model = SpoofDetectionModel(input_dim=59)
        
        if os.path.exists(SPEAKER_MODEL_PATH):
            speaker_model.load_state_dict(torch.load(SPEAKER_MODEL_PATH, map_location='cpu'))
            logger.info(f"Loaded speaker model from {SPEAKER_MODEL_PATH}")
        else:
            logger.warning(f"Speaker model not found. Using untrained model.")
            os.makedirs(os.path.dirname(SPEAKER_MODEL_PATH), exist_ok=True)
            
        if os.path.exists(SPOOF_MODEL_PATH):
            spoof_model.load_state_dict(torch.load(SPOOF_MODEL_PATH, map_location='cpu'))
            logger.info(f"Loaded spoof model from {SPOOF_MODEL_PATH}")
        else:
            logger.warning(f"Spoof model not found. Using untrained model.")
            os.makedirs(os.path.dirname(SPOOF_MODEL_PATH), exist_ok=True)
        
        speaker_model.eval()
        spoof_model.eval()
        
        return speaker_model, spoof_model
        
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise