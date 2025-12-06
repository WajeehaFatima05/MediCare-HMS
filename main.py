
"""
Main entry point for MediCare Hospital Management System
Run this file to start the application
"""

from console_interface import ConsoleInterface


def main():
    """Main function to run the application"""
    try:
        interface = ConsoleInterface()
        interface.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user.")
        print("✅ Thank you for using MediCare HMS!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please contact system administrator.")


if __name__ == "__main__":
    main()