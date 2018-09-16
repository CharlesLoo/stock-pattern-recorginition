# stock-pattern-recorginition
In conclusion, this project presents a method with deep learning for head and shoulders (HAS)
pattern recognition. This appraoce uses 2D candlestick chart as input instead of 1D vectors to
predict the stock trend. The reason for using 2D images is that images about the stock pricelike candlestick chart are more often used for stock investors and easier to understand. Compared with feeding with 1D vector, this approach almost does not need any preprocessing, and the model can feed with raw pixels. In addition, images can contain more
than one time-series. Another reason is that Convolutional Neural network (CNN) is more
stable.

This approach can help traders at all levels to analyze stock market
without much experience in the stock market. It can help investors find HAS patterns from
the stock market quickly without many human resources. 185 head and shoulders (HAS)
patterns are collected and labeled from 20 stock indexes. FR-CNN is used to train a model
with 150 of those images. As expected, with only 150 stock images, AP@0.5IOU is 64%.
There still exists the over-fitting problem in this model, because of 150 images are not
enough for training. To solve these over-fitting two methods are provided, including data
segmentation method and data variation method. Data segmentation aims to remove
noises from a simple chart. However, this method leads to a significant increase in false
positives. Data variation method is a better way to solve this problem. The model fed with
8000 variation images based on 30 original images has an AP@0.5IOU of 74% which
increased 10% compared with the model with 150 original images.

# stock pattern

Head and shoulders Head and shoulders pattern is one of the most used patterns in stock analysis, becauseofitsdistinctiveshapewhichisdevelopedbytwotrendlineswhichconverge. This pattern always exists in an increase period. Two valley makes the support line (or neckline) while ﬁrst and third peak make the resistance line. Similar to ‘M’ and ‘W’ pattern, once the price breaks through the support line, the price would decrease, traders would better to sell after breaking through the support line. On the contract, if the price breaks the resistance line, it normally would increase continually. Therefore, it is a better trade strategy to buy after the price break the resistance line.
<div align=center><img width="350" height="350" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/has.PNG"/></div>

Inverse Head and shoulders Inverse head and shoulders pattern is the opposite of head and shoulders pattern. This pattern always exists in a drop period. Two shoulders make the support line while ﬁrst and second peak make the resistance line (or neckline). Similarly, traders would better to sell after breaking through the support line while buying after the price break the resistance line.

<div align=center><img width="350" height="350" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/Ihas.PNG"/></div>

Stockchartpatternsplayanimportantroleinthestockanalysisandpredictiontechnical and can be a powerful asset for traders at any level. It is a very basic level of priceactionswhichhappenedinanytimeperiod: monthly,dailyandintraday. Even for a beginner trader, if they can recognize these patterns early, they will gain a real competitive advantage in the markets. In this part, I implemented a deep learning model to recognize the common stock patterns which are helpful for any level of stock traders. More importantly, recognizing with computers is much quicker than ﬁnding out all patterns by humans. For example, it may only need a few minutes for computers to track intraday history data of all stock indexes while it may need a group of investors to work weeks. Besides saving time, a stock pattern recognition can also help the investment companies save a lot of human resources since a computer can do much more jobs than a human in a similar time period.
# Data collection 
Candlestick chart Similar to previous experiments, images represented history data would be used as input. Open, close, high and low price is used in the experiment, because of using a candlestick as input for feeding the Neural Network. The reason for using candlestickchartsasinputisthatcancandlestickchartsareoneofthemostcommonways for traders to analyze the stock market. It turns numeric data into a visualization form that can be understood by human easily. In a candlestick, there are at least 4 kinds of data: open, close, high and low, as shown in Fig. 3.12. High and low are representedwithlinesasuppershadowandlowershadow,whileopenandcloseare presented with sticks as real-body. When the close price is greater than open price, the real-body stick is colored with green to represent the increasing trend. Otherwise, it real-body stick is colored with red to represent a decreasing trend as shown in Fig. 3.13.

<div align=center><img width="350" height="350" src="https://github.com/CharlesLoo/stockPrediction_CNN/blob/master/paper/candlesticks.PNG"/></div>

<div align=center><img width="350" height="350" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/input2.PNG"/></div>

30 American stock indexes are picked, including ’AAPL’, ’ABT’, ’ABBV’, ’ACN’, ’ACE’, ’ADBE’, ’ADT’, ’AAP’, ’AES’,’AET’,’AFL’,’AMG’,’A’,’GAS’,’ARE’,’APD’,’AKAM’,’AA’,’AGN’,’MSFT’, ’GOOG’,’ALXN’,’OMC’, ’OKE’, ’ORCL’, ’OI’, ’PCAR’,’DLPH’, ’DAL’, ’XRAY’. Their intraday data are collected from Google Finance. Time period is from Mar 2017 to Mar 2018. 

# Data segmentation 
Stockpricechartcontainsalotofpointsandnoises,itisatime-consumingjobtodetectthepatternsfromthestockpricechartdirectly. Isiteasiertodetectpatternsafter reducing these noises? But it is difﬁcult to remove those noises on the candlestick chart. Therefore, it should be changed to line chart before fed into the network for training. This process can be described in Fig. 3.16. After changing into line chart, the label is same, therefore it can be trained directly without labeling again. After training,trainedmodelcanbeusedtestedwithatestedlinechart. Thenabounding box would be obtained. Finally, the same bounding box can be drawn, because the bounding box on the line chart and candlestick chart are same. 



<div align=center><img width="550" height="550" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/ds.PNG"/></div>

