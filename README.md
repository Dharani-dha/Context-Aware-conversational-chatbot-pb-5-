# Context-Aware Conversational Chatbot (Problem Statement 5)

This project implements a multi-turn conversational customer support chatbot based on the exact requirements of Problem Statement 5.

## Included Deliverables
As requested by the problem statement, all deliverables have been created:
1. **Conversation Flow**: I have created `conversation_flow.md` which includes a Mermaid state diagram outlining the conversation states.
2. **Context Management Design**: I have created `context_management_design.md` explaining how user session states, entity variables (like order IDs), and chat history are securely retained.
3. **Sample Dialogues**: Examples are provided in `sample_dialogues.md`.
4. **Chatbot Implementation**: The fully functional codebase is in `chatbot.py`.

## Features Implemented
- **Intent Recognition**: Recognizes intents like greetings, tracking orders, and requesting refunds.
- **Context Memory**: Actively remembers variables (like an `order_id` you mentioned 2 turns ago) so you don't have to repeat yourself.
- **Coherent Dialogue Handling**: Uses a State Machine to smoothly ask for missing information if you omit it (e.g., asking for your order ID if you just say "track my order").

## How to Run the Project
1. Open your terminal in VS Code (or PowerShell).
2. Ensure you are in the correct directory:
   ```bash
   cd C:\Users\kanch\OneDrive\Desktop\placement
   ```
3. Run the Python script:
   ```bash
   python chatbot.py
   ```
4. You can now chat directly with the bot! You can test flows like:
   - "track my order" -> It will ask for an ID -> give an ID like "XYZ12345" -> It will give you tracking info.
   - "refund my order" -> It will remember the "XYZ12345" ID from your earlier message and process it seamlessly.
Type `quit` or `exit` to stop the bot.
