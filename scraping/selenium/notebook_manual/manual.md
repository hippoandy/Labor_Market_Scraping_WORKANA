# Instruction Manual

### Step 1. Install Anaconda

Anaconda is a software that allows you to run the Jupyter Notebook on your computer.
Please refer to this link for download:

[https://www.anaconda.com/download/](https://www.anaconda.com/download/)

Scroll down the page a little bit to find the following section:
![Download Page](./images/download.png)

Please download the ***Python 3.7 version*** of Anaconda

Then please install Anaconda using the downloaded executable.

#### Windows User
Please execute the installer and keep click on '***Next***' without changing any settings until you see this page:
![Windows Step](./images/win-install-step.png)

Make sure you check the option "**Add Anaconda to my PATH environment variable**" before you click "***Install***".

If the installer is asking you to install "MS Visual Studio Code", please ignore it.

### Step 2. Install Required Python Libraries

We are now installing the required Python libraries to allow the program to execute correctly.

#### Windows User
1\. Please open **CMD** program with "Administrator Privilege"

On the Windows taskbar, find a circle icon and click it
![CMD Step 0](./images/open-cmd-step0.png)

You will see a input field at the button, type "**cmd**"
![CMD Step 1](./images/open-cmd-step1.png)

The cmd program will show up in the window.

![CMD Step 2](./images/open-cmd-step2.png)

Please right click on it and choose "Run as administrator"

![CMD Step 3](./images/open-cmd-step3.png)

Here is the CMD window:

![CMD Step 4](./images/open-cmd-step4.png)

2\. Insert the command to install the libraries:

This is the command for installation:

> conda install -c conda-forge selenium pandas numpy

Copy & paste this line to the CMD window and press "Enter" key.

![Install lib. 1](./images/install-lib-step1.png)

Then, you will see a message like the following, type '**y**' and press "Enter" key.

![Install lib. 2](./images/install-lib-step2.png)

Wait until the progress complete.

### Step 3. Download additional Lib. file and the Program

#### 1\. Download Chrome Driver

Please refer to this link:
[https://chromedriver.storage.googleapis.com/index.html?path=2.42/](https://chromedriver.storage.googleapis.com/index.html?path=2.42/)

Download Windows version Chrome Driver as:
![Download driver](./images/download-driver.png)

Open the downloaded **.zip** file and extract the "**chromedriver.exe**" to your **Downloads** folder

![Extract driver step 1](./images/extract-driver-step1.png)

You will see a window shows up, change the pathe to your **Download** folder and click "**Extract**"

![Extract driver step 2](./images/extract-driver-step2.png)


#### 2\. Download the program files:

Please refer to this link:
[https://github.com/hippoandy/UN_Webscraping_WORKANA/](https://github.com/hippoandy/UN_Webscraping_WORKANA/)

Download the program .zip file as:
![Download program](./images/download-program.png)

Open the downloaded .zip file and extract the content:
![Extract program step 1](./images/extract-program-step1.png)

Make sure to change to destination path to your **Download** folder:
![Extract program step 2](./images/extract-program-step2.png)


### Step 4. Open Jupyter Notebook Application

#### 1\. Open Anaconda then Jupyter

Open you installed Anaconda Program, you should see a window like this:
![The Anaconda](./images/anaconda.png)

To launch the Jupyter Notebook, click the "**Launch**" button of it.

Then, you should see you browser opens up and shows a page like this:
![The Jupyter](./images/jupyter.png)

Navigate to your Download folder, and you should see this:
![Run notebool step 1](./images/run-program-step1.png)

Here you will see the downloaded files instructed in the previous section.
Continue to naviagate to the program folder:

> UN\_Webscrpaing\_WORKANA-master > scrpaing > selenium

Then, you should see this page:
![Run notebool step 2](./images/run-program-step2.png)

Click on the Jupyter Notebook to open the program.

Here is the Jupyter Notebook program
![Notebook](./images/notebook.png)

Please use the run button to execute the notebook.


#### 2\. Run the Notebook

Before execution, please find the driver section of the code, the section starts with the line:
> \#\#\# load the chrome driver executable

Replace the **<user>** tag to your computer user name:
![Driver path](./images/run-program-insert-path.png)

To find your user name, you may check the properties information of the **chromedriver.exe** file.

Headed to your Downloads folder, right click on the **chromedriver.exe** and choose "**Properties**".
![Find driver path step 1](./images/run-program-find-driver-path.png)

You will see a window like this, the location field indicated the user name:
![Find driver path step 2](./images/run-program-get-driver-path.png)

Here, the user name is "**Andy**".

Please go back to the Jupyter notebook and replace the user name with yours.


If you see this window while running the program, please click "**Allow**".
![Security Prompt](./images/run-program-security.png)








