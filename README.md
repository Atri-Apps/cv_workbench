# Testing workbench for driving license OCR project

This multi-page testing workbench aims at facilitating Machine Learning teams in recording and reviewing their detailed feedback corresponding to their test images. 

- Frontend, backend and deployment accomplished using Atri framework.
- YOLOv5 model was used to detect and extract test from the images. 

## Demo
![Demo](readme_assets/demo.gif)

## How to use this app?

### Step 1: Setup

```shell
git clone https://github.com/Atri-Apps/cv_workbench.git

cd cv_workbench

pipenv install
```

### Step 2: Save weights of trained model

Save the weights of the model trained on US Driving License data as `cv_transformations/yolov5/best.pt`. 

The weights are available at this [location](https://drive.google.com/file/d/1eOjN86OrxHSnmcAOnTMBFcczR_ahMdlu/view?usp=sharing). 

### Step 3: Create empty files

Create `data/tests.json` and `data/comments.json` with the following content in both:

```
{}
```


### Step 4: Start the editor

```shell
pipenv shell

atri start
```

## Resources
📚 Read the [Docs](https://docs.atrilabs.com/)

🧭 Follow Atri Labs on [LinkedIn](https://www.linkedin.com/company/atri-labs)

💬 Join our [Slack community](https://join.slack.com/t/atricommunity/shared_invite/zt-1e756m1at-bZBxngvw7KWWO0riI4pc0w)

❓ Share any [bugs](https://github.com/Atri-Labs/atrilabs-engine/issues) or ask any question in [Discussions](https://github.com/Atri-Labs/atrilabs-engine/discussions)

🎥 Watch along on [YouTube](https://www.youtube.com/channel/UC1uR2Q5x_8olWS_Y4PdK1Bw)

⭐️ Star [Atri framework](https://github.com/Atri-Labs/atrilabs-engine) if you find it helpful! 😎
