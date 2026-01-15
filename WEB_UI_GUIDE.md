# Web UI User Guide

## Overview

The Document Processing System includes a user-friendly web interface built with Streamlit. Access all features through your browser without using command-line tools.

## Starting the Web UI

### Quick Start

```bash
# Make sure you have set your API key in .env
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start the web application
./start_app.sh
```

Or manually:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Features

### Home Page
- Overview of the two-stage processing pipeline
- Quick navigation to all features
- Configuration status check
- Getting started guide

### Stage 1: Analysis Page (`/Stage_1_Analysis`)

**Upload Documents**
1. Click "Browse files" or drag-and-drop Word documents (.docx)
2. Upload one or multiple documents
3. Provide analysis instructions
4. Choose to save analysis report and/or JSON

**Run Analysis**
- Click "Run Stage 1 Analysis"
- Wait for Claude AI to process (typically 30-60 seconds)
- View results on the same page

**Results Display**
- Document metrics (count, total words, themes)
- 5 suggested keywords with primary marked
- Identified themes with descriptions
- NLP entities (nouns, verbs, adjectives) organized in tabs
- Semantic analysis (search considerations, attributes)
- Content preview
- Download options (JSON format)

**Navigation**
- Download results as JSON
- Continue to Stage 2 for rewriting
- Start a new analysis

### Stage 2: Rewriting Page (`/Stage_2_Rewriting`)

**Prerequisites**
- Stage 1 results (from current session or uploaded JSON file)

**Load Results**
- Automatically uses current session's Stage 1 results
- OR upload a previously saved Stage 1 JSON file

**Configuration Modes**

**1. Auto-Population (Easy)**
- Provide only required fields:
  - Article Topic
  - Primary Keyword (auto-suggested from Stage 1)
  - Article Title (H1)
- All other parameters filled from Stage 1 analysis
- Perfect for quick content generation

**2. Full Customization (Advanced)**
- Override all SEO parameters:
  - Word count target
  - Number of lists
  - Target audience
  - Output format (docx, txt, md)
  - Custom filename
- Override NLP entities:
  - Nouns, verbs, adjectives lists
- SEO optimization:
  - Keyword frequency
  - Section headings
  - LSI terms
- Additional parameters:
  - Search considerations
  - Content attributes
  - Characteristics

**Features**
- Preview prompt before running (checkbox option)
- Additional custom instructions field
- Real-time parameter validation

**Run Rewriting**
- Click "Run Stage 2 Rewriting"
- Wait for Claude AI to generate content (1-2 minutes)
- View generated content on the same page

**Results Display**
- Metadata (topic, keyword, word count)
- Full generated content in text area
- Download options:
  - Plain text (.txt)
  - Markdown (.md)
  - Word document (.docx) - saved to output folder
- Navigation to detailed views

### Full Pipeline Page (`/Full_Pipeline`)

**All-in-One Processing**
- Combines Stage 1 and Stage 2
- Fastest way to get results
- Single upload, single configuration

**Setup**
1. Upload documents
2. Provide Stage 1 analysis instruction
3. Fill in Stage 2 required fields:
   - Article Topic
   - Primary Keyword
   - Article Title

**Additional Options** (expandable)
- Word count, number of lists
- Target audience
- Output format
- Custom filename
- Additional rewriting instructions

**Execution**
- Progress bar shows current stage
- Real-time status updates
- Automatic transition between stages

**Results**
- Overall metrics dashboard
- Stage 1 summary (keywords, themes)
- Stage 2 summary (title, topic, word count)
- Content preview
- Multiple download options
- Links to detailed results

## Tips and Best Practices

### For Best Analysis Results
- Upload related documents on the same topic
- Provide clear, specific analysis instructions
- Use 2-5 documents for optimal analysis
- Save Stage 1 JSON for reuse

### For Best Rewriting Results
- Review Stage 1 keywords before proceeding
- Start with Auto-Population mode
- Use descriptive article titles
- Preview prompts to verify parameters
- Test with different configurations

