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

You will see an input field at the button, type "**cmd**"
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

Please wait for a couple of minutes. Then, you will see a message like the following, type '**y**' and press "Enter" key.

![Install lib. 2](./images/install-lib-step2.png)

Wait until the progress complete.

### Step 3. Download the Program Files

#### Download the program files:

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

Then, you should see your browser opens up and shows a page like this:
![The Jupyter](./images/jupyter.png)

Navigate to your Download folder, and you should see this:
![Run notebool step 1](./images/run-program-step1.png)

Here you will see the downloaded files instructed in the previous section.
Continue to navigate to the program folder:

> UN\_Webscrpaing\_WORKANA-master > scraping > selenium

Then, you should see this page:
![Run notebool step 2](./images/run-program-step2.png)

Click on the Jupyter Notebook to open the program.

Here is the Jupyter Notebook program
![Notebook](./images/notebook.png)

Please use the run button to execute the notebook.


#### 2\. Run the Notebook

If you see this window while running the program, please click "**Allow**".
![Security Prompt](./images/run-program-security.png)








