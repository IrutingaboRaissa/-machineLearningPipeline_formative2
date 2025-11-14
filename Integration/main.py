"""
Multimodal Authentication System - CLI Application
===================================================

This is the main CLI application that demonstrates:
1. Successful authentication attempts
2. Unauthorized/failed authentication attempts
3. Integration of facial recognition, voice verification, and product recommendation

Features:
- Multi-modal authentication (face + voice)
- Product recommendation based on verified user
- Comprehensive logging and security checks
- Simulation of success and failure scenarios
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Tuple, Dict, Optional
from datetime import datetime
import hashlib
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AuthenticationSystem:
    """Main authentication system for multimodal verification."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the authentication system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.registered_users = self._load_registered_users()
        self.authentication_log = []
        self.session_id = self._generate_session_id()
        
        logger.info("="*70)
        logger.info("MULTIMODAL AUTHENTICATION SYSTEM INITIALIZED")
        logger.info("="*70)
        logger.info(f"Session ID: {self.session_id}")
        logger.info(f"Registered Users: {len(self.registered_users)}")
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load system configuration."""
        default_config = {
            'face_confidence_threshold': 0.85,
            'voice_confidence_threshold': 0.80,
            'combined_confidence_threshold': 0.82,
            'max_attempts': 3,
            'attempt_timeout': 300,  # seconds
            'security_level': 'HIGH',
            'logging_enabled': True
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
                    logger.info(f"Loaded configuration from: {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}. Using defaults.")
        
        return default_config
    
    def _load_registered_users(self) -> Dict:
        """Load registered users from database."""
        users = {
            'Member1': {
                'user_id': 'USR001',
                'email': 'member1@company.com',
                'name': 'Wengelawit Ayalew Solomon',
                'department': 'Engineering',
                'registered_date': '2024-01-15',
                'face_model_path': 'models/face_recognition_rf.pkl',
                'voice_model_path': 'models/voiceprint_model.pkl',
            },
            'Member2': {
                'user_id': 'USR002',
                'email': 'member2@company.com',
                'name': 'Elyse Marie Uyiringiye',
                'department': 'Product',
                'registered_date': '2024-01-16',
                'face_model_path': 'models/face_recognition_rf.pkl',
                'voice_model_path': 'models/voiceprint_model.pkl',
            },
            'Member3': {
                'user_id': 'USR003',
                'email': 'member3@company.com',
                'name': 'Jean Jacques JABO',
                'department': 'Marketing',
                'registered_date': '2024-01-17',
                'face_model_path': 'models/face_recognition_rf.pkl',
                'voice_model_path': 'models/voiceprint_model.pkl',
            },
            'Member4': {
                'user_id': 'USR004',
                'email': 'member4@company.com',
                'name': 'Raissa Irutingabo',
                'department': 'Sales',
                'registered_date': '2024-01-18',
                'face_model_path': 'models/face_recognition_rf.pkl',
                'voice_model_path': 'models/voiceprint_model.pkl',
            }
        }
        return users
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().isoformat()
        random_str = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        session_str = f"{timestamp}_{random_str}"
        return hashlib.sha256(session_str.encode()).hexdigest()[:16]
    
    def verify_facial_recognition(self, user_identifier: str, 
                                  image_confidence: float = None) -> Tuple[bool, float, str]:
        """
        Verify user through facial recognition.
        
        Args:
            user_identifier: User ID or name
            image_confidence: Simulated confidence score (for testing)
            
        Returns:
            Tuple of (success, confidence_score, message)
        """
        logger.info(f"\n{'='*70}")
        logger.info("FACIAL RECOGNITION VERIFICATION")
        logger.info(f"{'='*70}")
        
        # If confidence not provided, simulate based on user
        if image_confidence is None:
            if user_identifier in self.registered_users:
                # Successful match
                image_confidence = round(random.uniform(0.92, 0.99), 4)
            else:
                # Failed match
                image_confidence = round(random.uniform(0.15, 0.45), 4)
        
        threshold = self.config['face_confidence_threshold']
        is_authorized = image_confidence >= threshold
        
        logger.info(f"User: {user_identifier}")
        logger.info(f"Confidence Score: {image_confidence:.2%}")
        logger.info(f"Threshold: {threshold:.2%}")
        
        if is_authorized:
            logger.info(f"[PASS] FACIAL RECOGNITION: PASSED")
            message = f"Facial recognition successful (confidence: {image_confidence:.2%})"
        else:
            logger.warning(f"[FAIL] FACIAL RECOGNITION: FAILED")
            message = f"Facial recognition failed (confidence: {image_confidence:.2%} < {threshold:.2%})"
        
        return is_authorized, image_confidence, message
    
    def verify_voice_recognition(self, user_identifier: str,
                                voice_confidence: float = None) -> Tuple[bool, float, str]:
        """
        Verify user through voice/audio recognition.
        
        Args:
            user_identifier: User ID or name
            voice_confidence: Simulated confidence score (for testing)
            
        Returns:
            Tuple of (success, confidence_score, message)
        """
        logger.info(f"\n{'='*70}")
        logger.info("VOICE VERIFICATION")
        logger.info(f"{'='*70}")
        
        # If confidence not provided, simulate based on user
        if voice_confidence is None:
            if user_identifier in self.registered_users:
                # Successful match
                voice_confidence = round(random.uniform(0.88, 0.98), 4)
            else:
                # Failed match
                voice_confidence = round(random.uniform(0.12, 0.40), 4)
        
        threshold = self.config['voice_confidence_threshold']
        is_authorized = voice_confidence >= threshold
        
        logger.info(f"User: {user_identifier}")
        logger.info(f"Confidence Score: {voice_confidence:.2%}")
        logger.info(f"Threshold: {threshold:.2%}")
        
        if is_authorized:
            logger.info(f"[PASS] VOICE VERIFICATION: PASSED")
            message = f"Voice verification successful (confidence: {voice_confidence:.2%})"
        else:
            logger.warning(f"[FAIL] VOICE VERIFICATION: FAILED")
            message = f"Voice verification failed (confidence: {voice_confidence:.2%} < {threshold:.2%})"
        
        return is_authorized, voice_confidence, message
    
    def recommend_products(self, user_identifier: str) -> Dict:
        """
        Generate product recommendations for authenticated user.
        
        Args:
            user_identifier: Authenticated user identifier
            
        Returns:
            Dictionary with product recommendations
        """
        logger.info(f"\n{'='*70}")
        logger.info("PRODUCT RECOMMENDATION")
        logger.info(f"{'='*70}")
        
        # Sample product recommendations based on user profile
        recommendations = {
            'Member1': {
                'top_products': ['Laptop', 'Monitor', 'Keyboard'],
                'categories': ['Electronics', 'Accessories'],
                'predicted_purchase_probability': 0.87
            },
            'Member2': {
                'top_products': ['Cloud Storage', 'Software License', 'Security Suite'],
                'categories': ['Software', 'Services'],
                'predicted_purchase_probability': 0.91
            },
            'Member3': {
                'top_products': ['Marketing Analytics Tool', 'Design Software', 'Social Media Manager'],
                'categories': ['Marketing Tools', 'Software'],
                'predicted_purchase_probability': 0.79
            },
            'Member4': {
                'top_products': ['CRM System', 'Sales Dashboard', 'Contact Manager'],
                'categories': ['Business Tools', 'Software'],
                'predicted_purchase_probability': 0.85
            }
        }
        
        user_recs = recommendations.get(user_identifier, {
            'top_products': ['Premium Plan', 'Extended Support'],
            'categories': ['Services'],
            'predicted_purchase_probability': 0.75
        })
        
        logger.info(f"User: {user_identifier}")
        logger.info(f"Top Products: {', '.join(user_recs['top_products'])}")
        logger.info(f"Categories: {', '.join(user_recs['categories'])}")
        logger.info(f"Purchase Probability: {user_recs['predicted_purchase_probability']:.1%}")
        
        return user_recs
    
    def authenticate_user(self, user_identifier: str, 
                         face_confidence: Optional[float] = None,
                         voice_confidence: Optional[float] = None) -> Dict:
        """
        Perform complete multimodal authentication.
        
        Args:
            user_identifier: User ID or name
            face_confidence: Optional simulated face confidence
            voice_confidence: Optional simulated voice confidence
            
        Returns:
            Dictionary with authentication results
        """
        logger.info("\n" + "="*70)
        logger.info("INITIATING MULTIMODAL AUTHENTICATION")
        logger.info("="*70)
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info(f"Session: {self.session_id}")
        logger.info(f"User Identifier: {user_identifier}")
        
        # Step 1: Facial Recognition
        face_success, face_score, face_msg = self.verify_facial_recognition(
            user_identifier, face_confidence
        )
        
        # Step 2: Voice Verification
        voice_success, voice_score, voice_msg = self.verify_voice_recognition(
            user_identifier, voice_confidence
        )
        
        # Step 3: Combined Authentication Decision
        logger.info(f"\n{'='*70}")
        logger.info("AUTHENTICATION DECISION")
        logger.info(f"{'='*70}")
        
        # Calculate combined confidence
        combined_confidence = (face_score + voice_score) / 2
        combined_threshold = self.config['combined_confidence_threshold']
        
        logger.info(f"Face Confidence: {face_score:.2%}")
        logger.info(f"Voice Confidence: {voice_score:.2%}")
        logger.info(f"Combined Confidence: {combined_confidence:.2%}")
        logger.info(f"Combined Threshold: {combined_threshold:.2%}")
        
        # Authentication logic
        auth_success = face_success and voice_success and (combined_confidence >= combined_threshold)
        
        result = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'user_identifier': user_identifier,
            'authenticated': auth_success,
            'face_verification': {
                'success': face_success,
                'confidence': face_score,
                'message': face_msg
            },
            'voice_verification': {
                'success': voice_success,
                'confidence': voice_score,
                'message': voice_msg
            },
            'combined_confidence': combined_confidence,
            'products': None
        }
        
        # Step 4: Provide recommendations if authenticated
        if auth_success:
            logger.info(f"\n[PASS] AUTHENTICATION SUCCESSFUL")
            result['status'] = 'AUTHENTICATED'
            result['products'] = self.recommend_products(user_identifier)
            
            # Get user details
            if user_identifier in self.registered_users:
                user_info = self.registered_users[user_identifier]
                result['user_info'] = {
                    'user_id': user_info['user_id'],
                    'name': user_info['name'],
                    'email': user_info['email'],
                    'department': user_info['department']
                }
        else:
            logger.warning(f"\n[FAIL] AUTHENTICATION FAILED")
            result['status'] = 'AUTHENTICATION_FAILED'
            if not face_success:
                result['failure_reason'] = "Facial recognition verification failed"
            elif not voice_success:
                result['failure_reason'] = "Voice verification failed"
            else:
                result['failure_reason'] = "Combined confidence below threshold"
        
        # Log authentication attempt
        self.authentication_log.append(result)
        
        return result
    
    def get_authentication_report(self) -> Dict:
        """Generate authentication session report."""
        successful = sum(1 for log in self.authentication_log if log['authenticated'])
        failed = len(self.authentication_log) - successful
        avg_confidence = sum(log['combined_confidence'] for log in self.authentication_log) / len(self.authentication_log) if self.authentication_log else 0
        
        report = {
            'session_id': self.session_id,
            'total_attempts': len(self.authentication_log),
            'successful_authentications': successful,
            'failed_authentications': failed,
            'success_rate': successful / len(self.authentication_log) if self.authentication_log else 0,
            'average_confidence': avg_confidence,
            'configuration': self.config,
            'attempts': self.authentication_log
        }
        
        return report
    
    def save_report(self, output_dir: str = "output"):
        """Save authentication report to file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        report = self.get_authentication_report()
        
        report_file = output_path / f"authentication_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n[DONE] Report saved: {report_file}")
        
        return report_file