### Performance Tips
- Larger documents take longer to process
- Multiple documents increase processing time
- Stage 1: ~30-60 seconds per batch
- Stage 2: ~1-2 minutes per article
- Save Stage 1 results to avoid re-analysis

### File Management
- **Uploads folder**: Temporary document storage
- **Output folder**: Generated files (.docx, reports, JSON)
- Download important files before clearing folders
- JSON files enable result reuse

## Keyboard Shortcuts

- `Ctrl+R` / `Cmd+R`: Refresh page
- `Ctrl+K` / `Cmd+K`: Focus search/filter
- `Esc`: Close expandable sections

## Troubleshooting

### Application Won't Start

**Issue**: "ANTHROPIC_API_KEY not found"
**Solution**:
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your API key
3. Restart the application

**Issue**: "Module not found"
**Solution**:
```bash
pip install -r requirements.txt
```

### Upload Issues

**Issue**: "Unsupported file format"
**Solution**: Only .docx files are supported. Convert .doc files to .docx

**Issue**: "File too large"
**Solution**: File size limit is 10MB per document (configurable in config.py)

### Processing Errors

**Issue**: "API error" or timeout
**Solution**:
- Check your API key is valid
- Verify internet connection
- Try with fewer/smaller documents

**Issue**: "No JSON found in response"
**Solution**:
- This is handled automatically with fallback
- Results still available in text format
- Review raw response for debugging

### Results Issues

**Issue**: Missing download button
**Solution**: Scroll down - results appear below the form

**Issue**: Cannot find saved files
**Solution**: Check `./output` folder in application directory

## Advanced Usage

### Reusing Stage 1 Results

1. Run Stage 1 analysis once
2. Download JSON file
3. Run Stage 2 multiple times with different parameters:
   - Different topics
   - Different audiences
   - Different formats
4. Generate multiple articles from one analysis

### Batch Processing

1. Use Full Pipeline for maximum efficiency
2. Process multiple document sets sequentially
3. Save all Stage 1 JSONs for later use
4. Generate content library from analyses

### Integration with Other Tools

**Export to CMS**
- Download as Markdown
- Copy content directly
- Import into WordPress, Medium, etc.

**SEO Tools**
- Export keywords from Stage 1
- Use in keyword research tools
- Track rankings for suggested keywords

**Content Calendar**
- Generate multiple versions
- Schedule across platforms
- Repurpose for different channels

## Deployment Options

### Local Deployment (Current)
```bash
streamlit run app.py
```
Accessible at `http://localhost:8501`

### Network Deployment
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```
Accessible from other devices on your network

### Production Deployment

**Using Streamlit Cloud**
1. Push repository to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Configure secrets for API key
4. Deploy automatically

**Using Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Using Cloud Platforms**
- Deploy to AWS, Google Cloud, Azure
- Use container services (ECS, Cloud Run, Container Apps)
- Configure environment variables
- Set up HTTPS with SSL

## Security Considerations

1. **API Key Protection**
   - Never commit `.env` file
   - Use environment variables in production
   - Rotate keys regularly

2. **File Uploads**
   - Files stored temporarily
   - Cleared on application restart
   - No persistent user data

3. **Network Access**
   - Default: localhost only
   - Configure firewall for network deployment
   - Use HTTPS in production

## Support and Resources

- **Documentation**: See README.md and USAGE_GUIDE.md
- **Architecture**: See ARCHITECTURE.md
- **Examples**: Check `examples/` folder
- **Issues**: Report at your repository's issue tracker

## Updates and Maintenance

### Updating the Application
```bash
git pull
pip install -r requirements.txt --upgrade
```

### Clearing Cache
```bash
streamlit cache clear
```

### Resetting State
- Refresh browser page
- Or use "New Analysis"/"New Rewrite" buttons

---

**Enjoy using the Document Processing System Web UI!**

For CLI usage, see USAGE_GUIDE.md
