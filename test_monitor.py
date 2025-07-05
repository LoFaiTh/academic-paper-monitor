#!/usr/bin/env python3
"""
Test script for the Academic Paper Monitor
"""

import json
import sys
import arxiv
from paper_monitor import PaperMonitor

def test_config_loading():
    """Test configuration loading"""
    print("Testing configuration loading...")
    try:
        monitor = PaperMonitor()
        print("✅ Configuration loaded successfully")
        print(f"   - Monitoring {len(monitor.search_queries)} research fields")
        print(f"   - Email notifications: {'enabled' if monitor.config['email']['enabled'] else 'disabled'}")
        print(f"   - Slack notifications: {'enabled' if monitor.config['slack']['enabled'] else 'disabled'}")
        print(f"   - GitHub deployment: {'enabled' if monitor.config['github']['enabled'] else 'disabled'}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_arxiv_connection():
    """Test arXiv API connection"""
    print("\nTesting arXiv API connection...")
    try:
        monitor = PaperMonitor()
        # Test a simple search
        search = arxiv.Search(
            query="computer vision",
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        results = list(monitor.client.results(search))
        if results:
            print("✅ arXiv API connection successful")
            print(f"   - Found paper: {results[0].title[:50]}...")
            return True
        else:
            print("❌ No results from arXiv API")
            return False
    except Exception as e:
        print(f"❌ arXiv API connection failed: {e}")
        return False

def test_slack_config():
    """Test Slack configuration"""
    print("\nTesting Slack configuration...")
    try:
        monitor = PaperMonitor()
        if monitor.config['slack']['enabled']:
            webhook_url = monitor.config['slack']['webhook_url']
            if webhook_url and webhook_url != "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK":
                print("✅ Slack webhook URL configured")
                return True
            else:
                print("⚠️  Slack enabled but webhook URL not configured")
                return False
        else:
            print("ℹ️  Slack notifications disabled")
            return True
    except Exception as e:
        print(f"❌ Slack configuration test failed: {e}")
        return False

def test_github_config():
    """Test GitHub configuration"""
    print("\nTesting GitHub configuration...")
    try:
        monitor = PaperMonitor()
        if monitor.config['github']['enabled']:
            repo_name = monitor.config['github']['repo_name']
            if repo_name and repo_name != "your-username/academic-paper-monitor":
                print("✅ GitHub repository configured")
                return True
            else:
                print("⚠️  GitHub enabled but repository not configured")
                return False
        else:
            print("ℹ️  GitHub deployment disabled")
            return True
    except Exception as e:
        print(f"❌ GitHub configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Academic Paper Monitor - Test Suite")
    print("=" * 50)
    
    tests = [
        test_config_loading,
        test_arxiv_connection,
        test_slack_config,
        test_github_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Configure your Slack webhook URL in config.json")
        print("2. Set up GitHub Pages in your repository settings")
        print("3. Add SLACK_WEBHOOK_URL to your GitHub repository secrets")
        print("4. Run: python paper_monitor.py")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main() 