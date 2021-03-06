# V1.3-1 for new embedded data with shape of 80*64 ( CSIC 2010)

#  changed the conv kernel (2*2) and 4*4


import tensorflow as tf 
import batch_data 
import os

os.environ['CUDA_VISIBLE_DEVICES']='0'
gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
# sess=tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))


def weight_variable(shape,Name):
    initial =tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial,name=Name)

def bias_variable(shape,Name):
    initial=tf.constant(0.1,shape=shape)
    return tf.Variable(initial,name=Name)

def conv2d_SAME(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')

def conv2d_VALID(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='VALID')

# cut down half
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# cut down 1
def max_pool_2x2_1(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,1,1,1],padding='VALID')

# no cut down
def max_pool_2x2_0(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,1,1,1],padding='SAME')


def Path_check(path):
    folder=os.path.exists(path)
    if not folder:
        print('Create the folder successfully')
        os.makedirs(path)
    else:
        print('The folder exists! Please check it')
        os._exit(0)



def train():
    save_path='New-CNN/V4/TrainedModels/V1.3-1-2-data10'
    # ----------------- Check the path ---------------------
    Path_check(save_path)

    # ----------------- graph ------------------
    x_in=tf.placeholder(tf.float32,[None,80*48],name='X_in')
    y_in=tf.placeholder(tf.float32,[None,2],name='Y_in')
    learning_rate=0.0001
    keep_prob=0.5
    alpha_1=tf.Variable(tf.constant(0.8,shape=[1]),name='alpha_1')
    beta_1=tf.Variable(tf.constant(0.2,shape=[1]),name='beta_1')
    alpha_2=tf.Variable(tf.constant(0.8,shape=[1]),name='alpha_2')
    beta_2=tf.Variable(tf.constant(0.2,shape=[1]),name='beta_2')
    alpha_3=tf.Variable(tf.constant(0.8,shape=[1]),name='alpha_3')
    beta_3=tf.Variable(tf.constant(0.2,shape=[1]),name='beta_3')
    alpha_4=tf.Variable(tf.constant(0.8,shape=[1]),name='alpha_4')
    beta_4=tf.Variable(tf.constant(0.2,shape=[1]),name='beta_4')
    # alpha_5=tf.Variable(tf.constant(0.8,shape=[1]),name='alpha_5')
    # beta_5=tf.Variable(tf.constant(0.2,shape=[1]),name='beta_5')

    x_image=tf.reshape(x_in,[-1,80,48,1])

    # ---------- para for data ----------------
    filein=['Data/CSIC+word_change+80-48/Encode-data10/encode_train.csv']
    labelsin=['Data/CSIC+word_change+80-48/Encode-data10/label_train.csv']
    num_data=150425
    data_size=80*48
    batch_size=20
    label_size=2
    epoches=6
    # ------------- end ------------------------

    #------------------ first layer --------------
    # -------- conv
    w_conv1=weight_variable([1,3,1,64],'w1')
    b_conv1=bias_variable([64],'b1')
    h_conv1=tf.nn.relu(conv2d_SAME(x_image,w_conv1)+b_conv1)
    # n*80*48*64
    w_conv2=weight_variable([1,3,64,128],'w1.1')
    b_conv2=bias_variable([128],'b1.1')
    h_conv2=tf.nn.relu(conv2d_SAME(h_conv1,w_conv2
    )+b_conv2)
    # ---------- out
    out1=h_conv2
    # n*80*48*128

    # --------------- second layer ----------------
    # ---------- conv
    w_conv3=weight_variable([1,3,128,128],'w3')
    b_conv3=bias_variable([128],'b3')
    h_conv3=tf.nn.relu(conv2d_SAME(out1,w_conv3)+b_conv3)
    # ---------- out
    out2=max_pool_2x2(alpha_1*out1+beta_1*h_conv3)
    # n*40*24*128

    # -------------- third layer ------------------
    # --------- conv
    w_conv4=weight_variable([1,3,128,128],'w4')
    b_conv4=bias_variable([128],'b4')
    h_conv4=tf.nn.relu(conv2d_SAME(out2,w_conv4)+b_conv4)
    # ---------- out
    out3=max_pool_2x2(alpha_2*out2+beta_2*h_conv4)
    # n*20*12*128

    # ------------- fourth layer ------------------
    # --------- conv
    w_conv5=weight_variable([1,3,128,128],'w5')
    b_conv5=bias_variable([128],'b5')
    h_conv5=tf.nn.relu(conv2d_SAME(out3,w_conv5)+b_conv5)
    # --------- out
    out4=max_pool_2x2(alpha_3*out3+beta_3*h_conv5)
    # n*10*6*128


    #-------------------------------------------- add ------------------------------------
    # -------------- fifth layer -------------------
    # --------- conv
    w_conv6=weight_variable([1,3,128,128],'w6')
    b_conv6=bias_variable([128],'b6')
    h_conv6=tf.nn.relu(conv2d_SAME(out4,w_conv6)+b_conv6)
    # --------- out
    out5=max_pool_2x2(alpha_4*out4+beta_4*h_conv6)
    # n*5*3*128

    # # ------------- sixth layer -------------------
    # w_conv7=weight_variable([3,3,128,128],'w7')
    # b_conv7=bias_variable([128],'b7')
    # h_conv7=tf.nn.relu(conv2d_SAME(out5,w_conv7)+b_conv7)
    # # --------- out
    # out6=max_pool_2x2_1(alpha_5*out5+beta_5*h_conv7)
    # # 7*4*128
    # print('out6: ',out6)
    # #---------------------------------------------------------------------------------------

    # --------------- full connect -----------------
    w_full_1=weight_variable([5*3*128,256],'w_full_1')
    b_full_1=bias_variable([256],'b_full_1')
    flat_out4=tf.reshape(out5,[-1,5*3*128])
    h_full_1=tf.nn.relu(tf.matmul(flat_out4,w_full_1)+b_full_1)

    # Drop out
    h_full_drop1=tf.nn.dropout(h_full_1,keep_prob=keep_prob)

    # --------------- full connect -------------------
    w_full_2=weight_variable([256,40],'w_full_2')
    b_full_2=bias_variable([40],'b_full_2')
    out7=tf.matmul(h_full_drop1,w_full_2)+b_full_2

    # Drop out
    h_full_drop2=tf.nn.dropout(out7,keep_prob=keep_prob)

    # --------------- last layer ---------------------
    w_full_3=weight_variable([40,2],'w_full_3')
    b_full_3=bias_variable([2],'b_full_3')
    y_out=tf.matmul(h_full_drop2,w_full_3)+b_full_3
    # print ('y_out: ',y_out)
    # --------------- loss ----------------------------
    cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_out,labels=y_in))
    train_step=tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

    #----------predict ----------------
    correct_prediction=tf.equal(tf.argmax(y_out,1),tf.argmax(y_in,1))
    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

    # ------- save the operations ------------
    tf.add_to_collection('loss',cross_entropy)
    tf.add_to_collection('train',train_step)
    tf.add_to_collection('acc',accuracy)

    #----------------- for data ----------------------------
    data,label=batch_data.get_shuffle_batch(file_data=filein,file_label=labelsin,data_size=data_size,batch_size=batch_size,label_size=label_size,epoches=epoches)


    # Training--------------------------
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        # sess.run(tf.global_variables_initializer())
        sess.run(tf.group(tf.local_variables_initializer(),tf.global_variables_initializer()))
        coord=tf.train.Coordinator()
        threads=tf.train.start_queue_runners(coord=coord)

        try:
            while not coord.should_stop():
                num_one_epoch=num_data//batch_size
                # one epoch 
                for i in range(num_one_epoch):
                    batch_x,batch_y=sess.run([data,label])
                    if i==1:
                        print ('start!!')
                    if i%50==0:
                        y_pred=sess.run(y_out,feed_dict={x_in:batch_x,y_in:batch_y})
                        loss=sess.run(cross_entropy,feed_dict={x_in:batch_x,y_in:batch_y})
                        train_accuracy=sess.run(accuracy,feed_dict={x_in:batch_x,y_in:batch_y})
                        #print ('y_pred :',y_pred)
                        print ('loss: %f,step %d ,training accuracy: %f'%(loss,i,train_accuracy))
                    sess.run(train_step,feed_dict={x_in:batch_x,y_in:batch_y})
        except tf.errors.OutOfRangeError:
            print ('Training is done!!')
        finally:
            coord.request_stop()
        coord.join(threads)

        # Save the model 
        saver=tf.train.Saver()
        saver.save(sess,'%s/Models_%s/Models_%s'%(save_path,learning_rate,learning_rate))
    print ('Model has been saved!')

