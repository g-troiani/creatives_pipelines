# Creatives Pipelines

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Configuration](#configuration)
  - [Advanced Usage](#advanced-usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Creatives Pipelines is a comprehensive system designed to automate the scraping, processing, and summarization of news and media content from various sources such as Hacker News, TechCrunch, and YouTube. The project leverages advanced NLP techniques and integrates multiple APIs to provide insightful summaries and analyses.

## Features

- Scraping news articles from Hacker News and TechCrunch
- Processing and summarizing YouTube videos
- Named Entity Recognition (NER) and Entity Relation Extraction (ERE)
- Syntactic analysis of text content
- Generating formatted summaries
- Storing processed data in SQLite databases
- Visualizing data with Neo4j

## Installation

To install and set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/g-troiani/creatives_pipelines.git
   cd creatives_pipelines

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required dependencies:
pip install -r requirements.txt

## Usage
Basic Usage
To run the main pipeline and start scraping and processing data, use the following command:

python ai_news_main.py

## Configuration
Ensure that you have the necessary API keys and configurations set up in environment variables or a configuration file. The required environment variables include:

OPENAI_API_KEY
GOOGLE_API_KEY
ANTHROPIC_API_KEY
YOUTUBE_API_KEY
SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD (for email notifications)

## Advanced Usage
To run individual components or modules, you can execute specific scripts. For example:

Scraping Hacker News:
python scrapers/ai_news_scrapers/hackernews_scraper/scrape_hacker_news.py

Processing YouTube videos:
python youtube_processor.py

## Project Structure
The project is organized as follows:


creatives_pipelines/
│
├── api/
│   ├── __init__.py
│   ├── anthropic_api.py
│   ├── google_api.py
│   ├── openai_api.py
│
├── ai_news_google_api/
│   ├── __init__.py
│   ├── generate_formatted_summary.py
│   ├── generate_hackernews_summary.py
│   ├── generate_summary.py
│   ├── generate_video_highlights.py
│   ├── perform_ere.py
│   ├── perform_ner.py
│   ├── perform_syntactic_analysis.py
│   ├── translate_video_highlights.py
│
├── scrapers/
│   ├── ai_news_scrapers/
│   │   ├── hackernews_scraper/
│   │   ├── techcrunch_scraper/
│   │   ├── youtube_api_scraper/
│
├── utils/
│   ├── __init__.py
│   ├── ai_news_content_creation.py
│   ├── api_utils.py
│   ├── email_sender.py
│   ├── nlp_utils.py
│   ├── report_generator.py
│   ├── ai_news_neo4j/
│   │   ├── __init__.py
│   │   ├── neo4j_utils.py
│   │   ├── neo4j_visualization.py
│   ├── database/
│   │   ├── ai_news_database/
│   │   │   ├── __init__.py
│   │   │   ├── create_daily_report_table.py
│   │   │   ├── create_hacker_news_table.py
│   │   │   ├── create_tables.py
│   │   │   ├── create_techcrunch_table.py
│   │   │   ├── create_video_highlights_table.py
│   │   │   ├── store_video_data.py
│   │   │   ├── store_video_highlights.py
│   ├── graph/
│   │   ├── ai_news_graph/
│   │   │   ├── __init__.py
│   │   │   ├── create_ere_table.py
│   │   │   ├── create_ner_table.py
│   │   │   ├── create_syntactic_table.py
│   │   │   ├── store_ere_data.py
│   │   │   ├── store_ner_data.py
│   │   │   ├── store_syntactic_data.py
│
├── pyautogui_images/
├── ai_news_main.py
├── generate_instagram_creatives.py
├── generate_video.py
├── graph_processor.py
├── ig_poster.py
├── requirements.txt
├── youtube_processor.py

## Contributing
We welcome contributions to improve the project. To contribute, please follow these steps:

Fork the repository:
git fork https://github.com/g-troiani/creatives_pipelines.git

Create a feature branch:
git checkout -b feature-branch


Commit your changes:
git commit -m "Add new feature"

Push to the branch:
git push origin feature-branch

Create a pull request:
Go to the repository on GitHub and open a pull request.

