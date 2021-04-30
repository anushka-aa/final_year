import os
from sqlalchemy.orm.session import Session
import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import *
import db
import attendanceproject as ap


def open_db():
    engine = create_engine("sqlite:///db.sqlite3")
    Session = sessionmaker(bind=engine)
    return Session()

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

st.title(TITLE)
choice = st.radio("select options",MENU)

if choice =='Add data':
    imgdata = st.file_uploader("select an image",type=['jpg','png'])
    name =st.text_input("enter name of student")
    roll_no=st.text_input("enter roll number")
    section=st.text_input("enter section")
    button=st.button('save')

    if imgdata and name and roll_no and section and button:
        
        im = Image.open(imgdata)
        path = os.path.join(UPLOAD_FOLDER,f"{name}_{roll_no}.{imgdata.name.split('.')[1]}")
        im.save(path,format=imgdata.type.split('/')[1])
        sess = open_db()
        student = db.Student(path=path,name=name,roll_no=roll_no,section=section)
        sess.add(student)
        sess.commit()
        sess.close()
        st.success('student details uploaded successfully')

if choice == 'Remove data':
    sess = open_db()
    images = sess.query(db.Student).all()
    sess.close()
    button=st.button('remove')
    
    select_img = st.sidebar.radio("select an image",images)
    if os.path.exists(select_img.path):
        im = Image.open(select_img.path)
        st.image(im,use_column_width=True)


if choice == 'Take attendance':
    btn=st.button('launch webcam')
    
    if btn:
        sess=open_db()
        ap.webcam(sess)
        sess.close()





if choice =='View attendance':
    sess = open_db()
    images = sess.query(db.Image).all()
    sess.close()
    
    select_img = st.sidebar.radio("select an image",images)
    if select_img and st.button("remove"):
        sess = open_db()
        sess.query(db.Image).filter(db.Image.id==select_img.id).delete()
        if os.path.exists(select_img.path):
            os.unlink(select_img.path)
        sess.commit()
        sess.close()