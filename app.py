
"""user autentication practise"""

from flask import Flask,render_template,session,flash,redirect 
from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db,User,Feedback
from forms import RegisterUser,LogInForm,FeedbackForm


app=Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI']="postgresql:///users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECRET_KEY'] = 'secretsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar=DebugToolbarExtension(app)


connect_db(app)
db.create_all()




@app.route("/",methods=["GET"])
def home():
    return redirect("/register")



@app.route("/register",methods=["GET","POST"])
def register():
    
    form=RegisterUser()
    
    if form.validate_on_submit():
       
        username=form.username.data
        password=form.password.data
        email=form.email.data
        firstname=form.firstname.data
        lastname=form.lastname.data

        user=User.register(username,password,email,firstname,lastname)
        db.session.add(user) 
        db.session.commit()
        session['user_name']=user.username
            
        return redirect(f'/users/{user.username}') #change this to secret later

    else:
        return render_template("register.html",form=form)



@app.route('/login',methods=["GET","POST"])
def log_in():
    form=LogInForm()

    

    if form.validate_on_submit():

        username=form.username.data
        password=form.password.data

        user=User.authenticate(username,password)
    
        if user:
            session['user_name']=user.username # keep logged in
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors=["wrong username or password"]
    return render_template("log-in-form.html",form=form)

@app.route('/logout',methods=["GET"])
def log_out():
    """log user out and redirect to home"""
    session.pop("user_name")

    return redirect('/')




# START ROUTES FOR USERS AND FEEDBACK

@app.route('/users/<user_name>')
def show_user(user_name):
    """Example hidden page for logged-in users only."""


    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect('/')
    else:
    
        
        user=User.query.get(user_name)
        form=LogInForm()
        return render_template("userinfo.html",user=user,form=form)
  

@app.route('/users/<user_name>/delete',methods=["POST"])
def delete_user(user_name):
    user=User.query.get(user_name)
    db.session.delete(user)
    db.session.commit()
    session.pop(user_name)

    flash("user deleted")

    return redirect('/login')



@app.route('/users/<user_name>/feedback/add',methods=["GET","POST"])
def process_feedback_form(user_name):

    if "user_name" not in session:
        flash("please log in to submit feedback")
        return redirect('/')


    form=FeedbackForm()
      
    if form.validate_on_submit():

        title=form.title.data
        content=form.content.data
       
        username=user_name
        
        feedback=Feedback(title=title,content=content,username=username)
            
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{session['user_name']}")
    else:
        return render_template('feedback-form.html',form=form)
        

@app.route('/feedback/<feedback_id>/update',methods=["GET","POST"])
def process_feedback_update(feedback_id):

    feedback=Feedback.query.get(feedback_id)
    if "user_name" not in session:
        flash("please log in to submit feedback")
        return redirect('/')
   
    form=FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        
        feedback.title=form.title.data
        feedback.content=form.content.data
       

        feedback=Feedback(title=feedback.title,content=feedback.content)
  
        db.session.commit()
        return redirect(f"/users/{session['user_name']}")  # (f"/users/{user_name}")  this brings up an error message that user_name is undefined

    else:
        return render_template("edit-feedback-form.html",form=form,feedback=feedback)




@app.route('/feedback/<feedback_id>/delete',methods=["POST"])
def delete_feedback(feedback_id):
    """delete a specific feedback """
    feedback=Feedback.query.get(feedback_id)

    if feedback.username==session['user_name']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted")
        return redirect(f"/users/{session['user_name']}")
    flash("please log in delete and create feedback.  Must be your own post to delete")
    return redirect('/register')