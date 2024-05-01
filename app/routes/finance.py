from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Finance
from app.classes.forms import FinanceForm
from flask_login import login_required
import datetime as dt

@app.route('/finance/new', methods=['GET', 'POST'])
@login_required
def financeNew():
    form = FinanceForm()    
    if form.validate_on_submit():
        newFinance = Finance(
            title = form.title.data,
            explanation = form.explanation.data,
            question  = form.question.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        newFinance.save()
        return redirect(url_for('finance',financeID=newFinance.id))
    return render_template('financeform.html',form=form)

@app.route('/finance/<financeID>')

@login_required
def finance(financeID):
   
    thisFinance = Finance.objects.get(id=financeID)
   
   
    return render_template('finance.html',finance=thisFinance)

@app.route('/finance/list')
@app.route('/finances')

@login_required
def financeList():
  
    finances = Finance.objects()
    
    return render_template('finances.html',finances=finances)


#edit
@app.route('/finance/edit/<financeID>', methods=['GET', 'POST'])
@login_required
def financeEdit(financeID):
    editFinance = Finance.objects.get(id=financeID)
   
    if current_user != editFinance.author:
        flash("You can't edit a finance you don't own.")
        return redirect(url_for('finance',financeID=financeID))
    # get the form object
    form = FinanceForm()
    
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editFinance.update(
            title = form.title.data,
            explanation = form.explanation.data,
            question = form.question.data,
            modifydate = dt.datetime.utcnow
        )
        
        return redirect(url_for('finance',financeID=financeID))

   
    form.title.data = editFinance.title
    form.explanation.data = editFinance.explanation
    form.question.data = editFinance.question


  
    return render_template('financeform.html',form=form)

#delete

@app.route('/finance/delete/<financeID>')
@login_required
def financedelete(financeID): 
    deleteFinance = Finance.objects.get(id=financeID)
    deleteFinance.delete()
    flash('The finance was deleted.')
    return redirect(url_for('financeList')) 

