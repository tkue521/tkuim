## LINUX 作業系統的樹莓派練習

當你燒錄好樹莓派的 micro SD 卡後，將卡插入樹莓派並接上螢幕、鍵盤、滑鼠和電源。等開機完後按 `ctrl+alt+t` 或是直接點上面的終端機圖示來開啟終端機。

1. 接著請在終端機裡輸入以下指令

    ```bash
    git clone https://github.com/tkue521/tkuim.git
    cd tkuim
    ```
2. 輸入 `ls` 來觀察資料夾裡的內容

    > README.md  cat_detector.py  catmeme.jpeg  haarcascade_frontalcatface.xml  images/  install.sh
3. 各檔案及其功能說明如下

    |檔案名稱|說明|
    |--|--|
    |README.md|你現在正在看的說明檔|
    |cat_detector.py|執行影像辨識的 Python 程式|
    |haarcascade_frontalcatface.xml|影像辨識的分類器|
    |images/|存放待辨識圖片的資料夾|
    |install.sh|安裝所需依賴套件的腳本|
4. 我們先將所需要之依賴套件裝起來，請輸入

    ```bash
    chmod +x install.sh
    ./install.sh
    ```
5. 等裝好後就可以直接嘗試辨識第一張圖片
    ```bash
    python cat_detector.py --image images/cat_01.jpg
    ```
    結果如下
    > ![](.README_imgs/result_01.jpg)
6. 同學們可以試著將 `cat_01.jpg` 改成 `cat_02.jpg`、`cat_03.jpg`。