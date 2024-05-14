import subprocess


def run(command, timeout=10):
    """执行终端命令

    Args:
        command (str, optional): 命令，比如ssh ns "df -Th".
    """
    try:
        # 执行命令并设置超时
        result = subprocess.run(command, shell=True, capture_output=True,
                                text=True, timeout=timeout, check=True)
        # 打印标准输出
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("命令执行超时")
    except subprocess.CalledProcessError as e:
        print(f"命令返回非零退出状态: {e.returncode}")
        print(f"标准错误输出: {e.stderr}")
    except Exception as e: # pylint: disable=w0718
        print(f"命令执行时发生错误: {e}")
    
    return ""
