"""
Multimodal Data Integration Script
====================================
Integrates three feature modalities:
1. Tabular Features (merged_dataset.csv) - Product Recommendation
2. Image Features (image_features.csv) - Facial Recognition  
3. Audio Features (audio_features.csv) - Voice Verification

This script creates an integrated multimodal dataset for the authentication system.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultimodalIntegrator:
    """Handles integration of multiple feature modalities."""
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the multimodal integrator.
        
        Args:
            base_path: Root path for the project
        """
        self.base_path = Path(base_path)
        self.product_rec_path = self.base_path / "product_recommendation"
        self.face_rec_path = self.base_path / "face_recognition"
        self.audio_path = self.base_path
        
        self.tabular_data = None
        self.image_features = None
        self.audio_features = None
        self.integrated_data = None
        
    def load_tabular_features(self) -> pd.DataFrame:
        """
        Load tabular features from product recommendation dataset.
        
        Returns:
            DataFrame with tabular features
        """
        try:
            csv_path = self.product_rec_path / "merged_dataset.csv"
            
            if not csv_path.exists():
                raise FileNotFoundError(f"Tabular dataset not found: {csv_path}")
            
            df = pd.read_csv(csv_path)
            logger.info(f"✓ Loaded tabular features: {df.shape}")
            logger.info(f"  Columns: {list(df.columns[:5])}... ({len(df.columns)} total)")
            
            self.tabular_data = df
            return df
            
        except Exception as e:
            logger.error(f"✗ Failed to load tabular features: {e}")
            raise
    
    def load_image_features(self) -> Optional[pd.DataFrame]:
        """
        Load image features from facial recognition system.
        
        Returns:
            DataFrame with image features or None if not found
        """
        try:
            # Check multiple possible locations
            possible_paths = [
                self.face_rec_path / "features" / "image_features.csv",
                self.face_rec_path / "image_features.csv",
                self.base_path / "image_features.csv",
            ]
            
            for csv_path in possible_paths:
                if csv_path.exists():
                    df = pd.read_csv(csv_path)
                    logger.info(f"✓ Loaded image features: {df.shape}")
                    logger.info(f"  Columns: {list(df.columns[:5])}... ({len(df.columns)} total)")
                    self.image_features = df
                    return df
            
            logger.warning("⚠ Image features file not found (image_features.csv)")
            logger.warning("  Expected location: face_recognition/features/image_features.csv")
            return None
            
        except Exception as e:
            logger.error(f"✗ Failed to load image features: {e}")
            return None
    
    def load_audio_features(self) -> Optional[pd.DataFrame]:
        """
        Load audio features from audio processing.
        
        Returns:
            DataFrame with audio features or None if not found
        """
        try:
            # Check multiple possible locations
            possible_paths = [
                self.base_path / "audio_features.csv",
                self.audio_path / "audio_features.csv",
            ]
            
            for csv_path in possible_paths:
                if csv_path.exists():
                    df = pd.read_csv(csv_path)
                    logger.info(f"✓ Loaded audio features: {df.shape}")
                    logger.info(f"  Columns: {list(df.columns[:5])}... ({len(df.columns)} total)")
                    self.audio_features = df
                    return df
            
            logger.warning("⚠ Audio features file not found (audio_features.csv)")
            return None
            
        except Exception as e:
            logger.error(f"✗ Failed to load audio features: {e}")
            return None
    
    def preprocess_features(self, df: pd.DataFrame, modality: str) -> pd.DataFrame:
        """
        Preprocess features for a specific modality.
        
        Args:
            df: Input DataFrame
            modality: Type of modality ('tabular', 'image', 'audio')
            
        Returns:
            Preprocessed DataFrame
        """
        df = df.copy()
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        # Fill numeric missing values with mean
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                df[col].fillna(df[col].mean(), inplace=True)
        
        # Fill categorical missing values with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isna().any():
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
        
        logger.info(f"✓ Preprocessed {modality} features")
        return df
    
    def normalize_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize numeric features to [0, 1] range.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with normalized numeric features
        """
        df = df.copy()
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            min_val = df[col].min()
            max_val = df[col].max()
            
            if max_val != min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)
            else:
                df[col] = 0
        
        logger.info(f"✓ Normalized {len(numeric_cols)} numeric features")
        return df
    
    def create_sample_image_features(self, n_samples: int = 50) -> pd.DataFrame:
        """
        Create sample image features if file doesn't exist.
        This is for demonstration purposes.
        
        Args:
            n_samples: Number of samples to create
            
        Returns:
            DataFrame with synthetic image features
        """
        logger.info(f"⚠ Creating synthetic image features ({n_samples} samples)")
        
        # Create feature columns
        feature_cols = {f'img_feature_{i}': np.random.randn(n_samples) for i in range(217)}
        
        df = pd.DataFrame(feature_cols)
        df['member'] = [f'Member{i%4 + 1}' for i in range(n_samples)]
        
        # Create augmentation list with exact length matching n_samples
        augmentation_types = ['original', 'rotated_15', 'rotated_-15', 'flipped', 
                              'grayscale', 'brightness_up', 'brightness_down', 'blurred']
        augmentation_list = (augmentation_types * (n_samples // len(augmentation_types) + 1))[:n_samples]
        df['augmentation'] = augmentation_list
        
        logger.info(f"✓ Generated synthetic image features: {df.shape}")
        return df
    
    def create_sample_audio_features(self, n_samples: int = 50) -> pd.DataFrame:
        """
        Create sample audio features if file doesn't exist.
        This is for demonstration purposes.
        
        Args:
            n_samples: Number of samples to create
            
        Returns:
            DataFrame with synthetic audio features
        """
        logger.info(f"⚠ Creating synthetic audio features ({n_samples} samples)")
        
        # Create MFCC features
        feature_cols = {}
        for i in range(1, 14):
            feature_cols[f'mfcc{i}'] = np.random.randn(n_samples)
        
        df = pd.DataFrame(feature_cols)
        df['filename'] = [f'audio_{i}.wav' for i in range(n_samples)]
        df['rolloff'] = np.random.randn(n_samples)
        df['energy'] = np.random.randn(n_samples)
        df['label'] = [f'Speaker{i%4 + 1}' for i in range(n_samples)]
        
        logger.info(f"✓ Generated synthetic audio features: {df.shape}")
        return df
    
    def align_image_features(self, df: pd.DataFrame, n_target: int) -> pd.DataFrame:
        """
        Align image features to target size by sampling.
        
        Args:
            df: Image features DataFrame
            n_target: Target number of samples
            
        Returns:
            Aligned DataFrame
        """
        if len(df) > n_target:
            df = df.sample(n=n_target, random_state=42)
        elif len(df) < n_target:
            # Upsample by repeating
            repeat_count = (n_target // len(df)) + 1
            df = pd.concat([df] * repeat_count, ignore_index=True).iloc[:n_target]
        
        return df.reset_index(drop=True)
    
    def align_audio_features(self, df: pd.DataFrame, n_target: int) -> pd.DataFrame:
        """
        Align audio features to target size by sampling.
        
        Args:
            df: Audio features DataFrame
            n_target: Target number of samples
            
        Returns:
            Aligned DataFrame
        """
        if len(df) > n_target:
            df = df.sample(n=n_target, random_state=42)
        elif len(df) < n_target:
            # Upsample by repeating
            repeat_count = (n_target // len(df)) + 1
            df = pd.concat([df] * repeat_count, ignore_index=True).iloc[:n_target]
        
        return df.reset_index(drop=True)
    
    def integrate(self, output_dir: str = "output") -> pd.DataFrame:
        """
        Integrate all modalities into a single dataset.
        
        Args:
            output_dir: Directory to save integrated data
            
        Returns:
            Integrated multimodal DataFrame
        """
        logger.info("\n" + "="*60)
        logger.info("MULTIMODAL DATA INTEGRATION")
        logger.info("="*60 + "\n")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Load tabular features (required)
        logger.info("Step 1: Loading Tabular Features")
        logger.info("-" * 40)
        self.load_tabular_features()
        tabular_processed = self.preprocess_features(self.tabular_data, "tabular")
        tabular_normalized = self.normalize_features(tabular_processed)
        
        # Get target size
        n_samples = len(tabular_normalized)
        logger.info(f"  Target samples: {n_samples}\n")
        
        # Load or create image features
        logger.info("Step 2: Loading Image Features")
        logger.info("-" * 40)
        image_loaded = self.load_image_features()
        if image_loaded is None:
            self.image_features = self.create_sample_image_features(n_samples)
        
        image_processed = self.preprocess_features(self.image_features, "image")
        image_normalized = self.normalize_features(image_processed)
        image_aligned = self.align_image_features(image_normalized, n_samples)
        
        # Rename image feature columns to avoid conflicts
        image_feature_cols = {col: f'img_{col}' for col in image_aligned.columns 
                             if col not in ['member', 'augmentation']}
        image_aligned = image_aligned.rename(columns=image_feature_cols)
        
        # Keep only feature columns
        image_features_only = image_aligned[[col for col in image_aligned.columns 
                                            if col.startswith('img_')]].reset_index(drop=True)
        logger.info(f"  Aligned samples: {len(image_features_only)}\n")
        
        # Load or create audio features
        logger.info("Step 3: Loading Audio Features")
        logger.info("-" * 40)
        audio_loaded = self.load_audio_features()
        if audio_loaded is None:
            self.audio_features = self.create_sample_audio_features(n_samples)
        
        audio_processed = self.preprocess_features(self.audio_features, "audio")
        audio_normalized = self.normalize_features(audio_processed)
        audio_aligned = self.align_audio_features(audio_normalized, n_samples)
        
        # Rename audio feature columns to avoid conflicts
        audio_feature_cols = {col: f'audio_{col}' for col in audio_aligned.columns 
                             if col not in ['filename', 'label']}
        audio_aligned = audio_aligned.rename(columns=audio_feature_cols)
        
        # Keep only feature columns
        audio_features_only = audio_aligned[[col for col in audio_aligned.columns 
                                            if col.startswith('audio_')]].reset_index(drop=True)
        logger.info(f"  Aligned samples: {len(audio_features_only)}\n")
        
        # Integrate all modalities
        logger.info("Step 4: Integrating Modalities")
        logger.info("-" * 40)
        
        integrated = pd.concat([
            tabular_normalized.reset_index(drop=True),
            image_features_only,
            audio_features_only
        ], axis=1)
        
        logger.info(f"✓ Integration successful!")
        logger.info(f"  Final shape: {integrated.shape}")
        logger.info(f"  Rows: {integrated.shape[0]} | Columns: {integrated.shape[1]}\n")
        
        # Save integrated data
        logger.info("Step 5: Saving Integrated Data")
        logger.info("-" * 40)
        
        output_file = output_path / "integrated_features.csv"
        integrated.to_csv(output_file, index=False)
        logger.info(f"✓ Saved: {output_file}\n")
        
        # Save summary statistics
        self._save_summary(integrated, output_path)
        
        # Save modality-specific mappings
        self._save_modality_info(output_path, image_features_only, audio_features_only)
        
        self.integrated_data = integrated
        return integrated
    
    def _save_summary(self, df: pd.DataFrame, output_path: Path):
        """Save summary statistics of integrated data."""
        summary = {
            'Total Samples': len(df),
            'Total Features': len(df.columns),
            'Data Types': df.dtypes.value_counts().to_dict(),
            'Missing Values': df.isna().sum().sum(),
            'Numeric Features': len(df.select_dtypes(include=[np.number]).columns),
            'Object Features': len(df.select_dtypes(include=['object']).columns),
        }
        
        summary_file = output_path / "integration_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("MULTIMODAL INTEGRATION SUMMARY\n")
            f.write("="*60 + "\n\n")
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")
            f.write("\n" + "="*60 + "\n")
            f.write("FEATURE BREAKDOWN\n")
            f.write("="*60 + "\n\n")
            f.write(f"Tabular Features: {len(self.tabular_data.columns)}\n")
            f.write(f"Image Features: {len([c for c in df.columns if c.startswith('img_')])}\n")
            f.write(f"Audio Features: {len([c for c in df.columns if c.startswith('audio_')])}\n")
        
        logger.info(f"✓ Saved summary: {summary_file}")
    
    def _save_modality_info(self, output_path: Path, image_df: pd.DataFrame, 
                           audio_df: pd.DataFrame):
        """Save modality-specific information."""
        info_file = output_path / "modality_info.txt"
        
        with open(info_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("MODALITY INFORMATION\n")
            f.write("="*60 + "\n\n")
            
            f.write("IMAGE FEATURES:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Features: {len(image_df.columns)}\n")
            f.write(f"Features: {', '.join(image_df.columns.tolist())}\n\n")
            
            f.write("AUDIO FEATURES:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Features: {len(audio_df.columns)}\n")
            f.write(f"Features: {', '.join(audio_df.columns.tolist())}\n\n")
            
            f.write("INTEGRATION METHOD:\n")
            f.write("-" * 40 + "\n")
            f.write("- All modalities normalized to [0, 1] range\n")
            f.write("- Missing values imputed with mean (numeric) or mode (categorical)\n")
            f.write("- Features aligned to same number of samples\n")
            f.write("- Concatenated horizontally (column-wise fusion)\n")
        
        logger.info(f"✓ Saved modality info: {info_file}")


def main():
    """Main execution function."""
    # Get current working directory
    cwd = os.getcwd()
    logger.info(f"Working directory: {cwd}")
    
    # Initialize integrator
    integrator = MultimodalIntegrator(base_path=cwd)
    
    # Perform integration
    integrated_df = integrator.integrate(output_dir="output")
    
    # Display integrated data info
    logger.info("\n" + "="*60)
    logger.info("INTEGRATED DATA PREVIEW")
    logger.info("="*60)
    logger.info(f"\nShape: {integrated_df.shape}")
    logger.info(f"\nFirst 3 rows:")
    logger.info(integrated_df.head(3).to_string())
    logger.info(f"\nData types:\n{integrated_df.dtypes.value_counts()}")
    logger.info(f"\nColumn names:\n{list(integrated_df.columns[:10])}...\n")
    
    return integrated_df


if __name__ == "__main__":
    integrated_data = main()
