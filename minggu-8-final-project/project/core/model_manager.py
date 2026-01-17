"""
Model Manager - Manage multiple Teachable Machine models
Week 8 Final Project

This module handles:
- Loading multiple models from models/ folder
- Switching between models
- Training new models
- Model versioning with timestamps
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import shutil


class ModelManager:
    """
    Manage Teachable Machine models
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize model manager
        
        Args:
            models_dir: Directory containing models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Metadata file
        self.metadata_file = self.models_dir / "models_metadata.json"
        
        # Load metadata
        self.metadata = self._load_metadata()
        
        # Current active model
        self.active_model = None
        
    def _load_metadata(self) -> Dict:
        """Load models metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load metadata: {e}")
        
        return {
            "models": [],
            "active_model": None
        }
    
    def _save_metadata(self):
        """Save models metadata"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, indent=2, fp=f)
        except Exception as e:
            print(f"Warning: Could not save metadata: {e}")
    
    def list_models(self) -> List[Dict]:
        """
        List all available models
        
        Returns:
            List of model info dictionaries
        """
        models = []
        
        # Scan models directory
        for item in self.models_dir.iterdir():
            if item.is_dir():
                model_file = item / "keras_model.h5"
                labels_file = item / "labels.txt"
                
                if model_file.exists() and labels_file.exists():
                    # Get metadata
                    meta = next((m for m in self.metadata["models"] if m["id"] == item.name), None)
                    
                    if not meta:
                        # Create metadata for existing model
                        meta = {
                            "id": item.name,
                            "name": item.name,
                            "created_at": datetime.fromtimestamp(model_file.stat().st_mtime).isoformat(),
                            "model_path": str(model_file),
                            "labels_path": str(labels_file)
                        }
                        self.metadata["models"].append(meta)
                        self._save_metadata()
                    
                    # Read classes
                    try:
                        with open(labels_file, 'r', encoding='utf-8') as f:
                            classes = [line.strip().split(maxsplit=1)[-1] for line in f if line.strip()]
                        meta["classes"] = classes
                        meta["num_classes"] = len(classes)
                    except:
                        meta["classes"] = []
                        meta["num_classes"] = 0
                    
                    models.append(meta)
        
        return sorted(models, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def get_model_path(self, model_id: str) -> Optional[tuple]:
        """
        Get model and labels path by ID
        
        Args:
            model_id: Model identifier
            
        Returns:
            Tuple of (model_path, labels_path) or None
        """
        model_dir = self.models_dir / model_id
        model_file = model_dir / "keras_model.h5"
        labels_file = model_dir / "labels.txt"
        
        if model_file.exists() and labels_file.exists():
            return (str(model_file), str(labels_file))
        
        return None
    
    def set_active_model(self, model_id: str) -> bool:
        """
        Set active model
        
        Args:
            model_id: Model identifier
            
        Returns:
            True if successful
        """
        paths = self.get_model_path(model_id)
        if paths:
            self.active_model = model_id
            self.metadata["active_model"] = model_id
            self._save_metadata()
            return True
        return False
    
    def get_active_model(self) -> Optional[Dict]:
        """Get currently active model info"""
        if not self.active_model:
            self.active_model = self.metadata.get("active_model")
        
        if self.active_model:
            models = self.list_models()
            return next((m for m in models if m["id"] == self.active_model), None)
        
        # Return first model if no active model
        models = self.list_models()
        if models:
            self.set_active_model(models[0]["id"])
            return models[0]
        
        return None
    
    def import_model(self, model_file: str, labels_file: str, name: Optional[str] = None) -> str:
        """
        Import a new model
        
        Args:
            model_file: Path to keras_model.h5
            labels_file: Path to labels.txt
            name: Optional model name
            
        Returns:
            Model ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_id = f"model_{timestamp}"
        
        if name:
            # Sanitize name
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-'))
            model_id = f"{safe_name}_{timestamp}"
        
        # Create model directory
        model_dir = self.models_dir / model_id
        model_dir.mkdir(exist_ok=True)
        
        # Copy files
        shutil.copy(model_file, model_dir / "keras_model.h5")
        shutil.copy(labels_file, model_dir / "labels.txt")
        
        # Add to metadata
        self.metadata["models"].append({
            "id": model_id,
            "name": name or model_id,
            "created_at": datetime.now().isoformat(),
            "model_path": str(model_dir / "keras_model.h5"),
            "labels_path": str(model_dir / "labels.txt")
        })
        self._save_metadata()
        
        return model_id
    
    def delete_model(self, model_id: str) -> bool:
        """
        Delete a model
        
        Args:
            model_id: Model identifier
            
        Returns:
            True if successful
        """
        model_dir = self.models_dir / model_id
        
        if model_dir.exists():
            try:
                shutil.rmtree(model_dir)
                
                # Remove from metadata
                self.metadata["models"] = [m for m in self.metadata["models"] if m["id"] != model_id]
                
                # Clear active if deleted
                if self.metadata.get("active_model") == model_id:
                    self.metadata["active_model"] = None
                    self.active_model = None
                
                self._save_metadata()
                return True
            except Exception as e:
                print(f"Error deleting model: {e}")
        
        return False
    
    def rename_model(self, model_id: str, new_name: str) -> bool:
        """
        Rename a model
        
        Args:
            model_id: Model identifier
            new_name: New model name
            
        Returns:
            True if successful
        """
        for model in self.metadata["models"]:
            if model["id"] == model_id:
                model["name"] = new_name
                self._save_metadata()
                return True
        return False


def main():
    """Test model manager"""
    print("="*60)
    print("Model Manager Test")
    print("="*60)
    
    manager = ModelManager()
    
    print("\nAvailable models:")
    models = manager.list_models()
    
    if not models:
        print("  No models found")
    else:
        for i, model in enumerate(models, 1):
            print(f"\n{i}. {model['name']}")
            print(f"   ID: {model['id']}")
            print(f"   Created: {model['created_at']}")
            print(f"   Classes: {', '.join(model.get('classes', []))}")
    
    active = manager.get_active_model()
    if active:
        print(f"\nActive model: {active['name']}")
    else:
        print("\nNo active model")


if __name__ == "__main__":
    main()
