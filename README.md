# Python Telegram Bot

A simple bot built using the python-telegram-bot library that responds to user messages.

## Setup

1. Clone the repository:

   ```bash
   git clone
   ```

2. Navigate to the project directory:

   ```bash
   cd python-telegram-bot
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Telegram bot token:

   ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

5. Activate your virtual environment (if using one):

   ```bash
   python3 -m venv venv # Create a virtual environment
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

6. Run the bot:

   ```bash
   python bot.py
   ```

7. To update requirements, use:

   ```bash
   pip freeze > requirements.txt
   ```
