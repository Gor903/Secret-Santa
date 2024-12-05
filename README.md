# Secret Santa 🎅🎁

This project helps organize and manage a **Secret Santa** event.

Send **/start** command to your bot.
When all users have registered successfully, send **/notify** command, then **/shufle**.

**Happy New Year🎄**

---

## 📥 How to Clone the Repository

To clone this repository, follow these steps:

1. Open your terminal (Command Prompt, Git Bash, or similar).
2. Navigate to the directory where you want to store the project.
3. Run the following command:
   ```bash
   git clone https://github.com/Gor903/Secret-Santa.git
   ```

## ❄️ How to run

To run the project, follow these steps:

1. Create .env file.
    ```bash
    touch .env
    ```
2. Your .env file should look like this.
    ```bash
    TOKEN="Telegram bot's token"

    DB_USERNAME="db-username"
    DB_PASSWORD="sb-password"
    DB_NAME="sb-name"
    ```
3. Run the following commands:
   ```bash
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. And last step
    ```bash
    python main.py
    ```