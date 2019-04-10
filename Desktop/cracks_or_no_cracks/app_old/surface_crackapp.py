# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 21:23:55 2019

@author: Davis
"""

import os 
from flask import Flask, render_template, request
import flask
from PIL import Image
from keras.models import load_model
import os
import numpy as np
from keras.preprocessing import image
#import tensorflow as tf
from shutil import copyfile
import shutil
from  flask_mail import Mail,Message
import imaplib, email
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from keras.models import load_model
import shutil
import sys
import json
import os
import urllib.request
from sendgrid.helpers.mail import *
from sendgrid import *
import base64
import email

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
model = load_model("CNN1_project.h5")
model_f_layer =load_model('CNN2.h5')

@app.route("/")
@app.route("/upload")
def index():
    return render_template("fix_rotation.html")

#def answer():
#    global string_total 
#    a=1
#    b=4
#    total  = a+b
#    string_total=str(int(total))
#    return string_total

#problems passing over results to page solved with the app run function on the bottom
def predict():
    # remove file if there is there is a file present, used to replace the files
    
#    path, dirs, files = next(os.walk('./image_email/'))
#    num_files_count = len(files)
#    path2, dirs2, files2 = next(os.walk('./image_feedback/'))
#    num_files_count2 = len(files2)
#    
#    
##    if os.path.exists(dirpath) and os.path.isdir(dirpath):
##    shutil.rmtree(dirpath)
##        
#    
#    #image_file= (files[0])
#    if num_files_count >0:
#        image_file= (files[0])
#        os.remove('./image_email/'+image_file)
#    else:
#        print("good")
#    if num_files_count2 >0:
#        feedback_file = (files2[0])
#        shutil.rmtree('./image_feedback/'+ feedback_file)
#    else:
#        print("good")
    
#    path, dirs, files = next(os.walk('./image_email/'))
#    num_files_count = len(files)
#    path2, dirs2, files2 = next(os.walk('./image_feedback/'))
#    num_files_count2 = len(files2)
    
    file_path ='./images/'
    file = os.listdir(file_path)[0]
    full_path = file_path+file
    email_picture = './image_email/'
    shutil.copy(full_path, email_picture)
    email_pic_file = os.listdir(email_picture)[0]
    full_path_email_pic_f = './image_email/'+email_pic_file# if you concatenate  full_path_email_pic+full_path_email_pic_f = error comes because it willl not put a dash before the file 
#    email_pic_file = os.listdir(email_picture)[0]   -> was trying to hold images in folder to preview them on browser
#    full_picture_file = picture_shower_path + picture_file
    
    feedback_picture = './image_feedback/'
    shutil.copy(full_path,feedback_picture)
    feedback_picture_file = os.listdir(feedback_picture)[0]
    feedback_picture_full_path = './image_feedback/'+feedback_picture_file
    
    img = image.load_img(full_path, target_size=(90, 90))
    img =  image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    images= np.vstack([img])
    predictions= model.predict_classes(images,batch_size=2)      
    
    if predictions[0] == 0:
        answer = "No surface crack found"
#    if predictions[0] == 1:
#        answer = "This is not a surface"
    if predictions[0] == 1:
        answer = "Thick crack"
        prediction_f = model_f_layer.predict_classes(images,batch_size=2)
        if prediction_f[0] == 0:
                answer ="Thick diagonal crack this is dangerous maintenance needed immediately "
        if prediction_f[0] == 1:
                answer ="Thick horizontal crack this is dangerous maintenance needed immediately"
        if prediction_f[0] == 2:
                answer ="Thick vertical crack this is dangerous maintenance needed immediately "
    if predictions[0] == 2:
        answer = "Thin crack"
        prediction_f = model_f_layer.predict_classes(images,batch_size=2)
        if prediction_f[0] == 0:
                answer ="Thin diagonal crack this is not too dangerous minor  maintenance needed "
        if prediction_f[0] == 1:
                answer ="Thin horizontal crack this is not too  dangerous minor maintenance needed"
        if prediction_f[0] == 2:
                answer ="Thin vertical crack this is not too  dangerous minor  maintenance needeed"
            
    
    
    os.rename(full_path_email_pic_f,'./image_email/'+answer+'.jpg')#if you do not put full file path it will delete the file in the email folder rather than rename it so then the send function cannot find file and error will occur that states that is beyond the index, the reason why this method was chosen was because the author wanted to pass the results to user without having the run the CNNs in the send function, this is computationaly expensive and will cause larger load time, but by renaming file of the chosen image to the results and passing the renamed file to the email folder will allow the send function to read the name of the file to use it as the message.
    os.rename(feedback_picture_full_path,'./image_feedback/'+answer+'.jpg')
    os.remove(full_path)# i needed to remove the first image from folder FIFO approach
    #return render_template('result.html',answer=answer)  
    return render_template('fix_rotation.html', answer= answer)
    #empty folder after function
    #os.remove(full_path)

@app.route("/upload", methods=['POST'])
def upload():
    #add validation 
    

    target = os.path.join(APP_ROOT, 'images/')
    target2 = os.path.join(APP_ROOT, 'image_email/')
    target3 = os.path.join(APP_ROOT, 'image_feedback/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    if not os.path.isdir(target2):
        os.mkdir(target2)
    if not os.path.isdir(target3):
        os.mkdir(target3)
    path, dirs, files = next(os.walk('./image_email/'))
    num_files_count = len(files)
    path2, dirs2, files2 = next(os.walk('./image_feedback/'))
    num_files_count2 = len(files2)
    #this replaces the image
        
    if num_files_count >0:
        image_file= (files[0])
        os.remove('./image_email/'+image_file)
    else:
        print("good")
    if num_files_count2 >0:
        feedback_file = (files2[0])
        os.remove('./image_feedback/'+ feedback_file)
    else:
        print("good")
        

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target2, filename])
        print(destination)
        file.save(destination)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target3, filename])
        print(destination)
        file.save(destination)
        path, dirs, files = next(os.walk('./image_email/'))
    num_files_count = len(files)
    path2, dirs2, files2 = next(os.walk('./image_feedback/'))
    num_files_count2 = len(files2)
    
    
#    if os.path.exists(dirpath) and os.path.isdir(dirpath):
#    shutil.rmtree(dirpath)
#        
    
    #image_file= (files[0])

    
        

    
    return predict()


#write feedback mechanisim
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/query", methods=['GET','POST'])
def query():
    feedback_file ='./image_feedback/'
    feedback_file_name = os.listdir(feedback_file)[0]
    #replace function to remove the word jpg
    if request.method == 'GET':
        return render_template("feedback.html")
    classification= format(request.form['classification'])
    reason= format(request.form['reason'])  
    mail= format(request.form['email'])
    feedback_folder = './image_feedback/'
    feedback_file = os.listdir(feedback_folder)[0]
    feedback_file_full= './image_feedback/'+feedback_file
    with open(feedback_file_full,'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "application/jpg"
    if attachment.type != "application/jpg":#allows only png and jpg
            attachment.type = "application/png"
            attachment.type = "application/png"
    attachment.filename = feedback_file_name
    attachment.disposition = "attachment"
    attachment.content_id = "image file"
    from_email = Email("up785062@myport.ac.uk")
    sg = sendgrid.SendGridAPIClient('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')
    subject = "Concrete Surface misclassification query"
    to_email = Email(mail)
    cc_email = Email("up785062@myport.ac.uk")
    p = Personalization()
    p.add_to(to_email)
    p.add_cc(cc_email)
    message= "your query:"+""+classification+" "+reason+". "+ "This is the query receipt. The incorrectly classified image is attached to the email " 
    #print(message)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    mail.add_personalization(p) # allows you to send  CC = carbon copy
    mail.add_attachment(attachment)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return render_template("finished_feedback.html")
    
    
     
    
    
    






@app.route("/email")
def email():
    return render_template("send_email.html")


# next is to get the results from the predictions
#remove images in files 

@app.route("/send", methods=['GET','POST'])
def send():
    result_file ='./image_email/'
    result_file_name = os.listdir(result_file)[0]
    #replace function to remove the word jpg
    if request.method == 'GET': # if someone presses on that send button it renders the email template
        return render_template("send_email.html")
        #return'<form action="send" method = "POST"><input name ="email"><input type ="submit"></form>' 
        #code above was used to test if email could be sent 
    mail= format(request.form['email'])
    location = format(request.form['location'])
    email_folder = './image_email/'
    files = os.listdir(email_folder)[0]
    image_file = './image_email/'+files
    with open(image_file,'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    #attachment.set_content(encoded) # there was no documentation to handle this problem figure this out by.
    attachment.content = encoded
    attachment.type = "application/jpg"
    if attachment.type != "application/jpg":#allows only png and jpg
            attachment.type = "application/png"
            attachment.type = "application/png"
    attachment.filename = result_file_name
    attachment.disposition = "attachment"
    attachment.content_id = "image file"
    from_email = Email("up785062@myport.ac.uk")
    sg = sendgrid.SendGridAPIClient('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')
    subject = "Concrete Surface Results"
    to_email = Email(mail)
    message = "this is the results"+" "+result_file_name +" "+"for building in:"+location+" "+"The attachment has been named to the classification results"
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return render_template("finished.html")

    
    
    
    
    
    #this code below is not safe it has my username password in it security is important as users can hack the system
#    subject ='Surface Crack Detection Results'
#    msg = MIMEMultipart()
#    msg['From']= mail
#    msg['To'] = 'agyemangdavis10@gmail.com'# does multiple users
#    msg['Subject'] = subject
#    msg.attach(MIMEText(result_file_name,'plain'))
#    email_folder = './image_email/'
#    email_file = os.listdir(email_folder)[0]
#    full_email_folder='./image_email/'+email_file
#    attachment = open(full_email_folder,'rb')
#    part = MIMEBase('application','octet-stream')
#    part.set_payload((attachment).read())
#    encoders.encode_base64(part)
#    part.add_header('Content-Disposition',"attachment; filename="+full_email_folder)
#    attachment.close() # this is important otherwise the systems will not be able to process the image as they are the same image at the same time
#    msg.attach(part)
#    text = msg.as_string()
#    server = smtplib.SMTP('smtp.gmail.com',587)
#    server.starttls()
#    server.login('agyemangdavis10@gmail.com','superpak123')
#
#
#    #server.sendmail(email_user,email_send,text)
#    server.sendmail('agyemangdavis10@gmail.com',mail,text)
#    server.quit()

    
   # return render_template("finished.html")
    


    

if __name__ == "__main__":
    app.run(debug = False, threaded = False)
