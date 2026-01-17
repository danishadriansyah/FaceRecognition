"""
Teachable Machine Face Recognizer Module
Week 8 Final Project - Teachable Machine Integration

This module provides face recognition using Teachable Machine Keras models.
Integrates custom trained models from Google Teachable Machine platform.
"""

import numpy as np
import cv2
import os
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import tensorflow as tf
from tensorflow import keras


class TeachableMachineRecognizer:
    """
    Face recognition using Teachable Machine Keras model
    Supports image classification from Google Teachable Machine
    """
    
    def __init__(self, model_path: str, labels_path: str, confidence_threshold: float = 0.7):
        """
        Initialize Teachable Machine recognizer
        
        Args:
            model_path: Path to keras_model.h5
            labels_path: Path to labels.txt
            confidence_threshold: Minimum confidence for recognition (default 0.7)
        """
        self.model_path = Path(model_path)
        self.labels_path = Path(labels_path)
        self.confidence_threshold = confidence_threshold
        
        # Load Keras model
        try:
            self.model = keras.models.load_model(self.model_path, compile=False)
            print(f"✅ Teachable Machine model loaded: {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
        
        # Load labels
        self.class_names = self._load_labels()
        print(f"✅ Loaded {len(self.class_names)} classes: {', '.join(self.class_names)}")
        
        # Model expects 224x224x3 input (standard Teachable Machine format)
        self.input_size = (224, 224)
        
        print(f"✅ TeachableMachineRecognizer initialized")
        print(f"   Input size: {self.input_size}")
        print(f"   Confidence threshold: {confidence_threshold}")
    
    def _load_labels(self) -> List[str]:
        """Load class labels from labels.txt"""
        labels = []
        try:
            with open(self.labels_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Format: "0 ClassName" or just "ClassName"
                    line = line.strip()
                    if line:
                        # Remove leading number if present
                        parts = line.split(maxsplit=1)
                        if len(parts) == 2 and parts[0].isdigit():
                            labels.append(parts[1])
                        else:
                            labels.append(line)
        except Exception as e:
            raise RuntimeError(f"Failed to load labels: {e}")
        
        return labels
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for Teachable Machine model
        
        Args:
            image: Input image (BGR format from OpenCV)
            
        Returns:
            Preprocessed image ready for model input
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size (224x224)
        resized = cv2.resize(rgb_image, self.input_size, interpolation=cv2.INTER_AREA)
        
        # Normalize to [0, 1] range
        normalized = resized.astype(np.float32) / 255.0
        
        # Add batch dimension
        batch = np.expand_dims(normalized, axis=0)
        
        return batch
    
    def recognize_face(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Tuple[Optional[str], float]:
        """
        Recognize person from face image using Teachable Machine model
        
        Args:
            image: Input image (BGR format from OpenCV)
            face_location: Optional face location (x, y, w, h) - if provided, crops to face region
            
        Returns:
            Tuple of (person_name, confidence) or (None, 0.0) if no match
        """
        try:
            # Crop face region if location provided
            if face_location is not None:
                x, y, w, h = face_location
                face_crop = image[y:y+h, x:x+w]
            else:
                face_crop = image
            
            # Check if image is valid
            if face_crop.size == 0:
                return None, 0.0
            
            # Preprocess image
            preprocessed = self.preprocess_image(face_crop)
            
            # Run prediction
            predictions = self.model.predict(preprocessed, verbose=0)
            
            # Get class with highest confidence
            class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][class_index])
            
            # Check if confidence meets threshold
            if confidence >= self.confidence_threshold:
                person_name = self.class_names[class_index]
                return person_name, confidence
            else:
                return None, confidence
                
        except Exception as e:
            print(f"⚠️  Recognition failed: {e}")
            return None, 0.0
    
    def recognize_faces_batch(self, images: List[np.ndarray]) -> List[Tuple[Optional[str], float]]:
        """
        Recognize multiple faces in batch
        
        Args:
            images: List of face images (BGR format)
            
        Returns:
            List of (person_name, confidence) tuples
        """
        results = []
        for image in images:
            result = self.recognize_face(image)
            results.append(result)
        return results
    
    def get_all_predictions(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Dict[str, float]:
        """
        Get confidence scores for all classes
        
        Args:
            image: Input image (BGR format from OpenCV)
            face_location: Optional face location (x, y, w, h)
            
        Returns:
            Dictionary mapping class names to confidence scores
        """
        try:
            # Crop face region if location provided
            if face_location is not None:
                x, y, w, h = face_location
                face_crop = image[y:y+h, x:x+w]
            else:
                face_crop = image
            
            # Check if image is valid
            if face_crop.size == 0:
                return {}
            
            # Preprocess image
            preprocessed = self.preprocess_image(face_crop)
            
            # Run prediction
            predictions = self.model.predict(preprocessed, verbose=0)
            
            # Create dictionary of all predictions
            result = {}
            for i, class_name in enumerate(self.class_names):
                result[class_name] = float(predictions[0][i])
            
            return result
            
        except Exception as e:
            print(f"⚠️  Prediction failed: {e}")
            return {}
    
    def update_confidence_threshold(self, new_threshold: float):
        """Update confidence threshold"""
        self.confidence_threshold = new_threshold
        print(f"✅ Confidence threshold updated to {new_threshold}")
    
    def get_model_info(self) -> Dict[str, any]:
        """Get model information"""
        return {
            'model_path': str(self.model_path),
            'labels_path': str(self.labels_path),
            'num_classes': len(self.class_names),
            'classes': self.class_names,
            'input_size': self.input_size,
            'confidence_threshold': self.confidence_threshold
        }


def main():
    """Test the Teachable Machine recognizer"""
    import sys
    
    # Setup paths
    current_dir = Path(__file__).parent
    models_dir = current_dir.parent / 'models'
    model_path = models_dir / 'keras_model.h5'
    labels_path = models_dir / 'labels.txt'
    
    # Check if model exists
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        print("Please ensure keras_model.h5 is in project/models/")
        sys.exit(1)
    
    if not labels_path.exists():
        print(f"❌ Labels not found: {labels_path}")
        print("Please ensure labels.txt is in project/models/")
        sys.exit(1)
    
    # Initialize recognizer
    print("\n" + "="*60)
    print("Testing Teachable Machine Recognizer")
    print("="*60 + "\n")
    
    recognizer = TeachableMachineRecognizer(
        model_path=str(model_path),
        labels_path=str(labels_path),
        confidence_threshold=0.7
    )
    
    # Print model info
    print("\n" + "="*60)
    print("Model Information:")
    print("="*60)
    info = recognizer.get_model_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Test with webcam
    print("\n" + "="*60)
    print("Testing with Webcam")
    print("="*60)
    print("Press 'q' to quit, 'space' to capture and recognize")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        sys.exit(1)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Display frame
        display_frame = frame.copy()
        cv2.putText(display_frame, "Press SPACE to recognize", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Teachable Machine Test', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            # Recognize
            print("\n🔍 Recognizing...")
            name, confidence = recognizer.recognize_face(frame)
            
            if name:
                print(f"✅ Recognized: {name} (confidence: {confidence:.2%})")
                
                # Show all predictions
                all_preds = recognizer.get_all_predictions(frame)
                print("\nAll predictions:")
                for class_name, conf in sorted(all_preds.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {class_name}: {conf:.2%}")
            else:
                print(f"❌ No match (max confidence: {confidence:.2%})")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Test completed")


if __name__ == "__main__":
    main()
