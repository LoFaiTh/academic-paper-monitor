#!/usr/bin/env python3
"""
Setup script for Academic Paper Monitor
"""

import json
import os
import sys

def create_config():
    """Create a basic configuration file"""
    config = {
        "email": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "sender_password": "",
            "recipient_emails": []
        },
        "slack": {
            "enabled": False,
            "webhook_url": "",
            "channel": "#general",
            "username": "Paper Monitor Bot"
        },
        "monitoring": {
            "days_back": 7,
            "max_results_per_query": 30,
            "categories": ["cs.CV", "cs.RO", "cs.GR", "cs.AI", "cs.LG"]
        },
        "github": {
            "enabled": False,
            "repo_name": "",
            "branch": "main",
            "pages_branch": "gh-pages",
            "token": ""
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created config.json with default settings")

def setup_slack():
    """Guide user through Slack setup"""
    print("\n🔧 Slack Setup")
    print("=" * 30)
    print("1. Go to https://api.slack.com/apps")
    print("2. Click 'Create New App' → 'From scratch'")
    print("3. Give it a name like 'Paper Monitor'")
    print("4. Go to 'Features' → 'Incoming Webhooks'")
    print("5. Toggle 'Activate Incoming Webhooks' to On")
    print("6. Click 'Add New Webhook to Workspace'")
    print("7. Choose your channel and copy the webhook URL")
    
    webhook_url = input("\nEnter your Slack webhook URL (or press Enter to skip): ").strip()
    
    if webhook_url:
        # Update config
        with open("config.json", "r") as f:
            config = json.load(f)
        
        config["slack"]["enabled"] = True
        config["slack"]["webhook_url"] = webhook_url
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Slack webhook configured!")
    else:
        print("ℹ️  Skipping Slack setup")

def setup_github():
    """Guide user through GitHub setup"""
    print("\n🔧 GitHub Setup")
    print("=" * 30)
    print("1. Create a new repository on GitHub")
    print("2. Push this code to your repository")
    print("3. Go to repository Settings → Pages")
    print("4. Set source to 'Deploy from a branch'")
    print("5. Select 'gh-pages' branch")
    print("6. Save the settings")
    
    repo_name = input("\nEnter your repository name (username/repo-name): ").strip()
    
    if repo_name:
        # Update config
        with open("config.json", "r") as f:
            config = json.load(f)
        
        config["github"]["enabled"] = True
        config["github"]["repo_name"] = repo_name
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ GitHub repository configured!")
        print(f"   Your site will be available at: https://{repo_name.split('/')[0]}.github.io/{repo_name.split('/')[1]}/")
    else:
        print("ℹ️  Skipping GitHub setup")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")

def main():
    """Main setup function"""
    print("🚀 Academic Paper Monitor Setup")
    print("=" * 40)
    
    # Check if config exists
    if os.path.exists("config.json"):
        print("ℹ️  config.json already exists")
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled")
            return
    
    # Create config
    create_config()
    
    # Install dependencies
    install_dependencies()
    
    # Setup Slack
    setup_slack()
    
    # Setup GitHub
    setup_github()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Test your setup: python test_monitor.py")
    print("2. Run the monitor: python paper_monitor.py")
    print("3. For GitHub Actions, add SLACK_WEBHOOK_URL to your repository secrets")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 