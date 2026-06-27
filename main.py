import customtkinter as ctk
import tweepy
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime

# Simple config - user fills these once
X_API_KEY = "YOUR_X_API_KEY"
X_API_SECRET = "YOUR_X_API_SECRET"
X_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
X_ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

EMAIL_SENDER = "your@email.com"
EMAIL_PASSWORD = "your_app_password"  # Use app password for Gmail etc.
EMAIL_RECEIVERS = ["fan1@example.com", "fan2@example.com"]  # Add your list here or load from file

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AutoShareApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoShareSuite - Post Everywhere Easy")
        self.geometry("700x600")
        
        # Title
        title = ctk.CTkLabel(self, text="AutoShareSuite", font=("Arial", 28, "bold"))
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(self, text="Type once. Share everywhere. Grow your music.", font=("Arial", 14))
        subtitle.pack()
        
        # Post composer
        self.post_text = ctk.CTkTextbox(self, height=120, width=650, font=("Arial", 14))
        self.post_text.pack(pady=10)
        self.post_text.insert("0.0", "New music out now! Check it out: ")
        
        self.link_entry = ctk.CTkEntry(self, placeholder_text="Paste your song link here", width=650)
        self.link_entry.pack(pady=5)
        
        # Platforms frame
        platforms_frame = ctk.CTkFrame(self)
        platforms_frame.pack(pady=10)
        
        self.x_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(platforms_frame, text="X (Twitter)", variable=self.x_var).pack(side="left", padx=10)
        
        self.email_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(platforms_frame, text="Email List", variable=self.email_var).pack(side="left", padx=10)
        
        # Note about other platforms
        note = ctk.CTkLabel(self, text="(Instagram, TikTok etc. coming in next updates - start with X + Email)", font=("Arial", 11))
        note.pack()
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=15)
        
        send_btn = ctk.CTkButton(button_frame, text="Send Now", command=self.send_now, width=150, height=40, font=("Arial", 16))
        send_btn.pack(side="left", padx=10)
        
        schedule_btn = ctk.CTkButton(button_frame, text="Schedule for Later", command=self.schedule_post, width=180, height=40, font=("Arial", 16))
        schedule_btn.pack(side="left", padx=10)
        
        # Status
        self.status_label = ctk.CTkLabel(self, text="Ready. Connect your accounts in the code file first.", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Instructions
        help_text = ctk.CTkLabel(self, text="1. Edit main.py with your X keys and email details once.\n2. Type your message above.\n3. Paste link.\n4. Check platforms.\n5. Hit Send Now or Schedule.", justify="left")
        help_text.pack(pady=10)
    
    def send_now(self):
        post = self.post_text.get("0.0", "end").strip()
        link = self.link_entry.get().strip()
        full_message = f"{post} {link}"
        
        success = []
        
        if self.x_var.get():
            if self.post_to_x(full_message):
                success.append("X")
        
        if self.email_var.get():
            if self.send_email(full_message):
                success.append("Email")
        
        if success:
            self.status_label.configure(text=f"Sent to: {', '.join(success)} at {datetime.now().strftime('%H:%M')}")
        else:
            self.status_label.configure(text="Nothing selected or error. Check your keys.")
    
    def post_to_x(self, message):
        try:
            client = tweepy.Client(
                consumer_key=X_API_KEY,
                consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )
            client.create_tweet(text=message)
            return True
        except Exception as e:
            self.status_label.configure(text=f"X error: {str(e)}")
            return False
    
    def send_email(self, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = "New from IAMBANDOBANDZ"
            msg['From'] = EMAIL_SENDER
            msg['To'] = ", ".join(EMAIL_RECEIVERS)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
            return True
        except Exception as e:
            self.status_label.configure(text=f"Email error: {str(e)}")
            return False
    
    def schedule_post(self):
        # Simple example - schedule in 1 hour
        schedule.every().hour.do(self.send_now)
        self.status_label.configure(text="Scheduled! It will run on timer. Keep app open.")
        # In real version this would be more advanced

if __name__ == "__main__":
    app = AutoShareApp()
    app.mainloop()