from flask import render_template, redirect, url_for, flash, request, session, abort, jsonify
from urllib.parse import urljoin
from app import app, db, bcrypt
from app.models import Roommate, Admin, FamilyMember
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse
from urllib.parse import urljoin
import pyotp
import os
import mailtrap as mt
import requests
import random
import pyrebase
import collections
import json
import numpy as np
from urllib.request import urlopen
from math import pow

@app.route('/', methods=['GET'])
def user_home():
    return render_template('home.html')

@app.route('/roommate/login', methods=['GET','POST'])
def roommate_login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('roommate_dashboard'))
    except:
        pass
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password']
        print(password)
        try:
            roommate = Roommate.query.filter_by(email=email, password=password, role='roommate').first()
            total_users = roommate.query.count()
            print("signin",roommate)
            print("pass:", roommate.password)

            if roommate:
                session['Roommate_Name'] = roommate.RoommateName
                session['email'] = roommate.email
                session['Roommate_id'] = roommate.id
                otp_secret = 'KQ7LYBX3KZU6RT3N' 
                totp = pyotp.TOTP(otp_secret)
                otp_code = totp.now()
                print(otp_code)
                session['otp_code'] = otp_code
                print("RECEIVED: ", roommate.email, password)

                flash('An OTP code has been sent to your phone', 'success')
                print("An OTP code has been sent to your phone")
                
                # mail = mt.Mail(
                #     sender=mt.Address(email="mailtrap@splitspace.tech", name="SplitSpace Notifications"),
                #     to=[mt.Address(email=email)],
                #     subject="SplitSpace Email Verification",

                #     html=f"""
                #                     <html>
                #                     <table width="100%" border="0" cellspacing="0" cellpadding="0">
                # <tbody>
                #     <tr>
                #     <td align="center">
                #         <table width="600" border="0" cellspacing="0" cellpadding="40" style="border:1px solid rgb(234,234,234);border-radius:5px;margin:40px 0px">
                #         <tbody>
                #             <tr>
                #             <td align="center">
                #                 <div style="text-align:left;width:465px">
                #                 <table width="100%" border="0" cellspacing="0" cellpadding="0" style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;width:465px">
                #                     <tbody>
                #                     <tr>
                #                         <td align="center">
                #                         <div>
                #                             <h1 style="font-size:24px;font-weight:normal;margin:30px 0px;padding:0px">
                #                             <b>
                #                                 <font color="#000000">Split</font>
                #                                 <font color="#6aa84f">Space</font>
                #                             </b>
                #                             </h1>
                #                         </div>
                #                         <h1 style="color:rgb(0,0,0);font-size:24px;font-weight:normal;margin:30px 0px;padding:0px">
                #                             <span>Verify</span>&nbsp;your email to sign up
                #                         </h1>
                #                         </td>
                #                     </tr>
                #                     </tbody>
                #                 </table>
                #                 <p style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(0,0,0);font-size:14px;line-height:24px">
                #                     <span style="color:rgb(34,34,34);font-family:Arial,Helvetica,sans-serif;font-size:small">You are receiving this email because you registered for SplitSpace.</span>
                #                     <br style="color:rgb(34,34,34);font-family:Arial,Helvetica,sans-serif;font-size:small">
                #                 </p>
                #                 <p style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(0,0,0);font-size:14px;line-height:24px">
                #                     <span style="color:rgb(34,34,34);font-family:Arial,Helvetica,sans-serif;font-size:small">To complete your registration you need to enter your verification code as show</span>
                #                     <br style="color:rgb(34,34,34);font-family:Arial,Helvetica,sans-serif;font-size:small">
                #                 </p>
                #                 <br>
                #                 <table "100%" border="0" cellspacing="0" cellpadding="0" style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;width:465px">
                #                     <tbody>
                #                     <tr>
                #                         <td align="center" bgcolor="#f6f6f6" valign="middle" height="40" style="font-size:16px;font-weight:bold">{otp_code}</td>
                #                     </tr>
                #                     </tbody>
                #                 </table>
                #                 <br>
                #                 <p style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;text-align:center;color:rgb(0,0,0);font-size:14px;line-height:24px">To complete the signup process, please click on the button below</p>
                #                 <div style="text-align:center">
                #                     <span style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                #                     <br>
                #                     </span>
                #                 </div>
                #                 <table "100%" border="0" cellspacing="0" cellpadding="0" style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;width:465px">
                #                     <tbody>
                #                     <tr>
                #                         <td align="center">
                #                         <div>
                #                             <a href="https://sustainai.tech/user/verification?P3o2kqyVUsKyZjLWfJHLuIyh4qgsrzimDUkDa1adUuQUHRgdAmxSCSMAKUev7wRm/code={otp_code}" style="color:rgb(255,255,255);background-color:rgb(0,0,0);border-radius:5px;display:inline-block;font-size:12px;line-height:50px;text-decoration-line:none;width:200px" target="_parent" data-saferedirecturl="https://sustainai.tech/user/verification">
                #                             <span>VERIFY</span>
                #                             </a>
                #                         </div>
                #                         </td>
                #                     </tr>
                #                     </tbody>
                #                 </table>
                #                 <br>
                #                 <p style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;text-align:center;color:rgb(0,0,0);line-height:24px">
                #                     <font size="4">Team EcoWarriors</font>
                #                 </p>
                #                 <hr style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;border-right:none;border-bottom:none;border-left:none;border-top-style:solid;border-top-color:rgb(234,234,234);margin:26px 0px;width:465px">
                #                 <p style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(102,102,102);font-size:12px;line-height:24px">If you didn't attempt to sign up but received this email please ignore this email. If you are concerned about your account's safety, please reply to this email to get in touch with us.</p>
                #                 </div>
                #             </td>
                #             </tr>
                #         </tbody>
                #         </table>
                #     </td>
                #     </tr>
                # </tbody>
                # </table>
                # </html>""",
                #     category="Verification",
                # )

                # client = mt.MailtrapClient(token=token)
                # print(client.send(mail))
                return redirect(url_for('roommate_verification'))
        except:
            return redirect(url_for('roommate_register'))

    else:
        flash('User not found. Please sign up.', 'danger')
        print("User not found. Please sign up")

    return render_template('roommate/login.html')

