"""
Encoding Generator: Generate face encodings using DeepFace
Converts face images to 512-dimensional embeddings
"""
import numpy as np
import pickle
from deepface import DeepFace
import cv2
import time

class EncodingGenerator:
    """Generate face encodings dengan DeepFace"""
    
    def __init__(self, model_name='Facenet512'):
        """
        Initialize encoding generator
        
        Args:
            model_name: DeepFace model to use
                - Facenet512 (default): 512-d, 97% accuracy, medium speed
                - ArcFace: 512-d, 99% accuracy, slower
                - SFace: 128-d, 95% accuracy, faster
                - VGG-Face: 4096-d, 95% accuracy, slow
        """
        self.model_name = model_name
        print(f"🔧 Loading DeepFace model: {model_name}")
        
        # Pre-load model (first call downloads ~100MB model)
        try:
            # Dummy call to load model
            dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)
            DeepFace.represent(
                dummy_img, 
                model_name=model_name,
                enforce_detection=False
            )
            print(f"✅ Model loaded! (size: {self._get_embedding_size()}-d embeddings)")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            raise
    
    def _get_embedding_size(self):
        """Get embedding dimension for the model"""
        sizes = {
            'Facenet512': 512,
            'ArcFace': 512,
            'SFace': 128,
            'VGG-Face': 4096,
            'Facenet': 128
        }
        return sizes.get(self.model_name, 512)
    
    def generate_encoding(self, image_path):
        """
        Generate face encoding from image file
        
        Args:
            image_path: Path to face image
            
        Returns:
            tuple: (encoding_array, generation_time)
        """
        start_time = time.time()
        
        try:
            # Generate embedding
            result = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                enforce_detection=False  # We already detected faces in Week 2
            )
            
            # Extract embedding (DeepFace returns list of dicts)
            if isinstance(result, list) and len(result) > 0:
                encoding = np.array(result[0]['embedding'], dtype=np.float32)
            else:
                encoding = np.array(result['embedding'], dtype=np.float32)
            
            elapsed_time = time.time() - start_time
            
            return encoding, elapsed_time
            
        except Exception as e:
            print(f"❌ Error generating encoding: {e}")
            return None, 0
    
    def generate_from_image_array(self, image_array):
        """
        Generate encoding from numpy array (for webcam frames)
        
        Args:
            image_array: numpy array (BGR format from OpenCV)
            
        Returns:
            numpy array: Face encoding
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            
            result = DeepFace.represent(
                img_path=rgb_image,
                model_name=self.model_name,
                enforce_detection=False
            )
            
            if isinstance(result, list) and len(result) > 0:
                encoding = np.array(result[0]['embedding'], dtype=np.float32)
            else:
                encoding = np.array(result['embedding'], dtype=np.float32)
            
            return encoding
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def serialize_encoding(self, encoding):
        """Convert numpy array to bytes for database storage"""
        return pickle.dumps(encoding)
    
    def deserialize_encoding(self, encoding_bytes):
        """Convert bytes back to numpy array"""
        return pickle.loads(encoding_bytes)
    
    def compare_encodings(self, encoding1, encoding2, threshold=0.6):
        """
        Compare two face encodings
        
        Args:
            encoding1: First encoding
            encoding2: Second encoding
            threshold: Distance threshold (lower = more similar)
                - 0.6: Default (good balance)
                - 0.4: Strict (fewer false positives)
                - 0.8: Lenient (more matches)
        
        Returns:
            tuple: (is_match, distance, confidence)
        """
        # Calculate Euclidean distance
        distance = np.linalg.norm(encoding1 - encoding2)
        
        # Check if match
        is_match = distance <= threshold
        
        # Calculate confidence (0-100%)
        # Lower distance = higher confidence
        confidence = max(0, min(100, (1 - distance) * 100))
        
        return is_match, distance, confidence


def test_encoding_generator():
    """Test encoding generator"""
    print("="*60)
    print("TEST: Encoding Generator")
    print("="*60)
    
    # Initialize
    generator = EncodingGenerator(model_name='Facenet512')
    
    # Test with dummy image
    print("\nCreating test image...")
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    print("Generating encoding from array...")
    encoding = generator.generate_from_image_array(test_image)
    
    if encoding is not None:
        print(f"✅ Encoding generated!")
        print(f"   Shape: {encoding.shape}")
        print(f"   Type: {encoding.dtype}")
        print(f"   Sample values: {encoding[:5]}")
        
        # Test serialization
        print("\nTesting serialization...")
        encoding_bytes = generator.serialize_encoding(encoding)
        print(f"✅ Serialized: {len(encoding_bytes)} bytes")
        
        decoded = generator.deserialize_encoding(encoding_bytes)
        print(f"✅ Deserialized: shape {decoded.shape}")
        
        # Test comparison
        print("\nTesting comparison...")
        encoding2 = generator.generate_from_image_array(test_image)
        is_match, distance, confidence = generator.compare_encodings(encoding, encoding2)
        print(f"Same image comparison:")
        print(f"   Distance: {distance:.4f}")
        print(f"   Confidence: {confidence:.2f}%")
        print(f"   Match: {is_match}")
    else:
        print("❌ Failed to generate encoding")


if __name__ == '__main__':
    test_encoding_generator()
