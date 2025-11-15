import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from main import AuthenticationSystem
except ImportError:
    print("Error: Could not import AuthenticationSystem from main.py")
    sys.exit(1)


class InteractiveCLI:
    
    def __init__(self):
        self.system = AuthenticationSystem()
        self.clear_screen()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        print(f"  {title.center(66)}")
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * 70)
    
    
    def display_welcome(self):
        self.clear_screen()
        self.print_header("MULTIMODAL AUTHENTICATION SYSTEM")
        print("  Face Recognition + Voice Verification + Product Recommendations")
        print()
        print("  This system uses multimodal authentication to verify your identity")
        print("  before providing personalized product recommendations.")
        print()
    
    def display_registered_users(self):
        """Display list of registered users."""
        print("\nREGISTERED USERS:")
        print()
        
        users = list(self.system.registered_users.items())
        for idx, (user_id, user_info) in enumerate(users, 1):
            print(f"  {idx}. {user_info['name']}")
        
        print(f"\n  {len(users) + 1}. Unauthorized User (Test Access Denial)")
        print(f"  0. Exit System")
        print()
    
    def get_user_choice(self) -> str:
        while True:
            try:
                choice = input("\nSelect user number: ").strip()
                
                if choice == '0':
                    return 'EXIT'
                
                choice_num = int(choice)
                users = list(self.system.registered_users.keys())
                
                if 1 <= choice_num <= len(users):
                    return users[choice_num - 1]
                elif choice_num == len(users) + 1:
                    return 'UNAUTHORIZED'
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def simulate_face_authentication(self, user_id: str):
        print("\nFACE AUTHENTICATION")
        self.print_separator()
        print("  Initializing camera...")
        time.sleep(0.5)
        print("  Capturing facial image...")
        time.sleep(1)
        print("  Analyzing facial features...")
        time.sleep(1)
        print("  Comparing with database...")
        time.sleep(1)
        
        # Get authentication result
        is_authorized, confidence, message = self.system.verify_facial_recognition(user_id)
        
        print(f"\n  Confidence Score: {confidence:.2%}")
        
        if is_authorized:
            print(f"  [PASS] {message}")
            print("  Status: FACE AUTHENTICATION PASSED")
        else:
            print(f"  [FAIL] {message}")
            print("  Status: FACE AUTHENTICATION FAILED")
        
        return is_authorized, confidence
    
    def simulate_voice_verification(self, user_id: str):
        print("\nVOICE VERIFICATION")
        self.print_separator()
        print("  Please say: 'Yes, approve'")
        time.sleep(0.5)
        print("  Recording audio...")
        time.sleep(1.5)
        print("  Processing voice sample...")
        time.sleep(1)
        print("  Analyzing voiceprint...")
        time.sleep(1)
        
        # Get verification result
        is_authorized, confidence, message = self.system.verify_voice_recognition(user_id)
        
        print(f"\n  Confidence Score: {confidence:.2%}")
        
        if is_authorized:
            print(f"  [PASS] {message}")
            print("  Status: VOICE VERIFICATION PASSED")
        else:
            print(f"  [FAIL] {message}")
            print("  Status: VOICE VERIFICATION FAILED")
        
        return is_authorized, confidence
    
    def display_product_recommendations(self, user_id: str):
        print("\nPRODUCT RECOMMENDATIONS")
        self.print_separator()
        print("  Generating personalized recommendations...")
        time.sleep(1)
        
        recommendations = self.system.recommend_products(user_id)
        
        print(f"\n  Top Products for You:")
        for idx, product in enumerate(recommendations['top_products'], 1):
            print(f"     {idx}. {product}")
        
        print(f"\n  Categories: {', '.join(recommendations['categories'])}")
        print(f"  Purchase Probability: {recommendations['predicted_purchase_probability']:.1%}")
        
        print("\n  These recommendations are based on your profile and history.")
    
    def display_access_denied(self, failed_step: str):
        print("\nACCESS DENIED")
        self.print_separator()
        print(f"  Authentication failed at: {failed_step}")
        print("  You do not have permission to access this system.")
        print()
        print("  Reasons for denial:")
        print("  - Identity verification failed")
        print("  - Confidence score below security threshold")
        print("  - User not registered in the system")
        print()
        print("  Please contact system administrator for assistance.")
    
    def authenticate_user_flow(self, user_id: str):
        self.print_separator()
        
        if user_id == 'UNAUTHORIZED':
            print("\n[WARNING] Attempting authentication as UNAUTHORIZED USER")
            user_id = 'UnknownUser'
        else:
            user_info = self.system.registered_users[user_id]
            print(f"\nAuthenticating: {user_info['name']}")
            print(f"   Department: {user_info['department']}")
        
        print("\nStarting Multi-Modal Authentication Process...")
        time.sleep(1)
        
        # Step 1: Face Authentication
        face_passed, face_conf = self.simulate_face_authentication(user_id)
        
        if not face_passed:
            self.display_access_denied("FACE AUTHENTICATION")
            return False
        
        time.sleep(1)
        
        # Step 2: Voice Verification
        voice_passed, voice_conf = self.simulate_voice_verification(user_id)
        
        if not voice_passed:
            self.display_access_denied("VOICE VERIFICATION")
            return False
        
        time.sleep(1)
        
        # Step 3: Authentication Success
        print("\n[SUCCESS] AUTHENTICATION SUCCESSFUL")
        print("  All security checks passed!")
        print(f"  Face Recognition: {face_conf:.2%}")
        print(f"  Voice Verification: {voice_conf:.2%}")
        
        time.sleep(1)
        
        # Step 4: Product Recommendations
        self.display_product_recommendations(user_id)
        
        return True
    
    def wait_for_continue(self):
        input("\n\n  Press Enter to continue...")
    
    def run(self):
        self.display_welcome()
        
        while True:
            self.display_registered_users()
            
            user_choice = self.get_user_choice()
            
            if user_choice == 'EXIT':
                print("\nThank you for using the Authentication System!")
                print("   Goodbye!\n")
                break
            
            # Run authentication flow
            self.authenticate_user_flow(user_choice)
            
            # Wait before returning to menu
            self.wait_for_continue()
            self.clear_screen()
            self.print_header("MULTIMODAL AUTHENTICATION SYSTEM")


def main():
    try:
        cli = InteractiveCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n[WARNING] Operation cancelled by user.")
        print("   Exiting safely...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
