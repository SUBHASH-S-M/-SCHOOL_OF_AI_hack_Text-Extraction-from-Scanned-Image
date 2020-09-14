import streamlit as st 
import cv2
from PIL import Image,ImageEnhance
import numpy as np 
import matplotlib.pyplot as plt
import os
from ipynb.fs.defs .Text_Extraction import image_resize,set_image_dpi,remove_noise_and_smooth,text_rotation,croping_image,order_points,four_point_transform,get_text,sentiment_analysis,word_cloud,send_mail,text_2_speech
from wordcloud import WordCloud
import pytesseract
pytesseract.pytesseract.tesseract_cmd="/app/.apt/usr/bin/tesseract"
import smtplib
import time
import base64


def text_localization(img):
     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     boxes = pytesseract.image_to_data(gray)
     for a,b in enumerate(boxes.splitlines()):
         if a!=0:
             b = b.split()
             if len(b)==12:
                 x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                 cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
                 cv2.rectangle(img, (x,y), (x+w, y+h), (50, 50, 255), 2)
     st.image(img)                 
     
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
def write_of_file(text,filename):
    with open("test.txt",'w',encoding = 'utf-8') as f:
            f.write(text)
    return filename
        
def make_downloable_file(filename):
    readfile=open("test.txt").read()
    b64 = base64.b64encode(readfile.encode()).decode()
    href= '<a href="data:file/readfile;base64,{}">Download file</a>(right click to save as file name)'.format(b64)
    return href


def main():
    local_css("style.css")
    activities = ["ABOUT","Text extraction","Text Detection"]
    choice = st.sidebar.selectbox("Select Activty",activities)
    if choice=="Text extraction":
        st.set_option('deprecation.showfileUploaderEncoding', False)
        html_temp = """
        <div style="background-color:indigo;padding:10px">
        <h2 style="color:white;text-align:center;">Text Extraction from scanned Image</h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg'])
        if image_file is not None:
            
            our_image = Image.open(image_file)
            
            
            st.title("Original Image")
            new_img = np.array(our_image.convert('RGB'))
            res_image=image_resize(new_img,750,750)
            st.image(res_image)
            dpi_image=set_image_dpi(image_file)
        
            
            
            st.title("CROP Image")
            st.subheader("Do you want to crop the image ? ")
            st.write("To crop the image following conditions should satisfy")
            st.write("1.Four corners of the page should be visible")
            st.write("2.Background of the image should be plain")
            crop = st.selectbox("Crop",["","NO","YES"])
            if crop=="YES":
               screenCnt =0
               croped_img=croping_image(dpi_image)
               croped_img=image_resize(croped_img)
               st.image(croped_img)
               st.subheader("Do you wish to apply the changes?")
               crop2 = st.selectbox("crop(confirmation)",["","NO","YES"])
               if crop2=="YES":
                   croped_img=croped_img
               elif crop2=="NO":
                   croped_img=dpi_image
               else:
                    pass
            
            else:
                st.subheader("Image is considered to be croped")
                croped_img=dpi_image
                croped_img=image_resize(croped_img,750,750)


         
                
            st.title("ROTATE Image")    
            st.subheader("Do you need to rotate the text?")
            rotate = st.selectbox("Rotate",["","NO","YES"])
    
                
            if rotate=="YES":
                rotated_img=text_rotation(croped_img)
                st.image(rotated_img)
                clear_image=remove_noise_and_smooth(rotated_img)
                text=pytesseract.image_to_string(clear_image,lang='eng')
                
            elif rotate=="NO":
                st.write("Image is considered to be in straight text")
                rotated_img=croped_img
                st.image(rotated_img)
                clear_image=remove_noise_and_smooth(rotated_img)
                text=pytesseract.image_to_string(clear_image,lang='eng')
            else:
                pass
            
    
            if st.button("Show Text"):
                
                st.write(text)
                
            if st.button("Sentiment analysis"):
                st.subheader("SENTIMENT ANALYSIS OF THE TEXT")
                
                st.title(sentiment_analysis(text))
            if st.button("Visualizing the text"):
                word_cloud(text)
                wordcloud = WordCloud().generate(text)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.pyplot()
            st.subheader("Do you need to get the text as mail?")
            mail = st.selectbox("Mail",["","NO","YES"])
            if mail=="YES":
                mail_id=st.text_input("Enter the mail address","Type Here")
                if st.button("Get_Mail"):
                    server=smtplib.SMTP_SSL("smtp.gmail.com",465)
                    server.login("text.extractor.005@gmail.com","Abcd#1234")
                    st.write("Login Success")
                    server.sendmail("text.extractor.005@gmail.com",mail_id,msg=text)
                    st.write("Email sent successfully")
            else:
                pass
            
            timestr=time.strftime("%Y%m%d-%H%M%S")
            file_name="Document"+timestr+".txt"
            
            st.subheader("Do you need to get the text as document?")
            docs = st.selectbox("Document",["","NO","YES"])
            if docs=="YES":
                file_to_download=write_of_file(text,file_name)
                st.info("Saved Result as ::{}".format(file_name))
                d_link=make_downloable_file(file_to_download)
                st.markdown(d_link,unsafe_allow_html=True)
            else :
                pass
    elif choice=="ABOUT":
        html_temp = """
        <div style="background-color:green;padding:2px">
        <h2 style="color:white;text-align:center;">\t\t\tWelcome to Text Extraction using Tesseract OCR</h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        #st.title("\t\t\tWelcome to Text Extraction using Tesseract OCR")
        st.subheader("Image To Text Extraction")
        st.write("We have developed an pretty good tool for conversion of image to text")
        st.title("Lets Start!!")
        st.subheader("Image Upload")
        st.write("->Click Text Extraction from the Select Activity drop down in sidebar")
        st.write("-> Now its time to upload your image in upload section")
        st.write("-->Then click browse and upload your image also you wil get preview of your image")
        st.title("Image Preview")
        st.title("Crop Section")
        st.subheader("Condition for Crop")
        st.write("To crop the image following conditions should satisfy \n ")
        st.write("1.Four corners of the page should be visible")
        st.write("2.Background of the image should be plain")
        st.subheader("Crop Section")
        st.write("-->Do you want to crop the image ?\nif your image satisfy above category go for crop by clicking YES from drop down")
        st.title("Rotate Section")
        st.write("->->if you want to rotate your image sometimes you have images in slanting order so you can reshape here")
        st.title("click Read text to see your coverted text")
        st.title("Salient Features ")
        st.subheader("We provide pre determined features \n 1)Email-If you choose this enter the mail id so you will get your converted text in your inbox")
        st.write("2)Sentiment Analysis - If you want to see the sentiment analysis of text click sentiment analysis")
        st.write("3)Word Cloud-We provide word cloud to understand the text easily with visualization")
        st.write("4)Export-If you need to get the converted text in Text document(.txt)click YES to download the file")
        st.title("\t\t\tThank you")
        st.title("Hope you enjoyed this conversion")
        
        
        
    else:
        
        st.set_option('deprecation.showfileUploaderEncoding', False)
        html_temp = """
        <div style="background-color:blue;padding:10px">
        <h2 style="color:white;text-align:center;">Text Detection and Localization</h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg'])

        if image_file is not None:
            
            our_image = Image.open(image_file)
            new_img = np.array(our_image.convert('RGB'))
            res_image=image_resize(new_img,750,750)

            st.image(res_image)
            
            if st.button("Show"):
                
                text_localization(new_img)
                    

        
if __name__ == '__main__':
		main()