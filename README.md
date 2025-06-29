# Academic Paper Monitor

A Python tool that monitors new academic papers in computer vision research fields including Structure from Motion (SFM), SLAM, 3D Gaussian Splatting (3DGS), and Neural Radiance Fields (NeRF). The tool can send notifications via Slack and deploy results to GitHub Pages.

## Features

- 🔍 **Multi-field monitoring**: Tracks papers in SFM, SLAM, 3DGS, and NeRF research areas
- 📧 **Email notifications**: Send reports via email (Gmail SMTP)
- 💬 **Slack integration**: Send notifications to Slack channels via webhooks
- 🌐 **GitHub Pages deployment**: Automatically deploy results to a web page
- 🤖 **Automated scheduling**: Run daily via GitHub Actions
- 📊 **Web reports**: Generate beautiful HTML reports for web viewing

## Research Fields Monitored

- **SFM (Structure from Motion)**: Bundle adjustment, visual SLAM, 3D reconstruction
- **SLAM (Simultaneous Localization and Mapping)**: Visual odometry, loop closure, mapping
- **3DGS (3D Gaussian Splatting)**: Neural splatting, 3D rendering, point cloud processing
- **NeRF (Neural Radiance Fields)**: Neural rendering, novel view synthesis, 3D scene representation

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/academic-paper-monitor.git
cd academic-paper-monitor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Monitor

Edit `config.json` to set up your preferences:

```json
{
  "email": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_emails": ["your-email@gmail.com"]
  },
  "slack": {
    "enabled": true,
    "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "channel": "#papers",
    "username": "Paper Monitor Bot"
  },
  "monitoring": {
    "days_back": 7,
    "max_results_per_query": 30,
    "categories": ["cs.CV", "cs.RO", "cs.GR", "cs.AI", "cs.LG"]
  },
  "github": {
    "enabled": true,
    "repo_name": "your-username/academic-paper-monitor",
    "branch": "main",
    "pages_branch": "gh-pages",
    "token": "your-github-token"
  }
}
```

### 4. Run the Monitor

```bash
python paper_monitor.py
```

## Setup Instructions

### Slack Integration

1. **Create a Slack App**:
   - Go to [api.slack.com/apps](https://api.slack.com/apps)
   - Click "Create New App" → "From scratch"
   - Give it a name like "Paper Monitor"

2. **Enable Incoming Webhooks**:
   - Go to "Features" → "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" to On
   - Click "Add New Webhook to Workspace"
   - Choose the channel where you want notifications
   - Copy the webhook URL

3. **Configure the Monitor**:
   - Set `slack.enabled` to `true` in `config.json`
   - Paste your webhook URL in `slack.webhook_url`
   - Set your preferred channel in `slack.channel`

### GitHub Pages Deployment

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages" section
   - Set source to "Deploy from a branch"
   - Select "gh-pages" branch
   - Save the settings

2. **Set up GitHub Actions**:
   - The workflow file `.github/workflows/paper-monitor.yml` is already included
   - It will run daily at 9 AM UTC
   - You can also trigger it manually from the Actions tab

3. **Configure Secrets** (for automated deployment):
   - Go to repository settings → "Secrets and variables" → "Actions"
   - Add `SLACK_WEBHOOK_URL` with your Slack webhook URL
   - `GITHUB_TOKEN` is automatically provided by GitHub Actions

### Email Notifications (Optional)

1. **Gmail Setup**:
   - Enable 2-factor authentication on your Gmail account
   - Generate an App Password: Google Account → Security → App passwords
   - Use the app password in `config.json`

2. **Configure Email**:
   - Set `email.enabled` to `true`
   - Add your Gmail credentials
   - Add recipient email addresses

## Configuration Options

### Monitoring Settings

- `days_back`: How many days back to search for papers (default: 7)
- `max_results_per_query`: Maximum papers per search query (default: 30)
- `categories`: arXiv categories to search in (default: cs.CV, cs.RO, cs.GR, cs.AI, cs.LG)

### Custom Research Fields

You can modify the `search_queries` in `paper_monitor.py` to monitor different research areas:

```python
self.search_queries = {
    "Your Field": ["keyword1", "keyword2", "keyword3"],
    # ... other fields
}
```

## Output Files

The monitor generates several output files:

- `report.txt`: Plain text report of new papers
- `index.html`: Web-friendly HTML report
- `papers_data.json`: Internal data tracking seen papers
- `deploy.sh`: Deployment script (if GitHub deployment is enabled)

## GitHub Actions

The included workflow will:

1. Run daily at 9 AM UTC
2. Install dependencies
3. Run the paper monitor
4. Send Slack notifications
5. Deploy results to GitHub Pages
6. Upload reports as artifacts

You can also trigger the workflow manually from the Actions tab in your repository.

## Troubleshooting

### Common Issues

1. **Slack notifications not working**:
   - Verify your webhook URL is correct
   - Check that the channel exists and the bot has access
   - Ensure `slack.enabled` is set to `true`

2. **GitHub Pages not updating**:
   - Check that GitHub Pages is enabled for the gh-pages branch
   - Verify the workflow is running successfully
   - Check the Actions tab for any errors

3. **No papers found**:
   - Try increasing `days_back` in the configuration
   - Check that the arXiv categories are correct
   - Verify your internet connection

### Logs

The monitor provides detailed logging. Check the console output for:
- Number of papers found per field
- Notification delivery status
- Any errors during execution

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 