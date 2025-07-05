# GitHub Deployment Guide

## Quick Setup (5 minutes)

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `academic-paper-monitor`
3. Make it **PUBLIC** (required for GitHub Pages)
4. **DO NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

### 2. Push Your Code

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/academic-paper-monitor.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository → Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `gh-pages`
4. Click "Save"

### 4. Test the Workflow

1. Go to your repository → Actions
2. Click "Paper Monitor" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for it to complete (about 2-3 minutes)

## What Happens Next

### Automated Daily Runs
- The workflow runs **daily at 9 AM UTC**
- Searches for new papers in SFM, SLAM, 3DGS, and NeRF
- Generates HTML report and deploys to GitHub Pages
- Uploads reports as artifacts

### Your Website
- Available at: `https://YOUR_USERNAME.github.io/academic-paper-monitor/`
- Updates automatically after each run
- Shows latest papers with links to arXiv

### Manual Triggers
- Go to Actions → Paper Monitor → "Run workflow"
- Useful for testing or immediate updates

## Monitoring

### Check Workflow Status
- Repository → Actions tab
- Green checkmark = success
- Red X = failure (check logs)

### View Generated Reports
- Actions → Paper Monitor → Artifacts
- Download `paper-report.zip` to see text and HTML reports

### Website Updates
- Takes 1-2 minutes after workflow completes
- Check your GitHub Pages URL for latest papers

## Troubleshooting

### Workflow Fails
1. Check Actions tab for error messages
2. Common issues:
   - Network timeout (retry manually)
   - Python dependency issues (check requirements.txt)

### Website Not Updating
1. Verify GitHub Pages is enabled
2. Check gh-pages branch exists
3. Wait 2-3 minutes for deployment

### No Papers Found
1. Check monitoring settings in config.json
2. Try increasing `days_back` value
3. Verify arXiv categories are correct

## Configuration

### Modify Search Fields
Edit `paper_monitor.py` → `search_queries` dictionary:

```python
self.search_queries = {
    "Your Field": ["keyword1", "keyword2"],
    # ... other fields
}
```

### Change Schedule
Edit `.github/workflows/paper-monitor.yml` → `cron` line:

```yaml
- cron: '0 9 * * *'  # Daily at 9 AM UTC
```

### Adjust Monitoring
Edit `config.json`:
- `days_back`: How many days to search
- `max_results_per_query`: Papers per search
- `categories`: arXiv categories to search

## Next Steps

Once deployed, you can:
1. Add Slack integration later
2. Customize research fields
3. Add email notifications
4. Modify the schedule
5. Customize the HTML template

Your paper monitor will now run automatically and keep you updated on the latest research! 🎉 