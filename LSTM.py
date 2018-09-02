#加载数据分析常用库
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

path = './data/bsm1LT.xlsx'
data_load = pd.read_excel(path)
data=data_load.iloc[:,1:].values


#定义常量
rnn_unit=20     #hidden layer units
input_size=2      
output_size=14
lr=0.0006         #学习率
tf.reset_default_graph()
#输入层、输出层权重、偏置
weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,output_size]))
         }
biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[output_size,]))
        }
#定义获得数据 
def get_data(batch_size=60,time_step=20,train_begin=0,train_end=46772):
    batch_index=[]
        
    scaler_for_x=MinMaxScaler(feature_range=(0,1))  #按列做minmax缩放
    scaler_for_y=MinMaxScaler(feature_range=(0,1))
    scaled_x_data=scaler_for_x.fit_transform(data[:,-2:])
    scaled_y_data=scaler_for_y.fit_transform(data[:,0:-2])
    
    label_train = scaled_y_data[train_begin:train_end]
    label_test = scaled_y_data[train_end:]
    normalized_train_data = scaled_x_data[train_begin:train_end]
    normalized_test_data = scaled_x_data[train_end:]
    
    train_x,train_y=[],[]   #训练集x和y初定义
    for i in range(len(normalized_train_data)-time_step):
        if i % batch_size==0:
            batch_index.append(i)
        x=normalized_train_data[i:i+time_step,-2:]
        y=label_train[i:i+time_step,np.newaxis]
        train_x.append(x.tolist())
        train_y.append(y.tolist())
    batch_index.append((len(normalized_train_data)-time_step))
    
    size=(len(normalized_test_data)+time_step-1)//time_step  #有size个sample 
    test_x,test_y=[],[]  
    for i in range(size-1):
        x=normalized_test_data[i*time_step:(i+1)*time_step,-2:]
        y=label_test[i*time_step:(i+1)*time_step]
        test_x.append(x.tolist())
        test_y.extend(y)
    test_x.append((normalized_test_data[(i+1)*time_step:,-2:]).tolist())
    test_y.extend((label_test[(i+1)*time_step:]).tolist())    
    
    return batch_index,train_x,train_y,test_x,test_y,scaler_for_y

class TS_LSTM(object):
    def __init__(self, hps):
        self._X = X = tf.placeholder(tf.float32, [None, hps.seq_size, 1])  
        self._Y = Y = tf.placeholder(tf.float32, [None, hps.seq_size])      
        W = tf.Variable(tf.random_normal([hps.hidden_size, 1]), name='W')  
        b = tf.Variable(tf.random_normal([1]), name='b')  
        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(hps.hidden_size)  #测试cost 1.3809

        outputs, states = tf.nn.dynamic_rnn(lstm_cell, X, dtype=tf.float32)  
        W_repeated = tf.tile(tf.expand_dims(W, 0), [tf.shape(X)[0], 1, 1])  
        output = tf.nn.xw_plus_b(outputs, W_repeated, b)  
        self._output = output = tf.squeeze(output)  
        self._cost = cost = tf.reduce_mean(tf.square(output - Y))  
        self._train_op = tf.train.AdamOptimizer(hps.learning_rate).minimize(cost)  

    def X(self):
        return self._X

    def Y(self):
        return self._Y   

    def cost(self):
        return self._cost

    def output(self):
        return self._output

    def train_op(self):
        return self._train_op

def train_test(hps, data):
     #训练数据准备
    train_data_len = len(data)*4//5
    train_x, train_y = [], []  
    for i in range(train_data_len - hps.seq_size - 1):  
        train_x.append(np.expand_dims(data[i : i + hps.seq_size], axis=1).tolist())  
        train_y.append(data[i + 1 : i + hps.seq_size + 1].tolist())  
    #测试数据准备20%作为测试数据    
    test_data_len = len(data)//5
    test_x, test_y = [], []  
    for i in range(train_data_len,
                   train_data_len+test_data_len - hps.seq_size - 1):  
        test_x.append(np.expand_dims(data[i : i + hps.seq_size], axis=1).tolist())  
        test_y.append(data[i + 1 : i + hps.seq_size + 1].tolist())  

    with tf.Graph().as_default(), tf.Session() as sess:  
        with tf.variable_scope('model',reuse=None):
            m_train = TS_LSTM(hps)         

        #训练
        tf.global_variables_initializer().run()
        for step in range(20000):  
            _, train_cost = sess.run([m_train.train_op, m_train.cost], 
                              feed_dict={m_train.X: train_x, m_train.Y: train_y})  

        #预测 
        test_cost, output = sess.run([m_train.cost, m_train.output],
                  feed_dict={m_train.X: test_x, m_train.Y: test_y})  
        #print(hps, train_cost, test_cost)
        return train_cost, test_cost
