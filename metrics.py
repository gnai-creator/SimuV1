import numpy as np
import tensorflow as tf

JUDGE = 4
CHANNELS = 1

def add_judge_channel(input_grid, juizo_value):
    h, w = input_grid.shape
    grid_with_channel = np.zeros((h, w, CHANNELS, JUDGE), dtype=np.float32)

    # Coloca input_grid no canal 0 de todos os CHANNELS
    grid_with_channel[:, :, 0, 0] = input_grid  # valor original
    grid_with_channel[:, :, 0, 1] = juizo_value  # canal de juízo

    return grid_with_channel

def standardize_grid_shapes(X, Y):
    """
    Garante que todos os grids tenham formato (H, W, C, J) com H >= W.
    Transpõe se necessário.
    """
    X_out, Y_out = [], []
    for x, y in zip(X, Y):
        if y.ndim != 4:
            raise ValueError(f"Esperado shape (H, W, C, J), mas veio {y.shape}")

        h, w = y.shape[:2]
        if h < w:
            x = np.transpose(x, (1, 0, 2, 3))  # H x W x C x J → W x H x C x J
            y = np.transpose(y, (1, 0, 2, 3))
        X_out.append(x)
        Y_out.append(y)
    return np.array(X_out), np.array(Y_out)


def pad_to_max_shape(X, Y):
    """
    Pad todos os exemplos para a maior altura e largura encontrada no batch.
    Suporta inputs 4D com shape (H, W, C, J).
    """
    max_h = max(y.shape[0] for y in Y)
    max_w = max(y.shape[1] for y in Y)
    padded_X = []
    padded_Y = []

    for x, y in zip(X, Y):
        pad_h = max_h - y.shape[0]
        pad_w = max_w - y.shape[1]

        if x.ndim == 4:
            x_pad = np.pad(x, ((0, pad_h), (0, pad_w), (0, 0), (0, 0)), mode='constant')
        else:
            raise ValueError("Esperado input com 4 dimensões: (H, W, C, J)")

        if y.ndim == 4:
            y_pad = np.pad(y, ((0, pad_h), (0, pad_w), (0, 0), (0, 0)), mode='constant')
        else:
            raise ValueError("Esperado label com 4 dimensões: (H, W, C, J)")

        padded_X.append(x_pad)
        padded_Y.append(y_pad)

    return np.array(padded_X), np.array(padded_Y)


def prepare_data(X, Y):
    X, Y = standardize_grid_shapes(X, Y)
    X, Y = pad_to_max_shape(X, Y)
    return X, Y


def pad_to_30x30_top_left(X, Y, pad_value=0):
    """
    Pad X e Y para shape (30, 30, C, J) no canto superior esquerdo.
    """
    padded_X, padded_Y = [], []

    for x, y in zip(X, Y):
        x_h, x_w, x_c, x_j = x.shape
        y_h, y_w, y_c, y_j = y.shape

        x_pad = np.full((30, 30, x_c, x_j), pad_value, dtype=x.dtype)
        x_pad[:x_h, :x_w, :, :] = x

        y_pad = np.full((30, 30, y_c, y_j), pad_value, dtype=y.dtype)
        y_pad[:y_h, :y_w, :, :] = y

        padded_X.append(x_pad)
        padded_Y.append(y_pad)

    return np.array(padded_X), np.array(padded_Y)



def pad_to_30x30_top_left_single(X, pad_value=0):
    """
    Pad uma lista de arrays X para shape (30, 30, C, J).
    """
    padded_X = []
    for x in X:
        if x.ndim != 4:
            raise ValueError(f"Esperado shape 4D (H, W, C, J), mas veio {x.shape}")
        h, w, c, j = x.shape
        x_pad = np.full((30, 30, c, j), pad_value, dtype=x.dtype)
        x_pad[:h, :w, :, :] = x
        padded_X.append(x_pad)
    return np.array(padded_X)
