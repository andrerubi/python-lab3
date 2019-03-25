from sys import argv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction


hello_msg = "Welcome in AmI Task List 237031 bot!\nHere's a list of commands you can use:\n" \
            "/showTasks - show all the existing tasks in alphabetic order\n" \
            "/newTask - insert a new task\n" \
            "/removeTask: remove a task (by typing its content, exactly)\n" \
            "/removeAllTasks: remove all the existing tasks that contain a provided string\n\n" \
            "All the commands are executed on the 'task_list.txt' file"

# getting the to do list
file_name = argv[1]
content = open(file_name)
todo = content.read().split('\n')  # creating the list from input file
content.close()


def start(bot, update):
    update.message.reply_text(hello_msg)


def echo(bot, update):
    update.message.reply_text("I'm sorry. I can't do that.")


def show_task(bot, update):
    update.message.reply_text("Here's the list of to do tasks:\n")
    output_msg = "Nothing to do, here!"

    if len(todo) != 0:
        output_msg = ""
        for task in todo:
            output_msg = output_msg + task + "\n"

    update.message.reply_text(output_msg)


def new_task(bot, update, args):
    task = " ".join(args)
    todo.append(task)

    content = open(file_name, "a")
    content.write(task)
    content.write('\n')
    content.close()


def remove_task(bot, update):
    update.message.reply_text("Remove")


def remove_all(bot, update):
    update.message.reply_text("Remove")


def main():
    updater = Updater(token='TOKEN')

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", show_task))
    dp.add_handler(CommandHandler("newTask", new_task, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
