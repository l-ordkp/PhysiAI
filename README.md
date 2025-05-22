# Multi-Agent System with LangGraph

This project implements a modular multi-agent architecture using LangGraph, featuring specialized agents for Retrieval-Augmented Generation (RAG), Email handling, Calendar management, and an Integrated Agent that routes tasks intelligently.

---

## Agents Overview

### 1. RAG Agent

The RAG agent processes user queries through several iterative steps to ensure groundedness and precision:

- Expands the user query for better retrieval
- Retrieves relevant documents/context
- Crafts a response based on retrieved data
- Scores the response for groundedness (relevance to context)
- Refines the response if grounding is weak
- Checks the precision of the response
- Refines the query if precision is low
- Repeats until response meets quality criteria or max iterations reached

**Workflow diagram:**  

![image](https://github.com/user-attachments/assets/9a4d901f-f1ef-4a50-86cb-dff4833c0eff)

### 2. Email Agent

Handles user intents related to email:

- Classifies the user’s intent (send email, summarize unread emails, or end)
- Routes to the appropriate action node
- Executes email sending or unread email summarization

**Workflow diagram:**  
![image](https://github.com/user-attachments/assets/ac93d449-8b17-45e2-a883-837fed33379c)


---

### 3. Calendar Agent

*Implementation placeholder.* Intended for scheduling, event queries, and calendar management.
![image](https://github.com/user-attachments/assets/e723c220-43db-417c-a570-9dcc6ab40709)


### 4. Integrated Agent

Acts as the top-level router, classifying user intent and dispatching to the correct specialized agent:

- Email Agent
- Calendar Agent
- RAG Agent
- Generic Question Handler

**Workflow diagram:**  
![image](https://github.com/user-attachments/assets/a1400711-6f27-4fbb-b3be-097ab2ebced0)


---

## How to Run

```bash
pip install -r requirements.txt
python main.py