# Generate variation data 
Anotherwayforsolvingtoaddmoretrainingdataandthisisthemostcommonway in deep learning. However, it is impossible to label thousands or millions of images from the actual datasets that would take too much time. Therefore, this work provides an approach to general some variation data to instead of real stock data for training. This is because even the stock market is volatile, stock pattern recognition is based on the shapes of patterns. The recognition model only considers the shape of the pattern, therefore no matter the shapes from variation data or real data, they areallcanbeusedfortraining. AsshowninFig.3.20,greencirclerepresentsallHAS patterns in the real-world, blue circle means 150 labeled HAS patterns in original images, and the red circle is generated variation data. It is obvious that those 150 images cannot cover all HAS patterns in the real-world, which leads to the overﬁttingproblem. AlthoughgeneratedvariationdatacannotcoverallrealHASpatterns and has some data that not included in real data, it has the ability to increase the covered area of training data.

Variation can be divided into 2 steps:
a) P1 = P1 + P1 * r1, P3 = P3 + P3 * r3
b) P2 = P2 - (P1 * r1 + P3 * r3) 
The ﬁrst step means the variation of the ﬁrst peak and third peak. R1 and r3 mean the percentage that the ﬁrst peak and third peak will change. P1, P2, and P3 mean each peak. These values are between -0.7 and 0.7, which means each peak can remove or insert at most 70% of their data. If the number is negative, the related peak will remove some data points according to the number uniformly. If the number is positive, related peak ﬁrst needs to insert data points. Finally, the second peak will insert or delete some data points according to the total changed point. Fig. 3.22 shows the process of variation on X-axis.

<div align=center><img width="650" height="450" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/vx.PNG"/></div>

<div align=center><img width="450" height="350" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_orginal/x.PNG"/></div>

Followed pictures shows some generated images of trainning data.

![some generated images](https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_with_generated_data/variation.jpg)

The AP@0.5IOU is:

<div align=center><img width="350" height="350" src="https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_with_generated_data/ap.png"/></div>

And the final result are shown in follow pictures.

![Some results of pattern recognition](https://github.com/CharlesLoo/stock-pattern-recorginition/blob/master/results/test_result_with_generated_data/whole.png)
# TensorFlow Object Detection Model Training

This is a summary of [this nice readme]( https://gist.github.com/douglasrizzo/c70e186678f126f1b9005ca83d8bd2ce).

1. [Install TensorFlow](https://www.tensorflow.org/install/).

2. Download the TensorFlow [models repository](https://github.com/tensorflow/models).

## Annotating the dataset
1. Fit the time serious with bottom-up or top-down segementation algorithms. 

2. Install [labelImg](https://github.com/tzutalin/labelImg). This is a Python package, you can install via pip, but the one from GitHub is better. It saves annotations in the PASCAL VOC format.

3. Annotate your dataset using labelImg.  

4. Use [this script](https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py) to convert the XML files generated by labelImg into a single CSV file.

    cd get_data/
    
      python xml2csv.py 

5. Separate the CSV file into two, one with training examples and one with evaluation examples. Images should be selected randomly, making sure that objects from all classes are present in both of them. The usual proportions are 75 to 80% training and the rest to the evaluation dataset.

6. Use [this script](https://github.com/datitran/raccoon_dataset/blob/master/generate_tfrecord.py) to convert the two CSV files (eg. train.csv and eval.csv) into TFRecord files (eg. train.record and eval.record), the data format TensorFlow is most familiar with.

    get_data/
    
    $ python general_tf_record.py --csv_input=label_training/raccoon_labels.csv --output_path=label_training/train.record

## Traversing the text file hell...

1. Create a label map, like [one of these](https://github.com/tensorflow/models/tree/master/research/object_detection/data). Make sure class numbers are exactly the ones that were used when creating the TFRecords.

2. Download one of the neural network models provided in [this page](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). The ones trained in the MSCoco dataset are the best ones, since they were also trained on objects.

3. Provide a training pipeline, which is a `config` that usually comes in the tar.gz file downloaded in the last step. If they don't, they can be found [here]( https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs) (they need some tweaking before using, for example, changing number of classes). A tutorial on how to create your own [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/configuring_jobs.md).

 * The pipeline config file has some fields that must be adjusted before training is started. Its header describes which ones. Usually, they are the fields that point to the label map, the training and evaluation directories and the neural network checkpoint. In case you downloaded one of the models provided in [this page](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md), you should untar the `tar.gz` file and point the checkpoint path inside the pipeline config file to the "untarred" directory of the model (see [this answer](https://stackoverflow.com/a/45363576/1245214) for help).

 * You should also check the number of classes. MSCoco has 90 classes, but your problem may have more or less.

## Training the network

1. Train the model. [This is how you do it locally](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md). **Optional:** in order to check training progress, TensorBoard can be started pointing its `--logdir`  to the `--train_dir` of object_detection/train.py.

2. Export the network, like [this](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/exporting_models.md).

3. Use the exported `.pb` in your object detector.

## Tips

In the _data augmentation_ section of the training pipeline, some options can be added or removed to try and make the training better. Some of the options are listed [here](https://stackoverflow.com/a/46901051)

1. If you are running out of memory and this is causing training to fail, there are a number of solutions you can try. First try adding  the arguments

      batch_queue_capacity: 2
      
      prefetch_queue_capacity: 2
  
  to your config file in the train_config section. For example, placing the two lines between gradient_clipping_by_norm and fine_tune_checkpoint will work. The number 2 above should only be starting values to get training to begin. The default for those values are 8 and 10 respectively and increasing those values should help speed up training.