@app.route('/roommate/register', methods=['GET', 'POST'])
def roommate_register():
    if current_user.is_authenticated:
        return redirect(url_for('roommate_dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        RoommateName = request.form['RoommateName']

        existing_user = Roommate.query.filter_by(email=email, role='roommate', contacted=False).first()

        if existing_user:
            flash('A roommate with this emailID already exists. Please choose a different one.', 'danger')
            print('A roommate with this emailID already exists. Please choose a different one.')
            return redirect(url_for('roommate_register'))
        else:
            registered_at = datetime.now()
            roommate = Roommate(email=email, password=password, RoommateName=RoommateName, role='roommate', contacted=False, registeredAt=registered_at)
            print("register",roommate)
            db.session.add(roommate)
            try:
                db.session.commit()
                flash('Your account has been created!', 'success')
                print('Your account has been created!')
                return redirect(url_for('roommate_login'))
            except IntegrityError as e:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again later.', 'danger')
                print(f'An error occurred while creating your account. Please try again later., Error: {str(e)}')
                return redirect(url_for('roommate_register'))

    return render_template('roommate/register.html')

@app.route('/roommate/verification', methods=['GET', 'POST'])
def roommate_verification():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
        
    stored_otp = session.get('otp_code')
    if request.method == 'POST':
        entered_otp = request.form.get('otp_code')


        if entered_otp == stored_otp:
            flash('OTP verification successful', 'success')
            Roommate_id = session.get('Roommate_id')
            roommate = Roommate.query.get(Roommate_id)
            session['user_role'] = 'roommate'
            session['Roommate_Name'] = roommate.RoommateName
            login_user(roommate)
            session.pop('otp_code', None)

            print('OTP verification successful')

            return redirect(url_for('roommate_dashboard'))

        else:
            flash('Invalid OTP code', 'danger')

    return render_template('roommate/verification.html', stored_otp=stored_otp)


@app.route('/roommate/dashboard', methods=['GET'])
def roommate_dashboard():
    if session["user_role"] == "roommate":
        return render_template('roommate/dashboard.html', name=session['Roommate_Name'])
    else:
        return redirect(url_for('roommate_login'))
