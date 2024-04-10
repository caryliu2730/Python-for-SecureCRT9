# $language = "Python3"
# $interface = "1.0"

# 该代码主要实现crt会话一对一的txt文件内命令行的逐行输入（文件最后留一个回车空行，已保证最后一条命令的执行），
#若代码执行过程中先匹配"#", "]", ">"终端提示符，有继续执行代码，反之中断；其次匹配"error", "invalid", "position"关键字，同理上述；
#若匹配到报错提示符，可进行选择是否继续执行输入；若拒绝执行则保留打开文件内未执行的命令行到名为[error]remaining_commands.txt的文件中（该文件路径与打开文件路径一致）

# 注意点：
# 1.必须开启屏幕不分页显示，思科中兴terminal length.*；华为华三screen-length.*
# 2.请仔细阅读代码作用
# 3.由于crt特性，若想中途退出代码，请在crt的脚本框内选择< 取消 >python代码

import os

def process_line(line):
    crt.Screen.Send(line)
    index = crt.Screen.WaitForStrings(["#", "]", ">", "error", "invalid", "position"])
    if index in [1, 2, 3]:
        crt.Sleep(550)    #crt特性，为同步屏幕执行，加上等待时间；该参数为毫秒，1000ms为 1s,建议可选范围 750-1ms
    elif index == 0:
        crt.Dialog.MessageBox("[均未匹配成功]")
        return True
    elif index in [4, 5, 6]:
        return handle_error()

def handle_error():
    while True:
        input_value = crt.Dialog.MessageBox("当前输出有关键字错误，请确认是否继续执行", "[重要告警]", buttons=4)
        if input_value == 6:
            return False
        elif input_value == 7:
            return True

def main():
    file_path = crt.Dialog.FileOpenDialog("请选择一个文件", "Open", "File.txt", "Log Files (*.txt)|*.txt")
    crt.Screen.Synchronous = True    #根据自我需求选择是否开启屏幕同步；默认为false
    crt.Screen.IgnoreCase = True     #开启全局的不区分大小；默认为false,区分大小写
    error_encountered = False
    remaining_lines = []

    if file_path:
        directory = os.path.dirname(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if not error_encountered:
                    error_encountered = process_line(line)
                else:
                    remaining_lines.append(line)

    if remaining_lines:
        save_remaining_commands(remaining_lines, directory)
    else:
        crt.Dialog.MessageBox("所有命令执行完毕！")
    crt.Screen.Synchronous = False

def save_remaining_commands(remaining_lines, directory):
    file_name = os.path.join(directory, '[error]remaining_commands.txt')
    with open(file_name, 'w') as remaining_file:
        for remaining_line in remaining_lines:
            remaining_file.write(remaining_line)
    crt.Dialog.MessageBox("[重要]已保留所有未执行命令行！")

main()
