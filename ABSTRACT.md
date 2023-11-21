The authors introduce **GDXray+: The GRIMA X-ray Database** comprising 20,966 X-ray images. These images are systematically organized in a public database named GDXray+, accessible for free but exclusively for research and educational purposes. The database encompasses five categories of X-ray images: ***castings***, ***welds***, ***baggages***, natural objects (***nature***), and ***settings***. Each category includes several ***series***, and each series comprises multiple X-ray images. Most series are annotated, providing either the coordinates of bounding boxes for objects of interest or labels for the images, stored in standard text files. GDXray, with a size of 3.5 GB, is available for download on the authors' website. The authors assert that GDXray makes a valuable contribution to the X-ray testing community by offering a resource for developing, testing, and evaluating image analysis and computer vision algorithms without the need for expensive X-ray equipment. Furthermore, they emphasize its utility as a benchmark for testing and comparing different approaches on the same dataset, along with its potential use in training programs for human inspectors.

Public databases of X-ray images for medical imaging exist, but, to the best knowledge of the authors, there has not been a public database specifically for digital X-ray images in X-ray testing. In service to the X-ray testing community, the authors have collected around 21k X-ray images for the development, testing, and evaluation of image analysis and computer vision algorithms. The authors highlight that GDXray is distinct in its structure, offering a resource for various applications and presenting opportunities for diverse experiments. They elaborate on the database's structure, providing insight into the organization of groups, series, and individual X-ray images.

## Castings

The Castings group, comprising 2,727 X-ray images in 67 series, focuses on automotive parts, particularly aluminum wheels and knuckles. The authors present examples and details of each series, emphasizing that experiments on this data can be found in various publications. Notably, they highlight a series (C0001) that contains a sequence of 72 X-ray images taken from an aluminum wheel, along with annotations of bounding boxes for 226 small defects and the calibration matrix for each image.

## Welds

The Welds group consists of 98 images in 3 series, taken by the BAM Federal Institute for Materials Research and Testing, Berlin, Germany. The authors showcase examples and detail each series, mentioning experiments conducted on this data and highlighting series (W0001 and W0002) that contain annotations for bounding boxes and binary images of the ground truth for 641 defects. Another series (W0003) includes 67 digitized radiographs from a round robin test on flaw recognition in welding seams, providing additional details on the data acquisition process.

## Baggages

The Baggage group, containing 9,700 X-ray images in 77 series, focuses on images of various items such as backpacks, pen cases, and wallets. The authors illustrate examples and present details for each series, noting experiments conducted on this data and highlighting series (B0046, B0047, and B0048) that contain 600 X-ray images suitable for the automated detection of handguns, shuriken, and razor blades. These series include bounding box annotations for the objects of interest.

## Nature

The Nature group encompasses 8,290 X-ray images in 13 series, featuring images of natural objects such as salmon filets, fruit, and wood pieces. The authors showcase examples and detail each series, emphasizing experiments conducted on this data. They highlight series (N0012 and N0013) that include annotations for bounding boxes and binary images of the ground truth for 73 fish bones. Additionally, they mention series (N0003) that provides over 7,500 labeled small crops for training purposes.

## Settings

The Settings group includes 151 X-ray images in 7 series, focusing on calibration objects like checkerboards and 3D objects with regular patterns. The authors present examples and provide details for each series, noting experiments conducted on this data. They highlight series (S0001) that contains X-ray images of a copper checkerboard along with the calibration matrix for each view. Another series (S0007) can be used for modeling the distortion of an image intensifier, providing coordinates for each hole of the calibration pattern in each view along with the coordinates of the 3D model.
