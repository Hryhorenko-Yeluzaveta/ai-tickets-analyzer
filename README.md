# 🚀 AI-Powered Tech Support Ticket Analyzer

A smart, lightweight Helpdesk/CRM web application built with Django that uses **Google Gemini AI** to automatically analyze and classify incoming customer support tickets. 

Instead of manual triage, the system instantly reads the customer's message, determines the urgency, analyzes the sentiment, categorizes the issue, and even generates a suggested response for the support agent.

## ✨ Features

* **🤖 AI Triage:** Automatically analyzes incoming tickets using `gemini-3.1-flash-lite-preview` via the modern `google-genai` SDK.
* **📊 Smart Classification:**
  * **Sentiment Analysis:** Positive, Negative, or Neutral.
  * **Urgency Scoring:** High, Medium, or Low.
  * **Auto-Categorization:** Dynamically assigns categories based on context.
  * **Suggested Responses:** Drafts a helpful reply for the agent to use.
* **📋 Dashboard & Pagination:** A clean, responsive Bootstrap 5 interface to view and manage all tickets.
* **🔄 Status Management:** Secure, POST-based ticket state transitions (`New` ➔ `In Progress` ➔ `Done` or `Rejected`).

## 🛠️ Tech Stack

* **Backend:** Python 3.13.2, Django 5+
* **AI Integration:** Google GenAI SDK (`google-genai`)
* **Frontend:** HTML5, Bootstrap 5 (Responsive UI, Flexbox, Grid)
* **Database:** PostgreSQL

## ⚙️ Prerequisites

* Python 3.10+
* A valid [Google Gemini API Key](https://aistudio.google.com/app/apikey)