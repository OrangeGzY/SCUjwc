from PIL import Image
import glob
import numpy as np
import os
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input, concatenate ,BatchNormalization
from keras.layers.convolutional import Conv2D, Convolution2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adadelta
from keras.utils.vis_utils import plot_model
import tensorflow as tf
import warnings
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

width=180
height=60

captcha_word=[
    '1','2','3','4','5','6','7','8','9','0',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
    'q','r','s','t','u','v','w','x','y','z'
]

word_len = 4

word_class = len(captcha_word)

samples = glob.glob(r'/Users/apple/desktop/train/*.jpg')

char_indices = dict((c, i) for i, c in enumerate(captcha_word))
indices_char = dict((i, c) for i, c in enumerate(captcha_word))
#print(char_indices)
#print(indices_char)

def captcha_2_vec(captcha):
    # 字符个数*字符种类
    vector = np.zeros(word_len*word_class)            #每个验证码4字符  每个字符wordclass种
    #print(vector.shape)

    for i,ch in enumerate(captcha):
        idex = i * word_class + char_indices[ch]
        vector[idex] = 1
    #print(vector)
    return vector

def get_size(path):
    im = Image.open(path)
    print('宽：%d,高：%d'%(im.size[0],im.size[1]))
    return im.size[0],im.size[1]

# 把数组转换回文字
def vec_to_captcha(vec):
    text = []
    # 把概率小于0.5的改为0，标记为错误
    vec[vec < 0.5] = 0

    char_pos = vec.nonzero()[0]

    for i, ch in enumerate(char_pos):
        text.append(captcha_word[ch % word_class])
    return ''.join(text)

def custom_accuracy(y_true, y_pred):
    predict = tf.reshape(y_pred, [-1, word_len, word_class])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(y_true, [-1, word_len,word_class]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    _result = tf.map_fn(fn=lambda e: tf.reduce_all(e),elems=correct_pred,dtype=tf.bool)
    return tf.reduce_mean(tf.cast(_result, tf.float32))


path="/Users/apple/desktop/train/3ggc.jpg"
image_list=[]
train_dir="/Users/apple/desktop/train"

for item in os.listdir(train_dir):
    image_list.append(item)

np.random.shuffle(image_list)


X = np.zeros((len(image_list), height, width, 3), dtype = np.uint8)

y = np.zeros((len(image_list), word_len * word_class), dtype = np.uint8)

for i,img in enumerate(image_list):
    if i % 10000 == 0:
        #print(i)
        pass
    img_path = train_dir + "/" + img
    #读取图片
    raw_img = image.load_img(img_path, target_size=(height, width))
    #讲图片转为np数组
    X[i] = image.img_to_array(raw_img)
    #讲标签转换为数组进行保存
    #print(img.split('.')[0])
    y[i] = captcha_2_vec(img.split('.')[0])

#print(X[1])
#print(len(y[4]))

input_tensor = Input(shape=(height, width, 3))
#print(x)
x = input_tensor


x = Convolution2D(32, 3, padding='same', activation='relu')(x)
x = Convolution2D(32, 3, padding='same', activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Convolution2D(64, 3, padding='same', activation='relu')(x)
x = Convolution2D(64, 3, padding='same', activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Convolution2D(128, 3, padding='same', activation='relu')(x)
x = Convolution2D(128, 3, padding='same',activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dropout(0.25)(x)
x= BatchNormalization()(x)
x = [Dense(word_class, activation='softmax', name='c%d'%(i+1))(x) for i in range(word_len)]
output = concatenate(x)
model = Model(inputs=input_tensor, outputs=output)
opt = Adadelta(lr=0.1)
model.compile(loss = 'categorical_crossentropy', optimizer=opt, metrics=['accuracy',custom_accuracy])
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.1,random_state=1)
epochs = 100
print("training start")
hist = model.fit(X_train,y_train,epochs=100,shuffle=True)
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test accuracy:', test_acc)
