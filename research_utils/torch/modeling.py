import math
import torch.nn as nn
from functools import reduce


def next_conv_dim(conv: nn.Conv2d, in_img_size: int):
  kernel_size = conv.kernel_size[0] if type(
    conv.kernel_size) is tuple else conv.kernel_size
  stride = conv.stride[0] if type(conv.stride) is tuple else conv.stride
  padding = conv.padding[0] if type(conv.padding) is tuple else conv.padding
  dilation = conv.dilation[0] if type(
    conv.dilation) is tuple else conv.dilation
  out_img_size = math.floor((
    in_img_size +
    2 * padding - dilation * (kernel_size - 1) - 1
  ) / stride + 1)
  return out_img_size

def next_conv_transpose_dim(convt: nn.ConvTranspose2d, in_img_size: int):
  kernel_size = convt.kernel_size[0] if type(
    convt.kernel_size) is tuple else convt.kernel_size
  stride = convt.stride[0] if type(convt.stride) is tuple else convt.stride
  padding = convt.padding[0] if type(convt.padding) is tuple else convt.padding
  dilation = convt.dilation[0] if type(
    convt.dilation) is tuple else convt.dilation
  output_padding = convt.output_padding[0] if type(convt.output_padding) is tuple else convt.output_padding

  out_img_size = math.floor(
    (in_img_size - 1) * stride - 
    2 * padding + dilation * (kernel_size - 1) + output_padding + 1
  )
  return out_img_size

def next_conv_block_dim(block: nn.Module, in_img_size: int):
  out_img_size = in_img_size
  for module in block:
    if isinstance(module, (nn.Conv2d, nn.MaxPool2d)):
      out_img_size = next_conv_dim(module, out_img_size)
    elif isinstance(module, nn.ConvTranspose2d):
      out_img_size = next_conv_transpose_dim(module, out_img_size)
    elif isinstance(module, (nn.Upsample, nn.UpsamplingBilinear2d, nn.UpsamplingNearest2d)):
      out_img_size *= module.scale_factor
  return out_img_size

def final_conv_dim(model: nn.Module, in_img_size: int):
  children = model.children()
  out_img_size = reduce(
    lambda _in_img_size, conv: next_conv_dim(conv, _in_img_size),
    children,
    in_img_size
  )
  return out_img_size