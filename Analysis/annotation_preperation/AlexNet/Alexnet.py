from typing import Any
import mxnet as mx
from mxnet.gluon.data.vision import transforms
from mxnet import Context, nd
from mxnet.gluon import nn
from mxnet.gluon.block import HybridBlock

class Alexnet_rect(HybridBlock):
    def __init__(self, context: Context, layer: int) -> None:
        super(Alexnet_rect, self).__init__()
        self.context = context
        self.fov = [16, 32, 32, 32, 64, 224, 224, 224]
        self.layer = layer

        with self.name_scope():
            self.features = nn.HybridSequential("")
            with self.features.name_scope():
                if layer >= 1:
                    self.features.add(nn.Conv2D(64, 11, 4, 2, activation="relu"))
                    self.features.add(nn.MaxPool2D(3, 2))
                if layer >= 2:
                    self.features.add(nn.Conv2D(192, 5, padding=2, activation="relu"))
                    self.features.add(nn.MaxPool2D(3, 2))
                if layer >= 3:
                    self.features.add(nn.Conv2D(384, 3, padding=1, activation="relu"))
                if layer >= 4:
                    self.features.add(nn.Conv2D(256, 3, padding=1, activation="relu"))
                if layer >= 5:
                    self.features.add(nn.Conv2D(256, 3, padding=1, activation="relu"))
                    self.features.add(nn.MaxPool2D(3, 2))
                if layer >= 6:
                    self.features.add(nn.Conv2D(4096, 6, activation="relu"))
                    self.features.add(nn.Dropout(0.5))
                if layer >= 7:
                    self.features.add(nn.Conv2D(4096, 1, activation="relu"))
                    self.features.add(nn.Dropout(0.5))
            if layer == 8:
                self.output = nn.Conv2D(1000, 1)

        self.load_parameters("/home/dorgoz/Desktop/Desktop/alex_rect_params.params", context, ignore_extra=True)

    def hybrid_forward(self, F: Any, x: nd.NDArray) -> nd.NDArray:
        return self.output(self.features(x)) if self.layer == 8 else self.features(x)

    @staticmethod
    def preprocess(context: Context, imgs: nd.NDArray, downsample=False) -> nd.NDArray:
        # return imagenet.transform_eval(x.as_in_context(context))
        if isinstance(imgs, mx.nd.NDArray):
            imgs = [imgs]
        for im in imgs:
            assert isinstance(im, mx.nd.NDArray), "Expect NDArray, got {}".format(type(im))
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)

        if downsample == True:
            transform_fn = transforms.Compose([
                transforms.Resize(224, keep_ratio=True),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ])

        else:
            transform_fn = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ])

        res = [transform_fn(img).expand_dims(0) for img in imgs]

        if len(res) == 1:
            return res[0]
        return res