def simulate_scenario(system: AuthenticationSystem, scenario_type: str, user_id: str = None):
    """
    Simulate authentication scenarios.
    
    Args:
        system: AuthenticationSystem instance
        scenario_type: Type of scenario ('success', 'unauthorized', 'spoofing', 'random')
        user_id: Optional specific user ID
    """
    logger.info(f"\n\n{'#'*70}")
    logger.info(f"SCENARIO: {scenario_type.upper()}")
    logger.info(f"{'#'*70}\n")
    
    if scenario_type == 'success':
        # Legitimate user authentication
        if user_id is None:
            user_id = random.choice(list(system.registered_users.keys()))
        
        result = system.authenticate_user(
            user_id,
            face_confidence=round(random.uniform(0.93, 0.99), 4),
            voice_confidence=round(random.uniform(0.90, 0.98), 4)
        )
    
    elif scenario_type == 'unauthorized':
        # Unauthorized user attempting access
        user_id = 'UnknownUser'
        
        result = system.authenticate_user(
            user_id,
            face_confidence=round(random.uniform(0.10, 0.40), 4),
            voice_confidence=round(random.uniform(0.15, 0.35), 4)
        )
    
    elif scenario_type == 'spoofing':
        # Attempt to spoof with partial success
        user_id = random.choice(list(system.registered_users.keys()))
        
        result = system.authenticate_user(
            f"SpoofAttempt_{user_id}",
            face_confidence=round(random.uniform(0.60, 0.82), 4),
            voice_confidence=round(random.uniform(0.50, 0.75), 4)
        )
    
    elif scenario_type == 'random':
        # Random scenario
        scenario = random.choice(['success', 'unauthorized', 'spoofing'])
        simulate_scenario(system, scenario, user_id)
        return
    
    else:
        logger.error(f"Unknown scenario type: {scenario_type}")
        return
    
    # Print result
    print_authentication_result(result)


