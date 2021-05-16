from flask_app.models.user import User
from flask_app import app
from flask import render_template,redirect,request,session,flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.message import Message


@app.route('/send', methods=['POST'])
def send_mssg():
    if 'user' not in session:
        flash('You must be logged in to send messages')
        return redirect('/')

    if len(request.form['content']) <= 5:
        flash("Message must be longer than 5 characters")
        return redirect('/wall')

    data = {
        'sender': session['user'],
        'receiver': int(request.form['receiver']),
        'content': request.form['content'],
    }
    Message.send_mssg(data)

    return redirect('/wall')



@app.route('/delete/<receiver_id>/<msg_id>')
def delete(receiver_id,msg_id):
    if 'user' not in session:
        flash('You must be logged in to delete messages')
        return redirect('/')
    
    if int(receiver_id) != int(session['user']):
        data = {
            'id':session['user']
        }
        dude = User.get_user_by_id(data)
        print(dude.hack_attempts)
        if (dude.hack_attempts == 1):
            Message.delete_mssg_from_user(data)
            User.delete_user(data)
            session.clear()
            flash('Your account has been delete')
            return redirect('/logout')

        User.update_attemps(data)
        return redirect('/nobueno')
        


    Message.delete_mssg({'msg_id': msg_id})
    return redirect('/wall')



@app.route('/nobueno')
def nobueno():
    return render_template('nobueno.html')