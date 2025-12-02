# Week 10: AI Integration in Multi-Domain Intelligence Platform

**Student Name:** Amal Krishna Mangalappilly Udhayakumar
**Student ID:** M01092986
**Course:** BSc Information Technology

## Project Description

In Week 10, the platform was enhanced with AI-powered assistants integrated into each domain dashboard. Users can now interact with AI to get insights, guidance, and analysis directly within the dashboards.

## Features

### Domain AI Assistants

- Cybersecurity Dashboard: Analyze incidents, threats, and provide technical guidance
- Data Science Dashboard: Assist with data analysis, visualization, and statistical insights
- IT Operations Dashboard: Help troubleshoot issues, optimize systems, and manage tickets

### AI Chat Functionality

- Chat available in a sidebar for each dashboard
- Separate chat history per dashboard
- Clear Chat button to reset conversations
- Powered by OpenAI GPT-4.1-mini

### Implementation Notes

- API key securely stored in `.env` (OPENAI_API_KEY)
- Uses streamlit for the UI and openai Python package for AI interaction
- Session state manages chat history independently for each domain