def print_authentication_result(result: Dict):
    """Pretty print authentication result."""
    print("\n" + "="*70)
    print("AUTHENTICATION RESULT")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"User: {result['user_identifier']}")
    print(f"Overall Confidence: {result['combined_confidence']:.2%}")
    
    if 'failure_reason' in result:
        print(f"Reason: {result['failure_reason']}")
    
    if result['authenticated'] and 'user_info' in result:
        print(f"\nUser Details:")
        info = result['user_info']
        print(f"  ID: {info['user_id']}")
        print(f"  Name: {info['name']}")
        print(f"  Email: {info['email']}")
        print(f"  Department: {info['department']}")
        
        if result['products']:
            print(f"\nRecommended Products:")
            for product in result['products']['top_products']:
                print(f"  - {product}")
    
    print("="*70 + "\n")


def main():
    """Main CLI application."""
    parser = argparse.ArgumentParser(
        description='Multimodal Authentication System - CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode demo                    # Run demo with all scenarios
  python main.py --mode single --user Member1   # Authenticate specific user
  python main.py --mode simulate --scenario success  # Run success scenario
  python main.py --mode list-users              # List registered users
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['demo', 'single', 'simulate', 'list-users', 'test'],
        default='demo',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--user',
        type=str,
        help='User identifier for single authentication'
    )
    
    parser.add_argument(
        '--scenario',
        choices=['success', 'unauthorized', 'spoofing', 'random'],
        default='random',
        help='Simulation scenario type'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of simulations to run'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Output directory for reports'
    )
    
    args = parser.parse_args()
    
    # Initialize system
    system = AuthenticationSystem(config_path=args.config)
    
    # Execute based on mode
    if args.mode == 'demo':
        logger.info("\n" + "="*70)
        logger.info("MULTIMODAL AUTHENTICATION SYSTEM - DEMONSTRATION")
        logger.info("="*70)
        
        # Run multiple scenarios
        scenarios = ['success', 'success', 'unauthorized', 'spoofing', 'success']
        
        for i, scenario in enumerate(scenarios, 1):
            logger.info(f"\n[DEMO {i}/{len(scenarios)}]")
            simulate_scenario(system, scenario)
    
    elif args.mode == 'single':
        if not args.user:
            print("Error: --user required for single mode")
            sys.exit(1)
        
        result = system.authenticate_user(args.user)
        print_authentication_result(result)
    
    elif args.mode == 'simulate':
        for i in range(args.count):
            logger.info(f"\n[SIMULATION {i+1}/{args.count}]")
            simulate_scenario(system, args.scenario)
    
    elif args.mode == 'list-users':
        logger.info("\nRegistered Users:")
        for user_id, user_info in system.registered_users.items():
            logger.info(f"\n  {user_id}")
            logger.info(f"    Name: {user_info['name']}")
            logger.info(f"    Email: {user_info['email']}")
            logger.info(f"    Department: {user_info['department']}")
    
    elif args.mode == 'test':
        # Comprehensive test
        logger.info("\n" + "="*70)
        logger.info("COMPREHENSIVE SYSTEM TEST")
        logger.info("="*70)
        
        for user in system.registered_users.keys():
            result = system.authenticate_user(user)
            print_authentication_result(result)
    
    # Save report
    system.save_report(output_dir=args.output)
    
    logger.info("\n" + "="*70)
    logger.info("EXECUTION COMPLETE")
    logger.info("="*70)


if __name__ == "__main__":
    main()
