---
title: 
    打包，压缩与解压

tags:
    - Linux
    - 打包
    - 压缩
    - 解压
---

!!! overview
    我在公司的设备上使用 Ubuntu 系统，尝尝有压缩文件、解压文件的需求（虽然有时候在文件资源管理器中双击即可实现解压），但是格式的支持并不丰富

常见的压缩包有很多种格式，在 windows 中常见的有 `.tar`, `.zip` 在各个类型的操作系统中都很常见，Linux 中最常用的格式就是 `.tar.gz`


!!! info 

    其实 `.tar.gz` 的产生需要两步: 
    
    - 首先需要先将目标文件或文件夹打包成单个 `.tar` 包
    - 然后使用 gzip 压缩 `.tar` 包为 `.tar.gz`


### zip 

===  "压缩"
    
    ``` bash
    # 单文件
    zip file.zip file_name

    # 多个文件
    zip files.zip a.txt b.txt c.txt

    # 文件夹
    zip -r project.zip project/

    # 压缩时排除某些文件或目录
    zip -r project.zip project/ -x "*.log"

    zip -r project.zip project/ -x "project/.venv/*"
    
    # 给 zip 包加密码
    zip -r -e secret.zip secret/
    ```

    !!! danger
        zip 加密强度有限，谨慎使用

=== "解压"

    ``` bash
    # 解压到当前目录
    unzip project.zip 

    # 解压到指定目录
    unzip project.zip -d ~/output/

    # 查看包内容不解压
    unzip -l project.zip
    ```


### .tar.gz
其流程是先把需要压缩的文件或文件夹使用 `tar` 打包成单个 `.tar` 包, 然后使用 `gzip` 压缩 `tar` 包,
并且 `gzip` 通常只用于压缩单个文件
===  "压缩"
    
    ``` bash
    tar -czf project.tar.gz project/

    - c: create 创建压缩包
    - z: 使用 gzip
    - f: 指定文件名
    ```

=== "解压"

    ``` bash
    tar -xzf  project.tar.gz

    - x: extract，解包
    - z: 使用 gzip
    - f: 指定文件名

    # 解压到指定目录，需要提前存在
    tar -xzf project.tar.gz -C output/

    # 查看压缩包内容但不解压
    tar -tzf project.tar.gz

    - t: 表示list
    ```


### rar
其多用于 windows 系统，各个 Linux 发行版大多不支持原生 `rar` 格式的压缩，需要先安装工具包：

``` bash
# Linux/Debian
sudo apt update
sudo apt install rar unrar
```

===  "压缩"
    
    ``` bash
    # 单文件
    rar a file.rar file_name

    # 多文件
    rar a files.rar a.txt b.txt c.txt

    # 文件夹
    rar a -r project.rar project/

    # 加密压缩
    rar a -p project.rar project/

    # 连同文件名加密压缩
    rar a -hp project.rar project/

    ```

=== "解压"

    ``` bash
    # 解压到当前目录
    unrar x project.rar

    # 解压到指定目录，不存在会先创建
    unrar x project.rar output/

    # 全部解压到当前目录，会破坏原目录结构
    unrar e project.rar

    # 查看目录内容但不解压
    unrar l project.rar

    # 测试压缩包是否损坏
    unrar t project.rar
    ```


