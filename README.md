### Install dependencies

If you have selected install_dependencies during the prompt, you can skip this part.

1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.
    ```
    $ virtualenv venv
    $ . venv/bin/activate
    ```
    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```

### 测试三个数据集的可视化效果

在test_vis_result.py文件中，我写了三小段代码，分别对应三个数据集的可视化效果，如果想要查看一个数据集的效果，就把另外两段注释掉，然后执行
```
$ python test_vis_result.py
```
   