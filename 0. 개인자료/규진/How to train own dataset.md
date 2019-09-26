# How to train own dataset





## Steps

### 1) COCO format

The easier way to to use this model is labelling your dataset with the [official coco format ](http://cocodataset.org/#format-data)according with the problem you have. In my case, It's for instance segmentation, so I used the detection format.

### 2) Creating a `Dataset` class for your data

Following the example [`coco.py`](https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/maskrcnn_benchmark/data/datasets/coco.py). Create a new class extending from [`torchvision.datasets.coco.CocoDetection`](https://pytorch.org/docs/0.4.0/_modules/torchvision/datasets/coco.html) (you can find another classes in the official docs), this class encapsulates the pycocoapi methods to manage your coco dataset.

This class has to be created in `maskrcnn-benchmark/maskrcnn_benchmark/data/datasets` folder, same as `coco.py`, and included in the `__init__.py`.

### 3) Adding dataset paths

This class will needs as parameters the paths for the `JSON` file, it contains the metadata of your dataset in coco format, and for the images, the folder where they are. The engine automatically searches in [`paths_catalog.py`](https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/maskrcnn_benchmark/config/paths_catalog.py) for these parameters, the easier way is including your paths to the dict `DATASETS` following the format of course, then include an `elif` statement in the `get` method.

### 4) Evaluation file

Here is the importance of use the coco format, if your dataset have the same structure then you can use the same evaluation file used for the class `COCODataset`, in the [`__init_.py`](https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/maskrcnn_benchmark/data/datasets/evaluation/__init__.py) file just add an if statement like the `COCODataset` statement.

This evaluation file follows the coco evaluation standard with the pycocoapi evaluation methods. You can create your own evaluation file, and you have to do it if your dataset have another structure.

### 5) Training script

[Here](https://github.com/facebookresearch/maskrcnn-benchmark/tree/master/tools) you can find the standard training and testing scripts for the model, add your own arguments, change the output dir (this one is very important), etc.

### 6) Changing the hyper-parameters

The engine uses [yacs config files](https://github.com/rbgirshick/yacs), in the repo you can find different ways to change the hyper-parameters.

If you are using a Single GPU, look at the [README](https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/README.md), there is a section for this case, you have to change some hyper-parameters, the default hyper-parameters have been written for Multi-GPUs (8 GPUs). I trained my model using a single one, so no problem at all, just change `SOLVER.IMS_PER_BATCH` and adjust the other `SOLVER` params.

Update `DATASETS.TRAIN` and `DATASETS.TEST` with the name that you used in `paths_catalog.py`. Also consider in change the min/max input sizes hyper-parameters.

### 7) Finetuning the model

The issue [#15](https://github.com/facebookresearch/maskrcnn-benchmark/issues/15) has all the explanation.

- Download the official weights for the model that you want to setup.
- Change in the config file `MODEL.ROI_BOX_HEAD.NUM_CLASSES = your_classes + background`.
- Use [`trim_detectron_model.py `](https://gist.github.com/wangg12/aea194aa6ab6a4de088f14ee193fd968)to remove those layers that are setup for the coco dataset, if you run the train model before this, there will be troubles with layers that expects the 81 classes (80 coco classes + background), those are the layers you have to remove.
- This script will save the new weights, link the path to the `MODEL.WEIGHT` hyper-parameter.

### Now all it is ready for trainnig!!

This the general modifications to the code for a custom dataset, I made more changes according to my needs.

### Visualizing the results

Once the model finishes the training, the weights are saved, you can use the [`Mask_R-CNN_demo.ipynb`](https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/demo/Mask_R-CNN_demo.ipynb) notebook to visualize the results of your model on the test dataset, **but** you have to change the class names in `predictor.py`, it has the coco classes by default, put them in the same order used for the annotations.