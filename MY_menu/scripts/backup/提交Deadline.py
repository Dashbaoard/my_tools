import subprocess
import os
import maya.cmds as cmds
# 指定JobInfo文件路径
job_info_path = r'U:\temp\zjd\MY_menu\scripts\ScriptPackages\JobInfo.job'
plugin_info_path = r'U:\temp\zjd\MY_menu\scripts\ScriptPackages\PluginInfo.job'

username = os.getlogin()
SceneFile=cmds.file(query=True,loc=True)
FilePath=os.path.dirname(SceneFile)
SceneBasename=os.path.basename(SceneFile)
SceneName=os.path.splitext(SceneBasename)[0]


FileDirSplit = os.path.normpath(FilePath).split(os.sep)


outputPath = r'W:\{}\renders\{}\{}\3d\lgt'.format(FileDirSplit[1], FileDirSplit[2], FileDirSplit[3])
print(outputPath)

startFrame=cmds.getAttr('defaultRenderGlobals.startFrame')
endFrame=cmds.getAttr('defaultRenderGlobals.endFrame')
Frames=f'{int(startFrame)}-{int(endFrame)}'
print(Frames)

# 定义要修改的参数及其新值
job_params_to_modify = {
    'Name': SceneName,
    'OutputDirectory0': outputPath,
    'UserName': username,
    'Frames': Frames
}

plugin_params_to_modify = {
    'ProjectPath': FilePath,
    'SceneFile': SceneFile,
    'OutputFilePath': outputPath
    
}

# 函数用于修改文件中的参数
def modify_file_params(file_path, params_to_modify):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        # 检查是否需要修改这一行
        for param in params_to_modify:
            if line.strip().startswith(param):
                # 修改参数
                new_lines.append(f"{param}={params_to_modify[param]}\n")
                break
        else:
            # 如果没有找到要修改的参数，保持原样
            new_lines.append(line)
    
    # 写回修改后的内容
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    print(f"Updated {file_path}")

# 修改JobInfo文件
modify_file_params(job_info_path, job_params_to_modify)

# 修改PluginInfo文件
modify_file_params(plugin_info_path, plugin_params_to_modify)




def submit_single_job(job_info_path, plugin_info_path):
    # 请确保替换为实际的 Deadline 安装目录路径
    deadline_install_dir = r'C:\Program Files\Thinkbox\Deadline10\bin'
    deadline_path = os.path.join(deadline_install_dir, 'deadlinecommand.exe')
    
    submit_cmd = f'"{deadline_path}" "{job_info_path}" "{plugin_info_path}"'
    
    try:
        with subprocess.Popen(submit_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"Error submitting job: {stderr.decode()}")
            jobID_lines = stdout.decode().splitlines()
            for line in jobID_lines:
                if line.startswith('JobID'):
                    jobID = line.lstrip('JobID=').rstrip('\r\n').strip()
                    return jobID
    except Exception as e:
        print(f"An exception occurred: {e}")
        return None


#JobInfoPath=r'X:\TLD\RCY\1550\3d\lgt\lgt\work\backup\JobInfo.job'
#PluginInfoPath=r'X:\TLD\RCY\1550\3d\lgt\lgt\work\backup\PluginInfo.job'
submit_single_job(job_info_path,plugin_info_path)
