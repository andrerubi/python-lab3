from sys import argv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction


hello_msg = "Welcome in AmI Task List 237031 bot!\nHere's a list of commands you can use:\n" \
            "/showTasks - show all the existing tasks in alphabetic order\n" \
            "/newTask - insert a new task\n" \
            "/removeTask - remove a task (by typing its content, exactly)\n" \
            "/removeAllTasks - remove all the existing tasks that contain a provided string\n" \
            "/help - read again this message\n\n" \
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

    if task != "":
        todo.append(task)
        content = open(file_name, "a")
        content.write(task)
        content.write('\n')
        content.close()

        update.message.reply_text("'" + task + "' insert in the list.")
    else:
        update.message.reply_text("You must write a task to be added in the list.")


def remove_task(bot, update, args):
    task = " ".join(args)
    removed = False

    content = open(file_name, "w")
    for t in todo:
        if t != task:  # task not to be deleted
            content.write(task)
            content.write('\n')
        else:
            todo.remove(task)
            update.message.reply_text("'" + task + "' removed")
            removed = True

    if not removed:
        update.message.reply_text("Can't find '" + task + "' in the list")
    content.close()


def remove_all(bot, update, args):
    task = " ".join(args)
    cont = 0  # count of deleted tasks
    remove_list = []

    content = open(file_name, "w")
    for t in todo:

        if task not in t:  # task not to be deleted
            content.write(t)
            content.write('\n')
        else:
            remove_list.append(t)
            cont = cont + 1
    content.close()

    for t in remove_list:
        if t in todo:
            todo.remove(t)

    update.message.reply_text(str(cont) + " task(s) containing '" + task + "' removed\n")


def main():
    updater = Updater(token='TOKEN')  # insert your token instead of TOKEN

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("showTasks", show_task))
    dp.add_handler(CommandHandler("newTask", new_task, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