def test():
    accs=[]
    file0=open('New-CNN/V4/Pred/pred-1.3-1-2-encode-data10.csv','wt')
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:

        filein=['Data/CSIC+word_change+80-48/Encode-data10/encode_test.csv']
        labelsin=['Data/CSIC+word_change+80-48/Encode-data10/label_test.csv']
        path_meta='New-CNN/V4/TrainedModels/V1.3-1-2-data10/Models_0.0001/Models_0.0001.meta'
        path_check='New-CNN/V4/TrainedModels/V1.3-1-2-data10/Models_0.0001'
        num_data=64469
        data_size=80*48
        batch_size=50
        label_size=2
        epoches=None

        #--------------------- load data --------------------
        data,label=batch_data.get_batch(file_data=filein,file_label=labelsin,data_size=data_size,batch_size=batch_size,label_size=label_size,epoches=epoches)
        sess.run(tf.global_variables_initializer())
        coord=tf.train.Coordinator()
        threads=tf.train.start_queue_runners(coord=coord,sess=sess)
        # -------------------- end -------------------------
        # path_meta='TrainedModels-MyCNN/V1.3-1/Models_0.001/Models_0.001.meta'
        # path_check='TrainedModels-MyCNN/V1.3-1/Models_0.001/'


        # ----------------- graph ------------------
        x_in=tf.placeholder(tf.float32,[None,80*48],name='X_in')
        y_in=tf.placeholder(tf.float32,[None,2],name='Y_in')

        #  load graph and variables
        saver = tf.train.import_meta_graph(path_meta)
        saver.restore(sess, tf.train.latest_checkpoint(path_check))

        alpha_1=sess.run('alpha_1:0')
        beta_1=sess.run('beta_1:0')
        alpha_2=sess.run('alpha_2:0')
        beta_2=sess.run('beta_2:0')
        alpha_3=sess.run('alpha_3:0')
        beta_3=sess.run('beta_3:0')
        alpha_4=sess.run('alpha_4:0')
        beta_4=sess.run('beta_4:0')
        # alpha_5=sess.run('alpha_5:0')
        # beta_5=sess.run('beta_5:0')

        x_image=tf.reshape(x_in,[-1,80,48,1])

        # ----------------- first layer ---------------
        # -------- conv
        w_conv1=sess.run('w1:0')
        b_conv1=sess.run('b1:0')
        h_conv1=tf.nn.relu(conv2d_SAME(x_image,w_conv1)+b_conv1)
        # n*38*26*64
        w_conv2=sess.run('w1.1:0')
        b_conv2=sess.run('b1.1:0')
        h_conv2=tf.nn.relu(conv2d_SAME(h_conv1,w_conv2
        )+b_conv2)
        # ---------- out
        out1=h_conv2

        # --------------- second layer ----------------
        # ---------- conv
        w_conv3=sess.run('w3:0')
        b_conv3=sess.run('b3:0')
        h_conv3=tf.nn.relu(conv2d_SAME(out1,w_conv3)+b_conv3)
        # ---------- out
        out2=max_pool_2x2(alpha_1*out1+beta_1*h_conv3)
        # n*40*32*128

        # -------------- third layer ------------------
        # --------- conv
        w_conv4=sess.run('w4:0')
        b_conv4=sess.run('b4:0')
        h_conv4=tf.nn.relu(conv2d_SAME(out2,w_conv4)+b_conv4)
        # ---------- out
        out3=max_pool_2x2(alpha_2*out2+beta_2*h_conv4)
        # n*20*16*128

        # ------------- fourth layer ------------------
        # --------- conv
        w_conv5=sess.run('w5:0')
        b_conv5=sess.run('b5:0')
        h_conv5=tf.nn.relu(conv2d_SAME(out3,w_conv5)+b_conv5)
        # --------- out
        out4=max_pool_2x2(alpha_3*out3+beta_3*h_conv5)
        # n*10*8*128

        # -------------- fifth layer -------------------
        # --------- conv
        w_conv6=sess.run('w6:0')
        b_conv6=sess.run('b6:0')
        h_conv6=tf.nn.relu(conv2d_SAME(out4,w_conv6)+b_conv6)
        # --------- out
        out5=max_pool_2x2(alpha_4*out4+beta_4*h_conv6)
        # n*5*4*128

        # # ------------- sixth layer -------------------
        # w_conv7=sess.run('w7:0')
        # b_conv7=sess.run('b7:0')
        # h_conv7=tf.nn.relu(conv2d_SAME(out5,w_conv7)+b_conv7)
        # # --------- out
        # out6=max_pool_2x2_1(alpha_5*out5+beta_5*h_conv7)
        # # 7*4*128
        # # print('out6: ',out6)
        #---------------------------------------------------------------------------------------

        # --------------- full connect -----------------
        w_full_1=sess.run('w_full_1:0')
        b_full_1=sess.run('b_full_1:0')
        flat_out4=tf.reshape(out5,[-1,5*3*128])
        h_full_1=tf.nn.relu(tf.matmul(flat_out4,w_full_1)+b_full_1)

        # # Drop out
        # h_full_drop1=tf.nn.dropout(h_full_1,keep_prob=keep_prob)

        # --------------- full connect -------------------
        w_full_2=sess.run('w_full_2:0')
        b_full_2=sess.run('b_full_2:0')
        out7=tf.matmul(h_full_1,w_full_2)+b_full_2

        # --------------- last layer ---------------------
        w_full_3=sess.run('w_full_3:0')
        b_full_3=sess.run('b_full_3:0')
        y_out=tf.matmul(out7,w_full_3)+b_full_3
        print ('y_out: ',y_out)
        print('-------------')
        # --------------- loss ----------------------------
        cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_out,labels=y_in))
        
        #-----------------predict ----------------
        correct_prediction=tf.equal(tf.argmax(y_out,1),tf.argmax(y_in,1))
        accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

        y_predict=tf.argmax(y_out,1)
        # file_out=open('Pred_label.csv','a+')


        for i in range (num_data//batch_size):
            test_x,test_y=sess.run([data,label])
            Y_pred=sess.run(y_predict,feed_dict={x_in:test_x,y_in:test_y})
            # print('pred: ',Y_pred)
            for j in range (batch_size):
                if Y_pred[j]==1:
                    file0.writelines('0,1\n')
                else:
                    file0.writelines('1,0\n')

            acc=sess.run(accuracy,feed_dict={x_in:test_x,y_in:test_y})
            accs.append(acc)
            # print(np.shape(Y_pred))
        file0.close()
        coord.request_stop()
    coord.join(threads)


    accur=0
    for i in range (len(accs)):
        accur+=accs[i]
    print('accur= ',accur/len(accs))


if __name__ == "__main__":
    # all pathes of files need to be replaced by pathes in ALL-New-V2 or your own folders
    train()
    # test()
    