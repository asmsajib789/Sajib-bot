import os
import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Conversation states
ASK_PHONE = 1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.getenv("7481628411:AAFNNO0jxsND9lu9UK4m_9IPTNOVnJf_7mM")
ADMIN_ID = int(os.getenv("ADMIN_ID", "1798348839"))  # default 0 if not set

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 হ্যালো {user.first_name}! আপনি রেজিস্ট্রেশনের জন্য আপনার মোবাইল নম্বর দিন:"
    )
    return ASK_PHONE

# Get phone number and save lead
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    phone = update.message.text

    lead = f"Name: {user.full_name}\nUsername: @{user.username}\nPhone: {phone}\nID: {user.id}\n---\n"

    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(lead)

    await update.message.reply_text("✅ ধন্যবাদ! আপনার তথ্য রেকর্ড করা হয়েছে।")
    return ConversationHandler.END

# Admin command to see leads
async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ আপনি এই কমান্ড ব্যবহার করতে পারবেন না!")
        return

    if not os.path.exists("leads.txt"):
        await update.message.reply_text("কোনো লিড পাওয়া যায়নি।")
        return

    with open("leads.txt", "r", encoding="utf-8") as f:
        leads_data = f.read()

    if not leads_data:
        await update.message.reply_text("লিড লিস্ট খালি।")
    else:
        await update.message.reply_text(f"📋 লিডস:\n\n{leads_data[:4000]}")  # Telegram msg limit

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ অপারেশন বাতিল করা হয়েছে।")
    return ConversationHandler.END

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("leads", leads))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
