#!/usr/bin/env python3
"""
Local deployment script for testing GitHub Pages functionality
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Local GitHub Pages Deployment Test")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not run_command("git status", "Checking git repository"):
        print("❌ Not in a git repository. Please run this from your project directory.")
        sys.exit(1)
    
    # Check if index.html exists
    if not os.path.exists("index.html"):
        print("❌ index.html not found. Please run the paper monitor first.")
        sys.exit(1)
    
    # Configure git for deployment
    if not run_command("git config user.name 'Paper Monitor Bot'", "Setting git user name"):
        sys.exit(1)
    
    if not run_command("git config user.email 'bot@example.com'", "Setting git user email"):
        sys.exit(1)
    
    # Create or switch to gh-pages branch
    if not run_command("git checkout --orphan gh-pages 2>/dev/null || git checkout gh-pages", "Switching to gh-pages branch"):
        sys.exit(1)
    
    # Remove all files except index.html
    if not run_command("git rm -rf .", "Clearing branch"):
        sys.exit(1)
    
    # Copy index.html
    if not run_command("cp index.html .", "Copying index.html"):
        sys.exit(1)
    
    # Add and commit
    if not run_command("git add index.html", "Adding index.html to git"):
        sys.exit(1)
    
    commit_message = f"Update paper monitor report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        sys.exit(1)
    
    # Push to gh-pages branch
    if not run_command("git push origin gh-pages --force", "Pushing to gh-pages branch"):
        print("⚠️  Push failed. This might be expected if you don't have push access.")
        print("   The deployment script is ready for use in GitHub Actions.")
        return
    
    print("\n🎉 Deployment completed successfully!")
    print("Your GitHub Pages site should be available at:")
    print("https://your-username.github.io/your-repo-name/")
    print("\nNote: It may take a few minutes for the changes to appear.")

if __name__ == "__main__":
    main() 